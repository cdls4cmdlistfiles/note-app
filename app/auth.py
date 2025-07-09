from flask import  render_template, redirect, url_for, flash, Blueprint
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user
from app import db
from app.models import User

app = Blueprint('auth',__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('views.home')) 
    return render_template('auth/login.html', title='Login', form=form)

