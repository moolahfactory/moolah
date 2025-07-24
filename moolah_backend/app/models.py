from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    points = Column(Integer, default=0)

    transactions = relationship("Transaction", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")
    budgets = relationship("Budget", back_populates="owner")
    rewards = relationship("Reward", back_populates="owner")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2))
    timestamp = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    owner = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    target_amount = Column(Numeric(10, 2))
    achieved = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="goals")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    transactions = relationship("Transaction", back_populates="category")


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (UniqueConstraint("owner_id", "month"),)

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, index=True)
    limit = Column(Numeric(10, 2))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="budgets")


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    points = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="rewards")


class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"

    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, unique=True, index=True)
    from_number = Column(String)
    body = Column(String)
    timestamp = Column(DateTime)
