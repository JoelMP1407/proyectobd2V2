# controllers/crud_controller.py
# Controlador (Blueprint) con la lógica de rutas para el CRUD genérico.
# Sirve a las entidades definidas en models/entities.py sin necesitar
# un controlador por cada tabla.
#
# Control de acceso por rol:
# - Todas las rutas de este blueprint exigen sesión iniciada (login).
# - Cada acción (ver/crear/editar/borrar) se valida contra permissions.py
#   según el rol del usuario logueado (ADMIN, INSTRUCTOR, RECEPCIONISTA,
#   MANTENIMIENTO, CLIENTE).
# - El rol CLIENTE, además, solo ve SUS PROPIAS filas en las entidades
#   marcadas en permissions.OWNER_COLUMN (filtro por CI en el SQL).

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash

from models.entities import ENTITIES, get_entity
from models import db
from auth import get_current_user
from permissions import can, allowed_entities, owner_column_for

crud_bp = Blueprint("crud", __name__)

PK_SEP = "~"  # separador para claves primarias compuestas en la URL


# ---------- Seguridad: exigir login en TODO el blueprint ----------

@crud_bp.before_request
def _require_login():
    if not get_current_user():
        flash("Debes iniciar sesión para continuar.", "warning")
        return redirect(url_for("auth.login"))


def _current_role():
    return get_current_user()["rol"]


def _forbid_unless(entity_key, action):
    """Aborta con 403 si el rol actual no tiene el permiso pedido."""
    if not can(_current_role(), entity_key, action):
        abort(403)


# ---------- Helpers internos del controlador ----------

def pk_to_str(values):
    return PK_SEP.join(str(v) for v in values)


def str_to_pk(pk_str):
    return pk_str.split(PK_SEP)


def parse_value(raw, col):
    """Convierte el valor de un <form> (siempre string) al tipo Python correcto."""
    if raw == "" or raw is None:
        return None
    if col["type"] == "number":
        try:
            return int(raw)
        except ValueError:
            return float(raw)
    if col["type"] == "date":
        return datetime.strptime(raw, "%Y-%m-%d").date()
    if col["type"] == "fk":
        try:
            return int(raw)
        except ValueError:
            return raw
    return raw  # text / select / password


def build_fk_options(col):
    ref = get_entity(col["ref"])
    return db.fetch_fk_options(ref["table"], ref["pk"][0], ref["display"])


def enrich_columns_with_options(entity):
    """Para cada columna fk, adjunta las opciones para el <select>."""
    enriched = []
    for col in entity["columns"]:
        c = dict(col)
        if c["type"] == "fk":
            c["fk_options"] = build_fk_options(c)
        enriched.append(c)
    return enriched


def _prepare_usuario_data(entity_key, data, is_edit):
    """
    Caso especial de la entidad 'usuario': la columna virtual PASSWORD
    (definida en entities.py) no existe como tal en la tabla; se
    convierte en PASSWORD_HASH antes de guardar. En edición, si viene
    vacía se conserva la contraseña anterior (no se sobreescribe).
    """
    if entity_key != "usuario":
        return data
    raw_password = data.pop("PASSWORD", None)
    if raw_password:
        data["PASSWORD_HASH"] = generate_password_hash(raw_password)
    elif not is_edit:
        raise ValueError("La contraseña es obligatoria al crear un usuario.")
    if "ACTIVO" in data and data["ACTIVO"] is not None:
        data["ACTIVO"] = int(data["ACTIVO"])
    return data


def _permissions_for_template(entity_key):
    rol = _current_role()
    return {
        "create": can(rol, entity_key, "create"),
        "edit": can(rol, entity_key, "edit"),
        "delete": can(rol, entity_key, "delete"),
    }


# ---------- Rutas ----------

@crud_bp.route("/")
def index():
    allowed = allowed_entities(_current_role())
    if allowed is None:
        visible_entities = ENTITIES
    else:
        visible_entities = {k: v for k, v in ENTITIES.items() if k in allowed}
    return render_template("index.html", entities=visible_entities)


