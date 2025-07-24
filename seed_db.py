import sys
from pathlib import Path
from typing import Optional

# Allow imports from the backend package
sys.path.append(str(Path(__file__).resolve().parent / "moolah_backend"))

from app.database import Base, engine, SessionLocal
from app import crud, schemas
from datetime import datetime


def month_iterator(start_year: int, start_month: int):
    """Generate datetime objects on the 15th of sequential months."""
    year, month = start_year, start_month
    while True:
        yield datetime(year, month, 15)
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1



def seed(reset: bool = False):
    """Populate the SQLite database with demo data.

    Parameters
    ----------
    reset: bool, optional
        Drop existing tables before creating them.
    """
    if reset:
        # Remove existing tables when requested
        Base.metadata.drop_all(bind=engine)
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    # Prepare month iterators for each demo user
    months_user1 = month_iterator(2023, 1)
    months_user2 = month_iterator(2023, 1)
    months_user3 = month_iterator(2023, 1)
    months_user4 = month_iterator(2023, 3)
    months_user5 = month_iterator(2023, 1)
    months_user6 = month_iterator(2023, 6)
    months_extra = month_iterator(2023, 1)

    def add_tx(user_id: int, amount: int, cat_id: Optional[int], it):
        crud.create_transaction(
            db,
            schemas.TransactionCreate(amount=amount, category_id=cat_id),
            user_id=user_id,
            timestamp=next(it),
        )
    try:
        # Create a demo user
        user = crud.create_user(
            db,
            schemas.UserCreate(email="alice@example.com", password="secret"),
        )

        # Categories
        food = crud.create_category(db, schemas.CategoryCreate(name="Comida"))
        transport = crud.create_category(db, schemas.CategoryCreate(name="Transporte"))
        entertainment = crud.create_category(db, schemas.CategoryCreate(name="Entretenimiento"))
        health = crud.create_category(db, schemas.CategoryCreate(name="Salud"))
        home = crud.create_category(db, schemas.CategoryCreate(name="Hogar"))
        travel = crud.create_category(db, schemas.CategoryCreate(name="Viajes"))
        education = crud.create_category(db, schemas.CategoryCreate(name="Educación"))
        gifts = crud.create_category(db, schemas.CategoryCreate(name="Regalos"))
        technology = crud.create_category(db, schemas.CategoryCreate(name="Tecnología"))
        clothing = crud.create_category(db, schemas.CategoryCreate(name="Ropa"))
        services = crud.create_category(db, schemas.CategoryCreate(name="Servicios"))
        taxes = crud.create_category(db, schemas.CategoryCreate(name="Impuestos"))
        pets = crud.create_category(db, schemas.CategoryCreate(name="Mascotas"))
        sports = crud.create_category(db, schemas.CategoryCreate(name="Deporte"))
        beauty = crud.create_category(db, schemas.CategoryCreate(name="Belleza"))
        donations = crud.create_category(db, schemas.CategoryCreate(name="Donaciones"))
        insurance = crud.create_category(db, schemas.CategoryCreate(name="Seguros"))
        other = crud.create_category(db, schemas.CategoryCreate(name="Otros"))
        crud.create_category(db, schemas.CategoryCreate(name="Inversiones"))
        crud.create_category(db, schemas.CategoryCreate(name="Niños"))
        crud.create_category(db, schemas.CategoryCreate(name="Cuidado personal"))
        crud.create_category(db, schemas.CategoryCreate(name="Ahorro"))
        crud.create_category(db, schemas.CategoryCreate(name="Imprevistos"))

        # Goal and budget for the user
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Ahorrar para laptop", target_amount=1000),
            user_id=user.id,
        )

        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-01", limit=500),
            user_id=user.id,
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-02", limit=450),
            user_id=user.id,
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-03", limit=550),
            user_id=user.id,
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-04", limit=600),
            user_id=user.id,
        )
        for month, limit in [
            ("2023-05", 650),
            ("2023-06", 700),
            ("2023-07", 750),
            ("2023-08", 700),
            ("2023-09", 720),
            ("2023-10", 680),
            ("2023-11", 690),
            ("2023-12", 710),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user.id,
            )
        for month, limit in [
            ("2024-01", 720),
            ("2024-02", 730),
            ("2024-03", 740),
            ("2024-04", 750),
            ("2024-05", 760),
            ("2024-06", 770),
            ("2024-07", 780),
            ("2024-08", 790),
            ("2024-09", 800),
            ("2024-10", 810),
            ("2024-11", 820),
            ("2024-12", 830),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user.id,
            )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Vacaciones", target_amount=1500),
            user_id=user.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Curso de inglés", target_amount=200),
            user_id=user.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Comprar bicicleta", target_amount=400),
            user_id=user.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Fondo de emergencia", target_amount=800),
            user_id=user.id,
        )

        # Second demo user
        user2 = crud.create_user(
            db,
            schemas.UserCreate(email="bob@example.com", password="secret"),
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-01", limit=300),
            user_id=user2.id,
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-02", limit=350),
            user_id=user2.id,
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-03", limit=320),
            user_id=user2.id,
        )
        for month, limit in [
            ("2023-04", 340),
            ("2023-05", 360),
            ("2023-06", 380),
            ("2023-07", 370),
            ("2023-08", 390),
            ("2023-09", 410),
            ("2023-10", 400),
            ("2023-11", 420),
            ("2023-12", 430),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user2.id,
            )
        for month, limit in [
            ("2024-01", 450),
            ("2024-02", 460),
            ("2024-03", 470),
            ("2024-04", 480),
            ("2024-05", 490),
            ("2024-06", 500),
            ("2024-07", 510),
            ("2024-08", 520),
            ("2024-09", 530),
            ("2024-10", 540),
            ("2024-11", 550),
            ("2024-12", 560),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user2.id,
            )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Fondo de emergencia", target_amount=500),
            user_id=user2.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Viaje en familia", target_amount=1200),
            user_id=user2.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Pagar deudas", target_amount=700),
            user_id=user2.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Comprar vehículo", target_amount=4000),
            user_id=user2.id,
        )

        # Third demo user
        user3 = crud.create_user(
            db,
            schemas.UserCreate(email="charlie@example.com", password="secret"),
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-01", limit=400),
            user_id=user3.id,
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-02", limit=380),
            user_id=user3.id,
        )
        for month, limit in [
            ("2023-03", 390),
            ("2023-04", 410),
            ("2023-05", 430),
            ("2023-06", 420),
            ("2023-07", 440),
            ("2023-08", 460),
            ("2023-09", 450),
            ("2023-10", 470),
            ("2023-11", 480),
            ("2023-12", 500),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user3.id,
            )
        for month, limit in [
            ("2024-01", 510),
            ("2024-02", 520),
            ("2024-03", 530),
            ("2024-04", 540),
            ("2024-05", 550),
            ("2024-06", 560),
            ("2024-07", 570),
            ("2024-08", 580),
            ("2024-09", 590),
            ("2024-10", 600),
            ("2024-11", 610),
            ("2024-12", 620),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user3.id,
            )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Nuevo portátil", target_amount=1200),
            user_id=user3.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Inversión", target_amount=1000),
            user_id=user3.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Mudanza", target_amount=1500),
            user_id=user3.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Fondo jubilación", target_amount=2000),
            user_id=user3.id,
        )

        # Fourth demo user
        user4 = crud.create_user(
            db,
            schemas.UserCreate(email="dana@example.com", password="secret"),
        )
        crud.create_budget(
            db,
            schemas.BudgetCreate(month="2023-03", limit=500),
            user_id=user4.id,
        )
        for month, limit in [
            ("2023-04", 520),
            ("2023-05", 540),
            ("2023-06", 560),
            ("2023-07", 580),
            ("2023-08", 600),
            ("2023-09", 620),
            ("2023-10", 640),
            ("2023-11", 660),
            ("2023-12", 680),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user4.id,
            )
        for month, limit in [
            ("2024-01", 690),
            ("2024-02", 700),
            ("2024-03", 710),
            ("2024-04", 720),
            ("2024-05", 730),
            ("2024-06", 740),
            ("2024-07", 750),
            ("2024-08", 760),
            ("2024-09", 770),
            ("2024-10", 780),
            ("2024-11", 790),
            ("2024-12", 800),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user4.id,
            )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Cursos online", target_amount=300),
            user_id=user4.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Membresía gimnasio", target_amount=250),
            user_id=user4.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Ahorro vacaciones", target_amount=1000),
            user_id=user4.id,
        )

        # Fifth demo user
        user5 = crud.create_user(
            db,
            schemas.UserCreate(email="eve@example.com", password="secret"),
        )
        for month, limit in [
            ("2023-01", 450),
            ("2023-02", 470),
            ("2023-03", 480),
            ("2023-04", 500),
            ("2023-05", 520),
            ("2023-06", 540),
            ("2023-07", 560),
            ("2023-08", 580),
            ("2023-09", 600),
            ("2023-10", 620),
            ("2023-11", 640),
            ("2023-12", 660),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user5.id,
            )
        for month, limit in [
            ("2024-01", 680),
            ("2024-02", 700),
            ("2024-03", 720),
            ("2024-04", 740),
            ("2024-05", 760),
            ("2024-06", 780),
            ("2024-07", 800),
            ("2024-08", 820),
            ("2024-09", 840),
            ("2024-10", 860),
            ("2024-11", 880),
            ("2024-12", 900),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user5.id,
            )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Ahorro coche", target_amount=5000),
            user_id=user5.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Máster", target_amount=3000),
            user_id=user5.id,
        )

        # Sixth demo user
        user6 = crud.create_user(
            db,
            schemas.UserCreate(email="frank@example.com", password="secret"),
        )
        for month, limit in [
            ("2023-06", 600),
            ("2023-07", 620),
            ("2023-08", 640),
            ("2023-09", 660),
            ("2023-10", 680),
            ("2023-11", 700),
            ("2023-12", 720),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user6.id,
            )
        for month, limit in [
            ("2024-01", 740),
            ("2024-02", 760),
            ("2024-03", 780),
            ("2024-04", 800),
            ("2024-05", 820),
            ("2024-06", 840),
            ("2024-07", 860),
            ("2024-08", 880),
            ("2024-09", 900),
            ("2024-10", 920),
            ("2024-11", 940),
            ("2024-12", 960),
        ]:
            crud.create_budget(
                db,
                schemas.BudgetCreate(month=month, limit=limit),
                user_id=user6.id,
            )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Boda", target_amount=10000),
            user_id=user6.id,
        )
        crud.create_goal(
            db,
            schemas.GoalCreate(description="Casa nueva", target_amount=20000),
            user_id=user6.id,
        )

        # Transactions
        add_tx(user.id, 1000, None, months_user1)
        add_tx(user.id, -50, food.id, months_user1)
        add_tx(user.id, -20, transport.id, months_user1)
        add_tx(user.id, -30, entertainment.id, months_user1)
        add_tx(user.id, -25, health.id, months_user1)
        for amt, cat in [
            (-80, home.id),
            (-15, transport.id),
            (500, None),
            (-60, entertainment.id),
            (-90, travel.id),
            (-20, gifts.id),
            (-10, education.id),
            (200, None),
        ]:
            add_tx(user.id, amt, cat, months_user1)
        for amt, cat in [
            (-70, food.id),
            (-100, transport.id),
            (-120, entertainment.id),
            (200, None),
            (-50, health.id),
            (-30, travel.id),
            (-25, gifts.id),
            (-60, technology.id),
            (-80, clothing.id),
            (-40, services.id),
            (-500, taxes.id),
            (-20, pets.id),
            (-100, home.id),
            (400, None),
            (-150, food.id),
            (-30, education.id),
            (-70, travel.id),
            (-15, transport.id),
            (-35, entertainment.id),
            (-90, gifts.id),
        ]:
            add_tx(user.id, amt, cat, months_user1)
        for amt, cat in [
            (250, None),
            (-40, beauty.id),
            (-60, sports.id),
            (-35, donations.id),
            (-120, technology.id),
            (-75, entertainment.id),
            (400, None),
            (-50, insurance.id),
            (-30, other.id),
        ]:
            add_tx(user.id, amt, cat, months_user1)

        # Transactions for second user
        add_tx(user2.id, 800, None, months_user2)
        add_tx(user2.id, -40, food.id, months_user2)
        for amt, cat in [
            (600, None),
            (-70, transport.id),
            (-35, entertainment.id),
            (-25, health.id),
            (-15, gifts.id),
            (-45, travel.id),
        ]:
            add_tx(user2.id, amt, cat, months_user2)
        for amt, cat in [
            (-55, food.id),
            (-30, transport.id),
            (-75, entertainment.id),
            (300, None),
            (-40, health.id),
            (-25, travel.id),
            (-20, gifts.id),
            (-50, technology.id),
            (-65, clothing.id),
            (-35, services.id),
            (-300, taxes.id),
            (-10, pets.id),
            (-70, home.id),
            (250, None),
            (-90, food.id),
            (-20, education.id),
            (-60, travel.id),
            (-10, transport.id),
            (-25, entertainment.id),
            (-85, gifts.id),
        ]:
            add_tx(user2.id, amt, cat, months_user2)
        for amt, cat in [
            (200, None),
            (-30, beauty.id),
            (-50, sports.id),
            (-20, donations.id),
            (-45, insurance.id),
            (-35, other.id),
            (-100, technology.id),
            (350, None),
        ]:
            add_tx(user2.id, amt, cat, months_user2)

        # Transactions for third user
        for amt, cat in [
            (900, None),
            (-60, food.id),
            (-20, home.id),
            (-50, education.id),
            (-80, travel.id),
        ]:
            add_tx(user3.id, amt, cat, months_user3)
        for amt, cat in [
            (-65, food.id),
            (-25, transport.id),
            (-70, entertainment.id),
            (350, None),
            (-55, health.id),
            (-45, travel.id),
            (-30, gifts.id),
            (-40, technology.id),
            (-70, clothing.id),
            (-30, services.id),
            (-250, taxes.id),
            (-20, pets.id),
            (-80, home.id),
            (500, None),
            (-120, food.id),
            (-40, education.id),
            (-90, travel.id),
            (-20, transport.id),
            (-30, entertainment.id),
            (-95, gifts.id),
        ]:
            add_tx(user3.id, amt, cat, months_user3)
        for amt, cat in [
            (600, None),
            (-50, beauty.id),
            (-70, sports.id),
            (-40, donations.id),
            (-60, insurance.id),
            (-30, other.id),
            (200, None),
        ]:
            add_tx(user3.id, amt, cat, months_user3)

        # Transactions for fourth user
        add_tx(user4.id, 300, None, months_user4)
        add_tx(user4.id, -100, education.id, months_user4)
        for amt, cat in [
            (400, None),
            (-60, food.id),
            (-20, transport.id),
            (-40, entertainment.id),
            (-30, health.id),
            (-50, travel.id),
            (-15, gifts.id),
            (-35, technology.id),
            (-45, clothing.id),
            (-25, services.id),
            (-200, taxes.id),
            (-20, pets.id),
            (-70, home.id),
            (150, None),
            (-80, education.id),
            (-30, travel.id),
            (-10, transport.id),
            (-20, entertainment.id),
            (-95, gifts.id),
        ]:
            add_tx(user4.id, amt, cat, months_user4)
        for amt, cat in [
            (200, None),
            (-40, beauty.id),
            (-30, sports.id),
            (-25, donations.id),
            (-50, insurance.id),
            (-40, other.id),
        ]:
            add_tx(user4.id, amt, cat, months_user4)

        # Transactions for fifth user
        add_tx(user5.id, 1200, None, months_user5)
        for amt, cat in [
            (-100, food.id),
            (-40, transport.id),
            (-80, entertainment.id),
            (-35, health.id),
            (-60, travel.id),
            (-25, gifts.id),
            (-70, technology.id),
            (-90, clothing.id),
            (-50, services.id),
            (-400, taxes.id),
            (-30, pets.id),
            (300, None),
        ]:
            add_tx(user5.id, amt, cat, months_user5)
        for amt, cat in [
            (350, None),
            (-60, beauty.id),
            (-55, sports.id),
            (-45, donations.id),
            (-40, insurance.id),
            (-30, other.id),
            (-120, technology.id),
        ]:
            add_tx(user5.id, amt, cat, months_user5)

        # Transactions for sixth user
        add_tx(user6.id, 1500, None, months_user6)
        for amt, cat in [
            (-150, food.id),
            (-60, transport.id),
            (-90, entertainment.id),
            (-70, health.id),
            (-100, travel.id),
            (-40, gifts.id),
            (-80, technology.id),
            (-110, clothing.id),
            (-65, services.id),
            (-500, taxes.id),
            (-40, pets.id),
            (500, None),
        ]:
            add_tx(user6.id, amt, cat, months_user6)
        for amt, cat in [
            (600, None),
            (-70, beauty.id),
            (-80, sports.id),
            (-55, donations.id),
            (-60, insurance.id),
            (-45, other.id),
        ]:
            add_tx(user6.id, amt, cat, months_user6)

        # Bulk demo users for larger datasets
        extra_users = []
        for i in range(7, 27):
            u = crud.create_user(
                db,
                schemas.UserCreate(
                    email=f"user{i}@example.com", password="secret"
                ),
            )
            extra_users.append(u)
            for year in ["2023", "2024", "2025", "2026"]:
                for m in range(1, 13):
                    limit = 300 + i * 5 + m
                    crud.create_budget(
                        db,
                        schemas.BudgetCreate(
                            month=f"{year}-{m:02d}", limit=limit
                        ),
                        user_id=u.id,
                    )
            crud.create_goal(
                db,
                schemas.GoalCreate(
                    description=f"Goal usuario {i}",
                    target_amount=1000 + i * 50,
                ),
                user_id=u.id,
            )
            add_tx(u.id, 500 + i * 10, None, months_extra)
            for cat in [food, transport, entertainment, health]:
                add_tx(u.id, -(i * 5), cat.id, months_extra)
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Seed the database with demo data"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop existing tables before seeding",
    )
    args = parser.parse_args()
    seed(reset=args.reset)
