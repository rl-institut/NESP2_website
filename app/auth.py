import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')

        user = User.query.first()

        if len(User.query.all()) == 0:
            # create new user with the form data. Hash the password so plaintext version isn't saved.
            new_user = User(name=name, password=generate_password_hash(password))
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

        #check if user actually exists
        #take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=True)
        return redirect(url_for('landing'))

    else:
        return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

