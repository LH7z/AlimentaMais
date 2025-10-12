from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from database import db
from models import Food

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alimentamais.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria as tabelas no primeiro acesso
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    foods = Food.query.filter_by(status="disponível").all()
    return render_template('home.html', foods=foods)


@app.route('/add', methods=['GET', 'POST'])
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
            location=location
        )

        db.session.add(new_food)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_food.html')


if __name__ == '__main__':
    app.run(debug=True)
