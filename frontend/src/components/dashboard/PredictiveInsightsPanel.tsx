import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import {
  Cloud,
  CloudRain,
  Sun,
  Calendar,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Lightbulb,
  RefreshCw,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

interface WeatherInsight {
  date: string;
  impact: "positive" | "negative" | "neutral";
  prediction: string;
  recommendation: string;
  confidence?: string;
}

interface HolidayInsight {
  holiday_name: string;
  date: string;
  expected_sales_increase: string;
  recommendation: string;
  product_suggestions?: string[];
}

interface Abnormality {
  date: string;
  type: "risk" | "opportunity";
  description: string;
  impact: string;
  mitigation?: string;
}

interface ActionableRecommendation {
  category: string;
  priority: "high" | "medium" | "low";
  recommendation: string;
  expected_outcome?: string;
  timeframe?: string;
}

interface Summary {
  overall_outlook: "positive" | "neutral" | "challenging";
  total_predicted_impact: string;
  key_dates_to_watch?: string[];
  top_3_priorities: string[];
}

interface PredictiveInsightsData {
  status: string;
  insights: {
    weather_insights: WeatherInsight[];
    holiday_insights: HolidayInsight[];
    abnormalities: Abnormality[];
    actionable_recommendations: ActionableRecommendation[];
    summary: Summary;
  };
  data_summary: {
    holidays_count: number;
    weather_days: number;
    sales_days_analyzed: number;
    avg_daily_sales: number;
    sales_trend: string;
  };
}

export function PredictiveInsightsPanel() {
  const [data, setData] = useState<PredictiveInsightsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState({
    weather: true,
    holidays: true,
    risks: true,
    recommendations: true,
  });

  const fetchPredictiveInsights = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8080/predictive-insights");
      if (!response.ok) throw new Error("Failed to fetch insights");

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPredictiveInsights();
  }, []);

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  const getImpactIcon = (impact: string) => {
    switch (impact.toLowerCase()) {
      case "positive":
        return <TrendingUp className="w-4 h-4 text-green-600" />;
      case "negative":
        return <TrendingDown className="w-4 h-4 text-red-600" />;
      default:
        return <Sun className="w-4 h-4 text-blue-600" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
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

  const getOutlookColor = (outlook: string) => {
    switch (outlook) {
      case "positive":
        return "text-green-600 bg-green-50 border-green-200";
      case "challenging":
        return "text-red-600 bg-red-50 border-red-200";
      default:
        return "text-blue-600 bg-blue-50 border-blue-200";
    }
  };

  if (loading) {
    return (
      <Card className="p-8 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
        <div className="flex flex-col items-center justify-center space-y-4">
          <RefreshCw className="w-12 h-12 text-[#8b5e3c] animate-spin" />
          <div className="text-center">
            <h3 className="text-[#8b5e3c] font-semibold">Analyzing Data...</h3>
            <p className="text-sm text-[#8b5e3c]/60 mt-1">
              Combining weather, holidays, and sales data
            </p>
          </div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-6 bg-red-50/60 backdrop-blur-sm border-red-200 rounded-2xl">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-6 h-6 text-red-600 flex-shrink-0" />
          <div>
            <h3 className="text-red-800 font-semibold">
              Failed to Load Insights
            </h3>
            <p className="text-sm text-red-600 mt-1">{error}</p>
            <Button
              onClick={fetchPredictiveInsights}
              className="mt-3 bg-red-600 hover:bg-red-700 text-white"
              size="sm"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Retry
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  if (!data || !data.insights) return null;

  const { insights, data_summary } = data;

  return (
    <div className="space-y-6">
      {/* Header with Summary */}
      <Card className="p-6 bg-gradient-to-br from-[#8b5e3c]/10 to-[#d8c3a5]/20 backdrop-blur-sm border-[#8b5e3c]/20 rounded-2xl">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-[#8b5e3c] mb-2">
               Predictive Business Intelligence
            </h2>
            <p className="text-sm text-[#8b5e3c]/70">
              AI-powered insights based on weather, holidays, and sales trends
            </p>
          </div>
          <Button
            onClick={fetchPredictiveInsights}
            disabled={loading}
            className="bg-[#8b5e3c] hover:bg-[#b08968] text-white"
            size="sm"
          >
            <RefreshCw
              className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`}
            />
            Refresh
          </Button>
        </div>

        {/* Summary Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="p-4 bg-white/80 rounded-xl border border-[#d8c3a5]/30">
            <p className="text-xs text-[#8b5e3c]/60 mb-1">Outlook (7 Days)</p>
            <div className="flex items-center gap-2">
              <Badge
                className={getOutlookColor(insights.summary.overall_outlook)}
              >
                {insights.summary.overall_outlook}
              </Badge>
              <span className="text-lg font-bold text-[#8b5e3c]">
                {insights.summary.total_predicted_impact}
              </span>
            </div>
          </div>
          <div className="p-4 bg-white/80 rounded-xl border border-[#d8c3a5]/30">
            <p className="text-xs text-[#8b5e3c]/60 mb-1">Avg Daily Sales</p>
            <p className="text-lg font-bold text-[#8b5e3c]">
              ${data_summary.avg_daily_sales?.toFixed(0) || "0"}
            </p>
            <p className="text-xs text-[#8b5e3c]/60 mt-1 capitalize">
              Trend: {data_summary.sales_trend}
            </p>
          </div>
          <div className="p-4 bg-white/80 rounded-xl border border-[#d8c3a5]/30">
            <p className="text-xs text-[#8b5e3c]/60 mb-1">Data Sources</p>
            <p className="text-sm text-[#8b5e3c]">
              {data_summary.holidays_count} holidays •{" "}
              {data_summary.weather_days}d weather
            </p>
            <p className="text-xs text-[#8b5e3c]/60 mt-1">
              {data_summary.sales_days_analyzed} days sales
            </p>
          </div>
          <div className="p-4 bg-white/80 rounded-xl border border-[#d8c3a5]/30">
            <p className="text-xs text-[#8b5e3c]/60 mb-1">Total Insights</p>
            <p className="text-lg font-bold text-[#8b5e3c]">
              {insights.weather_insights.length +
                insights.holiday_insights.length +
                insights.actionable_recommendations.length}
            </p>
          </div>
        </div>

        {/* Top Priorities */}
        <div className="p-4 bg-white/60 rounded-xl border border-[#d8c3a5]/30">
          <h4 className="text-sm font-semibold text-[#8b5e3c] mb-3 flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-yellow-600" />
            Top 3 Priorities
          </h4>
          <div className="space-y-2">
            {insights.summary.top_3_priorities.map((priority, index) => (
              <div key={index} className="flex items-start gap-2">
                <span className="flex-shrink-0 w-6 h-6 bg-[#8b5e3c] text-white rounded-full flex items-center justify-center text-xs font-bold">
                  {index + 1}
                </span>
                <p className="text-sm text-[#8b5e3c] flex-1">{priority}</p>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Weather Impact Section */}
      <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
        <button
          onClick={() => toggleSection("weather")}
          className="w-full flex items-center justify-between mb-4"
        >
          <div className="flex items-center gap-3">
            <Cloud className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-[#8b5e3c]">
               Weather Impact Analysis
            </h3>
            <Badge variant="outline" className="bg-blue-50 text-blue-700">
              {insights.weather_insights.length} insights
            </Badge>
          </div>
          {expandedSections.weather ? (
            <ChevronUp className="w-5 h-5 text-[#8b5e3c]" />
          ) : (
            <ChevronDown className="w-5 h-5 text-[#8b5e3c]" />
          )}
        </button>

        {expandedSections.weather && (
          <div className="space-y-3">
            {insights.weather_insights.map((insight, index) => (
              <div
                key={index}
                className="p-4 bg-gradient-to-r from-blue-50/50 to-white rounded-xl border border-blue-200/50"
              >
                <div className="flex items-start gap-3">
                  {getImpactIcon(insight.impact)}
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <p className="text-sm font-semibold text-[#8b5e3c]">
                        {insight.date}
                      </p>
                      <Badge
                        variant="outline"
                        className={
                          insight.impact === "positive"
                            ? "bg-green-50 text-green-700"
                            : insight.impact === "negative"
                            ? "bg-red-50 text-red-700"
                            : "bg-gray-50 text-gray-700"
                        }
                      >
                        {insight.impact}
                      </Badge>
                    </div>
                    <p className="text-sm text-[#8b5e3c] mb-2">
                      {insight.prediction}
                    </p>
                    <div className="p-2 bg-white/80 rounded-lg border border-blue-200/50">
                      <p className="text-xs text-[#8b5e3c]/70">
                        <strong>Action:</strong> {insight.recommendation}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Holiday Opportunities Section */}
      {insights.holiday_insights.length > 0 && (
        <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <button
            onClick={() => toggleSection("holidays")}
            className="w-full flex items-center justify-between mb-4"
          >
            <div className="flex items-center gap-3">
              <Calendar className="w-5 h-5 text-purple-600" />
              <h3 className="text-lg font-semibold text-[#8b5e3c]">
                 Holiday Opportunities
              </h3>
              <Badge variant="outline" className="bg-purple-50 text-purple-700">
                {insights.holiday_insights.length} holidays
              </Badge>
            </div>
            {expandedSections.holidays ? (
              <ChevronUp className="w-5 h-5 text-[#8b5e3c]" />
            ) : (
              <ChevronDown className="w-5 h-5 text-[#8b5e3c]" />
            )}
          </button>

          {expandedSections.holidays && (
            <div className="space-y-3">
              {insights.holiday_insights.map((insight, index) => (
                <div
                  key={index}
                  className="p-4 bg-gradient-to-r from-purple-50/50 to-white rounded-xl border border-purple-200/50"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <p className="text-lg font-bold text-[#8b5e3c]">
                        {insight.holiday_name}
                      </p>
                      <p className="text-sm text-[#8b5e3c]/60">
                        {insight.date}
                      </p>
                    </div>
                    <Badge className="bg-green-100 text-green-700 border-green-300">
                      +{insight.expected_sales_increase}
                    </Badge>
                  </div>
                  <p className="text-sm text-[#8b5e3c] mb-3">
                    {insight.recommendation}
                  </p>
                  {insight.product_suggestions &&
                    insight.product_suggestions.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {insight.product_suggestions.map((product, idx) => (
                          <Badge
                            key={idx}
                            variant="outline"
                            className="bg-white text-[#8b5e3c]"
                          >
                            {product}
                          </Badge>
                        ))}
                      </div>
                    )}
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Abnormalities & Risks Section */}
      {insights.abnormalities.length > 0 && (
        <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <button
            onClick={() => toggleSection("risks")}
            className="w-full flex items-center justify-between mb-4"
          >
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-orange-600" />
              <h3 className="text-lg font-semibold text-[#8b5e3c]">
                 Risks & Opportunities
              </h3>
              <Badge variant="outline" className="bg-orange-50 text-orange-700">
                {insights.abnormalities.length} alerts
              </Badge>
            </div>
            {expandedSections.risks ? (
              <ChevronUp className="w-5 h-5 text-[#8b5e3c]" />
            ) : (
              <ChevronDown className="w-5 h-5 text-[#8b5e3c]" />
            )}
          </button>

          {expandedSections.risks && (
            <div className="space-y-3">
              {insights.abnormalities.map((abnormality, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-xl border ${
                    abnormality.type === "risk"
                      ? "bg-gradient-to-r from-red-50/50 to-white border-red-200/50"
                      : "bg-gradient-to-r from-green-50/50 to-white border-green-200/50"
                  }`}
                >
                  <div className="flex items-start gap-3">
                    {abnormality.type === "risk" ? (
                      <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0" />
                    ) : (
                      <TrendingUp className="w-5 h-5 text-green-600 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <p className="text-sm font-semibold text-[#8b5e3c]">
                          {abnormality.date}
                        </p>
                        <Badge
                          variant="outline"
                          className={
                            abnormality.type === "risk"
                              ? "bg-red-100 text-red-700"
                              : "bg-green-100 text-green-700"
                          }
                        >
                          {abnormality.type}
                        </Badge>
                      </div>
                      <p className="text-sm text-[#8b5e3c] mb-2">
                        {abnormality.description}
                      </p>
                      <div className="space-y-2">
                        <div className="p-2 bg-white/80 rounded-lg border border-gray-200">
                          <p className="text-xs text-[#8b5e3c]/70">
                            <strong>Impact:</strong> {abnormality.impact}
                          </p>
                        </div>
                        {abnormality.mitigation && (
                          <div className="p-2 bg-white/80 rounded-lg border border-gray-200">
                            <p className="text-xs text-[#8b5e3c]/70">
                              <strong>Mitigation:</strong>{" "}
                              {abnormality.mitigation}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Actionable Recommendations Section */}
      <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
        <button
          onClick={() => toggleSection("recommendations")}
          className="w-full flex items-center justify-between mb-4"
        >
          <div className="flex items-center gap-3">
            <Lightbulb className="w-5 h-5 text-yellow-600" />
            <h3 className="text-lg font-semibold text-[#8b5e3c]">
               Actionable Recommendations
            </h3>
            <Badge variant="outline" className="bg-yellow-50 text-yellow-700">
              {insights.actionable_recommendations.length} actions
            </Badge>
          </div>
          {expandedSections.recommendations ? (
            <ChevronUp className="w-5 h-5 text-[#8b5e3c]" />
          ) : (
            <ChevronDown className="w-5 h-5 text-[#8b5e3c]" />
          )}
        </button>

        {expandedSections.recommendations && (
          <div className="space-y-3">
            {insights.actionable_recommendations.map((rec, index) => (
              <div
                key={index}
                className="p-4 bg-gradient-to-r from-yellow-50/50 to-white rounded-xl border border-yellow-200/50"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <Badge
                      variant="outline"
                      className="capitalize text-[#8b5e3c]"
                    >
                      {rec.category}
                    </Badge>
                    <Badge className={getPriorityColor(rec.priority)}>
                      {rec.priority} priority
                    </Badge>
                  </div>
                </div>
                <p className="text-sm text-[#8b5e3c] font-medium mb-2">
                  {rec.recommendation}
                </p>
                {rec.expected_outcome && (
                  <div className="p-2 bg-white/80 rounded-lg border border-yellow-200/50">
                    <p className="text-xs text-[#8b5e3c]/70">
                      <strong>Expected outcome:</strong> {rec.expected_outcome}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
