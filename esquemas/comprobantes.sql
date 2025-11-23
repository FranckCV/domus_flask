-- Agregar a tu base de datos
CREATE TABLE `comprobante` (
  `pedidoid` INT(11) NOT NULL PRIMARY KEY,
  `tipo_comprobante` ENUM('boleta', 'factura') NOT NULL,
  `numero_comprobante` VARCHAR(20) NOT NULL UNIQUE,
  `doc_identidad_cliente` VARCHAR(15) NOT NULL,
  `nombre_cliente` VARCHAR(150) NOT NULL,
  `razon_social` VARCHAR(200) DEFAULT NULL,
  `ruc` VARCHAR(11) DEFAULT NULL,
  `direccion_cliente` VARCHAR(200) DEFAULT NULL,
  `fecha_emision` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `subtotal` DECIMAL(9,2) NOT NULL,
  `igv` DECIMAL(9,2) NOT NULL,
  `total` DECIMAL(9,2) NOT NULL,
  `ruta_archivo` VARCHAR(300) NOT NULL,
  `registro_auditoria` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  FOREIGN KEY (`pedidoid`) REFERENCES `pedido` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- Tabla para secuencia de numeración
CREATE TABLE `secuencia_comprobante` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `tipo` ENUM('boleta', 'factura') NOT NULL,
  `serie` VARCHAR(4) NOT NULL,
  `ultimo_numero` INT(11) NOT NULL DEFAULT 0,
  `registro_auditoria` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  UNIQUE KEY `tipo_serie` (`tipo`, `serie`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- Insertar series iniciales
INSERT INTO `secuencia_comprobante` (`tipo`, `serie`, `ultimo_numero`) VALUES
('boleta', 'B001', 0),
('factura', 'F001', 0);