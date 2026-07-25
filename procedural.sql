--Inserta en una sola transacción la información personal, laboral y su teléfono inicial.

CREATE OR REPLACE PROCEDURE SP_REGISTRAR_TRABAJADOR (
    p_ci       IN NUMBER,
    p_nombre   IN VARCHAR2,
    p_paterno  IN VARCHAR2,
    p_materno  IN VARCHAR2,
    p_fecha_nac IN DATE,
    p_sexo    IN CHAR,
    p_salida  IN VARCHAR2,
    p_entrada IN VARCHAR2,
    p_sueldo  IN NUMBER,
    p_fono    IN NUMBER
) AS
    v_id_fono NUMBER;
BEGIN
    INSERT INTO PERSONA (ci, nombre, paterno, materno, fecha_nac, sexo)
    VALUES (p_ci, p_nombre, p_paterno, p_materno, p_fecha_nac, p_sexo);

    INSERT INTO TRABAJADOR (ci, salida, entrada, sueldo)
    VALUES (p_ci, p_salida, p_entrada, p_sueldo);

    IF p_fono IS NOT NULL THEN
        SELECT NVL(MAX(id_fono_persona), 0) + 1 INTO v_id_fono FROM FONO_PERSONA;
        INSERT INTO FONO_PERSONA (id_fono_persona, ci, fono)
        VALUES (v_id_fono, p_ci, p_fono);
    END IF;

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Trabajador registrado con éxito.');
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20001, 'Error al registrar el trabajador: ' || SQLERRM);
END;

-- Incrementa el sueldo de un trabajador aplicando un porcentaje.
CREATE OR REPLACE PROCEDURE SP_MODIFICAR_SUELDO (
    p_ci         IN NUMBER,
    p_porcentaje IN NUMBER
) AS
    v_existe NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_existe FROM TRABAJADOR WHERE ci = p_ci;
    
    IF v_existe = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'El trabajador con CI ' || p_ci || ' no existe.');
    END IF;

    UPDATE TRABAJADOR
    SET sueldo = sueldo + (sueldo * (p_porcentaje / 100))
    WHERE ci = p_ci;

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Sueldo actualizado exitosamente.');
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;

--
