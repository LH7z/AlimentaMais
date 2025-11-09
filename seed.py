from faker import Faker
from app import app, db
from models import Food
from datetime import timedelta
import random

fake = Faker('pt_BR')

NUM_FOODS = 20

with app.app_context():
    print("🧹 Limpando tabela de alimentos...")
    Food.query.delete()

    for _ in range(NUM_FOODS):
        name = fake.word().capitalize()
        quantity = random.randint(1, 15)
        location = fake.address()
        expiration_date = fake.future_date(end_date="+30d")

        food = Food(
            name=name,
            quantity=quantity,
            location=location,
            expiration_date=expiration_date,
            user_id=1,
        )

        db.session.add(food)

    db.session.commit()
    print(f"✅ {NUM_FOODS} alimentos falsos adicionados com sucesso!")
