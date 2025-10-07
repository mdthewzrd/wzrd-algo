"""
Data Integration Module
Handles fetching and preparing market data for signal generation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Any, Optional, Tuple
import requests
import os

class MarketDataFetcher:
    """Fetch market data from various sources"""

    def __init__(self, polygon_api_key: Optional[str] = None):
        self.polygon_api_key = polygon_api_key or os.getenv('POLYGON_API_KEY')
        self.base_url = "https://api.polygon.io/v2"

    def fetch_ohlcv_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days_back: int = 30
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data from Polygon API
        Returns DataFrame with columns: date, open, high, low, close, volume
        """
        if not self.polygon_api_key:
            raise ValueError("Polygon API key is required")

        # Calculate date range
        if not start_date:
            end_date = end_date or datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # Map timeframe to Polygon multiplier/timespan
        timeframe_map = {
            '1min': ('1', 'minute'),
            '5min': ('5', 'minute'),
            '15min': ('15', 'minute'),
            '30min': ('30', 'minute'),
            '1hour': ('1', 'hour'),
            '4hour': ('4', 'hour'),
            '1day': ('1', 'day')
        }

        if timeframe not in timeframe_map:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        multiplier, timespan = timeframe_map[timeframe]

        # Construct API URL
        url = f"{self.base_url}/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start_date}/{end_date}"

        params = {
            'adjusted': 'true',
            'sort': 'asc',
            'limit': 50000,
            'apiKey': self.polygon_api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('status') != 'OK' or 'results' not in data:
                raise ValueError(f"API returned invalid data: {data}")

            # Convert to DataFrame
            results = data['results']
            df = pd.DataFrame(results)

            # Convert timestamp to datetime
            df['date'] = pd.to_datetime(df['t'], unit='ms')

            # Rename columns to match expected format
            df = df.rename(columns={
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'v': 'volume',
                'n': 'trades'
            })

            # Select and reorder columns
            columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            if 'trades' in df.columns:
                columns.append('trades')

            df = df[columns]

            # Set timezone to US/Eastern for intraday data
            if timeframe in ['1min', '5min', '15min', '30min', '1hour', '4hour']:
                eastern = pytz.timezone('US/Eastern')
                df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert(eastern)

            return df

        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Data processing failed: {str(e)}")

    def fetch_reference_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch reference data for a symbol"""
        url = f"{self.base_url}/reference/tickers/{symbol}"
        params = {'apiKey': self.polygon_api_key}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Warning: Could not fetch reference data for {symbol}: {e}")
            return {}

class DataProcessor:
    """Process and clean market data for signal generation"""

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate OHLCV data"""
        # Remove rows with missing values
        df = df.dropna()

        # Ensure numeric columns are proper types
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Remove rows with invalid OHLC relationships
        df = df[df['high'] >= df['low']]
        df = df[df['high'] >= df['open']]
        df = df[df['high'] >= df['close']]
        df = df[df['low'] <= df['open']]
        df = df[df['low'] <= df['close']]

        # Remove rows with zero or negative prices/volume
        df = df[df['close'] > 0]
        df = df[df['volume'] > 0]

        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)

        return df

    @staticmethod
    def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features for strategy analysis"""
        df = df.copy()

        # Basic time features
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month

        # Session features
        df['is_regular_session'] = (
            (df['hour'] >= 9) & (df['hour'] < 16) &
            (df['day_of_week'] < 5)  # Monday to Friday
        )

        # Market open/close features
        df['is_market_open'] = (df['hour'] >= 9) & (df['hour'] < 16)
        df['is_pre_market'] = (df['hour'] >= 4) & (df['hour'] < 9)
        df['is_after_hours'] = (df['hour'] >= 16) & (df['hour'] < 20)

        return df

    @staticmethod
    def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate various return metrics"""
        df = df.copy()

        # Basic returns
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))

        # Intraday returns (for intraday timeframes)
        df['intraday_return'] = (df['close'] - df['open']) / df['open']

        # Gap returns (from previous close)
        df['gap_return'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)

        return df

    @staticmethod
    def detect_market_regime(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
        """Detect market regime (trending, ranging, volatile)"""
        df = df.copy()

        # Calculate volatility
        df['volatility'] = df['returns'].rolling(window=lookback).std()

        # Calculate trend strength
        df['trend_strength'] = abs(df['close'].rolling(window=lookback).mean().pct_change(lookback))

        # Classify regime
        volatility_threshold = df['volatility'].rolling(window=50).median()
        trend_threshold = df['trend_strength'].rolling(window=50).median()

        df['regime'] = 'ranging'
        df.loc[df['volatility'] > volatility_threshold, 'regime'] = 'volatile'
        df.loc[df['trend_strength'] > trend_threshold, 'regime'] = 'trending'

        return df

class DataValidator:
    """Validate data quality and completeness"""

    @staticmethod
    def validate_ohlcv(df: pd.DataFrame) -> Dict[str, Any]:
        """Validate OHLCV data and return quality metrics"""
        validation_results = {
            'is_valid': True,
            'issues': [],
            'quality_metrics': {}
        }

        # Check required columns
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            validation_results['is_valid'] = False
            validation_results['issues'].append(f"Missing columns: {missing_columns}")
            return validation_results

        # Check data completeness
        total_rows = len(df)
        null_counts = df[required_columns].isnull().sum()

        for col, null_count in null_counts.items():
            if null_count > 0:
                validation_results['issues'].append(f"Column {col} has {null_count} null values")

        # Check for data gaps
        if len(df) > 1:
            expected_frequency = pd.infer_freq(df['date'])
            if expected_frequency:
                expected_dates = pd.date_range(
                    start=df['date'].min(),
                    end=df['date'].max(),
                    freq=expected_frequency
                )
                missing_dates = set(expected_dates) - set(df['date'])
                if missing_dates:
                    validation_results['issues'].append(f"Missing {len(missing_dates)} data points")

        # Calculate quality metrics
        validation_results['quality_metrics'] = {
            'total_rows': total_rows,
            'date_range': f"{df['date'].min()} to {df['date'].max()}",
            'completeness_rate': (total_rows - sum(null_counts)) / (total_rows * len(required_columns)),
            'duplicate_rows': df.duplicated().sum(),
            'invalid_ohlc': len(df[df['high'] < df['low']]),
            'zero_prices': len(df[df['close'] <= 0]),
            'negative_volume': len(df[df['volume'] < 0])
        }

        # Determine overall validity
        critical_issues = [
            'Missing columns',
            'has null values'
        ]

        for issue in validation_results['issues']:
            if any(critical in issue for critical in critical_issues):
                validation_results['is_valid'] = False
                break

        return validation_results

    @staticmethod
    def generate_data_report(df: pd.DataFrame, symbol: str, timeframe: str) -> str:
        """Generate a comprehensive data quality report"""
        validation = DataValidator.validate_ohlcv(df)
        metrics = validation['quality_metrics']

        report = f"""
Data Quality Report for {symbol} ({timeframe})
{'=' * 50}

Overall Status: {'✅ VALID' if validation['is_valid'] else '❌ INVALID'}

Data Summary:
- Total Rows: {metrics['total_rows']:,}
- Date Range: {metrics['date_range']}
- Completeness Rate: {metrics['completeness_rate']:.1%}

Quality Metrics:
- Duplicate Rows: {metrics['duplicate_rows']:,}
- Invalid OHLC Relationships: {metrics['invalid_ohlc']:,}
- Zero/Negative Prices: {metrics['zero_prices']:,}
- Negative Volume: {metrics['negative_volume']:,}

"""

        if validation['issues']:
            report += "\nIssues Found:\n"
            for issue in validation['issues']:
                report += f"- {issue}\n"
        else:
            report += "\n✅ No issues found!\n"

        return report

# Convenience function for easy data fetching
def get_market_data(
    symbol: str,
    timeframe: str,
    days_back: int = 30,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    polygon_api_key: Optional[str] = None,
    clean_data: bool = True,
    add_features: bool = True
) -> pd.DataFrame:
    """
    Convenience function to fetch and prepare market data

    Args:
        symbol: Stock symbol (e.g., 'SPY', 'QQQ')
        timeframe: Timeframe (e.g., '5min', '1hour', '1day')
        days_back: Number of days to fetch (used if start_date not provided)
        start_date: Start date in 'YYYY-MM-DD' format (optional)
        end_date: End date in 'YYYY-MM-DD' format (optional)
        polygon_api_key: Polygon API key (optional, can use env var)
        clean_data: Whether to clean the data
        add_features: Whether to add time features and returns

    Returns:
        DataFrame with prepared market data
    """
    # Initialize fetcher
    fetcher = MarketDataFetcher(polygon_api_key)

    # Fetch data
    df = fetcher.fetch_ohlcv_data(symbol, timeframe, start_date=start_date, end_date=end_date, days_back=days_back)

    # Clean data if requested
    if clean_data:
        df = DataProcessor.clean_data(df)

    # Add features if requested
    if add_features:
        df = DataProcessor.add_time_features(df)
        df = DataProcessor.calculate_returns(df)
        df = DataProcessor.detect_market_regime(df)

    return df