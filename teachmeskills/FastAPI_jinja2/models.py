from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Forklift(Base):
    __tablename__ = "forklifts"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    number = Column(String, unique=True, index=True)
    capacity = Column(Float)

    downtimes = relationship("Downtime", back_populates="forklift")

class Downtime(Base):
    __tablename__ = "downtimes"

    id = Column(Integer, primary_key=True, index=True)
    forklift_id = Column(Integer, ForeignKey("forklifts.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    reason = Column(String, nullable=True)

    forklift = relationship("Forklift", back_populates="downtimes")


