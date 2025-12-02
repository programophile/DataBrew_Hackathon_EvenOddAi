import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { Button } from "../ui/button";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { apiService } from "../../services/api";

export function SalesChart() {
  const [salesData, setSalesData] = useState<Array<{ date: string; sales: number }>>([]);
  const [period, setPeriod] = useState("month");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSalesData = async () => {
      setLoading(true);
      try {
        const data = await apiService.getSalesData(period);
        setSalesData(data.sales_data);
      } catch (error) {
        console.error("Failed to fetch sales data:", error);
        // Fallback data
        setSalesData([
          { date: "Oct 1", sales: 8500 },
          { date: "Oct 3", sales: 9200 },
          { date: "Oct 5", sales: 8800 },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchSalesData();
  }, [period]);

  return (
    <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-[#8b5e3c]">Sales Trend Over Time</h3>
          <p className="text-sm text-[#8b5e3c]/60">
            {loading ? "Loading..." : `Past ${period === "today" ? "day" : period === "week" ? "7 days" : "30 days"} performance`}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className={`border-[#d8c3a5] text-[#8b5e3c] hover:bg-[#8b5e3c] hover:text-white ${period === "today" ? "bg-[#8b5e3c] text-white" : ""}`}
            onClick={() => setPeriod("today")}
          >
            Today
          </Button>
          <Button
            variant="outline"
            size="sm"
            className={`border-[#d8c3a5] text-[#8b5e3c] hover:bg-[#8b5e3c] hover:text-white ${period === "week" ? "bg-[#8b5e3c] text-white" : ""}`}
            onClick={() => setPeriod("week")}
          >
            Week
          </Button>
          <Button
            variant="outline"
            size="sm"
            className={`border-[#d8c3a5] text-[#8b5e3c] hover:bg-[#8b5e3c] hover:text-white ${period === "month" ? "bg-[#8b5e3c] text-white" : ""}`}
            onClick={() => setPeriod("month")}
          >
            Month
          </Button>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={salesData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#d8c3a5" opacity={0.3} />
          <XAxis dataKey="date" stroke="#8b5e3c" opacity={0.6} fontSize={12} />
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
            dataKey="sales"
            stroke="#8b5e3c"
            strokeWidth={3}
            dot={{ fill: "#8b5e3c", r: 4 }}
            activeDot={{ r: 6, fill: "#8b5e3c" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}
