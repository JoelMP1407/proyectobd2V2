from flask import Blueprint, render_template

main = Blueprint('main', __name__)

MODULOS = [
    ('persona.listar', 'Persona'),
    ('fono_persona.listar', 'Teléfonos'),
    ('trabajador.listar', 'Trabajador'),
    ('instructor.listar', 'Instructor'),
    ('mantenimiento.listar', 'Mantenimiento'),
    ('material_mantenimiento.listar', 'Materiales'),
    ('recepcionista.listar', 'Recepcionista'),
    ('cliente.listar', 'Cliente'),
    ('membresia.listar', 'Membresía'),
    ('paga.listar', 'Pagos'),
    ('area.listar', 'Área'),
    ('maquina.listar', 'Máquina'),
    ('actividad.listar', 'Actividad'),
    ('organiza.listar', 'Organiza'),
    ('casillero.listar', 'Casillero'),
    ('condicion_medica_cliente.listar', 'Condición médica'),
    ('suplemento.listar', 'Suplemento'),
    ('compra.listar', 'Compra'),
    ('vende.listar', 'Vende'),
    ('ofrece_sesion.listar', 'Sesiones'),
    ('mantiene.listar', 'Mantiene'),
    ('asiste.listar', 'Asiste'),
]


@main.route('/')
def index():
    return render_template('index.html', modulos=MODULOS)
