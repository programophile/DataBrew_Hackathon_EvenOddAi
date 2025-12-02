import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { Badge } from "../ui/badge";
import { Clock, Users } from "lucide-react";
import { apiService } from "../../services/api";

export function BaristaSchedule() {
  const [schedule, setSchedule] = useState<Array<{
    name: string;
    role: string;
    shift: string;
    performance: number;
  }>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const data = await apiService.getBaristaSchedule();
        setSchedule(data.schedule);
      } catch (error) {
        console.error("Failed to fetch barista schedule:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSchedule();
  }, []);

  return (
    <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-[#8b5e3c]">Barista Scheduling</h3>
          <p className="text-sm text-[#8b5e3c]/60">AI-optimized staff allocation</p>
        </div>
        <Badge className="bg-[#8b5e3c]/10 text-[#8b5e3c] border-[#8b5e3c]/20">
          <Clock className="w-3 h-3 mr-1" />
          This Week
        </Badge>
      </div>

      <div className="space-y-3">
        {loading ? (
          <div className="text-center text-[#8b5e3c]/60 py-4">Loading schedule...</div>
        ) : schedule.length === 0 ? (
          <div className="text-center text-[#8b5e3c]/60 py-4">No schedule data available</div>
        ) : (
          schedule.map((barista, index) => (
            <div
              key={index}
              className="p-4 bg-white/60 backdrop-blur-sm rounded-xl border border-[#d8c3a5]/30 hover:shadow-md transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-[#8b5e3c] to-[#b08968] rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold">{barista.name.charAt(0)}</span>
                  </div>
                  <div>
                    <h4 className="text-[#8b5e3c] font-medium">{barista.name}</h4>
                    <div className="flex items-center gap-2 text-sm text-[#8b5e3c]/60">
                      <Clock className="w-3 h-3" />
                      <span>{barista.shift}</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-[#8b5e3c]/60">Performance</p>
                  <p className="text-[#8b5e3c] font-semibold">{barista.performance.toFixed(1)}%</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
        <p className="text-xs text-orange-800">
          ⚠️ AI Suggestion: Add 2 baristas on Tuesday 2PM-8PM (High demand predicted)
        </p>
      </div>
    </Card>
  );
}
