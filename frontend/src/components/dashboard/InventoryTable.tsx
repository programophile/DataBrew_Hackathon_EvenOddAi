import { useEffect, useState } from "react";
import { Card } from "../ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table";
import { Badge } from "../ui/badge";
import { AlertCircle, AlertTriangle, CheckCircle } from "lucide-react";
import { apiService } from "../../services/api";

export function InventoryTable() {
  const [inventoryData, setInventoryData] = useState<Array<{
    product: string;
    current_stock: string;
    predicted_demand: string;
    demand_level: string;
    alert_level: string;
  }>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const data = await apiService.getInventoryPredictions();
        setInventoryData(data.inventory);
      } catch (error) {
        console.error("Failed to fetch inventory:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchInventory();
  }, []);
  const getAlertIcon = (level: string) => {
    switch (level) {
      case "critical":
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case "warning":
        return <AlertTriangle className="w-5 h-5 text-orange-500" />;
      case "safe":
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      default:
        return null;
    }
  };

  return (
    <Card className="p-6 bg-white/60 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
      <div className="mb-4">
        <h3 className="text-[#8b5e3c]">AI Predicted Product Demand</h3>
        <p className="text-sm text-[#8b5e3c]/60">Smart inventory forecasting for the next 7 days</p>
      </div>

      <Table>
        <TableHeader>
          <TableRow className="border-[#d8c3a5]/30">
            <TableHead className="text-[#8b5e3c]">Product</TableHead>
            <TableHead className="text-[#8b5e3c]">Current Stock</TableHead>
            <TableHead className="text-[#8b5e3c]">AI Predicted Demand</TableHead>
            <TableHead className="text-[#8b5e3c]">Reorder Alert</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {loading ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center text-[#8b5e3c]/60">
                Loading inventory...
              </TableCell>
            </TableRow>
          ) : inventoryData.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center text-[#8b5e3c]/60">
                No inventory data available
              </TableCell>
            </TableRow>
          ) : (
            inventoryData.map((item, index) => (
              <TableRow key={index} className="border-[#d8c3a5]/30 hover:bg-[#d8c3a5]/10">
                <TableCell className="text-[#8b5e3c]">{item.product}</TableCell>
                <TableCell className="text-[#8b5e3c]/80">{item.current_stock}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span className="text-[#8b5e3c]/80">{item.predicted_demand}</span>
                    <Badge
                      variant="outline"
                      className={`${
                        item.demand_level.includes("High")
                          ? "border-red-300 text-red-700 bg-red-50"
                          : item.demand_level.includes("Medium")
                          ? "border-orange-300 text-orange-700 bg-orange-50"
                          : "border-green-300 text-green-700 bg-green-50"
                      }`}
                    >
                      {item.demand_level}
                    </Badge>
                  </div>
                </TableCell>
                <TableCell>{getAlertIcon(item.alert_level)}</TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </Card>
  );
}
