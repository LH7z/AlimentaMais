from app import app, db
from models import User, Food

with app.app_context():
    User.query.delete()
    Food.query.delete()
    db.session.commit()
    print("Banco de dados deletado com sucesso!")
