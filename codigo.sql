CREATE TABLE PERSONA (
    ci NUMBER,
    nombre VARCHAR2(100) NOT NULL,
    paterno VARCHAR2(100) NOT NULL,
    materno VARCHAR2(100),
    fecha_nac DATE NOT NULL,
    sexo CHAR(1) NOT NULL,
    
    CONSTRAINT persona_pk PRIMARY KEY (ci),
    CONSTRAINT chk_sexo
        CHECK (sexo IN ('M', 'F'))
);
CREATE TABLE FONO_PERSONA(
    id_fono_persona number,
    ci number not null,
    fono number(8) not null, 
    CONSTRAINT fono_persona_pk PRIMARY KEY (id_fono_persona),
    CONSTRAINT fono_persona_fk FOREIGN KEY (ci) REFERENCES PERSONA(ci)
);
CREATE TABLE TRABAJADOR (
    ci number not null,
    salida varchar2(10),
    entrada varchar2(10),
    sueldo number,
    CONSTRAINT trabajador_pk PRIMARY KEY (ci),
    CONSTRAINT trabajador_fk FOREIGN KEY (ci) REFERENCES PERSONA(ci)    
);
CREATE TABLE INSTRUCTOR(
    ci NUMBER NOT NULL,
    certificacion VARCHAR2(100),
    anios_experiencia NUMBER,

    CONSTRAINT instructor_pk PRIMARY KEY (ci),
    CONSTRAINT instructor_fk FOREIGN KEY (ci)
        REFERENCES TRABAJADOR(ci)
);
CREATE TABLE MANTENIMIENTO(
    ci NUMBER NOT NULL,
    

    CONSTRAINT mantenimiento_pk PRIMARY KEY (ci),
    CONSTRAINT mantenimiento_fk FOREIGN KEY (ci)
        REFERENCES TRABAJADOR(ci)
);
CREATE TABLE MATERIAL_MANTENIMIENTO(
    id_material_mantenimiento NUMBER,
    ci NUMBER NOT NULL,
    material VARCHAR2(100) not null,

    CONSTRAINT material_mantenimiento_pk PRIMARY KEY (id_material_mantenimiento),
    CONSTRAINT material_mantenimiento_fk FOREIGN KEY (ci) REFERENCES MANTENIMIENTO(ci)
);

Create table cliente(
    ci number not null enable,
    ci_entrenador number,
    altura number,
    peso number,
    Constraint cliente_pk PRIMARY KEY (ci) enable,
    CONSTRAINT cliente_fk1 FOREIGN KEY (ci) REFERENCES Persona(ci) enable,
    CONSTRAINT cliente_fk2 FOREIGN KEY (ci_entrenador) REFERENCES INSTRUCTOR(ci)    
);

Create table Area(
    id_area number not null enable,
    descripcion varchar2(100),
    capacidad number,
    CONSTRAINT area_pk PRIMARY KEY (id_area) enable
);

create table RECEPCIONISTA(
    ci number not null enable,
    nro_caja number,
    constraint recepcionista_pk primary key(ci),
    constraint recepcionista_fk foreign key(ci) references trabajador(ci)
);
create table MEMBRESIA(
    id_membresia number not null enable,
    tipo varchar2(100),
    precio number,
    ci number,
    constraint menbresia_pk primary key (id_membresia),
    constraint membresia_fk foreign key (ci) references RECEPCIONISTA (ci)
);
create table PAGA(
    ci_cliente number,
    id_membresia number,
    fecha_ini date,
    fecha_fin date,
    turno varchar2(100),
    constraint paga_pk primary key(ci_cliente,id_membresia,fecha_ini),
    constraint paga_fk_cliente foreign key(ci_cliente) references CLIENTE(ci),
    constraint paga_fk_membresia foreign key(id_membresia)references MEMBRESIA(id_membresia),
    CONSTRAINT CHK_TURNO check(turno in('Tarde','Mañana','Noche'))
);
create table MAQUINA(
    id_maquina number not null enable,
    nombre varchar2(100),
    musculo_objetivo varchar2(100),
    marca varchar2(100),
    id_area number,
    constraint maquina_pk primary key(id_maquina),
    constraint maquina_fk foreign key(id_area)references AREA(id_area)    
);
create table ACTIVIDAD(
    id_actividad number not null enable,
    descripcion varchar2(100),
    capacidad number,
    nombre varchar2(100),
    id_area number,
    constraint actividad_pk primary key(id_actividad),
    constraint actividad_fk foreign key(id_area) references AREA(id_area)
);

