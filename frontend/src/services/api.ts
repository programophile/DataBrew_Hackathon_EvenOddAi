// API Configuration and Service
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Generic API fetch function with error handling
async function apiRequest<T>(endpoint: string): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    throw error;
  }
}

// API Service functions
export const apiService = {
  // Get forecast data
  getForecast: (days: number = 7) =>
    apiRequest<{
      forecast_next_days: number[];
      last_date_in_data: string;
      days_forecasted: number;
    }>(`/forecast?days=${days}`),

  // Get AI insights
  getAIInsights: () =>
    apiRequest<{
      insights: Array<{
        type: string;
        text: string;
        color: string;
      }>;
    }>("/ai-insights"),

  // Get sales data
  getSalesData: (period: string = "month") =>
    apiRequest<{
      sales_data: Array<{
        date: string;
        sales: number;
      }>;
      period: string;
    }>(`/sales-data?period=${period}`),

  // Get dashboard metrics
  getDashboardMetrics: () =>
    apiRequest<{
      total_sales: number;
      sales_trend: number;
      total_customers: number;
      profit_margin: number;
      active_baristas: number;
      sales_sparkline: number[];
    }>("/dashboard-metrics"),

  // Get best selling product
  getBestSelling: () =>
    apiRequest<{
      product_name: string;
      product_type: string;
      units_sold: number;
      revenue: number;
      change_percent: number;
    }>("/best-selling"),

  // Get inventory predictions
  getInventoryPredictions: () =>
    apiRequest<{
      inventory: Array<{
        product: string;
        current_stock: string;
        predicted_demand: string;
        demand_level: string;
        alert_level: string;
      }>;
    }>("/inventory-predictions"),

  // Get barista schedule
  getBaristaSchedule: () =>
    apiRequest<{
      schedule: Array<{
        name: string;
        role: string;
        shift: string;
        performance: number;
      }>;
    }>("/barista-schedule"),

  // Get customer feedback
  getCustomerFeedback: () =>
    apiRequest<{
      feedback: Array<{
        customer: string;
        rating: number;
        comment: string;
        date: string;
      }>;
    }>("/customer-feedback"),

  // Get sales analytics
  getSalesAnalytics: () =>
    apiRequest<{
      total_revenue: number;
      total_orders: number;
      avg_order_value: number;
      profit_margin: number;
      product_sales: Array<{
        name: string;
        sales: number;
        percentage: number;
      }>;
      hourly_sales: Array<{
        time: string;
        sales: number;
      }>;
      monthly_sales: Array<{
        date: string;
        sales: number;
        target: number;
      }>;
    }>("/sales-analytics"),

  // Get cash flow data
  getCashFlow: (period: string = "month") =>
    apiRequest<{
      cash_flow: Array<{
        month: string;
        income: number;
        expenses: number;
      }>;
      period: string;
    }>(`/cash-flow?period=${period}`),

  // Generate new AI insights
  generateInsights: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-insights`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error generating insights:`, error);
      throw error;
    }
  },
};
