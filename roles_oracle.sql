-- ============================================================
-- roles_oracle.sql
-- Roles de Oracle para el sistema del Gimnasio (seguridad a nivel BD).
--
-- IMPORTANTE:
-- Esto es INDEPENDIENTE del login de la app Flask (tabla USUARIO,
-- ver codigo.sql). La app hoy se conecta a Oracle con un único
-- usuario fijo (bd272, ver config.py), y controla los permisos por
-- rol dentro del propio código Python (ver permissions.py). Estos
-- roles/GRANT de Oracle sirven como una segunda capa de seguridad
-- a nivel de base de datos y para el requisito académico de crear
-- roles con privilegios diferenciados.
--
-- Si más adelante quieres que cada tipo de usuario se conecte a
-- Oracle con SU PROPIO usuario (en vez de siempre bd272), puedes
-- crear un USER de Oracle por persona/rol (ver sección 7) y cambiar
-- config.py para que la conexión use esas credenciales según el rol
-- que inició sesión en la app.
--
-- Ejecutar conectado como el dueño del esquema (bd272) o como DBA.
-- Si lo ejecutas como DBA, antepone "bd272." a cada nombre de tabla,
-- por ejemplo: GRANT SELECT ON bd272.PERSONA TO rol_recepcionista;
-- ============================================================


-- 1) Crear los roles ---------------------------------------------------
CREATE ROLE rol_admin;
CREATE ROLE rol_instructor;
CREATE ROLE rol_recepcionista;
CREATE ROLE rol_mantenimiento;
CREATE ROLE rol_cliente;


-- 2) rol_admin: control total sobre todas las tablas del esquema -------
GRANT SELECT, INSERT, UPDATE, DELETE ON PERSONA                    TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON FONO_PERSONA               TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON TRABAJADOR                 TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON INSTRUCTOR                 TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON MANTENIMIENTO              TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON MATERIAL_MANTENIMIENTO     TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON RECEPCIONISTA              TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON CLIENTE                    TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON AREA                       TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON MEMBRESIA                  TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON PAGA                       TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON MAQUINA                    TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ACTIVIDAD                  TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ORGANIZA                   TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON CASILLERO                  TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON CONDICION_MEDICA_CLIENTE   TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON SUPLEMENTO                 TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON COMPRA                     TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON VENDE                      TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON OFRECE_SESION              TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON MANTIENE                   TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ASISTE                     TO rol_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON USUARIO                    TO rol_admin;
-- El admin además puede crear objetos nuevos en su propio esquema
-- (útil si administra la estructura de la BD, no solo los datos):
GRANT CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO rol_admin;


-- 3) rol_instructor (entrenador) ----------------------------------------
-- Ve a sus clientes, áreas y máquinas; administra actividades/clases,
-- quién las organiza y el control de asistencia; edita su propio perfil.
GRANT SELECT, UPDATE               ON INSTRUCTOR TO rol_instructor;
GRANT SELECT                       ON CLIENTE     TO rol_instructor;
GRANT SELECT                       ON AREA        TO rol_instructor;
GRANT SELECT                       ON MAQUINA     TO rol_instructor;
GRANT SELECT, INSERT, UPDATE, DELETE ON ACTIVIDAD TO rol_instructor;
GRANT SELECT, INSERT, UPDATE, DELETE ON ORGANIZA  TO rol_instructor;
GRANT SELECT, INSERT, UPDATE, DELETE ON ASISTE    TO rol_instructor;


-- 4) rol_recepcionista ---------------------------------------------------
-- Atiende mostrador: altas de personas/clientes, membresías, pagos,
-- casilleros, venta de suplementos y sesiones ofrecidas.
GRANT SELECT, INSERT, UPDATE, DELETE ON PERSONA        TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON FONO_PERSONA   TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON CLIENTE        TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON MEMBRESIA      TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON PAGA           TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON CASILLERO      TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON SUPLEMENTO     TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON COMPRA         TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON VENDE          TO rol_recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON OFRECE_SESION  TO rol_recepcionista;
GRANT SELECT                       ON AREA             TO rol_recepcionista;
GRANT SELECT                       ON MAQUINA          TO rol_recepcionista;
GRANT SELECT                       ON ACTIVIDAD        TO rol_recepcionista;
GRANT SELECT                       ON INSTRUCTOR       TO rol_recepcionista;


-- 5) rol_mantenimiento -----------------------------------------------------
-- Administra materiales de mantenimiento y qué área mantiene cada quien.
GRANT SELECT, INSERT, UPDATE, DELETE ON MATERIAL_MANTENIMIENTO TO rol_mantenimiento;
GRANT SELECT, INSERT, UPDATE, DELETE ON MANTIENE               TO rol_mantenimiento;
GRANT SELECT                       ON AREA                     TO rol_mantenimiento;
GRANT SELECT                       ON MAQUINA                  TO rol_mantenimiento;


-- 6) rol_cliente -------------------------------------------------------------
-- Solo lectura. Oracle no filtra automáticamente "solo mis filas": ese
-- filtro por CI se aplica en la app (ver permissions.OWNER_COLUMN). Si
-- quisieras que la propia BD filtre filas por cliente, se necesitaría
-- Row Level Security / VPD (DBMS_RLS), que queda fuera de este alcance.
GRANT SELECT ON PERSONA                  TO rol_cliente;
GRANT SELECT ON CLIENTE                  TO rol_cliente;
GRANT SELECT ON PAGA                     TO rol_cliente;
GRANT SELECT ON CASILLERO                TO rol_cliente;
GRANT SELECT ON COMPRA                   TO rol_cliente;
GRANT SELECT ON ASISTE                   TO rol_cliente;
GRANT SELECT ON OFRECE_SESION            TO rol_cliente;
GRANT SELECT ON CONDICION_MEDICA_CLIENTE TO rol_cliente;
GRANT SELECT ON MEMBRESIA                TO rol_cliente;
GRANT SELECT ON SUPLEMENTO               TO rol_cliente;
GRANT SELECT ON ACTIVIDAD                TO rol_cliente;
GRANT SELECT ON AREA                     TO rol_cliente;
GRANT SELECT ON MAQUINA                  TO rol_cliente;


-- 7) (OPCIONAL) usuarios de Oracle de ejemplo, uno por rol -------------------
-- Descomenta y cambia las contraseñas si quieres probar cada rol
-- conectándote directamente a Oracle (SQL Developer, etc.), separado
-- de la app Flask.
--
CREATE USER demo_admin          IDENTIFIED BY "A12%$%BGfdas";
CREATE USER demo_instructor     IDENTIFIED BY "AUSH16$%&asd";
CREATE USER demo_recepcionista  IDENTIFIED BY "dasjiYD628$%";
CREATE USER demo_mantenimiento  IDENTIFIED BY "uh(aUIH&8731";
CREATE USER demo_cliente        IDENTIFIED BY "87HIShydas%&";
--
GRANT CONNECT TO demo_admin, demo_instructor, demo_recepcionista, demo_mantenimiento, demo_cliente;
--
GRANT rol_admin          TO demo_admin;
GRANT rol_instructor     TO demo_instructor;
GRANT rol_recepcionista  TO demo_recepcionista;
GRANT rol_mantenimiento  TO demo_mantenimiento;
GRANT rol_cliente        TO demo_cliente;


-- 8) Para revertir todo (limpieza) -------------------------------------------
-- DROP ROLE rol_admin;
-- DROP ROLE rol_instructor;
-- DROP ROLE rol_recepcionista;
-- DROP ROLE rol_mantenimiento;
-- DROP ROLE rol_cliente;
