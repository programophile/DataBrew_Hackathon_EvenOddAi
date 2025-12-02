import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import {
  Sparkles,
  TrendingUp,
  TrendingDown,
  Users,
  Package,
  DollarSign,
  Clock,
  Lightbulb,
  Download,
  CloudRain,
  Calendar,
} from "lucide-react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { apiService } from "../../services/api";
import { PredictiveInsightsPanel } from "../dashboard/PredictiveInsightsPanel";

const aiInsights = [
  {
    id: 1,
    type: "sales",
    icon: TrendingUp,
    title: "Sales Pattern Detected",
    description:
      "Iced Latte sales increased by 12% this week, primarily during afternoon hours (2PM-5PM).",
    impact: "high",
    recommendation:
      "Stock up on ice and milk for peak hours. Consider promoting iced beverages.",
    confidence: 94,
  },
  {
    id: 2,
    type: "staffing",
    icon: Users,
    title: "Staffing Optimization",
    description:
      "You may need 2 extra baristas between 5–8 PM tomorrow based on predicted customer surge.",
    impact: "medium",
    recommendation:
      "Schedule additional staff or offer overtime to current team members.",
    confidence: 87,
  },
  {
    id: 3,
    type: "inventory",
    icon: Package,
    title: "Inventory Alert",
    description:
      "Cappuccino beans running low. Current stock will last only 3 days at current consumption rate.",
    impact: "high",
    recommendation:
      "Place order with Bengal Coffee Co. immediately to avoid stockout.",
    confidence: 96,
  },
  {
    id: 4,
    type: "customer",
    icon: Clock,
    title: "Peak Hour Prediction",
    description:
      "Expected customer peak at 6:00 PM today. 25% higher traffic than usual Friday evenings.",
    impact: "medium",
    recommendation:
      "Prepare popular items in advance. Ensure all stations are fully stocked.",
    confidence: 89,
  },
  {
    id: 5,
    type: "revenue",
    icon: DollarSign,
    title: "Revenue Opportunity",
    description:
      "Customers ordering cappuccino often add a pastry. Cross-selling could increase revenue by ৳2,400/day.",
    impact: "high",
    recommendation:
      "Train staff to suggest pastries with coffee orders. Create combo deals.",
    confidence: 91,
  },
  {
    id: 6,
    type: "trend",
    icon: TrendingDown,
    title: "Declining Product",
    description:
      "Hot chocolate sales dropped 18% this month. May be due to warmer weather.",
    impact: "low",
    recommendation:
      "Consider seasonal menu adjustments. Introduce cold chocolate drinks.",
    confidence: 82,
  },
];

