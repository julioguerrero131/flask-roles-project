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
    """Crea un usuario administrador."""
    from .models import Usuario, Rol

    admin_role = Rol.query.filter_by(nombre='admin').first()
    if not admin_role:
        click.echo("❌ Error: El rol 'admin' no existe. Ejecuta 'flask create-roles' primero.")
        return

    if Usuario.query.filter_by(correo=correo).first():
        click.echo(f"ℹ️  El usuario '{correo}' ya existe.")
        return

    admin = Usuario(
        correo=correo,
        nombre='Admin',
        apellido='User',
        password=generate_password_hash(password),
        rol=admin_role.id,
        id_establecimiento=None
    )

    try:
        db.session.add(admin)
        db.session.commit()
        click.echo(f"✅ Administrador {correo} creado con éxito.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error inesperado al crear el administrador: {e}")


@click.command("create-roles")
@with_appcontext
def create_roles_command():
    """Crea los roles iniciales (admin, manager, vendedor) si no existen."""
    from .models import Rol

    roles_to_create = ['admin', 'manager', 'vendedor']

    try:
        for role_name in roles_to_create:
            if not Rol.query.filter_by(nombre=role_name).first():
                new_role = Rol(nombre=role_name)
                db.session.add(new_role)
                click.echo(f"✅ Rol '{role_name}' creado.")
            else:
                click.echo(f"ℹ️  Rol '{role_name}' ya existe.")
        db.session.commit()
        click.echo("\n✨ Operación de roles completada.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error al procesar los roles: {e}")
