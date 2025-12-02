import { useEffect, useState } from "react";
import { MetricCard } from "../dashboard/MetricCard";
import { SalesChart } from "../dashboard/SalesChart";
import { CashFlowChart } from "../dashboard/CashFlowChart";
import { InventoryTable } from "../dashboard/InventoryTable";
import { AIInsightsPanel } from "../dashboard/AIInsightsPanel";
import { BaristaSchedule } from "../dashboard/BaristaSchedule";
import { BestSelling } from "../dashboard/BestSelling";
import { CustomerFeedback } from "../dashboard/CustomerFeedback";
import { Coffee, Users, DollarSign, UserCheck } from "lucide-react";
import { apiService } from "../../services/api";

export function DashboardPage() {
  const [metrics, setMetrics] = useState({
    total_sales: 0,
    sales_trend: 0,
    total_customers: 0,
    profit_margin: 0,
    active_baristas: 0,
    sales_sparkline: [8200, 8500, 9100, 8800, 9300, 10200, 12540],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await apiService.getDashboardMetrics();
        setMetrics(data);
      } catch (error) {
        console.error("Failed to fetch dashboard metrics:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  return (
    <div className="space-y-6">
      {/* Section A - Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={Coffee}
          title="Total Sales (Today)"
          value={loading ? "Loading..." : `৳${metrics.total_sales.toLocaleString()}`}
          trend={metrics.sales_trend >= 0 ? "up" : "down"}
          trendValue={`${metrics.sales_trend >= 0 ? '+' : ''}${metrics.sales_trend.toFixed(1)}%`}
          sparkData={metrics.sales_sparkline}
          iconColor="#8b5e3c"
        />
        <MetricCard
          icon={Users}
          title="Total Customers"
          value={loading ? "Loading..." : metrics.total_customers.toString()}
          trend="up"
          trendValue="+12%"
          sparkData={[180, 220, 250, 280, 290, 310, metrics.total_customers]}
          iconColor="#b08968"
        />
        <MetricCard
          icon={DollarSign}
          title="Net Profit Margin"
          value={loading ? "Loading..." : `${metrics.profit_margin}%`}
          trend="up"
          trendValue="+3.5%"
          sparkData={[18, 18.5, 19, 20, 21, 21.5, metrics.profit_margin]}
          iconColor="#22c55e"
        />
        <MetricCard
          icon={UserCheck}
          title="Active Baristas Needed"
          value={loading ? "Loading..." : metrics.active_baristas.toString()}
          trend="down"
          trendValue="6 PM – 10 PM"
          sparkData={[2, 2, 3, 4, 3, 3, metrics.active_baristas]}
          iconColor="#f59e0b"
        />
      </div>

      {/* Section B - Sales & Cash Flow Graphs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SalesChart />
        <CashFlowChart />
      </div>

      {/* Section C - Inventory Table */}
      <InventoryTable />

      {/* Section D & E - AI Insights and Barista Schedule */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AIInsightsPanel />
        <BaristaSchedule />
      </div>

      {/* Optional Widgets - Best Selling & Customer Feedback */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <BestSelling />
        <CustomerFeedback />
      </div>
    </div>
  );
}
