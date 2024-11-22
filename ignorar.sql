CREATE TABLE marca (
  id             int(10) NOT NULL AUTO_INCREMENT, 
  marca          varchar(45) NOT NULL, 
  img_logo       longblob NOT NULL, 
  img_banner     longblob, 
  fecha_registro date NOT NULL DEFAULT current_timestamp, 
  disponibilidad tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (id));

CREATE TABLE producto (
  id             int(10) NOT NULL AUTO_INCREMENT, 
  nombre         varchar(150) NOT NULL, 
  price_regular  numeric(9, 2), 
  precio_online  numeric(9, 2) NOT NULL, 
  precio_oferta  numeric(9, 2), 
  info_adicional text,
  stock          int(11) NOT NULL, 
  fecha_registro date NOT NULL DEFAULT current_timestamp(), 
  disponibilidad tinyint(1) NOT NULL, 
  MARCAid        int(10) NOT NULL, 
  SUBCATEGORIAid int(10) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE subcategoria (
  id             int(10) NOT NULL AUTO_INCREMENT, 
  subcategoria   varchar(50) NOT NULL, 
  faicon_subcat  varchar(50) NOT NULL, 
  disponibilidad tinyint(1) NOT NULL, 
  CATEGORIAid    int(10) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE categoria (
  id             int(10) NOT NULL AUTO_INCREMENT, 
  categoria      varchar(50) NOT NULL, 
  faicon_cat     varchar(50) NOT NULL, 
  disponibilidad tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE pedido (
  id              int(10) NOT NULL AUTO_INCREMENT, 
  fecha_compra    date,
  subtotal        numeric(9, 2), 
  METODO_PAGOid   int(11), 
  USUARIOid       int(10) NOT NULL, 
  ESTADO_PEDIDOid int(11) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE usuario (
  id               int(10) NOT NULL AUTO_INCREMENT, 
  nombres          varchar(50) NOT NULL, 
  apellidos        varchar(50) NOT NULL, 
  doc_identidad    varchar(15) NOT NULL, 
  img_usuario      longblob, 
  genero           tinyint(1) NOT NULL, 
  fecha_nacimiento date NOT NULL, 
  telefono         varchar(15) NOT NULL, 
  correo           varchar(60) NOT NULL UNIQUE, 
  contrasenia       varchar(100) NOT NULL, 
  disponibilidad   tinyint(1) NOT NULL,
  fecha_registro date NOT NULL DEFAULT current_timestamp(), 
  TIPO_USUARIOid   int(11) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE img_producto (
  id           int(10) NOT NULL AUTO_INCREMENT, 
  img_nombre   varchar(100), 
  imagen       longblob NOT NULL, 
  imgPrincipal tinyint(1) NOT NULL, 
  PRODUCTOid   int(10) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE detalles_pedido (
  PRODUCTOid int(10) NOT NULL, 
  PEDIDOid   int(10) NOT NULL, 
  cantidad   int(2) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (PRODUCTOid, 
  PEDIDOid));

CREATE TABLE lista_deseos (
  PRODUCTOid int(10) NOT NULL, 
  USUARIOid  int(10) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (PRODUCTOid, 
  USUARIOid));

CREATE TABLE comentario (
  id                  int(11) NOT NULL AUTO_INCREMENT, 
  nombres             varchar(50) NOT NULL, 
  apellidos           varchar(50) NOT NULL, 
  email               varchar(70) NOT NULL, 
  celular             varchar(80) NOT NULL, 
  mensaje             text NOT NULL, 
  fecha_registro date NOT NULL DEFAULT current_timestamp(),  
  estado              tinyint(1) NOT NULL, 
  MOTIVO_COMENTARIOid int(11) NOT NULL, 
  USUARIOid           int(10),
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE motivo_comentario (
  id             int(11) NOT NULL AUTO_INCREMENT, 
  motivo         varchar(50) NOT NULL, 
  disponibilidad tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE tipo_novedad (
  id      int(10) NOT NULL AUTO_INCREMENT, 
  nomTipo varchar(55) NOT NULL,  
  disponibilidad tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE novedad (
  id                int(10) NOT NULL AUTO_INCREMENT, 
  nombre            varchar(55) NOT NULL, 
  titulo            varchar(55) NOT NULL, 
  fecha_inicio      date NOT NULL, 
  fecha_vencimiento date NOT NULL, 
  terminos          text NOT NULL, 
  fecha_registro date NOT NULL DEFAULT current_timestamp(), 
  disponibilidad    tinyint(1) NOT NULL, 
  MARCAid           int(10), 
  SUBCATEGORIAid    int(10), 
  TIPO_NOVEDADid    int(10) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE CARACTERISTICA_PRODUCTO (
  CARACTERISTICAid int(11) NOT NULL, 
  PRODUCTOid       int(10) NOT NULL, 
  valor            varchar(50) NOT NULL, 
  principal        tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (CARACTERISTICAid, 
  PRODUCTOid));

CREATE TABLE METODO_PAGO (
  id             int(11) NOT NULL AUTO_INCREMENT, 
  metodo         varchar(50) NOT NULL, 
  disponibilidad tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE TIPO_IMG_NOVEDAD (
  id             int(11) NOT NULL AUTO_INCREMENT, 
  tipo           varchar(50) NOT NULL, 
  disponibilidad tinyint(1) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE IMG_NOVEDAD (
  id                 int(11) NOT NULL AUTO_INCREMENT, 
  nomImagen          varchar(100), 
  imagen             longblob NOT NULL, 
  TIPO_IMG_NOVEDADid int(11) NOT NULL, 
  NOVEDADid          int(10) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE ESTADO_PEDIDO (
  id        int(11) NOT NULL AUTO_INCREMENT, 
  nomEstado varchar(55) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE TIPO_USUARIO (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  tipo        varchar(55) NOT NULL,
  imagen      longblob NOT NULL,
  descripcion varchar(300) NOT NULL,
  disponibilidad tinyint(1) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE CARACTERISTICA (
  id             int(11) NOT NULL AUTO_INCREMENT, 
  campo          varchar(100) NOT NULL, 
  disponibilidad tinyint(1) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE CARACTERISTICA_SUBCATEGORIA (
  CARACTERISTICAid int(11) NOT NULL, 
  SUBCATEGORIAid   int(10) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (CARACTERISTICAid, 
  SUBCATEGORIAid));

CREATE TABLE REDES_SOCIALES (
  id         int(11) NOT NULL AUTO_INCREMENT, 
  nomRed     varchar(150) NOT NULL, 
  faicon_red varchar(30) NOT NULL, 
  enlace     varchar(200) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));

CREATE TABLE INFORMACION_DOMUS (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  correo      varchar(200) NOT NULL, 
  numero      varchar(20) NOT NULL, 
  imgLogo     longblob NOT NULL, 
  imgIcon     longblob NOT NULL, 
  descripcion text NOT NULL, 
  historia    text NOT NULL, 
  vision      text NOT NULL, 
  valores     text NOT NULL, 
  mision      text NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));
CREATE TABLE TIPO_CONTENIDO_INFO (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(255) NOT NULL, 
  descripcion text NOT NULL, 
  faicon_cont varchar(50) NOT NULL,
  disponibilidad tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));
CREATE TABLE CONTENIDO_INFO (
  id                    int(11) NOT NULL AUTO_INCREMENT, 
  titulo                text NOT NULL, 
  cuerpo                text NOT NULL, 
  TIPO_CONTENIDO_INFOid int(11) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));
CREATE TABLE CUPON (
  id                int(11) NOT NULL AUTO_INCREMENT, 
  codigo            varchar(30) NOT NULL, 
  fecha_inicio      date NOT NULL, 
  fecha_vencimiento date NOT NULL, 
  cant_descuento    numeric(6, 2) NOT NULL,
  fecha_registro date NOT NULL DEFAULT current_timestamp(), 
  disponibilidad tinyint(1) NOT NULL,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id));
CREATE TABLE CUPON_USUARIO (
  CUPONid   int(11) NOT NULL, 
  USUARIOid int(10) NOT NULL, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (CUPONid, 
  USUARIOid));

ALTER TABLE CUPON_USUARIO ADD CONSTRAINT FKCUPON_USUA433993 FOREIGN KEY (CUPONid) REFERENCES CUPON (id);
ALTER TABLE CUPON_USUARIO ADD CONSTRAINT FKCUPON_USUA70914 FOREIGN KEY (USUARIOid) REFERENCES USUARIO (id);
ALTER TABLE PRODUCTO ADD CONSTRAINT FKPRODUCTO990798 FOREIGN KEY (MARCAid) REFERENCES MARCA (id);
ALTER TABLE PRODUCTO ADD CONSTRAINT FKPRODUCTO953045 FOREIGN KEY (SUBCATEGORIAid) REFERENCES SUBCATEGORIA (id);
ALTER TABLE SUBCATEGORIA ADD CONSTRAINT FKSUBCATEGOR822804 FOREIGN KEY (CATEGORIAid) REFERENCES CATEGORIA (id);
ALTER TABLE PEDIDO ADD CONSTRAINT FKPEDIDO787527 FOREIGN KEY (METODO_PAGOid) REFERENCES METODO_PAGO (id);
ALTER TABLE PEDIDO ADD CONSTRAINT FKPEDIDO832373 FOREIGN KEY (USUARIOid) REFERENCES USUARIO (id);
ALTER TABLE IMG_PRODUCTO ADD CONSTRAINT FKIMG_PRODUC616199 FOREIGN KEY (PRODUCTOid) REFERENCES PRODUCTO (id);
ALTER TABLE DETALLES_PEDIDO ADD CONSTRAINT FKDETALLES_P873247 FOREIGN KEY (PRODUCTOid) REFERENCES PRODUCTO (id);
ALTER TABLE DETALLES_PEDIDO ADD CONSTRAINT FKDETALLES_P720300 FOREIGN KEY (PEDIDOid) REFERENCES PEDIDO (id);
ALTER TABLE LISTA_DESEOS ADD CONSTRAINT FKLISTA_DESE59890 FOREIGN KEY (PRODUCTOid) REFERENCES PRODUCTO (id);
ALTER TABLE LISTA_DESEOS ADD CONSTRAINT FKLISTA_DESE907029 FOREIGN KEY (USUARIOid) REFERENCES USUARIO (id);
ALTER TABLE COMENTARIO ADD CONSTRAINT FKCOMENTARIO473576 FOREIGN KEY (MOTIVO_COMENTARIOid) REFERENCES MOTIVO_COMENTARIO (id);
ALTER TABLE COMENTARIO ADD CONSTRAINT FKCOMENTARIO180941 FOREIGN KEY (USUARIOid) REFERENCES USUARIO (id);
ALTER TABLE NOVEDAD ADD CONSTRAINT FKNOVEDAD215901 FOREIGN KEY (MARCAid) REFERENCES MARCA (id);
ALTER TABLE NOVEDAD ADD CONSTRAINT FKNOVEDAD821851 FOREIGN KEY (SUBCATEGORIAid) REFERENCES SUBCATEGORIA (id);
ALTER TABLE NOVEDAD ADD CONSTRAINT FKNOVEDAD812313 FOREIGN KEY (TIPO_NOVEDADid) REFERENCES TIPO_NOVEDAD (id);
ALTER TABLE IMG_NOVEDAD ADD CONSTRAINT FKIMG_NOVEDA411983 FOREIGN KEY (TIPO_IMG_NOVEDADid) REFERENCES TIPO_IMG_NOVEDAD (id);
ALTER TABLE IMG_NOVEDAD ADD CONSTRAINT FKIMG_NOVEDA721180 FOREIGN KEY (NOVEDADid) REFERENCES NOVEDAD (id);
ALTER TABLE PEDIDO ADD CONSTRAINT FKPEDIDO259150 FOREIGN KEY (ESTADO_PEDIDOid) REFERENCES ESTADO_PEDIDO (id);
ALTER TABLE USUARIO ADD CONSTRAINT FKUSUARIO533117 FOREIGN KEY (TIPO_USUARIOid) REFERENCES TIPO_USUARIO (id);
ALTER TABLE CARACTERISTICA_PRODUCTO ADD CONSTRAINT FKCARACTERIS944109 FOREIGN KEY (CARACTERISTICAid) REFERENCES CARACTERISTICA (id);
ALTER TABLE CARACTERISTICA_PRODUCTO ADD CONSTRAINT FKCARACTERIS256942 FOREIGN KEY (PRODUCTOid) REFERENCES PRODUCTO (id);
ALTER TABLE CARACTERISTICA_SUBCATEGORIA ADD CONSTRAINT FKCARACTERIS872968 FOREIGN KEY (CARACTERISTICAid) REFERENCES CARACTERISTICA (id);
ALTER TABLE CARACTERISTICA_SUBCATEGORIA ADD CONSTRAINT FKCARACTERIS460748 FOREIGN KEY (SUBCATEGORIAid) REFERENCES SUBCATEGORIA (id);
ALTER TABLE CONTENIDO_INFO ADD CONSTRAINT FKCONTENIDO_553733 FOREIGN KEY (TIPO_CONTENIDO_INFOid) REFERENCES TIPO_CONTENIDO_INFO (id);


