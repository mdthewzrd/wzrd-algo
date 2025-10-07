"use client";

import { useAuth } from "@clerk/nextjs";
import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  DollarSign,
  MoreVertical,
  Package,
  Pause,
  Play,
  Plus,
  RefreshCw,
  TrendingUp,
  Users,
  Zap,
  BarChart3,
  Eye,
  Trash2,
  Copy,
} from "lucide-react";
import { formatNumber, formatCurrency, formatRelativeTime, calculateProgress, getStatusColor } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

export default function DashboardPage() {
  const { isSignedIn, isLoaded } = useAuth();
  const router = useRouter();
  const [selectedStatus, setSelectedStatus] = useState<string>("all");
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Redirect to sign-in if not authenticated
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push("/");
    }
  }, [isLoaded, isSignedIn, router]);

  // Fetch data with real-time updates (only when authenticated)
  const campaigns = useQuery(
    api.campaigns.getCampaigns, 
    isSignedIn ? {
      status: selectedStatus === "all" ? undefined : selectedStatus as any,
    } : "skip"
  );
  
  const stats = useQuery(
    api.metrics.getDashboardStats,
    isSignedIn ? undefined : "skip"
  );
  
  const notifications = useQuery(
    api.notifications.getNotifications, 
    isSignedIn ? { 
      unreadOnly: true, 
      limit: 5 
    } : "skip"
  );

  // Mutations
  const pauseCampaign = useMutation(api.campaigns.pauseCampaign);
  const resumeCampaign = useMutation(api.campaigns.resumeCampaign);
  const startCampaign = useMutation(api.campaigns.startCampaign);
  const cancelCampaign = useMutation(api.campaigns.cancelCampaign);

  // Auto-refresh for real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setIsRefreshing(true);
      setTimeout(() => setIsRefreshing(false), 500);
    }, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const handleCampaignAction = async (action: string, campaignId: string, campaignName: string) => {
    try {
      switch (action) {
        case "pause":
          await pauseCampaign({ id: campaignId });
          toast.success(`Campaign "${campaignName}" paused`);
          break;
        case "resume":
          await resumeCampaign({ id: campaignId });
          toast.success(`Campaign "${campaignName}" resumed`);
          break;
        case "start":
          await startCampaign({ id: campaignId });
          toast.success(`Campaign "${campaignName}" started`);
          break;
        case "cancel":
          await cancelCampaign({ id: campaignId });
          toast.warning(`Campaign "${campaignName}" cancelled`);
          break;
      }
    } catch (error) {
      toast.error(`Failed to ${action} campaign: ${error.message}`);
    }
  };

  // Show loading state while checking authentication
  if (!isLoaded || !isSignedIn) {
    return <DashboardSkeleton />;
  }

  // Show loading state while fetching data
  if (!stats || !campaigns) {
    return <DashboardSkeleton />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Campaign Dashboard
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Monitor and manage your SMM drip feed campaigns in real-time
            </p>
          </div>
          <div className="flex gap-3">
            <Button
              variant="outline"
              size="icon"
              onClick={() => {
                setIsRefreshing(true);
                setTimeout(() => setIsRefreshing(false), 1000);
              }}
              className={isRefreshing ? "animate-spin" : ""}
            >
              <RefreshCw className="h-4 w-4" />
            </Button>
            <Button onClick={() => router.push("/campaigns/new")} className="gap-2">
              <Plus className="h-4 w-4" />
              New Campaign
            </Button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="Active Campaigns"
            value={stats.campaigns.active}
            total={stats.campaigns.total}
            icon={<Activity className="h-5 w-5" />}
            trend={stats.campaigns.active > 0 ? "up" : "neutral"}
            color="blue"
          />
          <StatsCard
            title="Delivery Rate"
            value={`${stats.delivery.deliveryRate.toFixed(1)}%`}
            subtitle={`${formatNumber(stats.delivery.totalDelivered)} / ${formatNumber(stats.delivery.totalOrdered)}`}
            icon={<TrendingUp className="h-5 w-5" />}
            trend={stats.delivery.deliveryRate > 90 ? "up" : "down"}
            color="green"
          />
          <StatsCard
            title="Success Rate"
            value={`${stats.performance.successRate.toFixed(1)}%`}
            subtitle={`Last 24h: ${stats.performance.dispatchesLast24h} dispatches`}
            icon={<CheckCircle className="h-5 w-5" />}
            trend={stats.performance.successRate > 95 ? "up" : "down"}
            color="purple"
          />
          <StatsCard
            title="Total Spent"
            value={formatCurrency(stats.financial.totalSpent)}
            subtitle={`Avg: ${formatCurrency(stats.financial.avgCampaignCost)}`}
            icon={<DollarSign className="h-5 w-5" />}
            trend="neutral"
            color="orange"
          />
        </div>

        {/* Alerts and Notifications */}
        {notifications && notifications.length > 0 && (
          <Alert className="border-yellow-200 bg-yellow-50 dark:bg-yellow-900/20">
            <AlertCircle className="h-4 w-4 text-yellow-600" />
            <AlertTitle>System Notifications</AlertTitle>
            <AlertDescription>
              You have {notifications.length} unread notifications
            </AlertDescription>
          </Alert>
        )}

        {/* Campaigns Table */}
        <Card className="overflow-hidden shadow-xl">
          <CardHeader className="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900">
            <div className="flex justify-between items-center">
              <div>
                <CardTitle className="text-2xl">Active Campaigns</CardTitle>
                <CardDescription>
                  Real-time monitoring of all your drip feed campaigns
                </CardDescription>
              </div>
              <Tabs value={selectedStatus} onValueChange={setSelectedStatus}>
                <TabsList>
                  <TabsTrigger value="all">All</TabsTrigger>
                  <TabsTrigger value="active">Active</TabsTrigger>
                  <TabsTrigger value="paused">Paused</TabsTrigger>
                  <TabsTrigger value="completed">Completed</TabsTrigger>
                </TabsList>
              </Tabs>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-800 border-b">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Campaign
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Progress
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Delivery
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Started
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {campaigns?.items.map((campaign) => {
                    const totalOrdered = campaign.services.reduce((sum, s) => sum + s.totalQuantity, 0);
                    const totalDelivered = campaign.services.reduce((sum, s) => sum + s.deliveredQuantity, 0);
                    const progress = calculateProgress(totalDelivered, totalOrdered);

                    return (
                      <tr
                        key={campaign._id}
                        className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors cursor-pointer"
                        onClick={() => router.push(`/campaigns/${campaign._id}`)}
                      >
                        <td className="px-6 py-4">
                          <div>
                            <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                              {campaign.name}
                            </div>
                            <div className="text-sm text-gray-500 truncate max-w-xs">
                              {campaign.targetURL}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <Badge className={getStatusColor(campaign.status)}>
                            {campaign.status === "active" && <Zap className="h-3 w-3 mr-1" />}
                            {campaign.status === "paused" && <Pause className="h-3 w-3 mr-1" />}
                            {campaign.status === "completed" && <CheckCircle className="h-3 w-3 mr-1" />}
                            {campaign.status}
                          </Badge>
                        </td>
                        <td className="px-6 py-4">
                          <div className="w-32">
                            <div className="flex justify-between text-xs text-gray-600 mb-1">
                              <span>{progress.toFixed(1)}%</span>
                              <span className="text-gray-400">
                                {campaign.status === "active" && isRefreshing && (
                                  <RefreshCw className="h-3 w-3 animate-spin inline" />
                                )}
                              </span>
                            </div>
                            <Progress value={progress} className="h-2" />
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm">
                            <div className="font-medium">
                              {formatNumber(totalDelivered)} / {formatNumber(totalOrdered)}
                            </div>
                            <div className="text-gray-500">
                              {campaign.services.length} services
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {campaign.startedAt
                            ? formatRelativeTime(campaign.startedAt)
                            : "Not started"}
                        </td>
                        <td className="px-6 py-4" onClick={(e) => e.stopPropagation()}>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" size="icon">
                                <MoreVertical className="h-4 w-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuLabel>Actions</DropdownMenuLabel>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem
                                onClick={() => router.push(`/campaigns/${campaign._id}`)}
                              >
                                <Eye className="h-4 w-4 mr-2" />
                                View Details
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => router.push(`/campaigns/${campaign._id}/analytics`)}
                              >
                                <BarChart3 className="h-4 w-4 mr-2" />
                                Analytics
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              {campaign.status === "draft" && (
                                <DropdownMenuItem
                                  onClick={() => handleCampaignAction("start", campaign._id, campaign.name)}
                                >
                                  <Play className="h-4 w-4 mr-2" />
                                  Start Campaign
                                </DropdownMenuItem>
                              )}
                              {campaign.status === "active" && (
                                <DropdownMenuItem
                                  onClick={() => handleCampaignAction("pause", campaign._id, campaign.name)}
                                >
                                  <Pause className="h-4 w-4 mr-2" />
                                  Pause Campaign
                                </DropdownMenuItem>
                              )}
                              {campaign.status === "paused" && (
                                <DropdownMenuItem
                                  onClick={() => handleCampaignAction("resume", campaign._id, campaign.name)}
                                >
                                  <Play className="h-4 w-4 mr-2" />
                                  Resume Campaign
                                </DropdownMenuItem>
                              )}
                              <DropdownMenuItem
                                onClick={() => {
                                  navigator.clipboard.writeText(campaign._id);
                                  toast.success("Campaign ID copied");
                                }}
                              >
                                <Copy className="h-4 w-4 mr-2" />
                                Copy ID
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem
                                className="text-red-600"
                                onClick={() => handleCampaignAction("cancel", campaign._id, campaign.name)}
                              >
                                <Trash2 className="h-4 w-4 mr-2" />
                                Cancel Campaign
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              {campaigns?.items.length === 0 && (
                <div className="text-center py-12">
                  <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No campaigns found</p>
                  <Button
                    variant="outline"
                    className="mt-4"
                    onClick={() => router.push("/campaigns/new")}
                  >
                    Create Your First Campaign
                  </Button>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => router.push("/packages")}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5" />
                Packages
              </CardTitle>
              <CardDescription>
                {stats.packages.active} active packages
              </CardDescription>
            </CardHeader>
          </Card>
          <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => router.push("/analytics")}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Analytics
              </CardTitle>
              <CardDescription>
                View detailed performance metrics
              </CardDescription>
            </CardHeader>
          </Card>
          <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => router.push("/settings")}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Settings
              </CardTitle>
              <CardDescription>
                Configure API keys and preferences
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    </div>
  );
}

function StatsCard({ title, value, subtitle, total, icon, trend, color }) {
  const trendColors = {
    up: "text-green-600",
    down: "text-red-600",
    neutral: "text-gray-600",
  };

  const bgColors = {
    blue: "bg-blue-100 dark:bg-blue-900/20",
    green: "bg-green-100 dark:bg-green-900/20",
    purple: "bg-purple-100 dark:bg-purple-900/20",
    orange: "bg-orange-100 dark:bg-orange-900/20",
  };

  const iconColors = {
    blue: "text-blue-600",
    green: "text-green-600",
    purple: "text-purple-600",
    orange: "text-orange-600",
  };

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {title}
            </p>
            <div className="mt-2">
              <span className="text-3xl font-bold">{value}</span>
              {total && (
                <span className="text-sm text-gray-500 ml-2">/ {total}</span>
              )}
            </div>
            {subtitle && (
              <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
            )}
          </div>
          <div className={`p-3 rounded-lg ${bgColors[color]}`}>
            <div className={iconColors[color]}>{icon}</div>
          </div>
        </div>
      </CardHeader>
    </Card>
  );
}

function DashboardSkeleton() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto p-6 space-y-8">
        <div className="flex justify-between items-center">
          <div>
            <Skeleton className="h-10 w-64" />
            <Skeleton className="h-4 w-96 mt-2" />
          </div>
          <div className="flex gap-3">
            <Skeleton className="h-10 w-10" />
            <Skeleton className="h-10 w-32" />
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-8 w-32 mt-2" />
              </CardHeader>
            </Card>
          ))}
        </div>
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-48" />
            <Skeleton className="h-4 w-64 mt-2" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-64 w-full" />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}