import functools

from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, url_for
)
from flask_sqlalchemy import session
from werkzeug.security import check_password_hash

from flaskr.models import Establecimiento, Rol, Usuario
from .db import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.query.get(user_id)
        g.role = Rol.query.get(g.user.role_id)
        g.establecimiento = Establecimiento.query.get(g.user.establecimiento_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def roles_required(*roles):
    """
    Roles que tienen permitido acceder a la vista decorada.
    """
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None or g.role.nombre not in roles:
                abort(403) 
            
            return view(**kwargs)
        return wrapped_view
    return decorator


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
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))

    return render_template('auth/login.html')

