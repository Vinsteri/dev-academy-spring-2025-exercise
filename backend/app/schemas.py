from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class DailyStat(BaseModel):
    date: date
    total_consumption: float
    total_production: float
    average_price: float
    longest_negative_price_streak: Optional[float]  # or int if you want an integer

    class Config:
        orm_mode = True


class SingleDayStat(BaseModel):
    date: date
    total_consumption: float
    total_production: float
    average_price: float

    class Config:
        orm_mode = True


class HourDetail(BaseModel):
    startTime: datetime
    consumption_production_diff: float

    class Config:
        orm_mode = True


class HourPrice(BaseModel):
    startTime: datetime
    hourlyPrice: float

    class Config:
        orm_mode = True


class SingleDayView(BaseModel):
    dailyStats: SingleDayStat
    maxConsumptionVsProduction: Optional[HourDetail]
    cheapestHours: list[HourPrice] = []
