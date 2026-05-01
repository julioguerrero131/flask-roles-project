import click
from flask.cli import with_appcontext
from .db import db 
from werkzeug.security import generate_password_hash

# flask --app flaskr <command>

@click.command("create-admin")
@click.argument("correo")
@click.argument("password")
@with_appcontext
def create_admin_command(correo, password):
    from .models import Usuario 
    
    admin = Usuario(
        correo=correo,
        nombre='Admin',
        apellido='User',
        password=generate_password_hash(password),
        rol=1,
        id_establecimiento=None
    )
    
    try:
        db.session.add(admin)
        db.session.commit()
        click.echo(f"✅ Administrador {correo} creado con éxito.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error al crear el administrador: {e}")


@click.command("create-admin-role")
@with_appcontext
def create_admin_role_command():
    from .models import Rol

    admin_role = Rol(
        nombre='admin'
    )

    try:
        db.session.add(admin_role)
        db.session.commit()
        click.echo("✅ Rol de administrador creado con éxito.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error al crear el rol de administrador: {e}")
