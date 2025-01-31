from sqlalchemy import Column, Integer, Date, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ElectricityData(Base):
    __tablename__ = "electricitydata"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    startTime = Column(DateTime)
    productionAmount = Column(Numeric(11, 5))
    consumptionAmount = Column(Numeric(11, 3))
    hourlyPrice = Column(Numeric(6, 3))
