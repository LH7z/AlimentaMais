from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from database import db
from models import Food, User
from flask_cors import CORS
from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user, current_user


app = Flask(__name__, template_folder='templates')
app.secret_key = "minha_senha_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alimentamais.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = LoginManager()
manager.init_app(app)
manager.login_view = 'login'
CORS(app)

db.init_app(app)

# Cria as tabelas no primeiro acesso
with app.app_context():
    db.create_all()

@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "Usuário já existe", 400
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        login_user(user)
        flash('Registro realizado com sucesso!')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Login realizado com sucesso!')
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu com sucesso!')
    return redirect(url_for('login'))

@app.route('/')
def home():
    foods = Food.query.filter_by(status="disponível").all()
    return render_template('home.html', foods=foods)


@app.route('/my_foods')
@login_required
def my_foods():
    foods = Food.query.filter_by(owner=current_user).all()
    return render_template('my_foods.html', foods=foods)


@app.route('/change_status/<int:food_id>/')
@login_required
def change_status(food_id):
    food = Food.query.get_or_404(food_id)
    food.status = "indisponível" if food.status == "disponível" else "disponível"
    db.session.commit()
    flash('Status do alimento atualizado com sucesso!')
    return redirect(url_for('my_foods'))

@app.route('/reserved_foods')
@login_required
def reserved_foods():
    foods = Food.query.filter_by(reserved_by=current_user.id).all()
    return render_template('reserved_foods.html', foods=foods)

@app.route('/cancel_reservation/<int:food_id>/')
@login_required
def cancel_reservation(food_id):
    food = Food.query.get_or_404(food_id)
    food.status = "disponível"
    food.reserved_by = None
    db.session.commit()
    flash('Reserva cancelada com sucesso!')
    return redirect(url_for('reserved_foods'))

@app.route('/reserve_food/<int:food_id>')
@login_required
def reserve_food(food_id):
    food = Food.query.get_or_404(food_id)
    food.status = "indisponível"
    food.reserved_by = current_user.id
    db.session.commit()
    flash('Alimento reservado com sucesso!')
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_food():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
        location = request.form['location']

        new_food = Food(
            name=name,
            quantity=quantity,
            expiration_date=expiration_date,
            location=location,
            owner=current_user
        )

        db.session.add(new_food)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_food.html')

@app.route('/delete/<int:food_id>')
@login_required
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('Alimento excluído com sucesso!')
    return redirect(url_for('home'))

@app.route('/edit/<int:food_id>', methods=['GET', 'POST'])
@login_required
def edit_food(food_id):
    food = Food.query.get_or_404(food_id)

    if request.method == 'POST':
        food.name = request.form['name']
        food.quantity = request.form['quantity']
        food.expiration_date = datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
        food.location = request.form['location']

        db.session.commit()
        flash('Alimento atualizado com sucesso!')
        return redirect(url_for('home'))

    return render_template('edit_food.html', food=food)


if __name__ == '__main__':
    app.run(debug=True)
