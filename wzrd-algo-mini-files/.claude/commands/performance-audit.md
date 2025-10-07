# Performance Audit Command

## Description
Run comprehensive performance optimization analysis

## Usage
```
/performance-audit [target]
```

## Targets
- `full` - Complete application audit
- `page:[path]` - Specific page audit
- `component:[name]` - Component performance
- `bundle` - Bundle size analysis
- `runtime` - Runtime performance

## Metrics Analyzed
### Core Web Vitals
- **LCP** (Largest Contentful Paint) < 2.5s
- **FID** (First Input Delay) < 100ms
- **CLS** (Cumulative Layout Shift) < 0.1

### Additional Metrics
- Time to Interactive (TTI)
- First Contentful Paint (FCP)
- Total Blocking Time (TBT)
- Bundle size analysis
- Memory usage
- Network requests

## Process
1. **Analysis Phase**
   - Lighthouse audit
   - Bundle analysis
   - Runtime profiling
   - Memory leak detection

2. **Optimization Phase**
   - Code splitting recommendations
   - Image optimization
   - Caching strategies
   - Lazy loading implementation

3. **Validation Phase**
   - Re-run metrics
   - Compare improvements
   - Generate report

## Example
```
/performance-audit page:/dashboard
```

## Output
- Performance report (JSON/HTML)
- Optimization recommendations
- Before/after comparisons
- Implementation priority list