from sqlalchemy import Column, Integer, Date, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ElectricityData(Base):
    __tablename__ = "electricitydata"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    starttime = Column(DateTime)
    productionamount = Column(Numeric(11, 5))
    consumptionamount = Column(Numeric(11, 3))
    hourlyprice = Column(Numeric(6, 3))
