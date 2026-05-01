from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash

from flaskr.models import Rol, Usuario

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        error = None

        user = Usuario.query.filter_by(correo=email).first()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error:
            flash(error)
        else:
            return redirect(url_for('main.index'))

    return render_template('auth/login.html')


