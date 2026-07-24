# controllers/auth_controller.py
# Blueprint con la ventana de login y el logout.
# Usa la tabla USUARIO (ver models/entities.py -> "usuario" y codigo.sql)
# y compara contraseñas con hash (werkzeug), nunca en texto plano.

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from models import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ya hay sesión iniciada, no tiene sentido ver el login de nuevo.
    if session.get("user"):
        return redirect(url_for("crud.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        usuario = db.get_usuario_by_username(username)

        if not usuario:
            flash("Usuario o contraseña incorrectos.", "danger")
        elif int(usuario["ACTIVO"]) != 1:
            flash("Este usuario está deshabilitado.", "danger")
        elif not check_password_hash(usuario["PASSWORD_HASH"], password):
            flash("Usuario o contraseña incorrectos.", "danger")
        else:
            session["user"] = {
                "id_usuario": usuario["ID_USUARIO"],
                "username": usuario["USERNAME"],
                "rol": usuario["ROL"],
                "ci": usuario["CI"],
            }
            flash(f"Bienvenido, {usuario['USERNAME']} ({usuario['ROL']}).", "success")
            return redirect(url_for("crud.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