@crud_bp.route("/<entity_key>/")
def list_entity(entity_key):
    entity = get_entity(entity_key)
    if not entity:
        abort(404)
    _forbid_unless(entity_key, "view")

    filter_col = None
    filter_value = None
    if _current_role() == "CLIENTE":
        filter_col = owner_column_for(entity_key)
        filter_value = get_current_user()["ci"]

    rows = db.fetch_all(entity["table"], filter_col=filter_col, filter_value=filter_value)
    for row in rows:
        row["_pk_str"] = pk_to_str([row[c] for c in entity["pk"]])
    return render_template(
        "list.html",
        entity_key=entity_key,
        entity=entity,
        rows=rows,
        perms=_permissions_for_template(entity_key),
    )


@crud_bp.route("/<entity_key>/new", methods=["GET", "POST"])
def new_entity(entity_key):
    entity = get_entity(entity_key)
    if not entity:
        abort(404)
    _forbid_unless(entity_key, "create")

    if request.method == "POST":
        data = {}
        for col in entity["columns"]:
            if col.get("auto"):
                continue
            raw = request.form.get(col["name"], "")
            data[col["name"]] = parse_value(raw, col)

        try:
            data = _prepare_usuario_data(entity_key, data, is_edit=False)

            # Generar IDs automáticos (surrogados) que no vienen del formulario
            for col in entity["columns"]:
                if col.get("auto"):
                    data[col["name"]] = db.next_id(entity["table"], col["name"])

            db.insert_row(entity["table"], data)
            flash(f"{entity['label']} creado correctamente.", "success")
            return redirect(url_for("crud.list_entity", entity_key=entity_key))
        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"Error al guardar: {e}", "danger")

    columns = enrich_columns_with_options(entity)
    return render_template(
        "form.html",
        entity_key=entity_key,
        entity=entity,
        columns=columns,
        row=None,
        mode="new",
    )


@crud_bp.route("/<entity_key>/edit/<path:pk_str>", methods=["GET", "POST"])
def edit_entity(entity_key, pk_str):
    entity = get_entity(entity_key)
    if not entity:
        abort(404)
    _forbid_unless(entity_key, "edit")

    pk_values_raw = str_to_pk(pk_str)
    pk_cols_def = {c["name"]: c for c in entity["columns"]}
    pk_values = [
        parse_value(v, pk_cols_def[name])
        for name, v in zip(entity["pk"], pk_values_raw)
    ]

    if request.method == "POST":
        data = {}
        for col in entity["columns"]:
            if col.get("pk"):
                continue  # la PK no se edita
            raw = request.form.get(col["name"], "")
            data[col["name"]] = parse_value(raw, col)

        data = _prepare_usuario_data(entity_key, data, is_edit=True)

        try:
            db.update_row(entity["table"], data, entity["pk"], pk_values)
            flash(f"{entity['label']} actualizado correctamente.", "success")
            return redirect(url_for("crud.list_entity", entity_key=entity_key))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    row = db.fetch_one(entity["table"], entity["pk"], pk_values)
    if not row:
        abort(404)

    columns = enrich_columns_with_options(entity)
    return render_template(
        "form.html",
        entity_key=entity_key,
        entity=entity,
        columns=columns,
        row=row,
        mode="edit",
        pk_str=pk_str,
    )


@crud_bp.route("/<entity_key>/delete/<path:pk_str>", methods=["POST"])
def delete_entity(entity_key, pk_str):
    entity = get_entity(entity_key)
    if not entity:
        abort(404)
    _forbid_unless(entity_key, "delete")

    pk_values_raw = str_to_pk(pk_str)
    pk_cols_def = {c["name"]: c for c in entity["columns"]}
    pk_values = [
        parse_value(v, pk_cols_def[name])
        for name, v in zip(entity["pk"], pk_values_raw)
    ]
    try:
        db.delete_row(entity["table"], entity["pk"], pk_values)
        flash(f"{entity['label']} eliminado correctamente.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar (probablemente tiene registros relacionados): {e}", "danger")

    return redirect(url_for("crud.list_entity", entity_key=entity_key))
