# app/routers/electricity.py
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.schemas import (
    DailyStat,
    SingleDayView,
    SingleDayStat,
    HourDetail,
    HourPrice,
)

router = APIRouter()


@router.get("/daily-stats", response_model=List[DailyStat])
def get_daily_stats(db: Session = Depends(get_db)):
    """
    Returns a list of daily aggregated statistics:
      - total consumption
      - total production
      - average price
      - longest consecutive negative price streak
    """
    # You can do this as a single SQL query or with a combination
    # of SQLAlchemy queries. Below is a raw SQL approach:
    raw_sql = """
        SELECT d.date,
               SUM(d."consumptionAmount") AS total_consumption,
               SUM(d."productionAmount") AS total_production,
               AVG(d."hourlyPrice") AS average_price,
               (
                   SELECT MAX(consecutive_hours)
                   FROM (
                       SELECT
                           COUNT(*) AS consecutive_hours,
                           MIN("hourlyPrice") as min_price
                       FROM (
                           SELECT e."date",
                                  e."startTime",
                                  e."hourlyPrice",
                                  SUM(CASE WHEN "hourlyPrice" < 0 THEN 0 ELSE 1 END)
                                  OVER (PARTITION BY e."date" ORDER BY e."startTime"
                                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as breaker
                           FROM electricitydata e
                           WHERE e."date" = d."date"
                           ORDER BY e."startTime"
                       ) x
                       WHERE x."hourlyPrice" < 0
                       GROUP BY x.breaker
                   ) y
               ) AS longest_negative_price_streak
        FROM electricitydata d
        GROUP BY d.date
        ORDER BY d.date
    """
    rows = db.execute(raw_sql).fetchall()

    results = []
    for row in rows:
        # row: (date, total_consumption, total_production, avg_price, longest_streak)
        results.append(
            {
                "date": row[0],
                "total_consumption": float(row[1]) if row[1] is not None else 0.0,
                "total_production": float(row[2]) if row[2] is not None else 0.0,
                "average_price": float(row[3]) if row[3] is not None else 0.0,
                "longest_negative_price_streak": (
                    float(row[4]) if row[4] is not None else 0.0
                ),
            }
        )

    return results


@router.get("/daily-stats/{selected_date}", response_model=SingleDayView)
def get_single_day_view(selected_date: date, db: Session = Depends(get_db)):
    # 1) Summaries
    summary_sql = """
        SELECT 
            date,
            SUM("consumptionAmount") AS total_consumption,
            SUM("productionAmount") AS total_production,
            AVG("hourlyPrice") AS average_price
        FROM electricitydata
        WHERE date = :selected_date
        GROUP BY date
        LIMIT 1
    """

    summary_row = db.execute(summary_sql, {"selected_date": selected_date}).fetchone()
    if not summary_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for date {selected_date}",
        )

    dailyStats = SingleDayStat(
        date=summary_row[0],
        total_consumption=float(summary_row[1]) if summary_row[1] else 0.0,
        total_production=float(summary_row[2]) if summary_row[2] else 0.0,
        average_price=float(summary_row[3]) if summary_row[3] else 0.0,
    )

    # 2) Hour with max consumption-production difference
    max_diff_sql = """
        SELECT "startTime",
               ("consumptionAmount" - "productionAmount") AS diff
        FROM electricitydata
        WHERE date = :selected_date
        ORDER BY diff DESC NULLS LAST
        LIMIT 1
    """
    max_diff_row = db.execute(max_diff_sql, {"selected_date": selected_date}).fetchone()
    maxConsumptionVsProduction = None
    if max_diff_row:
        maxConsumptionVsProduction = HourDetail(
            startTime=max_diff_row[0],
            consumption_production_diff=(
                float(max_diff_row[1]) if max_diff_row[1] else 0.0
            ),
        )

    # 3) Cheapest hours (top 3)
    cheapest_sql = """
        SELECT "startTime", "hourlyPrice"
        FROM electricitydata
        WHERE date = :selected_date
        ORDER BY "hourlyPrice" ASC NULLS LAST
        LIMIT 3
    """
    cheapest_rows = db.execute(
        cheapest_sql, {"selected_date": selected_date}
    ).fetchall()

    cheapestHours = [
        HourPrice(startTime=row[0], hourlyPrice=float(row[1]) if row[1] else 0.0)
        for row in cheapest_rows
    ]

    return SingleDayView(
        dailyStats=dailyStats,
        maxConsumptionVsProduction=maxConsumptionVsProduction,
        cheapestHours=cheapestHours,
    )