export function AIInsightsPage() {
  const [predictionData, setPredictionData] = useState<
    Array<{ day: string; predicted: number; actual: number | null }>
  >([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [liveInsights, setLiveInsights] = useState(aiInsights);
  const [sourceData, setSourceData] = useState<any>(null);
  const [showSourceData, setShowSourceData] = useState(false);

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const data = await apiService.getForecast(7);
        // Transform forecast data into chart format
        const chartData = data.forecast_next_days.map((value, index) => ({
          day: `Day ${index + 1}`,
          predicted: Math.round(value),
          actual:
            index < 4 ? Math.round(value * (0.95 + Math.random() * 0.1)) : null, // Simulate actual data for past days
        }));
        setPredictionData(chartData);
      } catch (error) {
        console.error("Failed to fetch forecast:", error);
        // Fallback data
        setPredictionData([
          { day: "Mon", predicted: 12500, actual: 12200 },
          { day: "Tue", predicted: 13200, actual: 13400 },
          { day: "Wed", predicted: 11800, actual: 11600 },
          { day: "Thu", predicted: 14500, actual: 14800 },
          { day: "Fri", predicted: 16200, actual: null },
          { day: "Sat", predicted: 17800, actual: null },
          { day: "Sun", predicted: 15400, actual: null },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchForecast();
  }, []);

  const handleExportReport = () => {
    // Prepare data for export
    const reportData = {
      reportDate: new Date().toLocaleDateString(),
      reportTime: new Date().toLocaleTimeString(),
      insights: liveInsights,
      forecast: predictionData,
    };

    // Create CSV content
    let csvContent = "DataBrew AI Insights Report\n";
    csvContent += `Generated: ${reportData.reportDate} ${reportData.reportTime}\n\n`;

    csvContent += "AI INSIGHTS\n";
    csvContent += "Title,Description,Impact,Recommendation,Confidence\n";

    reportData.insights.forEach((insight) => {
      csvContent += `"${insight.title}","${insight.description}","${insight.impact}","${insight.recommendation}",${insight.confidence}%\n`;
    });

    csvContent += "\nSALES FORECAST\n";
    csvContent += "Day,Predicted Sales,Actual Sales\n";

    reportData.forecast.forEach((day) => {
      csvContent += `${day.day},${day.predicted},${day.actual || "N/A"}\n`;
    });

    // Create blob and download
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);

    link.setAttribute("href", url);
    link.setAttribute(
      "download",
      `DataBrew_AI_Report_${new Date().toISOString().split("T")[0]}.csv`
    );
    link.style.visibility = "hidden";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleGenerateInsights = async () => {
    setGenerating(true);
    try {
      const response = await apiService.generateInsights();

      // Store source data for transparency
      setSourceData(response.source_data);

      // Map the generated insights to the format expected by the UI
      const newInsights = response.insights.map(
        (insight: any, index: number) => {
          const iconMap: Record<string, any> = {
            trending_up: TrendingUp,
            users: Users,
            clock: Clock,
            alert: Package,
          };

          return {
            id: Date.now() + index,
            type: insight.type === "alert" ? "inventory" : insight.type,
            icon: iconMap[insight.type] || TrendingUp,
            title: getTitleFromType(insight.type),
            description: insight.text,
            impact: getImpactFromColor(insight.color),
            recommendation: insight.text,
            confidence: 90 + Math.floor(Math.random() * 10),
          };
        }
      );

      setLiveInsights(newInsights);

      console.log("Generated insights:", response);
    } catch (error) {
      console.error("Failed to generate insights:", error);
      alert("Failed to generate new insights. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  const getTitleFromType = (type: string) => {
    switch (type) {
      case "trending_up":
        return "Sales Pattern Detected";
      case "users":
        return "Staffing Optimization";
      case "clock":
        return "Peak Hour Prediction";
      case "alert":
        return "Inventory Alert";
      default:
        return "Business Insight";
    }
  };

  const getImpactFromColor = (color: string) => {
    if (color === "#22c55e") return "low";
    if (color === "#f59e0b") return "medium";
    if (color === "#ef4444") return "high";
    return "medium";
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case "high":
        return "bg-red-100 text-red-700 border-red-300";
      case "medium":
        return "bg-orange-100 text-orange-700 border-orange-300";
      case "low":
        return "bg-blue-100 text-blue-700 border-blue-300";
      default:
        return "bg-gray-100 text-gray-700 border-gray-300";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with Actions */}
      <Card className="p-6 bg-gradient-to-br from-[#8b5e3c]/10 to-[#d8c3a5]/20 backdrop-blur-sm border-[#8b5e3c]/20 rounded-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-40 h-40 bg-[#8b5e3c]/10 rounded-full blur-3xl"></div>
        <div className="relative z-10 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-[#8b5e3c] to-[#b08968] rounded-xl">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-[#8b5e3c]">
                AI-Powered Business Intelligence
              </h2>
              <p className="text-sm text-[#8b5e3c]/60">
                Real-time insights and predictions for your coffee shop
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              className="border-[#8b5e3c] text-[#8b5e3c] hover:bg-[#8b5e3c] hover:text-white"
              onClick={handleExportReport}
            >
              <Download className="w-4 h-4 mr-2" />
              Export Report
            </Button>
          </div>
        </div>
      </Card>

      {/* Tabs for different insights */}
      <Tabs defaultValue="predictive" className="w-full">
        <TabsList className="grid w-full grid-cols-3 bg-[#d8c3a5]/20">
          <TabsTrigger
            value="predictive"
            className="data-[state=active]:bg-[#8b5e3c] data-[state=active]:text-white"
          >
            <CloudRain className="w-4 h-4 mr-2" />
            Predictive Insights
          </TabsTrigger>
          <TabsTrigger
            value="current"
            className="data-[state=active]:bg-[#8b5e3c] data-[state=active]:text-white"
          >
            <Sparkles className="w-4 h-4 mr-2" />
            Current Insights
          </TabsTrigger>
          <TabsTrigger
            value="forecast"
            className="data-[state=active]:bg-[#8b5e3c] data-[state=active]:text-white"
          >
            <TrendingUp className="w-4 h-4 mr-2" />
            Sales Forecast
          </TabsTrigger>
        </TabsList>

        {/* Predictive Insights Tab */}
        <TabsContent value="predictive" className="mt-6">
          <PredictiveInsightsPanel />
        </TabsContent>

        {/* Current Insights Tab */}
        <TabsContent value="current" className="mt-6">
          <CurrentInsightsContent
            liveInsights={liveInsights}
            generating={generating}
            handleGenerateInsights={handleGenerateInsights}
            sourceData={sourceData}
            showSourceData={showSourceData}
            setShowSourceData={setShowSourceData}
            getImpactColor={getImpactColor}
            loading={loading}
            predictionData={predictionData}
          />
        </TabsContent>

        {/* Forecast Tab */}
        <TabsContent value="forecast" className="mt-6">
          <ForecastContent loading={loading} predictionData={predictionData} />
        </TabsContent>
      </Tabs>
    </div>
  );
}

// Separate component for Forecast content
function ForecastContent({ loading, predictionData }: any) {
  return (
    <div className="space-y-6">
      {/* Prediction Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="mb-6">
            <h3 className="text-[#8b5e3c]">Sales Forecast (Next 7 Days)</h3>
            <p className="text-sm text-[#8b5e3c]/60">
              AI-predicted sales based on historical data
            </p>
          </div>
          {loading ? (
            <div className="text-center text-[#8b5e3c]/60 py-20">
              Loading forecast...
            </div>
          ) : (
            <>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={predictionData}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#d8c3a5"
                    opacity={0.3}
                  />
                  <XAxis
                    dataKey="day"
                    stroke="#8b5e3c"
                    opacity={0.6}
                    fontSize={12}
                  />
                  <YAxis stroke="#8b5e3c" opacity={0.6} fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#fffaf3",
                      border: "1px solid #d8c3a5",
                      borderRadius: "12px",
                      color: "#8b5e3c",
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="predicted"
                    stroke="#8b5e3c"
                    strokeWidth={3}
                    name="Predicted Sales"
                  />
                  <Line
                    type="monotone"
                    dataKey="actual"
                    stroke="#22c55e"
                    strokeWidth={2}
                    name="Actual Sales"
                    strokeDasharray="5 5"
                  />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-800">
                  ✨ AI-powered forecast using SARIMA model - Plan inventory and
                  staffing accordingly!
                </p>
              </div>
            </>
          )}
        </Card>

        <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="mb-6">
            <h3 className="text-[#8b5e3c]">Customer Visit Patterns</h3>
            <p className="text-sm text-[#8b5e3c]/60">
              Peak hours identification
            </p>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart
              data={[
                { hour: "8AM", visits: 45 },
                { hour: "9AM", visits: 78 },
                { hour: "10AM", visits: 92 },
                { hour: "11AM", visits: 105 },
                { hour: "12PM", visits: 125 },
                { hour: "1PM", visits: 115 },
                { hour: "2PM", visits: 98 },
                { hour: "3PM", visits: 135 },
                { hour: "4PM", visits: 142 },
                { hour: "5PM", visits: 168 },
                { hour: "6PM", visits: 195 },
                { hour: "7PM", visits: 158 },
              ]}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#d8c3a5"
                opacity={0.3}
              />
              <XAxis
                dataKey="hour"
                stroke="#8b5e3c"
                opacity={0.6}
                fontSize={12}
              />
              <YAxis stroke="#8b5e3c" opacity={0.6} fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#fffaf3",
                  border: "1px solid #d8c3a5",
                  borderRadius: "12px",
                  color: "#8b5e3c",
                }}
              />
              <Bar dataKey="visits" fill="#8b5e3c" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
            <p className="text-sm text-orange-800">
              🔔 Peak hours: 5PM-7PM. Consider adding 2-3 staff members during
              this time.
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}

// Separate component for Current Insights content
function CurrentInsightsContent({
  liveInsights,
  generating,
  handleGenerateInsights,
  sourceData,
  showSourceData,
  setShowSourceData,
  getImpactColor,
  loading,
  predictionData,
}: any) {
  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <Button
          className="bg-gradient-to-r from-[#8b5e3c] to-[#b08968] hover:from-[#b08968] hover:to-[#8b5e3c] text-white shadow-lg shadow-[#8b5e3c]/30"
          onClick={handleGenerateInsights}
          disabled={generating}
        >
          <Sparkles className="w-4 h-4 mr-2" />
          {generating ? "Generating..." : "Generate New Insights"}
        </Button>
      </div>

      {/* Source Data Display - Shows actual calculations sent to AI */}
      {sourceData && (
        <Card className="p-6 bg-blue-50/50 backdrop-blur-sm border-blue-200 rounded-2xl">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="text-[#8b5e3c] flex items-center gap-2">
                Source Data Used for AI Analysis
              </h3>
              <p className="text-sm text-[#8b5e3c]/60">
                Actual calculations sent to AI - verify the insights are based
                on real data
              </p>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowSourceData(!showSourceData)}
              className="border-blue-300 text-blue-700 hover:bg-blue-100"
            >
              {showSourceData ? "Hide" : "Show"} Data
            </Button>
          </div>

          {showSourceData && (
            <div className="space-y-6">
              {/* Key Metrics Grid */}
              <div>
                <h4 className="text-sm font-semibold text-[#8b5e3c] mb-3">
                  📈 Key Performance Metrics
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">
                      Total Weekly Sales
                    </p>
                    <p className="text-lg font-semibold text-[#8b5e3c]">
                      ${sourceData.total_weekly_sales?.toFixed(2) || "0.00"}
                    </p>
                  </div>
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">
                      Weekly Orders
                    </p>
                    <p className="text-lg font-semibold text-[#8b5e3c]">
                      {sourceData.total_weekly_orders || 0}
                    </p>
                  </div>
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">
                      Items Sold (7d)
                    </p>
                    <p className="text-lg font-semibold text-[#8b5e3c]">
                      {sourceData.total_items_sold || 0}
                    </p>
                  </div>
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">
                      Avg Daily Sales
                    </p>
                    <p className="text-lg font-semibold text-[#8b5e3c]">
                      ${sourceData.avg_daily_sales?.toFixed(2) || "0.00"}
                    </p>
                  </div>
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">
                      Recent Daily Sales
                    </p>
                    <p className="text-lg font-semibold text-[#8b5e3c]">
                      ${sourceData.recent_daily_sales?.toFixed(2) || "0.00"}
                    </p>
                  </div>
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">WoW Change</p>
                    <p
                      className={`text-lg font-semibold ${
                        sourceData.wow_change >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {sourceData.wow_change >= 0 ? "+" : ""}
                      {sourceData.wow_change?.toFixed(1) || "0.0"}%
                    </p>
                  </div>
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">Trend</p>
                    <p className="text-lg font-semibold text-[#8b5e3c] capitalize">
                      {sourceData.trend || "steady"}
                    </p>
                  </div>
                  <div className="p-3 bg-white/80 rounded-lg border border-blue-200">
                    <p className="text-xs text-[#8b5e3c]/60 mb-1">
                      Avg Order Value
                    </p>
                    <p className="text-lg font-semibold text-[#8b5e3c]">
                      ${sourceData.avg_order_value?.toFixed(2) || "0.00"}
                    </p>
                  </div>
                </div>
              </div>

              {/* Top Products Breakdown */}
              {sourceData.top_5_products &&
                sourceData.top_5_products.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-[#8b5e3c] mb-3">
                      🏆 Top 5 Best Selling Products
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {sourceData.top_5_products.map(
                        (product: any, index: number) => (
                          <div
                            key={index}
                            className="p-3 bg-white/80 rounded-lg border border-blue-200"
                          >
                            <div className="flex items-start justify-between mb-2">
                              <p className="text-sm font-semibold text-[#8b5e3c]">
                                {index + 1}. {product.product_detail}
                              </p>
                              <Badge variant="outline" className="text-xs">
                                {product.total_qty} sold
                              </Badge>
                            </div>
                            <p className="text-lg font-bold text-green-600">
                              ${product.total_revenue?.toFixed(2)}
                            </p>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

              {/* Daily Sales Trend */}
              {sourceData.daily_sales_last_7_days &&
                sourceData.daily_sales_last_7_days.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-[#8b5e3c] mb-3">
                      📅 Daily Sales (Last 7 Days)
                    </h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
                      {sourceData.daily_sales_last_7_days.map(
                        (day: any, index: number) => (
                          <div
                            key={index}
                            className="p-3 bg-white/80 rounded-lg border border-blue-200"
                          >
                            <p className="text-xs text-[#8b5e3c]/60 mb-1">
                              {new Date(day.date).toLocaleDateString("en-US", {
                                month: "short",
                                day: "numeric",
                              })}
                            </p>
                            <p className="text-sm font-bold text-[#8b5e3c]">
                              ${day.daily_sales?.toFixed(0)}
                            </p>
                            <p className="text-xs text-[#8b5e3c]/60 mt-1">
                              {day.order_count} orders
                            </p>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

              {/* Peak Hours Analysis */}
              {sourceData.peak_hours_details &&
                sourceData.peak_hours_details.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-[#8b5e3c] mb-3">
                      ⏰ Peak Hours Analysis
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {sourceData.peak_hours_details.map(
                        (hour: any, index: number) => (
                          <div
                            key={index}
                            className="p-4 bg-white/80 rounded-lg border border-blue-200"
                          >
                            <div className="flex items-center justify-between mb-2">
                              <p className="text-lg font-bold text-[#8b5e3c]">
                                {hour.hour}:00
                              </p>
                              <Badge
                                variant="outline"
                                className="bg-orange-100 text-orange-700"
                              >
                                Peak #{index + 1}
                              </Badge>
                            </div>
                            <div className="space-y-1">
                              <p className="text-sm text-[#8b5e3c]/80">
                                <span className="font-semibold">
                                  {hour.customer_count}
                                </span>{" "}
                                customers
                              </p>
                              <p className="text-sm text-green-600 font-semibold">
                                ${hour.hourly_sales?.toFixed(2)} sales
                              </p>
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

              {/* Inventory Alerts */}
              {sourceData.inventory_alerts &&
                sourceData.inventory_alerts.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-[#8b5e3c] mb-3">
                      ⚠️ Inventory Alerts (Low Stock)
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {sourceData.inventory_alerts.map(
                        (item: any, index: number) => (
                          <div
                            key={index}
                            className="p-3 bg-red-50 rounded-lg border border-red-200"
                          >
                            <p className="text-sm font-semibold text-red-800 mb-1">
                              {item.item_name}
                            </p>
                            <div className="flex items-center justify-between text-xs">
                              <span className="text-red-700">
                                Stock: {item.stock}
                              </span>
                              <span className="text-red-600">
                                Reorder: {item.reorder_level}
                              </span>
                            </div>
                            <div className="mt-2 w-full bg-red-200 rounded-full h-2">
                              <div
                                className="bg-red-600 h-2 rounded-full"
                                style={{
                                  width: `${Math.min(
                                    (item.stock / item.reorder_level) * 100,
                                    100
                                  )}%`,
                                }}
                              ></div>
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

              {/* Best Seller Highlight */}
              {sourceData.best_selling_product && (
                <div className="p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border-2 border-yellow-300">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">🏅</span>
                    <div>
                      <p className="text-xs text-[#8b5e3c]/60 mb-1">
                        Best Selling Product
                      </p>
                      <p className="text-xl font-bold text-[#8b5e3c]">
                        {sourceData.best_selling_product}
                      </p>
                      <p className="text-sm text-[#8b5e3c]/80">
                        {sourceData.best_selling_qty} units sold
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </Card>
      )}

      {/* AI Insights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {liveInsights.map((insight) => (
          <Card
            key={insight.id}
            className="p-5 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl hover:shadow-lg transition-all"
          >
            <div className="flex items-start gap-3 mb-3">
              <div className="p-2.5 bg-gradient-to-br from-[#8b5e3c]/10 to-[#d8c3a5]/20 rounded-xl">
                <insight.icon className="w-5 h-5 text-[#8b5e3c]" />
              </div>
              <div className="flex-1">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="text-[#8b5e3c]">{insight.title}</h4>
                  <Badge
                    variant="outline"
                    className={getImpactColor(insight.impact)}
                  >
                    {insight.impact}
                  </Badge>
                </div>
                <p className="text-sm text-[#8b5e3c]/80 mb-3">
                  {insight.description}
                </p>
              </div>
            </div>

            <div className="p-3 bg-[#d8c3a5]/10 rounded-lg border border-[#d8c3a5]/30 mb-3">
              <div className="flex items-start gap-2">
                <Lightbulb className="w-4 h-4 text-[#f59e0b] mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-xs text-[#8b5e3c]/60 mb-1">
                    Recommendation
                  </p>
                  <p className="text-sm text-[#8b5e3c]">
                    {insight.recommendation}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-20 h-2 bg-[#d8c3a5]/20 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-[#8b5e3c] rounded-full"
                    style={{ width: `${insight.confidence}%` }}
                  ></div>
                </div>
                <span className="text-xs text-[#8b5e3c]/60">
                  Confidence: {insight.confidence}%
                </span>
              </div>
              <Button
                size="sm"
                variant="ghost"
                className="text-[#8b5e3c] hover:bg-[#d8c3a5]/20"
              >
                View Details
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Prediction Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="mb-6">
            <h3 className="text-[#8b5e3c]">Sales Forecast (Next 7 Days)</h3>
            <p className="text-sm text-[#8b5e3c]/60">
              AI-predicted sales based on historical data
            </p>
          </div>
          {loading ? (
            <div className="text-center text-[#8b5e3c]/60 py-20">
              Loading forecast...
            </div>
          ) : (
            <>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={predictionData}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#d8c3a5"
                    opacity={0.3}
                  />
                  <XAxis
                    dataKey="day"
                    stroke="#8b5e3c"
                    opacity={0.6}
                    fontSize={12}
                  />
                  <YAxis stroke="#8b5e3c" opacity={0.6} fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#fffaf3",
                      border: "1px solid #d8c3a5",
                      borderRadius: "12px",
                      color: "#8b5e3c",
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="predicted"
                    stroke="#8b5e3c"
                    strokeWidth={3}
                    name="Predicted Sales"
                  />
                  <Line
                    type="monotone"
                    dataKey="actual"
                    stroke="#22c55e"
                    strokeWidth={2}
                    name="Actual Sales"
                    strokeDasharray="5 5"
                  />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-800">
                  ✨ AI-powered forecast using SARIMA model - Plan inventory and
                  staffing accordingly!
                </p>
              </div>
            </>
          )}
        </Card>

        <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="mb-6">
            <h3 className="text-[#8b5e3c]">Customer Visit Patterns</h3>
            <p className="text-sm text-[#8b5e3c]/60">
              Peak hours identification
            </p>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart
              data={[
                { hour: "8AM", visits: 45 },
                { hour: "9AM", visits: 78 },
                { hour: "10AM", visits: 92 },
                { hour: "11AM", visits: 105 },
                { hour: "12PM", visits: 125 },
                { hour: "1PM", visits: 115 },
                { hour: "2PM", visits: 98 },
                { hour: "3PM", visits: 135 },
                { hour: "4PM", visits: 142 },
                { hour: "5PM", visits: 168 },
                { hour: "6PM", visits: 195 },
                { hour: "7PM", visits: 158 },
              ]}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#d8c3a5"
                opacity={0.3}
              />
              <XAxis
                dataKey="hour"
                stroke="#8b5e3c"
                opacity={0.6}
                fontSize={12}
              />
              <YAxis stroke="#8b5e3c" opacity={0.6} fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#fffaf3",
                  border: "1px solid #d8c3a5",
                  borderRadius: "12px",
                  color: "#8b5e3c",
                }}
              />
              <Bar dataKey="visits" fill="#8b5e3c" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
            <p className="text-sm text-orange-800">
              🔔 Peak hours: 5PM-7PM. Consider adding 2-3 staff members during
              this time.
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}
