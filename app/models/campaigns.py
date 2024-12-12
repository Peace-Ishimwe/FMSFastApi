from datetime import datetime
from sqlalchemy import Column, DateTime, Decimal, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# SQLAlchemy Models

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    goal_amount = Column(Decimal(12, 2), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    created_by = relationship("CustomUser", back_populates="created_campaigns")
    fundings = relationship("Funding", back_populates="campaign", cascade="all, delete-orphan")

    def total_funded(self):
        return sum(funding.amount for funding in self.fundings)


class Funding(Base):
    __tablename__ = "fundings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    amount = Column(Decimal(10, 2), nullable=False)
    funded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("CustomUser", back_populates="fundings")
    campaign = relationship("Campaign", back_populates="fundings")