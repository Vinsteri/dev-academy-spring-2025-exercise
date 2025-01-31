from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database import get_db
from app.schemas import (
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
    raw_sql = text(
        """
        SELECT d.date,
               SUM(d."consumptionamount") AS total_consumption,
               SUM(d."productionamount") AS total_production,
               AVG(d."hourlyprice") AS average_price,
               (
                   SELECT MAX(consecutive_hours)
                   FROM (
                       SELECT
                           COUNT(*) AS consecutive_hours,
                           MIN("hourlyprice") as min_price
                       FROM (
                           SELECT e."date",
                                  e."starttime",
                                  e."hourlyprice",
                                  SUM(CASE WHEN "hourlyprice" < 0 THEN 0 ELSE 1 END)
                                  OVER (PARTITION BY e."date" ORDER BY e."starttime"
                                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as breaker
                           FROM electricitydata e
                           WHERE e."date" = d."date"
                           ORDER BY e."starttime"
                       ) x
                       WHERE x."hourlyprice" < 0
                       GROUP BY x.breaker
                   ) y
               ) AS longest_negative_price_streak
        FROM electricitydata d
        GROUP BY d.date
        ORDER BY d.date
        """
    )
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
    summary_sql = text(
        """
        SELECT 
            date,
            SUM("consumptionamount") AS total_consumption,
            SUM("productionamount") AS total_production,
            AVG("hourlyprice") AS average_price
        FROM electricitydata
        WHERE date = :selected_date
        GROUP BY date
        LIMIT 1
        """
    )

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
    max_diff_sql = text(
        """
        SELECT "starttime",
               ("consumptionamount" - "productionamount") AS diff
        FROM electricitydata
        WHERE date = :selected_date
        ORDER BY diff DESC NULLS LAST
        LIMIT 1
        """
    )
    max_diff_row = db.execute(max_diff_sql, {"selected_date": selected_date}).fetchone()
    maxConsumptionVsProduction = None
    if max_diff_row:
        maxConsumptionVsProduction = HourDetail(
            starttime=max_diff_row[0],
            consumption_production_diff=(
                float(max_diff_row[1]) if max_diff_row[1] else 0.0
            ),
        )

    # 3) Cheapest hours (top 3)
    cheapest_sql = text(
        """
        SELECT "starttime", "hourlyprice"
        FROM electricitydata
        WHERE date = :selected_date
        ORDER BY "hourlyprice" ASC NULLS LAST
        LIMIT 3
        """
    )
    cheapest_rows = db.execute(
        cheapest_sql, {"selected_date": selected_date}
    ).fetchall()

    cheapestHours = [
        HourPrice(starttime=row[0], hourlyprice=float(row[1]) if row[1] else 0.0)
        for row in cheapest_rows
    ]

    return SingleDayView(
        dailyStats=dailyStats,
        maxConsumptionVsProduction=maxConsumptionVsProduction,
        cheapestHours=cheapestHours,
    )
