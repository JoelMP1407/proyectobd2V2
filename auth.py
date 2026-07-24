# auth.py
# Utilidades de autenticación/autorización basadas en Flask session.
# No usamos Flask-Login para mantener el proyecto simple y sin
# dependencias nuevas: basta con la sesión de Flask que ya se usa
# para los mensajes flash.

from functools import wraps
from flask import session, redirect, url_for, flash, abort

from permissions import can


def get_current_user():
    """Devuelve el dict del usuario logueado (o None) desde la sesión."""
    return session.get("user")


def login_required(f):
    """Exige sesión iniciada. Se usa en rutas sueltas (fuera del CRUD)."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def require_permission(entity_key, action):
    """
    Chequeo de permiso "en línea" (no decorador), porque entity_key llega
    como parte dinámica de la URL en las rutas del CRUD genérico.
    Aborta con 403 si el rol del usuario no tiene ese permiso.
    Uso dentro de una vista: require_permission(entity_key, "edit")
    """
    user = get_current_user()
    if not user or not can(user["rol"], entity_key, action):
        abort(403)
