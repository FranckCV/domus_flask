create table marca (
  id             int(10) not null auto_increment, 
  marca          varchar(45) not null, 
  img_logo       longblob not null, 
  img_banner     longblob, 
  fecha_registro timestamp not null default current_timestamp(), 
  disponibilidad tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table producto (
  id             int(10) not null auto_increment, 
  nombre         varchar(150) not null, 
  price_regular  numeric(9, 2), 
  precio_online  numeric(9, 2) not null, 
  precio_oferta  numeric(9, 2), 
  info_adicional text,
  stock          int(11) not null, 
  fecha_registro timestamp not null default current_timestamp(), 
  disponibilidad tinyint(1) not null, 
  marcaid        int(10) not null, 
  subcategoriaid int(10) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table subcategoria (
  id             int(10) not null auto_increment, 
  subcategoria   varchar(50) not null, 
  faicon_subcat  varchar(50) not null, 
  disponibilidad tinyint(1) not null, 
  categoriaid    int(10) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table categoria (
  id             int(10) not null auto_increment, 
  categoria      varchar(50) not null, 
  faicon_cat     varchar(50) not null, 
  disponibilidad tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table pedido (
  id              int(10) not null auto_increment, 
  fecha_compra    date,
  subtotal        numeric(9, 2), 
  metodo_pagoid   int(11), 
  usuarioid       int(10) not null, 
  estado_pedidoid int(11) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table usuario (
  id               int(10) not null auto_increment, 
  nombres          varchar(50) not null, 
  apellidos        varchar(50) not null, 
  doc_identidad    varchar(15) not null, 
  img_usuario      longblob, 
  genero           tinyint(1) not null, 
  fecha_nacimiento date not null, 
  telefono         varchar(15) not null, 
  correo           varchar(60) not null unique, 
  contrasenia       varchar(100) not null, 
  disponibilidad   tinyint(1) not null,
  fecha_registro timestamp not null default current_timestamp(), 
  tipo_usuarioid   int(11) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table img_producto (
  id           int(10) not null auto_increment, 
  img_nombre   varchar(100), 
  imagen       longblob not null, 
  imgprincipal tinyint(1) not null, 
  productoid   int(10) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table detalles_pedido (
  productoid int(10) not null, 
  pedidoid   int(10) not null, 
  cantidad   int(2) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (productoid, 
  pedidoid));

create table lista_deseos (
  productoid int(10) not null, 
  usuarioid  int(10) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (productoid, 
  usuarioid));

create table comentario (
  id                  int(11) not null auto_increment, 
  nombres             varchar(50) not null, 
  apellidos           varchar(50) not null, 
  email               varchar(70) not null, 
  celular             varchar(80) not null, 
  mensaje             text not null, 
  fecha_registro timestamp not null default current_timestamp(),  
  estado              tinyint(1) not null, 
  motivo_comentarioid int(11) not null, 
  usuarioid           int(10),
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table motivo_comentario (
  id             int(11) not null auto_increment, 
  motivo         varchar(50) not null, 
  disponibilidad tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table tipo_novedad (
  id      int(10) not null auto_increment, 
  nomtipo varchar(55) not null,  
  disponibilidad tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table novedad (
  id                int(10) not null auto_increment, 
  nombre            varchar(55) not null, 
  titulo            varchar(55) not null, 
  fecha_inicio      date not null, 
  fecha_vencimiento date not null, 
  terminos          text not null, 
  fecha_registro timestamp not null default current_timestamp(),  
  disponibilidad    tinyint(1) not null, 
  marcaid           int(10), 
  subcategoriaid    int(10), 
  tipo_novedadid    int(10) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table caracteristica_producto (
  caracteristicaid int(11) not null, 
  productoid       int(10) not null, 
  valor            varchar(50) not null, 
  principal        tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (caracteristicaid, 
  productoid));

create table metodo_pago (
  id             int(11) not null auto_increment, 
  metodo         varchar(50) not null, 
  disponibilidad tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table tipo_img_novedad (
  id             int(11) not null auto_increment, 
  tipo           varchar(50) not null, 
  disponibilidad tinyint(1) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table img_novedad (
  id                 int(11) not null auto_increment, 
  nomimagen          varchar(100), 
  imagen             longblob not null, 
  tipo_img_novedadid int(11) not null, 
  novedadid          int(10) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table estado_pedido (
  id        int(11) not null auto_increment, 
  nomestado varchar(55) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table tipo_usuario (
  id          int(11) not null auto_increment, 
  tipo        varchar(55) not null,
  imagen      longblob not null,
  descripcion varchar(300) not null,
  disponibilidad tinyint(1) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table caracteristica (
  id             int(11) not null auto_increment, 
  campo          varchar(100) not null, 
  disponibilidad tinyint(1) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table caracteristica_subcategoria (
  caracteristicaid int(11) not null, 
  subcategoriaid   int(10) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (caracteristicaid, 
  subcategoriaid));

create table redes_sociales (
  id         int(11) not null auto_increment, 
  nomred     varchar(150) not null, 
  faicon_red varchar(30) not null, 
  enlace     varchar(200) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

create table informacion_domus (
  id          int(11) not null auto_increment, 
  correo      varchar(200) not null, 
  numero      varchar(20) not null, 
  imglogo     longblob not null, 
  imgicon     longblob not null, 
  descripcion text not null, 
  historia    text not null, 
  vision      text not null, 
  valores     text not null, 
  mision      text not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));
create table tipo_contenido_info (
  id          int(11) not null auto_increment, 
  nombre      varchar(255) not null, 
  descripcion text not null, 
  faicon_cont varchar(50) not null,
  disponibilidad tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));
create table contenido_info (
  id                    int(11) not null auto_increment, 
  titulo                text not null, 
  cuerpo                text not null, 
  tipo_contenido_infoid int(11) not null, 
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));
create table cupon (
  id                int(11) not null auto_increment, 
  codigo            varchar(30) not null, 
  fecha_inicio      date not null, 
  fecha_vencimiento date not null, 
  cant_descuento    numeric(6, 2) not null,
  fecha_registro timestamp not null default current_timestamp(),  
  disponibilidad tinyint(1) not null,
  registro_auditoria timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  primary key (id));

alter table producto add constraint fkproducto990798 foreign key (marcaid) references marca (id);
alter table producto add constraint fkproducto953045 foreign key (subcategoriaid) references subcategoria (id);
alter table subcategoria add constraint fksubcategor822804 foreign key (categoriaid) references categoria (id);
alter table pedido add constraint fkpedido787527 foreign key (metodo_pagoid) references metodo_pago (id);
alter table pedido add constraint fkpedido832373 foreign key (usuarioid) references usuario (id);
alter table img_producto add constraint fkimg_produc616199 foreign key (productoid) references producto (id);
alter table detalles_pedido add constraint fkdetalles_p873247 foreign key (productoid) references producto (id);
alter table detalles_pedido add constraint fkdetalles_p720300 foreign key (pedidoid) references pedido (id);
alter table lista_deseos add constraint fklista_dese59890 foreign key (productoid) references producto (id);
alter table lista_deseos add constraint fklista_dese907029 foreign key (usuarioid) references usuario (id);
alter table comentario add constraint fkcomentario473576 foreign key (motivo_comentarioid) references motivo_comentario (id);
alter table comentario add constraint fkcomentario180941 foreign key (usuarioid) references usuario (id);
alter table novedad add constraint fknovedad215901 foreign key (marcaid) references marca (id);
alter table novedad add constraint fknovedad821851 foreign key (subcategoriaid) references subcategoria (id);
alter table novedad add constraint fknovedad812313 foreign key (tipo_novedadid) references tipo_novedad (id);
alter table img_novedad add constraint fkimg_noveda411983 foreign key (tipo_img_novedadid) references tipo_img_novedad (id);
alter table img_novedad add constraint fkimg_noveda721180 foreign key (novedadid) references novedad (id);
alter table pedido add constraint fkpedido259150 foreign key (estado_pedidoid) references estado_pedido (id);
alter table usuario add constraint fkusuario533117 foreign key (tipo_usuarioid) references tipo_usuario (id);
alter table caracteristica_producto add constraint fkcaracteris944109 foreign key (caracteristicaid) references caracteristica (id);
alter table caracteristica_producto add constraint fkcaracteris256942 foreign key (productoid) references producto (id);
alter table caracteristica_subcategoria add constraint fkcaracteris872968 foreign key (caracteristicaid) references caracteristica (id);
alter table caracteristica_subcategoria add constraint fkcaracteris460748 foreign key (subcategoriaid) references subcategoria (id);
alter table contenido_info add constraint fkcontenido_553733 foreign key (tipo_contenido_infoid) references tipo_contenido_info (id);


