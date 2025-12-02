import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { Button } from "../ui/button";
import { Sparkles, TrendingUp, Users, Clock } from "lucide-react";
import { apiService } from "../../services/api";

const iconMap: Record<string, any> = {
  trending_up: TrendingUp,
  users: Users,
  clock: Clock,
};

export function AIInsightsPanel() {
  const [insights, setInsights] = useState<Array<{
    type: string;
    text: string;
    color: string;
  }>>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const data = await apiService.getAIInsights();
        setInsights(data.insights);
      } catch (error) {
        console.error("Failed to fetch AI insights:", error);
        // Fallback to default insights
        setInsights([
          {
            type: "trending_up",
            text: "Loading insights...",
            color: "#22c55e",
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, []);

  const handleGenerateReport = async () => {
    setGenerating(true);
    try {
      const response = await apiService.generateInsights();
      setInsights(response.insights);
      console.log("Generated new insights:", response);
    } catch (error) {
      console.error("Failed to generate insights:", error);
      alert("Failed to generate new insights. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <Card className="p-6 bg-gradient-to-br from-[#8b5e3c]/5 to-[#d8c3a5]/10 backdrop-blur-sm border-[#8b5e3c]/20 rounded-2xl relative overflow-hidden">
      {/* Glow effect */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-[#8b5e3c]/10 rounded-full blur-3xl"></div>
      
      <div className="relative z-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="p-2 bg-gradient-to-br from-[#8b5e3c] to-[#b08968] rounded-xl">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-[#8b5e3c]">AI Insights</h3>
        </div>

        <div className="space-y-3 mb-6">
          {loading ? (
            <div className="text-center text-[#8b5e3c]/60">Loading insights...</div>
          ) : (
            insights.map((insight, index) => {
              const Icon = iconMap[insight.type] || TrendingUp;
              return (
                <div
                  key={index}
                  className="flex items-start gap-3 p-4 bg-white/60 backdrop-blur-sm rounded-xl border border-[#d8c3a5]/30 hover:shadow-md transition-all"
                >
                  <div className="p-2 rounded-lg" style={{ backgroundColor: `${insight.color}15` }}>
                    <Icon className="w-4 h-4" style={{ color: insight.color }} />
                  </div>
                  <p className="text-sm text-[#8b5e3c]/90 flex-1">{insight.text}</p>
                </div>
              );
            })
          )}
        </div>

        <Button
          className="w-full bg-gradient-to-r from-[#8b5e3c] to-[#b08968] hover:from-[#b08968] hover:to-[#8b5e3c] text-white shadow-lg shadow-[#8b5e3c]/30"
          onClick={handleGenerateReport}
          disabled={generating}
        >
          <Sparkles className="w-4 h-4 mr-2" />
          {generating ? "Generating..." : "Generate AI Report"}
        </Button>
      </div>
    </Card>
  );
}
