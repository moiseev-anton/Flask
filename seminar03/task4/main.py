from flask import Flask, render_template, request
from models import db, User
from forms import RegisterForm
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '3ee0ff7813c30b8aafe0651c0cd9369b2e8e2464874c224f906c2082f2ff8409'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


@app.cli.command('init-db')
def init():
    db.create_all()
    print('OK')


@app.get('/')
def get_books():
    users = User.query.all()
    context = {
        'title': 'Users',
        'users': users
    }
    return render_template('users.html', **context)


@app.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return 'Регистрация прошла успешно'

    return render_template('sign_up.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)