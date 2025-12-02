import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { Button } from "../ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { TrendingUp, DollarSign, ShoppingCart, Percent } from "lucide-react";
import { apiService } from "../../services/api";

const COLORS = ["#8b5e3c", "#b08968", "#d8c3a5", "#e8d5c4", "#f5ebe0"];

export function SalesAnalyticsPage() {
  const [analytics, setAnalytics] = useState({
    total_revenue: 0,
    total_orders: 0,
    avg_order_value: 0,
    profit_margin: 0,
    product_sales: [] as Array<{
      name: string;
      sales: number;
      percentage: number;
    }>,
    hourly_sales: [] as Array<{ time: string; sales: number }>,
    monthly_sales: [] as Array<{ date: string; sales: number; target: number }>,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await apiService.getSalesAnalytics();
        setAnalytics(data);
      } catch (error) {
        console.error("Failed to fetch sales analytics:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-gradient-to-br from-[#8b5e3c]/10 to-[#d8c3a5]/20 rounded-xl">
              <DollarSign className="w-6 h-6 text-[#8b5e3c]" />
            </div>
            <div>
              <p className="text-sm text-[#8b5e3c]/60">Total Revenue</p>
              <p className="text-2xl text-[#8b5e3c]">
                {loading
                  ? "Loading..."
                  : `৳${analytics.total_revenue.toLocaleString()}`}
              </p>
            </div>
          </div>
          <p className="text-xs text-green-600">Last 30 days</p>
        </Card>

        <Card className="p-5 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-gradient-to-br from-[#8b5e3c]/10 to-[#d8c3a5]/20 rounded-xl">
              <ShoppingCart className="w-6 h-6 text-[#b08968]" />
            </div>
            <div>
              <p className="text-sm text-[#8b5e3c]/60">Total Orders</p>
              <p className="text-2xl text-[#8b5e3c]">
                {loading
                  ? "Loading..."
                  : analytics.total_orders.toLocaleString()}
              </p>
            </div>
          </div>
          <p className="text-xs text-green-600">Last 30 days</p>
        </Card>

        <Card className="p-5 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-gradient-to-br from-[#8b5e3c]/10 to-[#d8c3a5]/20 rounded-xl">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-[#8b5e3c]/60">Avg Order Value</p>
              <p className="text-2xl text-[#8b5e3c]">
                {loading
                  ? "Loading..."
                  : `৳${Math.round(analytics.avg_order_value)}`}
              </p>
            </div>
          </div>
          <p className="text-xs text-green-600">Per transaction</p>
        </Card>

        <Card className="p-5 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-gradient-to-br from-[#8b5e3c]/10 to-[#d8c3a5]/20 rounded-xl">
              <Percent className="w-6 h-6 text-[#f59e0b]" />
            </div>
            <div>
              <p className="text-sm text-[#8b5e3c]/60">Profit Margin</p>
              <p className="text-2xl text-[#8b5e3c]">
                {loading ? "Loading..." : `${analytics.profit_margin}%`}
              </p>
            </div>
          </div>
          <p className="text-xs text-green-600">Estimated</p>
        </Card>
      </div>

      {/* Tabs for Different Views */}
      <Tabs defaultValue="hourly" className="w-full">
        <TabsList className="bg-white/60 border border-[#d8c3a5]/30">
          <TabsTrigger
            value="hourly"
            className="data-[state=active]:bg-[#8b5e3c] data-[state=active]:text-white"
          >
            Hourly Sales
          </TabsTrigger>
          <TabsTrigger
            value="products"
            className="data-[state=active]:bg-[#8b5e3c] data-[state=active]:text-white"
          >
            Product Breakdown
          </TabsTrigger>
          <TabsTrigger
            value="monthly"
            className="data-[state=active]:bg-[#8b5e3c] data-[state=active]:text-white"
          >
            Monthly Performance
          </TabsTrigger>
        </TabsList>

        <TabsContent value="hourly" className="mt-6">
          <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-[#8b5e3c]">Hourly Sales Breakdown</h3>
                <p className="text-sm text-[#8b5e3c]/60">
                  Today's sales by hour
                </p>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="border-[#d8c3a5] text-[#8b5e3c] hover:bg-[#8b5e3c] hover:text-white bg-[#8b5e3c] text-white"
                >
                  Today
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="border-[#d8c3a5] text-[#8b5e3c] hover:bg-[#8b5e3c] hover:text-white"
                >
                  Yesterday
                </Button>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={analytics.hourly_sales}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#d8c3a5"
                  opacity={0.3}
                />
                <XAxis
                  dataKey="time"
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
                <Bar dataKey="sales" fill="#8b5e3c" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>

        <TabsContent value="products" className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
              <h3 className="text-[#8b5e3c] mb-6">
                Sales Distribution by Product
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={analytics.product_sales}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percentage }) => `${name} ${percentage}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="sales"
                  >
                    {analytics.product_sales.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#fffaf3",
                      border: "1px solid #d8c3a5",
                      borderRadius: "12px",
                      color: "#8b5e3c",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </Card>

            <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
              <h3 className="text-[#8b5e3c] mb-4">Top Products Performance</h3>
              <div className="space-y-4">
                {analytics.product_sales.map((product, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: COLORS[index] }}
                        ></div>
                        <span className="text-sm text-[#8b5e3c]">
                          {product.name}
                        </span>
                      </div>
                      <span className="text-sm text-[#8b5e3c]">
                        ৳{product.sales.toLocaleString()}
                      </span>
                    </div>
                    <div className="w-full h-2 bg-[#d8c3a5]/20 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all"
                        style={{
                          width: `${product.percentage * 3}%`,
                          backgroundColor: COLORS[index],
                        }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="monthly" className="mt-6">
          <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
            <div className="mb-6">
              <h3 className="text-[#8b5e3c]">Monthly Sales vs Target</h3>
              <p className="text-sm text-[#8b5e3c]/60">
                Last 6 months performance
              </p>
            </div>
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={analytics.monthly_sales}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#d8c3a5"
                  opacity={0.3}
                />
                <XAxis
                  dataKey="date"
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
                <Legend />
                <Line
                  type="monotone"
                  dataKey="sales"
                  stroke="#8b5e3c"
                  strokeWidth={3}
                  name="Actual Sales"
                />
                <Line
                  type="monotone"
                  dataKey="target"
                  stroke="#d8c3a5"
                  strokeWidth={3}
                  strokeDasharray="5 5"
                  name="Target"
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