CREATE TABLE organiza(
    ci number,
    id_actividad number,
    fecha date not null,
    hora varchar2(10),
    constraint organiza_pk primary key(ci,id_actividad),
    constraint organiza_fk1 foreign key (ci) 
    references INSTRUCTOR(ci),
    constraint organiza_fk2 foreign key (id_actividad) 
    references ACTIVIDAD(id_actividad)   
);








create table Casillero(
    id_casillero number not null enable,
    tamanio varchar2(100),
    ci number,
    CONSTRAINT casillero_pk PRIMARY KEY (id_casillero) enable,
    CONSTRAINT casillero_fk FOREIGN KEY (ci) REFERENCES Cliente(ci) enable
);


create table condicion_medica_cliente(
    id_condicion number not null enable,
    ci number,
    condicion_medica varchar2(100),
    Constraint condicion_medica_pk PRIMARY KEY (id_condicion) enable,
    CONSTRAINT condicion_medica_fk FOREIGN KEY (ci) REFERENCES cliente(ci) enable 
);

Create table Suplemento(
    id_suplemento number not null enable,
    peso number,
    nombre varchar2(100),
    precio number,
    CONSTRAINT suplemento_pk PRIMARY KEY (id_suplemento) enable
);

Create table Compra(
    id_compra number not null enable,
    ci number,
    id_suplemento number,
    Constraint compra_pk PRIMARY KEY (id_compra) enable,
    Constraint compra_fk1 FOREIGN KEY (ci) REFERENCES CLIENTE(ci) enable,
    Constraint compra_fk2 FOREIGN KEY (id_suplemento) REFERENCES SUPLEMENTO(id_suplemento) enable
);



Create table vende(
    id_vende number,
    fecha_venta date,
    ci number,
    id_suplemento number,
    CONSTRAINT vende_pk PRIMARY KEY (id_vende) enable,
    CONSTRAINT vende_fk1 FOREIGN KEY (ci) REFERENCES RECEPCIONISTA(ci) enable,
    CONSTRAINT vende_fk2 FOREIGN KEY (id_suplemento) REFERENCES SUPLEMENTO(id_suplemento) enable
);

Create table ofrece_sesion(
    id_ofrece number not null enable,
    ci_C number,
    ci_R number,
    hora varchar2(100),
    costo number,
    fecha date,
    CONSTRAINT ofrece_sesion_pk PRIMARY KEY (id_ofrece) enable,
    CONSTRAINT ofrece_sesion_fk1 FOREIGN KEY (ci_C) REFERENCES CLIENTE(ci) enable,
    CONSTRAINT ofrece_sesion_fk2 FOREIGN KEY (ci_R) REFERENCES RECEPCIONISTA(ci) enable   
);

Create table mantiene(
    id_mantiene number not null enable,
    ci number,
    id_area number,
    CONSTRAINT mantiene_pk PRIMARY KEY (id_mantiene) enable,
    CONSTRAINT mantiene_fk1 FOREIGN KEY (ci) REFERENCES Mantenimiento(ci) enable,
    CONSTRAINT mantiene_fk2 FOREIGN KEY (id_area) REFERENCES Area(id_area) enable
);

-- ============================================================
-- Tabla de usuarios para el LOGIN de la aplicación Flask.
-- No confundir con los ROLES DE ORACLE (esos están en roles_oracle.sql):
-- esta tabla es la que usa la app para saber quién entra y con qué rol,
-- y así mostrar/permitir solo las opciones de su rol dentro de Flask.
-- ============================================================
CREATE TABLE USUARIO (
    id_usuario NUMBER,
    ci NUMBER,
    username VARCHAR2(50) NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    rol VARCHAR2(20) NOT NULL,
    activo NUMBER(1) DEFAULT 1 NOT NULL,
    CONSTRAINT usuario_pk PRIMARY KEY (id_usuario),
    CONSTRAINT usuario_username_uk UNIQUE (username),
    CONSTRAINT usuario_fk FOREIGN KEY (ci) REFERENCES PERSONA(ci),
    CONSTRAINT chk_rol CHECK (rol IN ('ADMIN','INSTRUCTOR','RECEPCIONISTA','MANTENIMIENTO','CLIENTE')),
    CONSTRAINT chk_usuario_activo CHECK (activo IN (0,1))
);

Create table asiste(
    id_asiste number not null enable,
    id_actividad number,
    ci number,
    CONSTRAINT asiste_pk PRIMARY KEY (id_asiste) enable,
    CONSTRAINT asiste_fk1 FOREIGN KEY (id_actividad) REFERENCES ACTIVIDAD(id_actividad) enable,
    CONSTRAINT asiste_fk2 FOREIGN KEY (ci) REFERENCES Cliente(ci) enable
);

