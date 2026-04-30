from sqlalchemy.sql import func

from .db import db


class Rol(db.Model):
    __tablename__ = "Rol"

    id = db.Column(db.Integer, primary_key=True)
    nom_rol = db.Column(db.String(50), nullable=False)


class TipoEstablecimiento(db.Model):
    __tablename__ = "Tipo_Establecimiento"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)


class Producto(db.Model):
    __tablename__ = "Producto"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)


class Establecimiento(db.Model):
    __tablename__ = "Establecimiento"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(
        db.Integer,
        db.ForeignKey("Tipo_Establecimiento.id", ondelete="RESTRICT"),
        nullable=False,
    )


class Usuario(db.Model):
    __tablename__ = "Usuario"

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), nullable=False, unique=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Integer, db.ForeignKey("Rol.id", ondelete="RESTRICT"), nullable=False)
    id_establecimiento = db.Column(
        db.Integer,
        db.ForeignKey("Establecimiento.id", ondelete="SET NULL"),
        nullable=True,
    )
    activo = db.Column(db.Boolean, nullable=False, default=True)
    creado = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    modificado = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())


class EstablecimientoProducto(db.Model):
    __tablename__ = "Establecimiento_Producto"

    id_establecimiento = db.Column(
        db.Integer,
        db.ForeignKey("Establecimiento.id", ondelete="CASCADE"),
        primary_key=True,
    )
    id_producto = db.Column(
        db.Integer,
        db.ForeignKey("Producto.id", ondelete="CASCADE"),
        primary_key=True,
    )
    cantidad = db.Column(db.Integer, nullable=False, default=0)
