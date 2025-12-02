from typing import Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas import WeeklySalesItem, WeeklySalesTrend, WeeklySalesSummary


def get_weekly_sales(db: Session):
    """
    Aggregate total quantity per product per week.
    Uses SQLite strftime('%W', ...) to get week-of-year.
    """
    rows = (
        db.query(
            Transaction.product_id,
            Transaction.product_type.label("product_name"),
            func.strftime('%W', Transaction.transaction_datetime).label("week_index"),
            func.sum(Transaction.transaction_qty).label("total_qty"),
        )
        .group_by(
            Transaction.product_id,
            Transaction.product_type,
            "week_index",
        )
        .all()
    )

    return rows


def get_top_increase_decrease(db: Session) -> WeeklySalesSummary:
    rows = get_weekly_sales(db)

    # Build structure: { product_id: { "product_name": str, "weeks": {week_index: qty} } }
    products: Dict[int, Dict] = {}

    for product_id, product_name, week_index, total_qty in rows:
        week_index = int(week_index)
        if product_id not in products:
            products[product_id] = {
                "product_name": product_name,
                "weeks": {}
            }
        products[product_id]["weeks"][week_index] = total_qty

    trends: List[WeeklySalesTrend] = []

    for product_id, info in products.items():
        weeks_dict = info["weeks"]
        # sort weeks
        sorted_weeks = sorted(weeks_dict.items())  # [(week_index, qty), ...]

        if len(sorted_weeks) < 2:
            # need at least two weeks to compute change
            continue

        # last two weeks
        (prev_week, prev_qty), (curr_week, curr_qty) = sorted_weeks[-2], sorted_weeks[-1]

        if prev_qty == 0:
            # avoid division by zero
            continue

        percent_change = ((curr_qty - prev_qty) / prev_qty) * 100.0

        history_items = [
            WeeklySalesItem(week_index=w, total_qty=q) for w, q in sorted_weeks
        ]

        trends.append(
            WeeklySalesTrend(
                product_id=product_id,
                product_name=info["product_name"],
                history=history_items,
                percent_change=percent_change,
            )
        )

    if not trends:
        return WeeklySalesSummary(top_increase=None, top_decrease=None)

    # highest positive change
    top_increase = max(trends, key=lambda t: t.percent_change or float("-inf"))
    # most negative change
    top_decrease = min(trends, key=lambda t: t.percent_change or float("inf"))

    return WeeklySalesSummary(
        top_increase=top_increase,
        top_decrease=top_decrease,
    )