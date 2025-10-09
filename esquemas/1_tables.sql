CREATE TABLE caracteristica (
    id int(11) NOT NULL AUTO_INCREMENT,
    campo varchar(100) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 71 DEFAULT CHARSET = utf8mb3;
CREATE TABLE caracteristica_producto (
    caracteristicaid int(11) NOT NULL,
    productoid int(11) NOT NULL,
    valor varchar(50) NOT NULL,
    principal tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (caracteristicaid, productoid)
) DEFAULT CHARSET = utf8mb3;
CREATE TABLE caracteristica_subcategoria (
    caracteristicaid int(11) NOT NULL,
    subcategoriaid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (caracteristicaid, subcategoriaid)
) DEFAULT CHARSET = utf8mb3;
CREATE TABLE categoria (
    id int(11) NOT NULL AUTO_INCREMENT,
    categoria varchar(50) NOT NULL,
    faicon_cat varchar(50) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 8 DEFAULT CHARSET = utf8mb3;
CREATE TABLE comentario (
    id int(11) NOT NULL AUTO_INCREMENT,
    nombres varchar(50) NOT NULL,
    apellidos varchar(50) NOT NULL,
    email varchar(70) NOT NULL,
    celular varchar(80) NOT NULL,
    mensaje text NOT NULL,
    fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    estado tinyint(1) NOT NULL,
    motivo_comentarioid int(11) NOT NULL,
    usuarioid int(11),
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 2 DEFAULT CHARSET = utf8mb3;
CREATE TABLE contenido_info (
    id int(11) NOT NULL AUTO_INCREMENT,
    titulo text NOT NULL,
    cuerpo text NOT NULL,
    tipo_contenido_infoid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 28 DEFAULT CHARSET = utf8mb3;
CREATE TABLE cupon (
    id int(11) NOT NULL AUTO_INCREMENT,
    codigo varchar(30) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_vencimiento date NOT NULL,
    cant_descuento decimal(6, 2) NOT NULL,
    fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 2 DEFAULT CHARSET = utf8mb3;
CREATE TABLE detalles_pedido (
    productoid int(11) NOT NULL,
    pedidoid int(11) NOT NULL,
    cantidad int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (productoid, pedidoid)
) DEFAULT CHARSET = utf8mb3;
CREATE TABLE estado_pedido (
    id int(11) NOT NULL AUTO_INCREMENT,
    nomestado varchar(55) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8mb3;
CREATE TABLE img_novedad (
    id int(11) NOT NULL AUTO_INCREMENT,
    nomimagen varchar(100),
    imagen text NOT NULL,
    tipo_img_novedadid int(11) NOT NULL,
    novedadid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 9 DEFAULT CHARSET = utf8mb3;
CREATE TABLE img_producto (
    id int(11) NOT NULL AUTO_INCREMENT,
    img_nombre varchar(100),
    imagen text NOT NULL,
    imgprincipal tinyint(1) NOT NULL,
    productoid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 21 DEFAULT CHARSET = utf8mb3;
CREATE TABLE informacion_domus (
    id int(11) NOT NULL AUTO_INCREMENT,
    correo varchar(200) NOT NULL,
    numero varchar(20) NOT NULL,
    imglogo text NOT NULL,
    imgicon text NOT NULL,
    descripcion text NOT NULL,
    historia text NOT NULL,
    vision text NOT NULL,
    valores text NOT NULL,
    mision text NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 2 DEFAULT CHARSET = utf8mb3;
CREATE TABLE lista_deseos (
    productoid int(11) NOT NULL,
    usuarioid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (productoid, usuarioid)
) DEFAULT CHARSET = utf8mb3;
CREATE TABLE marca (
    id int(11) NOT NULL AUTO_INCREMENT,
    marca varchar(45) NOT NULL,
    img_logo text NOT NULL,
    img_banner text,
    fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 67 DEFAULT CHARSET = utf8mb3;
CREATE TABLE metodo_pago (
    id int(11) NOT NULL AUTO_INCREMENT,
    metodo varchar(50) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb3;
CREATE TABLE motivo_comentario (
    id int(11) NOT NULL AUTO_INCREMENT,
    motivo varchar(50) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 7 DEFAULT CHARSET = utf8mb3;
CREATE TABLE novedad (
    id int(11) NOT NULL AUTO_INCREMENT,
    nombre varchar(55) NOT NULL,
    titulo varchar(55) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_vencimiento date NOT NULL,
    terminos text NOT NULL,
    fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    marcaid int(11),
    subcategoriaid int(11),
    tipo_novedadid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 8 DEFAULT CHARSET = utf8mb3;
CREATE TABLE pedido (
    id int(11) NOT NULL AUTO_INCREMENT,
    fecha_compra date,
    subtotal decimal(9, 2),
    metodo_pagoid int(11),
    usuarioid int(11) NOT NULL,
    estado_pedidoid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 26 DEFAULT CHARSET = utf8mb3;
CREATE TABLE producto (
    id int(11) NOT NULL AUTO_INCREMENT,
    nombre varchar(150) NOT NULL,
    price_regular decimal(9, 2),
    precio_online decimal(9, 2) NOT NULL,
    precio_oferta decimal(9, 2),
    info_adicional text,
    stock int(11) NOT NULL,
    fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    marcaid int(11) NOT NULL,
    subcategoriaid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 15 DEFAULT CHARSET = utf8mb3;
CREATE TABLE redes_sociales (
    id int(11) NOT NULL AUTO_INCREMENT,
    nomred varchar(150) NOT NULL,
    faicon_red varchar(30) NOT NULL,
    enlace varchar(200) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 7 DEFAULT CHARSET = utf8mb3;
CREATE TABLE subcategoria (
    id int(11) NOT NULL AUTO_INCREMENT,
    subcategoria varchar(50) NOT NULL,
    faicon_subcat varchar(50) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    categoriaid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 61 DEFAULT CHARSET = utf8mb3;
CREATE TABLE tipo_contenido_info (
    id int(11) NOT NULL AUTO_INCREMENT,
    nombre varchar(255) NOT NULL,
    descripcion text NOT NULL,
    faicon_cont varchar(50) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 7 DEFAULT CHARSET = utf8mb3;
CREATE TABLE tipo_img_novedad (
    id int(11) NOT NULL AUTO_INCREMENT,
    tipo varchar(50) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 6 DEFAULT CHARSET = utf8mb3;
CREATE TABLE tipo_novedad (
    id int(11) NOT NULL AUTO_INCREMENT,
    nomtipo varchar(55) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb3;
CREATE TABLE tipo_usuario (
    id int(11) NOT NULL AUTO_INCREMENT,
    tipo varchar(55) NOT NULL,
    imagen text NOT NULL,
    descripcion varchar(300) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb3;
CREATE TABLE usuario (
    id int(11) NOT NULL AUTO_INCREMENT,
    nombres varchar(50) NOT NULL,
    apellidos varchar(50) NOT NULL,
    doc_identidad varchar(15) NOT NULL,
    img_usuario text,
    genero tinyint(1) NOT NULL,
    fecha_nacimiento date NOT NULL,
    telefono varchar(15) NOT NULL,
    correo varchar(60) NOT NULL,
    contrasenia varchar(100) NOT NULL,
    disponibilidad tinyint(1) NOT NULL,
    fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    tipo_usuarioid int(11) NOT NULL,
    registro_auditoria timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 35 DEFAULT CHARSET = utf8mb3;
CREATE UNIQUE INDEX correo ON usuario (correo);
ALTER TABLE caracteristica_producto
ADD CONSTRAINT fkcaracteris256942 FOREIGN KEY (productoid) REFERENCES producto (id);
ALTER TABLE caracteristica_subcategoria
ADD CONSTRAINT fkcaracteris460748 FOREIGN KEY (subcategoriaid) REFERENCES subcategoria (id);
ALTER TABLE caracteristica_subcategoria
ADD CONSTRAINT fkcaracteris872968 FOREIGN KEY (caracteristicaid) REFERENCES caracteristica (id);
ALTER TABLE caracteristica_producto
ADD CONSTRAINT fkcaracteris944109 FOREIGN KEY (caracteristicaid) REFERENCES caracteristica (id);
ALTER TABLE comentario
ADD CONSTRAINT fkcomentario180941 FOREIGN KEY (usuarioid) REFERENCES usuario (id);
ALTER TABLE comentario
ADD CONSTRAINT fkcomentario473576 FOREIGN KEY (motivo_comentarioid) REFERENCES motivo_comentario (id);
ALTER TABLE contenido_info
ADD CONSTRAINT fkcontenido_553733 FOREIGN KEY (tipo_contenido_infoid) REFERENCES tipo_contenido_info (id);
ALTER TABLE detalles_pedido
ADD CONSTRAINT fkdetalles_p720300 FOREIGN KEY (pedidoid) REFERENCES pedido (id);
ALTER TABLE detalles_pedido
ADD CONSTRAINT fkdetalles_p873247 FOREIGN KEY (productoid) REFERENCES producto (id);
ALTER TABLE img_novedad
ADD CONSTRAINT fkimg_noveda411983 FOREIGN KEY (tipo_img_novedadid) REFERENCES tipo_img_novedad (id);
ALTER TABLE img_novedad
ADD CONSTRAINT fkimg_noveda721180 FOREIGN KEY (novedadid) REFERENCES novedad (id);
ALTER TABLE img_producto
ADD CONSTRAINT fkimg_produc616199 FOREIGN KEY (productoid) REFERENCES producto (id);
ALTER TABLE lista_deseos
ADD CONSTRAINT fklista_dese59890 FOREIGN KEY (productoid) REFERENCES producto (id);
ALTER TABLE lista_deseos
ADD CONSTRAINT fklista_dese907029 FOREIGN KEY (usuarioid) REFERENCES usuario (id);
ALTER TABLE novedad
ADD CONSTRAINT fknovedad215901 FOREIGN KEY (marcaid) REFERENCES marca (id);
ALTER TABLE novedad
ADD CONSTRAINT fknovedad812313 FOREIGN KEY (tipo_novedadid) REFERENCES tipo_novedad (id);
ALTER TABLE novedad
ADD CONSTRAINT fknovedad821851 FOREIGN KEY (subcategoriaid) REFERENCES subcategoria (id);
ALTER TABLE pedido
ADD CONSTRAINT fkpedido259150 FOREIGN KEY (estado_pedidoid) REFERENCES estado_pedido (id);
ALTER TABLE pedido
ADD CONSTRAINT fkpedido787527 FOREIGN KEY (metodo_pagoid) REFERENCES metodo_pago (id);
ALTER TABLE pedido
ADD CONSTRAINT fkpedido832373 FOREIGN KEY (usuarioid) REFERENCES usuario (id);
ALTER TABLE producto
ADD CONSTRAINT fkproducto953045 FOREIGN KEY (subcategoriaid) REFERENCES subcategoria (id);
ALTER TABLE producto
ADD CONSTRAINT fkproducto990798 FOREIGN KEY (marcaid) REFERENCES marca (id);
ALTER TABLE subcategoria
ADD CONSTRAINT fksubcategor822804 FOREIGN KEY (categoriaid) REFERENCES categoria (id);
ALTER TABLE usuario
ADD CONSTRAINT fkusuario533117 FOREIGN KEY (tipo_usuarioid) REFERENCES tipo_usuario (id);