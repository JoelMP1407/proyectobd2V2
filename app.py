# app.py
# Punto de entrada de la aplicación. Crea la app Flask y registra
# los Blueprints: autenticación (login/logout) y el CRUD genérico.

from flask import Flask, session
from config import SECRET_KEY
from controllers.crud_controller import crud_bp
from controllers.auth_controller import auth_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.register_blueprint(auth_bp)
    app.register_blueprint(crud_bp)

    @app.context_processor
    def inject_current_user():
        # Deja "current_user" disponible en todos los templates
        # (usado por base.html para mostrar usuario/rol y el botón salir).
        return {"current_user": session.get("user")}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
