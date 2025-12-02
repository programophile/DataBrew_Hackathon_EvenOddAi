from sqlalchemy import Column, Integer, String, Float, Date, Time, DateTime
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Raw transaction fields
    transaction_date = Column(Date, index=True)
    transaction_time = Column(Time, index=True)
    transaction_qty  = Column(Integer)

    product_id   = Column(Integer, index=True)
    unit_price   = Column(Float)
    product_type = Column(String, index=True)  # coffee name

    transaction_datetime = Column(DateTime, index=True)

    # Derived fields
    day      = Column(String, index=True)    # Sunday, Monday...
    day_time = Column(String, index=True)    # Morning / Afternoon / Evening / Night