from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from data.products import Product
from forms.register import RegisterForm
from forms.login import LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/shop.db")
    app.run()


@app.route('/')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/kitchens')
def kitchens():
    db_sess = db_session.create_session()
    kitchen = db_sess.query(Product).filter(Product.id <= 8)
    return render_template('kitchens.html', kitchen=kitchen)


@app.route('/living_rooms')
def living_rooms():
    db_sess = db_session.create_session()
    livingroom = db_sess.query(Product).filter(Product.id > 16).filter(Product.id <= 24)
    return render_template('living_rooms.html', livingroom=livingroom)


@app.route('/beds')
def beds():
    db_sess = db_session.create_session()
    bed = db_sess.query(Product).filter(Product.id > 24)
    return render_template('beds.html', bed=bed)


@app.route('/bedrooms')
def bedrooms():
    db_sess = db_session.create_session()
    bedroom = db_sess.query(Product).filter(Product.id > 8).filter(Product.id <= 16)
    return render_template('bedrooms.html', bedroom=bedroom)


if __name__ == '__main__':
    main()
