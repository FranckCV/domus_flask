CREATE TABLE `caracteristica` (
  `id` int NOT NULL AUTO_INCREMENT,
  `campo` varchar(100) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `caracteristica_producto` (
  `caracteristicaid` int NOT NULL,
  `productoid` int NOT NULL,
  `valor` varchar(50) NOT NULL,
  `principal` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`caracteristicaid`,`productoid`),
  KEY `fkcaracteris256942` (`productoid`),
  CONSTRAINT `fkcaracteris256942` FOREIGN KEY (`productoid`) REFERENCES `producto` (`id`),
  CONSTRAINT `fkcaracteris944109` FOREIGN KEY (`caracteristicaid`) REFERENCES `caracteristica` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `caracteristica_subcategoria` (
  `caracteristicaid` int NOT NULL,
  `subcategoriaid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`caracteristicaid`,`subcategoriaid`),
  KEY `fkcaracteris460748` (`subcategoriaid`),
  CONSTRAINT `fkcaracteris460748` FOREIGN KEY (`subcategoriaid`) REFERENCES `subcategoria` (`id`),
  CONSTRAINT `fkcaracteris872968` FOREIGN KEY (`caracteristicaid`) REFERENCES `caracteristica` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `categoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categoria` varchar(50) NOT NULL,
  `faicon_cat` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `comentario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `email` varchar(70) NOT NULL,
  `celular` varchar(80) NOT NULL,
  `mensaje` text NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint(1) NOT NULL,
  `motivo_comentarioid` int NOT NULL,
  `usuarioid` int DEFAULT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkcomentario473576` (`motivo_comentarioid`),
  KEY `fkcomentario180941` (`usuarioid`),
  CONSTRAINT `fkcomentario180941` FOREIGN KEY (`usuarioid`) REFERENCES `usuario` (`id`),
  CONSTRAINT `fkcomentario473576` FOREIGN KEY (`motivo_comentarioid`) REFERENCES `motivo_comentario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `contenido_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` text NOT NULL,
  `cuerpo` text NOT NULL,
  `tipo_contenido_infoid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkcontenido_553733` (`tipo_contenido_infoid`),
  CONSTRAINT `fkcontenido_553733` FOREIGN KEY (`tipo_contenido_infoid`) REFERENCES `tipo_contenido_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `cupon` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(30) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `cant_descuento` decimal(6,2) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `detalles_pedido` (
  `productoid` int NOT NULL,
  `pedidoid` int NOT NULL,
  `cantidad` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`productoid`,`pedidoid`),
  KEY `fkdetalles_p720300` (`pedidoid`),
  CONSTRAINT `fkdetalles_p720300` FOREIGN KEY (`pedidoid`) REFERENCES `pedido` (`id`),
  CONSTRAINT `fkdetalles_p873247` FOREIGN KEY (`productoid`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `estado_pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomestado` varchar(55) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `img_novedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomimagen` varchar(100) DEFAULT NULL,
  `imagen` longblob NOT NULL,
  `tipo_img_novedadid` int NOT NULL,
  `novedadid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkimg_noveda411983` (`tipo_img_novedadid`),
  KEY `fkimg_noveda721180` (`novedadid`),
  CONSTRAINT `fkimg_noveda411983` FOREIGN KEY (`tipo_img_novedadid`) REFERENCES `tipo_img_novedad` (`id`),
  CONSTRAINT `fkimg_noveda721180` FOREIGN KEY (`novedadid`) REFERENCES `novedad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `img_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img_nombre` varchar(100) DEFAULT NULL,
  `imagen` longblob NOT NULL,
  `imgprincipal` tinyint(1) NOT NULL,
  `productoid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkimg_produc616199` (`productoid`),
  CONSTRAINT `fkimg_produc616199` FOREIGN KEY (`productoid`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `informacion_domus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `correo` varchar(200) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `imglogo` longblob NOT NULL,
  `imgicon` longblob NOT NULL,
  `descripcion` text NOT NULL,
  `historia` text NOT NULL,
  `vision` text NOT NULL,
  `valores` text NOT NULL,
  `mision` text NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `lista_deseos` (
  `productoid` int NOT NULL,
  `usuarioid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`productoid`,`usuarioid`),
  KEY `fklista_dese907029` (`usuarioid`),
  CONSTRAINT `fklista_dese59890` FOREIGN KEY (`productoid`) REFERENCES `producto` (`id`),
  CONSTRAINT `fklista_dese907029` FOREIGN KEY (`usuarioid`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `marca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `marca` varchar(45) NOT NULL,
  `img_logo` longblob NOT NULL,
  `img_banner` longblob,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `metodo_pago` (
  `id` int NOT NULL AUTO_INCREMENT,
  `metodo` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `motivo_comentario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `motivo` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `novedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(55) NOT NULL,
  `titulo` varchar(55) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `terminos` text NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `disponibilidad` tinyint(1) NOT NULL,
  `marcaid` int DEFAULT NULL,
  `subcategoriaid` int DEFAULT NULL,
  `tipo_novedadid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fknovedad215901` (`marcaid`),
  KEY `fknovedad821851` (`subcategoriaid`),
  KEY `fknovedad812313` (`tipo_novedadid`),
  CONSTRAINT `fknovedad215901` FOREIGN KEY (`marcaid`) REFERENCES `marca` (`id`),
  CONSTRAINT `fknovedad812313` FOREIGN KEY (`tipo_novedadid`) REFERENCES `tipo_novedad` (`id`),
  CONSTRAINT `fknovedad821851` FOREIGN KEY (`subcategoriaid`) REFERENCES `subcategoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;




CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_compra` date DEFAULT NULL,
  `subtotal` decimal(9,2) DEFAULT NULL,
  `metodo_pagoid` int DEFAULT NULL,
  `usuarioid` int NOT NULL,
  `estado_pedidoid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkpedido787527` (`metodo_pagoid`),
  KEY `fkpedido832373` (`usuarioid`),
  KEY `fkpedido259150` (`estado_pedidoid`),
  CONSTRAINT `fkpedido259150` FOREIGN KEY (`estado_pedidoid`) REFERENCES `estado_pedido` (`id`),
  CONSTRAINT `fkpedido787527` FOREIGN KEY (`metodo_pagoid`) REFERENCES `metodo_pago` (`id`),
  CONSTRAINT `fkpedido832373` FOREIGN KEY (`usuarioid`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `price_regular` decimal(9,2) DEFAULT NULL,
  `precio_online` decimal(9,2) NOT NULL,
  `precio_oferta` decimal(9,2) DEFAULT NULL,
  `info_adicional` text,
  `stock` int NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `disponibilidad` tinyint(1) NOT NULL,
  `marcaid` int NOT NULL,
  `subcategoriaid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkproducto990798` (`marcaid`),
  KEY `fkproducto953045` (`subcategoriaid`),
  CONSTRAINT `fkproducto953045` FOREIGN KEY (`subcategoriaid`) REFERENCES `subcategoria` (`id`),
  CONSTRAINT `fkproducto990798` FOREIGN KEY (`marcaid`) REFERENCES `marca` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `redes_sociales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomred` varchar(150) NOT NULL,
  `faicon_red` varchar(30) NOT NULL,
  `enlace` varchar(200) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `subcategoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subcategoria` varchar(50) NOT NULL,
  `faicon_subcat` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `categoriaid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fksubcategor822804` (`categoriaid`),
  CONSTRAINT `fksubcategor822804` FOREIGN KEY (`categoriaid`) REFERENCES `categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `tipo_contenido_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `faicon_cont` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `tipo_img_novedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `tipo_novedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomtipo` varchar(55) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `tipo_usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(55) NOT NULL,
  `imagen` longblob NOT NULL,
  `descripcion` varchar(300) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;


CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `doc_identidad` varchar(15) NOT NULL,
  `img_usuario` longblob,
  `genero` tinyint(1) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `correo` varchar(60) NOT NULL,
  `contrasenia` varchar(100) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo_usuarioid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  KEY `fkusuario533117` (`tipo_usuarioid`),
  CONSTRAINT `fkusuario533117` FOREIGN KEY (`tipo_usuarioid`) REFERENCES `tipo_usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb3;
