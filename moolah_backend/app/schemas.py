from __future__ import annotations

from decimal import Decimal
from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)
from datetime import datetime
from typing import List, Optional


class DecimalBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    @field_serializer('*', when_used='json')
    def _serialize_decimals(self, value):
        if isinstance(value, Decimal):
            return float(value)
        return value


class TransactionBase(DecimalBaseModel):
    amount: Decimal
    category_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(DecimalBaseModel):
    amount: Optional[Decimal] = None
    category_id: Optional[int] = None


class Transaction(TransactionBase):
    id: int
    timestamp: datetime
    owner_id: int


class GoalBase(DecimalBaseModel):
    description: str
    target_amount: Decimal


class GoalCreate(GoalBase):
    pass


class GoalUpdate(DecimalBaseModel):
    description: Optional[str] = None
    target_amount: Optional[Decimal] = None
    achieved: Optional[bool] = None


class Goal(GoalBase):
    id: int
    achieved: bool
    owner_id: int


class UserBase(DecimalBaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    is_admin: bool = False


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    points: int
    transactions: List[Transaction] = Field(default_factory=list)
    goals: List[Goal] = Field(default_factory=list)
    budgets: List["Budget"] = Field(default_factory=list)
    rewards: List["Reward"] = Field(default_factory=list)



class Token(DecimalBaseModel):
    access_token: str
    token_type: str


class TokenData(DecimalBaseModel):
    email: Optional[str] = None


class CategoryBase(DecimalBaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(DecimalBaseModel):
    name: Optional[str] = None


class Category(CategoryBase):
    id: int


class BudgetBase(DecimalBaseModel):
    month: str
    limit: Decimal

    @field_validator("month")
    @classmethod
    def validate_month(cls, v: str):
        try:
            datetime.strptime(v, "%Y-%m")
        except ValueError:
            raise ValueError("month must be in YYYY-MM format")
        return v

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: Decimal):
        if v <= 0:
            raise ValueError("limit must be greater than zero")
        return v


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(DecimalBaseModel):
    month: Optional[str] = None
    limit: Optional[Decimal] = None

    @field_validator("month")
    @classmethod
    def validate_month(cls, v: Optional[str]):
        if v is None:
            return v
        try:
            datetime.strptime(v, "%Y-%m")
        except ValueError:
            raise ValueError("month must be in YYYY-MM format")
        return v

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: Optional[Decimal]):
        if v is not None and v <= 0:
            raise ValueError("limit must be greater than zero")
        return v


class Budget(BudgetBase):
    id: int
    owner_id: int


class RewardBase(DecimalBaseModel):
    level: str
    points: int


class Reward(RewardBase):
    id: int
    timestamp: datetime
    owner_id: int


class UserProgress(DecimalBaseModel):
    points: int
    rewards: List[Reward]


class MonthlySummary(DecimalBaseModel):
    month: str
    total: Decimal


class CategorySummary(DecimalBaseModel):
    category: str
    total: Decimal


class WhatsAppWebhook(DecimalBaseModel):
    entry: List[dict] = Field(default_factory=list)


class WhatsAppMessageBase(DecimalBaseModel):
    wa_id: str = Field(alias="id")
    from_number: str = Field(alias="from")
    body: str
    timestamp: datetime


class WhatsAppMessageCreate(WhatsAppMessageBase):
    pass


class WhatsAppMessage(WhatsAppMessageBase):
    id: int


# Resolve forward references
User.model_rebuild()
