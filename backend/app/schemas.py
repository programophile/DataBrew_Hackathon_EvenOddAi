from pydantic import BaseModel
from typing import List, Optional


# ===============================
# Weekly Sales History Item
# ===============================
class WeeklySalesItem(BaseModel):
    week_index: int        # week number (0, 1, 2, ...)
    total_qty: int         # total sold


# ===============================
# Weekly Sales Trend for One Product
# ===============================
class WeeklySalesTrend(BaseModel):
    product_id: int
    product_name: str
    history: List[WeeklySalesItem]
    percent_change: Optional[float]  # positive = increase, negative = decrease


# ===============================
# Final Response: Top Increase + Top Decrease
# ===============================
class WeeklySalesSummary(BaseModel):
    top_increase: Optional[WeeklySalesTrend]
    top_decrease: Optional[WeeklySalesTrend]