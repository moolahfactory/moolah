from fastapi import FastAPI

from .database import Base, engine
from .routers import (
    auth,
    users,
    transactions,
    goals,
    categories,
    budgets,
    rewards,
    analytics,
    whatsapp,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Moolah API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(goals.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(rewards.router)
app.include_router(analytics.router)
app.include_router(whatsapp.router)
