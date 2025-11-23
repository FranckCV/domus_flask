-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: DomusMarket.mysql.pythonanywhere-services.com    Database: DomusMarket$domus_market
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bitacora`
--

DROP TABLE IF EXISTS `bitacora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bitacora` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuarioid` int NOT NULL,
  `fecha_hora_inicio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuarioid`),
  CONSTRAINT `bitacora_ibfk_1` FOREIGN KEY (`usuarioid`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacora`
--

LOCK TABLES `bitacora` WRITE;
/*!40000 ALTER TABLE `bitacora` DISABLE KEYS */;
INSERT INTO `bitacora` VALUES (1,3,'2025-10-25 16:51:59'),(2,3,'2025-10-25 17:46:15'),(3,32,'2025-10-25 17:48:28'),(4,32,'2025-10-25 17:53:44'),(5,3,'2025-10-30 02:49:13'),(6,3,'2025-10-30 03:14:58'),(7,3,'2025-10-30 03:21:56'),(8,3,'2025-10-30 03:55:51'),(9,3,'2025-10-30 04:11:12'),(10,3,'2025-10-30 04:11:35'),(11,3,'2025-10-30 04:16:30'),(12,3,'2025-10-30 04:27:41'),(13,3,'2025-10-30 04:32:56'),(14,3,'2025-10-30 04:39:53'),(15,3,'2025-10-30 04:44:50'),(16,3,'2025-10-30 04:45:29'),(17,3,'2025-10-30 12:37:29'),(18,3,'2025-10-30 12:51:28'),(19,3,'2025-10-30 12:55:34'),(20,3,'2025-10-30 12:58:54'),(21,3,'2025-10-30 13:13:48');
/*!40000 ALTER TABLE `bitacora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caracteristica`
--

DROP TABLE IF EXISTS `caracteristica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `caracteristica` (
  `id` int NOT NULL AUTO_INCREMENT,
  `campo` varchar(100) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caracteristica`
--

LOCK TABLES `caracteristica` WRITE;
/*!40000 ALTER TABLE `caracteristica` DISABLE KEYS */;
INSERT INTO `caracteristica` VALUES (1,'Carga rápida',1,'2024-12-06 22:59:17'),(2,'Cámara Frontal',1,'2024-12-06 22:59:17'),(3,'Color',1,'2024-12-06 22:59:17'),(4,'Entrada carga',1,'2024-12-06 22:59:17'),(5,'Pantalla',1,'2024-12-06 22:59:17'),(6,'RAM',1,'2024-12-06 22:59:17'),(7,'Almacenamiento',1,'2024-12-06 22:59:17'),(8,'Cámara posterior',1,'2024-12-06 22:59:17'),(9,'Procesador',1,'2024-12-06 22:59:17'),(10,'Modelo',1,'2024-12-06 22:59:17'),(11,'Batería',1,'2024-12-06 22:59:17'),(12,'Sistema operativo',1,'2024-12-06 22:59:17'),(13,'Resolución de pantalla',1,'2024-12-06 22:59:17'),(14,'Tamaño de pantalla',1,'2024-12-06 22:59:17'),(15,'Capacidad de la batería',1,'2024-12-06 22:59:17'),(16,'Tipo de red',1,'2024-12-06 22:59:17'),(17,'Capacidad de carga rápida',1,'2024-12-06 22:59:17'),(18,'Sensor de huellas dactilares',1,'2024-12-06 22:59:17'),(19,'Protección contra agua/polvo',1,'2024-12-06 22:59:17'),(20,'Resolución de pantalla',1,'2024-12-06 22:59:17'),(21,'Tamaño de pantalla',1,'2024-12-06 22:59:17'),(22,'Almacenamiento interno',1,'2024-12-06 22:59:17'),(23,'Memoria RAM',1,'2024-12-06 22:59:17'),(24,'Conectividad',1,'2024-12-06 22:59:17'),(25,'Duración de la batería',1,'2024-12-06 22:59:17'),(26,'Soporte para lápiz óptico',1,'2024-12-06 22:59:17'),(27,'Sistema operativo',1,'2024-12-06 22:59:17'),(28,'Tipo de conectividad',1,'2024-12-06 22:59:17'),(29,'Duración de la batería',1,'2024-12-06 22:59:17'),(30,'Cancelación de ruido',1,'2024-12-06 22:59:17'),(31,'Compatibilidad con asistentes de voz',1,'2024-12-06 22:59:17'),(32,'Rango de frecuencia',1,'2024-12-06 22:59:17'),(33,'Potencia de salida',1,'2024-12-06 22:59:17'),(34,'Impermeabilidad',1,'2024-12-06 22:59:17'),(35,'Resolución de pantalla',1,'2024-12-06 22:59:17'),(36,'Tipo de teclado',1,'2024-12-06 22:59:17'),(37,'DPI',1,'2024-12-06 22:59:17'),(38,'Capacidad de respuesta',1,'2024-12-06 22:59:17'),(39,'Compatibilidad con consolas/PC',1,'2024-12-06 22:59:17'),(40,'Tipo de conexión',1,'2024-12-06 22:59:17'),(41,'Tipo de procesador',1,'2024-12-06 22:59:17'),(42,'Procesador',1,'2024-12-06 22:59:17'),(43,'Memoria RAM',1,'2024-12-06 22:59:17'),(44,'Disco duro',1,'2024-12-06 22:59:17'),(45,'Tarjeta gráfica',1,'2024-12-06 22:59:17'),(46,'Sistema operativo',1,'2024-12-06 22:59:17'),(47,'Tamaño de pantalla',1,'2024-12-06 22:59:17'),(48,'Resolución de pantalla',1,'2024-12-06 22:59:17'),(49,'Conectividad',1,'2024-12-06 22:59:17'),(50,'Resolución de cámara',1,'2024-12-06 22:59:17'),(51,'Tipo de lente',1,'2024-12-06 22:59:17'),(52,'Tamaño del sensor',1,'2024-12-06 22:59:17'),(53,'Capacidad de grabación en 4K',1,'2024-12-06 22:59:17'),(54,'Tipo de batería',1,'2024-12-06 22:59:17'),(55,'Almacenamiento compatible',1,'2024-12-06 22:59:17'),(56,'Modo manual/automático',1,'2024-12-06 22:59:17'),(57,'Tamaño de pantalla',1,'2024-12-06 22:59:17'),(58,'Resolución',1,'2024-12-06 22:59:17'),(59,'Tipo de panel',1,'2024-12-06 22:59:17'),(60,'Tasa de refresco',1,'2024-12-06 22:59:17'),(61,'Soporte para HDR',1,'2024-12-06 22:59:17'),(62,'Conectividad (HDMI, USB)',1,'2024-12-06 22:59:17'),(63,'Sistemas de sonido integrados',1,'2024-12-06 22:59:17'),(64,'Sistema operativo',1,'2024-12-06 22:59:17'),(65,'Tipo de conexión',1,'2024-12-06 22:59:17'),(66,'Compatibilidad (USB, Bluetooth)',1,'2024-12-06 22:59:17'),(67,'Autonomía de la batería',1,'2024-12-06 22:59:17'),(68,'Tamaño o dimensiones',1,'2024-12-06 22:59:17'),(69,'Material de fabricación',1,'2024-12-06 22:59:17'),(70,'Funciones adicionales (RGB, teclas programables)',1,'2024-12-06 22:59:17');
/*!40000 ALTER TABLE `caracteristica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caracteristica_producto`
--

DROP TABLE IF EXISTS `caracteristica_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caracteristica_producto`
--

LOCK TABLES `caracteristica_producto` WRITE;
/*!40000 ALTER TABLE `caracteristica_producto` DISABLE KEYS */;
INSERT INTO `caracteristica_producto` VALUES (1,1,'25W',1,'2024-12-06 23:25:41'),(7,1,'128GB',0,'2024-12-06 23:25:41'),(12,1,'Android',0,'2024-12-06 23:25:41');
/*!40000 ALTER TABLE `caracteristica_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caracteristica_subcategoria`
--

DROP TABLE IF EXISTS `caracteristica_subcategoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `caracteristica_subcategoria` (
  `caracteristicaid` int NOT NULL,
  `subcategoriaid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`caracteristicaid`,`subcategoriaid`),
  KEY `fkcaracteris460748` (`subcategoriaid`),
  CONSTRAINT `fkcaracteris460748` FOREIGN KEY (`subcategoriaid`) REFERENCES `subcategoria` (`id`),
  CONSTRAINT `fkcaracteris872968` FOREIGN KEY (`caracteristicaid`) REFERENCES `caracteristica` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caracteristica_subcategoria`
--

LOCK TABLES `caracteristica_subcategoria` WRITE;
/*!40000 ALTER TABLE `caracteristica_subcategoria` DISABLE KEYS */;
INSERT INTO `caracteristica_subcategoria` VALUES (1,1,'2024-12-06 23:25:41'),(2,1,'2024-12-06 23:25:41'),(3,1,'2024-12-06 23:25:41'),(4,1,'2024-12-06 23:25:41'),(5,1,'2024-12-06 23:25:41'),(6,1,'2024-12-06 23:25:41'),(7,1,'2024-12-06 23:25:41'),(8,1,'2024-12-06 23:25:41'),(9,1,'2024-12-06 23:25:41'),(10,1,'2024-12-06 23:25:41'),(11,1,'2024-12-06 23:25:41'),(12,1,'2024-12-06 23:25:41'),(13,1,'2024-12-06 23:25:41'),(14,1,'2024-12-06 23:25:41'),(15,1,'2024-12-06 23:25:41'),(16,1,'2024-12-06 23:25:41'),(17,1,'2024-12-06 23:25:41'),(18,1,'2024-12-06 23:25:41'),(19,1,'2024-12-06 23:25:41'),(20,1,'2024-12-06 23:25:41'),(21,1,'2024-12-06 23:25:41'),(22,1,'2024-12-06 23:25:41'),(23,1,'2024-12-06 23:25:41'),(24,1,'2024-12-06 23:25:41'),(25,1,'2024-12-06 23:25:41'),(26,1,'2024-12-06 23:25:41'),(27,1,'2024-12-06 23:25:41'),(28,1,'2024-12-06 23:25:41'),(29,1,'2024-12-06 23:25:41'),(30,1,'2024-12-06 23:25:41'),(31,1,'2024-12-06 23:25:41'),(32,1,'2024-12-06 23:25:41'),(33,1,'2024-12-06 23:25:41'),(34,1,'2024-12-06 23:25:41'),(35,1,'2024-12-06 23:25:41'),(36,1,'2024-12-06 23:25:41'),(37,1,'2024-12-06 23:25:41'),(38,1,'2024-12-06 23:25:41'),(39,1,'2024-12-06 23:25:41'),(40,1,'2024-12-06 23:25:41'),(41,1,'2024-12-06 23:25:41'),(42,1,'2024-12-06 23:25:41'),(43,1,'2024-12-06 23:25:41'),(44,1,'2024-12-06 23:25:41'),(45,1,'2024-12-06 23:25:41'),(46,1,'2024-12-06 23:25:41'),(47,1,'2024-12-06 23:25:41'),(48,1,'2024-12-06 23:25:41'),(49,1,'2024-12-06 23:25:41'),(50,1,'2024-12-06 23:25:41'),(51,1,'2024-12-06 23:25:41'),(52,1,'2024-12-06 23:25:41'),(53,1,'2024-12-06 23:25:41'),(54,1,'2024-12-06 23:25:41'),(55,1,'2024-12-06 23:25:41'),(56,1,'2024-12-06 23:25:41'),(57,1,'2024-12-06 23:25:41'),(58,1,'2024-12-06 23:25:41'),(59,1,'2024-12-06 23:25:41'),(60,1,'2024-12-06 23:25:41'),(61,1,'2024-12-06 23:25:41'),(62,1,'2024-12-06 23:25:41'),(63,1,'2024-12-06 23:25:41'),(64,1,'2024-12-06 23:25:41'),(65,1,'2024-12-06 23:25:41'),(66,1,'2024-12-06 23:25:41'),(67,1,'2024-12-06 23:25:41'),(68,1,'2024-12-06 23:25:41'),(69,1,'2024-12-06 23:25:41'),(70,1,'2024-12-06 23:25:41');
/*!40000 ALTER TABLE `caracteristica_subcategoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `faicon_cat` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Alimentos','fa-solid fa-drumstick-bite',1,'2024-12-06 22:59:06'),(2,'Deportes','fa-solid fa-person-running',1,'2024-12-06 22:59:06'),(3,'Hogar','fa-solid fa-house-chimney',1,'2024-12-06 22:59:06'),(4,'Libreria y Oficina','fa-solid fa-book',1,'2024-12-06 22:59:06'),(5,'Mascotas','fa-solid fa-paw',1,'2024-12-06 22:59:06'),(6,'Ropa y Calzado','fa-solid fa-shirt',1,'2024-12-06 22:59:06'),(7,'Tecnologia','fa-solid fa-microchip',1,'2024-12-06 22:59:06');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comentario`
--

DROP TABLE IF EXISTS `comentario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  KEY `fkcomentario180941` (`usuarioid`),
  KEY `fkcomentario473576` (`motivo_comentarioid`),
  CONSTRAINT `fkcomentario180941` FOREIGN KEY (`usuarioid`) REFERENCES `usuario` (`id`),
  CONSTRAINT `fkcomentario473576` FOREIGN KEY (`motivo_comentarioid`) REFERENCES `motivo_comentario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comentario`
--

LOCK TABLES `comentario` WRITE;
/*!40000 ALTER TABLE `comentario` DISABLE KEYS */;
INSERT INTO `comentario` VALUES (1,'Junior','yopsquienmas','yuliver_max@hotmail.com','946666666','VENGO A RECLAMAR MIS DERECHOS COMO CONSUMIDOR','2024-12-07 03:30:07',0,1,NULL,'2024-12-07 03:30:07');
/*!40000 ALTER TABLE `comentario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comprobante`
--

DROP TABLE IF EXISTS `comprobante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comprobante` (
  `pedidoid` int NOT NULL,
  `tipo_comprobante` enum('boleta','factura') NOT NULL,
  `numero_comprobante` varchar(20) NOT NULL,
  `doc_identidad_cliente` varchar(15) NOT NULL,
  `nombre_cliente` varchar(150) NOT NULL,
  `razon_social` varchar(200) DEFAULT NULL,
  `ruc` varchar(11) DEFAULT NULL,
  `direccion_cliente` varchar(200) DEFAULT NULL,
  `fecha_emision` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `subtotal` decimal(9,2) NOT NULL,
  `igv` decimal(9,2) NOT NULL,
  `total` decimal(9,2) NOT NULL,
  `ruta_archivo` varchar(300) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pedidoid`),
  UNIQUE KEY `numero_comprobante` (`numero_comprobante`),
  CONSTRAINT `comprobante_ibfk_1` FOREIGN KEY (`pedidoid`) REFERENCES `pedido` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comprobante`
--

LOCK TABLES `comprobante` WRITE;
/*!40000 ALTER TABLE `comprobante` DISABLE KEYS */;
INSERT INTO `comprobante` VALUES (16,'boleta','B001-00000001','12345678','Juan Pérez García',NULL,NULL,NULL,'2025-11-22 17:11:41',20.00,3.60,23.60,'boleta_16_20251122_171141.pdf','2025-11-22 17:11:41'),(21,'boleta','B001-00000002','12345678','Juan Pérez García',NULL,NULL,NULL,'2025-11-22 17:15:30',11.50,2.07,13.57,'boleta_21_20251122_171530.pdf','2025-11-22 17:15:30'),(27,'boleta','B001-00000003','12345678','Juan Pérez García',NULL,NULL,NULL,'2025-11-22 17:32:52',599.94,107.99,707.93,'boleta_27_20251122_173252.pdf','2025-11-22 17:32:52');
/*!40000 ALTER TABLE `comprobante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contenido_info`
--

DROP TABLE IF EXISTS `contenido_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contenido_info`
--

LOCK TABLES `contenido_info` WRITE;
/*!40000 ALTER TABLE `contenido_info` DISABLE KEYS */;
INSERT INTO `contenido_info` VALUES (1,'Generalidades','Estos términos y condiciones regulan el uso del sitio web de Domus Market y la compra de productos a través del mismo.\r\n\r\n',1,'2024-12-06 22:59:17'),(2,'Registro','Para realizar compras, debes registrarte proporcionando información veraz y actualizada. Es tu responsabilidad mantener la confidencialidad de tu cuenta.\r\n\r\n',1,'2024-12-06 22:59:17'),(3,'Pedidos','Todos los pedidos están sujetos a disponibilidad de stock. Nos reservamos el derecho de cancelar o rechazar un pedido por cualquier motivo.\r\n\r\n',1,'2024-12-06 22:59:17'),(4,'Precios y Pagos\r\n','Los precios están sujetos a cambios sin previo aviso. Aceptamos varios métodos de pago, incluyendo tarjetas de crédito y débito.\r\n\r\n',1,'2024-12-06 22:59:17'),(5,'Envíos y Entregas','Ofrecemos envíos a nivel nacional. Los tiempos de entrega pueden variar según la ubicación y disponibilidad del producto.',1,'2024-12-06 22:59:17'),(6,'Devoluciones y Cambios','Consulta nuestra política de devoluciones para más detalles sobre cómo devolver o cambiar un producto.',1,'2024-12-06 22:59:17'),(7,'Privacidad','Nos comprometemos a proteger tu privacidad. Consulta nuestra política de privacidad para más información.',1,'2024-12-06 22:59:17'),(8,'Modificaciones','Nos reservamos el derecho de modificar estos términos en cualquier momento. Los cambios serán efectivos una vez publicados en nuestro sitio web.',1,'2024-12-06 22:59:17'),(9,'Lima','Dirección: Av. Javier Prado 1234, San Isidro\r\n\r\nTeléfono: 01 2345678\r\n\r\nHorario: Lun-Sab 9:00am - 9:00pm, Dom 10:00am - 6:00pm',2,'2024-12-06 22:59:17'),(10,'Arequipa','Dirección: Av. Ejército 567, Cayma\r\n\r\nTeléfono: 054 234567\r\n\r\nHorario: Lun-Sab 9:00am - 8:00pm, Dom 10:00am - 5:00pm',2,'2024-12-06 22:59:17'),(11,'Trujillo','Dirección: Av. España 890, Trujillo\r\n\r\nTeléfono: 044 234567\r\n\r\nHorario: Lun-Sab 9:00am - 7:00pm, Dom 10:00am - 4:00pm',2,'2024-12-06 22:59:17'),(12,'¿Cómo puedo realizar una compra?\r\n','Para realizar una compra, simplemente navega por nuestro catálogo, añade los productos al carrito y sigue el proceso de pago. Asegúrate de estar registrado y haber iniciado sesión.',3,'2024-12-06 22:59:17'),(13,'¿Qué métodos de pago aceptan?','Aceptamos pagos con tarjetas de crédito y débito (Visa, MasterCard, American Express), así como pagos mediante transferencias bancarias y pagos contra entrega en algunas ubicaciones.',3,'2024-12-06 22:59:17'),(14,'¿Cuánto tiempo tarda en llegar mi pedido?','El tiempo de entrega varía según la ubicación. Generalmente, los pedidos se entregan entre 3 y 7 días hábiles. Durante promociones o eventos especiales, este tiempo puede extenderse.',3,'2024-12-06 22:59:17'),(15,'¿Puedo devolver un producto?','Sí, aceptamos devoluciones dentro de los 30 días posteriores a la compra. El producto debe estar en su estado original y con el empaque intacto. Consulta nuestra política de devoluciones para más detalles.',3,'2024-12-06 22:59:17'),(16,'¿Cómo puedo contactar al servicio al cliente?','Puedes contactarnos a través de nuestro formulario de contacto en la página web, enviándonos un correo electrónico a servicioalcliente@domus.pe o llamándonos al 074 606240.',3,'2024-12-06 22:59:17'),(17,'Devoluciones','Los productos pueden ser devueltos dentro de los 30 días posteriores a la compra. Deben estar en su estado original, sin signos de uso y en su empaque original.\r\n\r\n',4,'2024-12-06 22:59:17'),(18,'Cambios','Si necesitas cambiar un producto por otra talla, color o modelo, puedes hacerlo dentro de los 30 días posteriores a la compra. El producto debe estar en perfecto estado.',4,'2024-12-06 22:59:17'),(19,'Proceso de Devolución\r\n','Para iniciar una devolución, sigue estos pasos:\r\n\r\n- Contacta a nuestro servicio al cliente a través de servicioalcliente@domus.pe o al 074 606240.\r\n- Proporciona tu número de pedido y el motivo de la devolución.\r\n- Empaca el producto en su empaque original junto con todos los accesorios y etiquetas.\r\n- Envía el paquete a la dirección proporcionada por nuestro equipo de servicio al cliente.',4,'2024-12-06 22:59:17'),(20,'Reembolsos','Los reembolsos se procesarán una vez que hayamos recibido y revisado el producto devuelto. El reembolso se realizará a través del mismo método de pago utilizado en la compra original.\r\n\r\n',4,'2024-12-06 22:59:17'),(21,'Excepciones','Algunos productos, como los artículos personalizados o perecederos, no son elegibles para devoluciones o cambios. Consulta nuestra política completa para más detalles.\r\n\r\n',4,'2024-12-06 22:59:17'),(22,'Garantía Legal','Todos los productos cuentan con una garantía legal de 6 meses contra defectos de fabricación. Esta garantía cubre reparaciones y, en algunos casos, reemplazos del producto.\r\n\r\n\r\n',5,'2024-12-06 22:59:17'),(23,'Garantía del Fabricante','Adicionalmente, muchos de nuestros productos cuentan con una garantía del fabricante que puede variar entre 1 y 3 años. Consulta la documentación del producto para más detalles.',5,'2024-12-06 22:59:17'),(24,'Garantía Extendida','Ofrecemos la opción de adquirir garantías extendidas para ciertos productos. Estas garantías amplían la cobertura más allá del período estándar.\r\n\r\n',5,'2024-12-06 22:59:17'),(25,'Contacto Inicial','Contacta a nuestro servicio al cliente a través de servicioalcliente@domus.pe o al 074 606240 para reportar tu reclamo. Proporciona todos los detalles posibles, incluyendo tu número de pedido y una descripción del problema.\r\n\r\n',6,'2024-12-06 22:59:17'),(26,'Revisión del Reclamo','Nuestro equipo revisará tu reclamo y te proporcionará una respuesta dentro de los 5 días hábiles. En algunos casos, puede ser necesario solicitar información adicional o pruebas para procesar tu reclamo.',6,'2024-12-06 22:59:17'),(27,'Resolución','Una vez revisado, te ofreceremos una solución que puede incluir el reemplazo del producto, un reembolso, o cualquier otra medida correctiva que consideremos apropiada.\r\n\r\n',6,'2024-12-06 22:59:17');
/*!40000 ALTER TABLE `contenido_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cupon`
--

DROP TABLE IF EXISTS `cupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cupon`
--

LOCK TABLES `cupon` WRITE;
/*!40000 ALTER TABLE `cupon` DISABLE KEYS */;
INSERT INTO `cupon` VALUES (1,'DOMUSESMICASA50','2025-01-01','2024-11-28',20.00,'2024-11-05 05:00:00',1,'2024-12-06 22:58:50');
/*!40000 ALTER TABLE `cupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_pedido`
--

DROP TABLE IF EXISTS `detalles_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_pedido`
--

LOCK TABLES `detalles_pedido` WRITE;
/*!40000 ALTER TABLE `detalles_pedido` DISABLE KEYS */;
INSERT INTO `detalles_pedido` VALUES (1,20,1,'2024-12-07 03:36:16'),(1,24,1,'2025-11-15 09:21:27'),(1,41,2,'2025-11-17 19:21:56'),(1,52,1,'2025-11-22 06:34:24'),(2,26,5,'2025-11-15 07:09:32'),(2,41,1,'2025-11-17 19:21:56'),(5,16,2,'2024-12-07 02:13:03'),(5,20,1,'2024-12-07 05:44:05'),(5,41,1,'2025-11-17 19:21:56'),(5,44,1,'2025-11-20 14:24:33'),(5,45,3,'2025-11-20 14:56:42'),(5,55,1,'2025-11-22 15:27:35'),(6,20,3,'2024-12-07 05:43:23'),(6,21,1,'2024-12-07 03:53:36'),(6,23,1,'2024-12-07 04:53:54'),(6,42,2,'2025-11-20 06:17:40'),(6,46,2,'2025-11-20 16:03:16'),(6,47,2,'2025-11-21 02:29:25'),(6,49,5,'2025-11-22 00:26:02'),(6,54,2,'2025-11-22 15:23:04'),(7,20,3,'2024-12-07 03:21:38'),(7,23,1,'2024-12-07 04:53:55'),(7,43,2,'2025-11-20 12:36:29'),(7,44,3,'2025-11-20 14:24:49'),(7,46,3,'2025-11-20 16:02:42'),(7,47,4,'2025-11-21 02:29:27'),(7,54,1,'2025-11-22 15:23:11'),(8,20,1,'2024-12-07 03:52:15'),(8,23,1,'2024-12-07 04:53:56'),(8,28,1,'2025-11-15 16:00:38'),(8,42,1,'2025-11-20 06:17:30'),(8,45,1,'2025-11-20 14:56:56'),(9,18,2,'2024-12-07 02:32:43'),(9,19,3,'2024-12-07 03:17:08'),(9,26,1,'2025-11-15 07:09:32'),(9,28,2,'2025-11-15 15:49:17'),(9,32,2,'2025-11-15 16:58:37'),(9,34,1,'2025-11-15 17:08:43'),(9,36,1,'2025-11-15 17:10:35'),(9,43,4,'2025-11-20 12:37:14'),(9,47,1,'2025-11-21 05:44:02'),(9,48,1,'2025-11-21 22:49:57'),(9,49,2,'2025-11-22 00:23:08'),(9,55,2,'2025-11-22 15:27:38'),(11,26,7,'2025-11-15 07:09:32'),(11,39,2,'2025-11-15 17:20:01'),(12,20,1,'2024-12-07 05:43:55'),(12,28,1,'2025-11-15 16:00:36'),(12,55,1,'2025-11-22 15:27:31'),(13,17,1,'2024-12-07 02:42:41'),(13,26,5,'2025-11-15 07:09:32'),(13,28,1,'2025-11-15 15:56:51'),(13,32,1,'2025-11-15 16:58:45'),(13,33,1,'2025-11-15 17:04:39'),(14,20,1,'2024-12-07 06:06:04'),(14,26,1,'2025-11-15 07:09:32'),(14,33,1,'2025-11-15 17:04:37'),(14,34,1,'2025-11-15 17:08:44'),(15,27,4,'2025-11-15 15:27:19'),(15,32,1,'2025-11-15 16:58:36'),(15,34,1,'2025-11-15 17:08:42'),(15,47,2,'2025-11-21 19:30:03'),(16,28,3,'2025-11-15 15:34:19'),(16,29,1,'2025-11-15 16:49:09'),(16,31,1,'2025-11-15 16:50:28'),(16,32,1,'2025-11-15 16:58:34'),(16,35,1,'2025-11-15 17:09:17'),(16,39,2,'2025-11-20 03:34:34'),(16,46,2,'2025-11-21 02:00:15'),(16,48,1,'2025-11-21 22:50:56'),(16,50,1,'2025-11-22 05:05:20'),(16,52,3,'2025-11-22 06:33:15'),(16,53,1,'2025-11-22 12:21:41'),(17,27,2,'2025-11-15 15:27:11'),(17,35,1,'2025-11-15 17:09:16'),(17,37,1,'2025-11-15 17:11:10'),(17,38,2,'2025-11-15 17:18:07'),(17,40,1,'2025-11-15 17:21:45'),(17,42,2,'2025-11-20 03:52:02'),(17,43,4,'2025-11-20 13:11:51'),(17,46,6,'2025-11-21 01:49:24'),(17,47,1,'2025-11-21 14:44:52'),(17,48,1,'2025-11-21 22:51:08'),(17,50,1,'2025-11-22 01:51:31'),(17,51,2,'2025-11-22 06:07:50'),(17,52,1,'2025-11-22 06:40:03'),(17,53,1,'2025-11-22 15:34:39'),(71,68,1,'2025-11-23 22:37:45'),(76,58,1,'2025-11-23 22:04:14'),(76,68,1,'2025-11-23 22:37:45'),(76,69,1,'2025-11-23 22:40:24'),(77,58,1,'2025-11-23 22:04:14'),(77,68,1,'2025-11-23 22:37:46'),(84,64,1,'2025-11-23 05:53:11'),(85,64,1,'2025-11-23 05:51:56'),(85,66,1,'2025-11-23 06:21:18');
/*!40000 ALTER TABLE `detalles_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_pedido`
--

DROP TABLE IF EXISTS `estado_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(55) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_pedido`
--

LOCK TABLES `estado_pedido` WRITE;
/*!40000 ALTER TABLE `estado_pedido` DISABLE KEYS */;
INSERT INTO `estado_pedido` VALUES (1,'En proceso','2024-12-06 22:58:50'),(2,'Comprado','2024-12-06 22:58:50');
/*!40000 ALTER TABLE `estado_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `img_novedad`
--

DROP TABLE IF EXISTS `img_novedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `img_novedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `img` text NOT NULL,
  `tipo_img_novedadid` int NOT NULL,
  `novedadid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkimg_noveda411983` (`tipo_img_novedadid`),
  KEY `fkimg_noveda721180` (`novedadid`),
  CONSTRAINT `fkimg_noveda411983` FOREIGN KEY (`tipo_img_novedadid`) REFERENCES `tipo_img_novedad` (`id`),
  CONSTRAINT `fkimg_noveda721180` FOREIGN KEY (`novedadid`) REFERENCES `novedad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `img_novedad`
--

LOCK TABLES `img_novedad` WRITE;
/*!40000 ALTER TABLE `img_novedad` DISABLE KEYS */;
INSERT INTO `img_novedad` VALUES (1,'Celulares en cuadro azul','/static/img/samsungProm1.png',2,1,'2024-12-07 04:19:44'),(2,'Banner Samsung','/static/img/samsungProm1.png',1,1,'2024-12-07 04:20:34'),(3,'audifonos samsung','/static/img/samsungProm1.png',4,2,'2024-12-07 04:21:54'),(4,'tv samsung','/static/img/samsungProm1.png',4,3,'2024-12-07 04:22:10'),(5,'apple oferta','/static/img/samsungProm1.png',3,4,'2024-12-07 04:22:38'),(6,'lenovo oferta','/static/img/samsungProm1.png',3,5,'2024-12-07 04:22:48'),(7,'cuadro Oster licuadora','/static/img/samsungProm1.png',2,7,'2024-12-07 04:22:53'),(8,'cuadro Gloria Yogurt','/static/img/samsungProm1.png',2,6,'2024-12-07 04:22:59'),(9,'xiaomiProm.png','/static/img/img_novedad/xiaomiProm.png',1,9,'2025-11-21 03:24:02'),(10,'banner-tecstore-1430x450-huawei_1.jpg','/static/img/img_novedad/banner-tecstore-1430x450-huawei_1.jpg',1,10,'2025-11-21 03:32:35');
/*!40000 ALTER TABLE `img_novedad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `img_producto`
--

DROP TABLE IF EXISTS `img_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `img_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img_nombre` varchar(100) DEFAULT NULL,
  `imagen` text NOT NULL,
  `imgprincipal` tinyint(1) NOT NULL,
  `productoid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkimg_produc616199` (`productoid`),
  CONSTRAINT `fkimg_produc616199` FOREIGN KEY (`productoid`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `img_producto`
--

LOCK TABLES `img_producto` WRITE;
/*!40000 ALTER TABLE `img_producto` DISABLE KEYS */;
INSERT INTO `img_producto` VALUES (1,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png','/static/img/1.png',1,1,'2024-12-07 09:25:56'),(2,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png\n','/static/img/img_producto/Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png',0,1,'2024-12-07 09:26:10'),(3,'Televisor SAMSUNG CRYSTAL UHD 55\" UHD 4K Smart TV ...\n','/static/img/3.png',0,2,'2024-12-07 09:26:43'),(4,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png\n','/static/img/img_producto/Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png',0,1,'2024-12-07 09:26:43'),(5,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png\n','/static/img/img_producto/Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png',0,1,'2024-12-07 09:26:43'),(6,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png\n','/static/img/img_producto/Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png',0,1,'2024-12-07 09:26:43'),(7,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png\n','/static/img/img_producto/Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png',0,1,'2024-12-07 09:26:43'),(8,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png\n','/static/img/img_producto/Celular Samsung Galaxy A24 128GB 4GB RAM Negro.png',0,1,'2024-12-07 09:26:43'),(9,'Celular Samsung Galaxy A15 256GB, 8GB ram, cámara ...\n','/static/img/9.png',1,3,'2024-12-07 09:27:03'),(10,'Laptop LENOVO 15AMN8 15.6\" AMD Ryzen 5 (7000 serie...','/static/img/10.webp',1,4,'2024-12-07 09:27:04'),(11,'Chocolates Surtidos','/static/img/11.webp',1,14,'2024-12-07 09:27:21'),(12,'Cereal CORN FLAKES','/static/img/12.webp',1,13,'2024-12-07 09:27:23'),(13,'Pack Galleta NABISCO Oreo Regular Sixpack x 3un','/static/img/13.webp',1,12,'2024-12-07 09:27:35'),(14,'Galletas OREO sabor Cookies&Cream Paquete 6un','/static/img/14.webp',1,11,'2024-12-07 09:27:37'),(15,'Pack Galletas FIELD Coronita Sixpack x 3un\r\n','/static/img/15.webp',1,10,'2024-12-07 09:27:58'),(16,'Pack Galleta Chocosoda FIELD Sixpack x 3un','/static/img/16.webp',1,9,'2024-12-07 09:27:59'),(17,'Café Instantáneo ALTOMAYO Gourmet Lata 190g','/static/img/17.webp',1,7,'2024-12-07 09:28:06'),(18,'Café Tostado Molido ALTOMAYO Gourmet Caja 450g + Prensa','/static/img/18.webp',1,8,'2024-12-07 09:28:06'),(19,'Yogurt Bebible LAIVE Bio Sabor a Fresa Galonera 1.7Kg','/static/img/19.webp',1,6,'2024-12-07 09:28:14'),(20,'Yogurt Parcialmente Descremado GLORIA Sabor a Vainilla Botella 180g Paquete 6un','/static/img/20.webp',1,5,'2024-12-07 09:28:14'),(21,'20241102_133833.jpg','/static/img/20241102_133833.jpg',1,15,'2025-10-31 03:32:07'),(22,'Screenshot_20251019_110431_Chrome.jpg','/static/img/Screenshot_20251019_110431_Chrome.jpg',1,16,'2025-10-31 03:34:36'),(23,'20240522_211052.jpg','/static/img/20240522_211052.jpg',1,17,'2025-11-03 02:04:41'),(24,'Almendras con Cobertura de Chocolate Vizzio 69g','/static/img/img_producto/Almendras con Cobertura de Chocolate Vizzio 69g.png',1,21,'2025-11-22 23:04:21'),(25,'Audífonos Inalámbricos In-Ear HUAWEI FreeBuds SE 2 Azul','/static/img/img_producto/Audífonos Inalámbricos In-Ear HUAWEI FreeBuds SE 2 Azul.png',1,22,'2025-11-22 23:04:21'),(26,'Audífonos inalámbricos verdaderos con cancelación de ruido Samsung Galaxy Buds Live (Mystic Black)','/static/img/img_producto/Audífonos inalámbricos verdaderos con cancelación de ruido Samsung Galaxy Buds Live (Mystic Black).png',1,23,'2025-11-22 23:04:21'),(27,'Audífonos Samsung SM-R510NZAADBT Galaxy Buds 2 Pro','/static/img/img_producto/Audífonos Samsung SM-R510NZAADBT Galaxy Buds 2 Pro.png',1,24,'2025-11-22 23:04:21'),(28,'Batería Krea 7 Piezas Antiadherente','/static/img/img_producto/Batería Krea 7 Piezas Antiadherente.png',1,25,'2025-11-22 23:04:21'),(29,'Bombones con Relleno de Avellanas Ferrero Rocher 8un','/static/img/img_producto/Bombones con Relleno de Avellanas Ferrero Rocher 8un.png',1,26,'2025-11-22 23:04:21'),(30,'Bombones Surtidos Nestlé Multipack 45un','/static/img/img_producto/Bombones Surtidos Nestlé Multipack 45un.png',1,27,'2025-11-22 23:04:21'),(31,'BZBGEAR Universal HDMI-SDI-USB Cámara PTZ de transmisión en vivo con zoom 12x (plata)','/static/img/img_producto/BZBGEAR Universal HDMI-SDI-USB Cámara PTZ de transmisión en vivo con zoom 12x (plata).png',1,28,'2025-11-22 23:04:21'),(32,'Cafetera OSTER 4 Tazas BVSTDCDR5B-053','/static/img/img_producto/Cafetera OSTER 4 Tazas BVSTDCDR5B-053.png',1,29,'2025-11-22 23:04:21'),(33,'Casaca Diger Denim Stretch Hombre Pionier','/static/img/img_producto/Casaca Diger Denim Stretch Hombre Pionier.png',1,30,'2025-11-22 23:04:21'),(34,'Celular Apple Iphone 13 128GB Negro','/static/img/img_producto/Celular Apple Iphone 13 128GB Negro.png',1,31,'2025-11-23 02:59:55'),(35,'Celular Samsung Galaxy A34 5G 128GB Rom 6GB Ram NEGRO','/static/img/img_producto/Celular Samsung Galaxy A34 5G 128GB Rom 6GB Ram NEGRO.png',1,32,'2025-11-23 02:59:55'),(36,'Celular Samsung Galaxy A54 5G 256GB 8GB RAM Negro','/static/img/img_producto/Celular Samsung Galaxy A54 5G 256GB 8GB RAM Negro.png',1,33,'2025-11-23 02:59:55'),(37,'Celular Samsung Galaxy S21 Plus 5G 128GB - Púrpura','/static/img/img_producto/Celular Samsung Galaxy S21 Plus 5G 128GB - Púrpura.png',1,34,'2025-11-23 02:59:55'),(38,'Celular Samsung Galaxy S23 FE 6.4 256GB 8GB Morado','/static/img/img_producto/Celular Samsung Galaxy S23 FE 6.4 256GB 8GB Morado.png',1,35,'2025-11-23 02:59:55'),(39,'Celular Samsung S23 Ultra 5G 256GB 12GB Ram Color Lavender','/static/img/img_producto/Celular Samsung S23 Ultra 5G 256GB 12GB Ram Color Lavender.png',1,36,'2025-11-23 02:59:55'),(40,'Celular Xiaomi Redmi 13C 6.74 8GB RAM 256GB Negro','/static/img/img_producto/Celular Xiaomi Redmi 13C 6.74 8GB RAM 256GB Negro.png',1,37,'2025-11-23 02:59:55'),(41,'Consola Nintendo Switch Modelo Oled Neón','/static/img/img_producto/Consola Nintendo Switch Modelo Oled Neón.png',1,38,'2025-11-23 02:59:55'),(42,'Consola PS5 Slim Con Lector De Disco 1TB','/static/img/img_producto/Consola PS5 Slim Con Lector De Disco 1TB.png',1,39,'2025-11-23 02:59:55'),(43,'Freidora de Aire OSTER 4L Digital Negro','/static/img/img_producto/Freidora de Aire OSTER 4L Digital Negro.png',1,40,'2025-11-23 02:59:55'),(44,'Freidora de Aire Oster CKSTAF18DDF-053 Digital 1.8L Negro','/static/img/img_producto/Freidora de Aire Oster CKSTAF18DDF-053 Digital 1.8L Negro.png',1,41,'2025-11-23 02:59:55'),(45,'Horno Microondas Oster POGGM3901M 700W 25 Litros','/static/img/img_producto/Horno Microondas Oster POGGM3901M 700W 25 Litros.png',1,42,'2025-11-23 02:59:55'),(46,'Impresora Epson L4260 Ecotank','/static/img/img_producto/Impresora Epson L4260 Ecotank.png',1,43,'2025-11-23 02:59:55'),(47,'Iphone 11 6.1 4GB 64GB 12MP Blanco','/static/img/img_producto/Iphone 11 6.1 4GB 64GB 12MP Blanco.png',1,44,'2025-11-23 02:59:55'),(48,'Juego de Vajilla Krea Opal Flores 16 Piezas','/static/img/img_producto/Juego de Vajilla Krea Opal Flores 16 Piezas.png',1,45,'2025-11-23 02:59:55'),(50,'Laptop Lenovo IdeaPad Gaming3 15IAH7 i5-12450H 8GB RAM 512GB SSD RTX3060','/static/img/img_producto/Laptop Lenovo IdeaPad Gaming3 15IAH7 i5-12450H 8GB RAM 512GB SSD RTX3060.png',1,47,'2025-11-23 02:59:55'),(51,'Lavadora SAMSUNG Carga Superior 18Kg WA18T6260BV Negro','/static/img/img_producto/Lavadora SAMSUNG Carga Superior 18Kg WA18T6260BV Negro.png',1,48,'2025-11-23 02:59:55'),(52,'Leche Condensada GLORIA Doypack 200g','/static/img/img_producto/Leche Condensada GLORIA Doypack 200g.png',1,49,'2025-11-23 02:59:55'),(53,'Leche GLORIA UHT Chocolatada Caja 1L','/static/img/img_producto/Leche GLORIA UHT Chocolatada Caja 1L.png',1,50,'2025-11-23 02:59:55'),(54,'Leche Light GLORIA Lata 390g Paquete 6un','/static/img/img_producto/Leche Light GLORIA Lata 390g Paquete 6un.png',1,51,'2025-11-23 02:59:55'),(55,'Lenovo HE05 + Reloj Pulsera Digital de REGALO','/static/img/img_producto/Lenovo HE05 + Reloj Pulsera Digital de REGALO.png',1,52,'2025-11-23 02:59:55'),(56,'Licuadora Oster Xpert Series BLST3BCPG con Control de Textura','/static/img/img_producto/Licuadora Oster Xpert Series BLST3BCPG con Control de Textura.png',1,53,'2025-11-23 02:59:55'),(57,'Mantequilla con Sal Gloria 390g','/static/img/img_producto/Mantequilla con Sal Gloria 390g.png',1,54,'2025-11-23 02:59:55'),(58,'Mermelada de Fresa Gloria Frasco 1 kg','/static/img/img_producto/Mermelada de Fresa Gloria Frasco 1 kg.png',1,55,'2025-11-23 02:59:55'),(59,'Olla Arrocera OSTER 1.8L CKSTRC1700R Rojo','/static/img/img_producto/Olla Arrocera OSTER 1.8L CKSTRC1700R Rojo.png',1,56,'2025-11-23 02:59:55'),(60,'Parlante Amazon Alexa Echo Dot 5ta Generación Smart Hub Blanco','/static/img/img_producto/Parlante Amazon Alexa Echo Dot 5ta Generación Smart Hub Blanco.png',1,57,'2025-11-23 02:59:55'),(61,'Plancha de vapor ligera Oster GCSTBS3802','/static/img/img_producto/Plancha de vapor ligera Oster GCSTBS3802.png',1,58,'2025-11-23 02:59:55'),(62,'Samsung S22 Ultra 256GB 12GB Borgoña','/static/img/img_producto/Samsung S22 Ultra 256GB 12GB Borgoña.png',1,59,'2025-11-23 02:59:55'),(63,'Refrigeradora OSTER 559L No Frost OS-PSBSME20SSEBDI Black Inox','/static/img/img_producto/Refrigeradora OSTER 559L No Frost OS-PSBSME20SSEBDI Black Inox.png',1,60,'2025-11-23 02:59:55'),(64,'Refrigeradora Samsung Side by Side RS52B3000M9 PE 490L Gris Metal','/static/img/img_producto/Refrigeradora Samsung Side by Side RS52B3000M9 PE 490L Gris Metal.png',1,61,'2025-11-23 02:59:55'),(65,'Samsung A25 5G 256GB 8GB Negro','/static/img/img_producto/Samsung A25 5G 256GB 8GB Negro.png',1,62,'2025-11-23 02:59:55'),(66,'Samsung Galaxy A25 128Gb 6Ram Blue Light','/static/img/img_producto/Samsung Galaxy A25 128Gb 6Ram Blue Light.png',1,63,'2025-11-23 02:59:55'),(67,'Samsung Galaxy S22 Ultra - 12GB RAM + 256GB + Cargador 45W - Borgoña','/static/img/img_producto/Samsung Galaxy S22 Ultra - 12GB RAM + 256GB + Cargador 45W - Borgoña.png',1,64,'2025-11-23 02:59:55'),(68,'Samsung Galaxy S24 Plus 512gb 12gb Negro','/static/img/img_producto/Samsung Galaxy S24 Plus 512gb 12gb Negro.png',1,65,'2025-11-23 02:59:55'),(69,'Samsung Galaxy S24 Ultra 6.8 12GB RAM 256GB - Violeta Titanio+ CARGADOR 45w','/static/img/img_producto/Samsung Galaxy S24 Ultra 6.8 12GB RAM 256GB - Violeta Titanio+ CARGADOR 45w.png',1,66,'2025-11-23 02:59:55'),(70,'Samsung Galaxy S24 Ultra 6.8 12GB RAM 512GB - Negro Titanio + CARGADOR 45w','/static/img/img_producto/Samsung Galaxy S24 Ultra 6.8 12GB RAM 512GB - Negro Titanio + CARGADOR 45w.png',1,67,'2025-11-23 02:59:55'),(71,'Samsung Note 10 Plus 5G 256GB 12GB Aurora Glow','/static/img/img_producto/Samsung Note 10 Plus 5G 256GB 12GB Aurora Glow.png',1,68,'2025-11-23 02:59:55'),(72,'Samsung Note 10 Plus 5G 256GB 12GB Negro','/static/img/img_producto/Samsung Note 10 Plus 5G 256GB 12GB Negro.png',1,69,'2025-11-23 02:59:55'),(73,'Samsung Note 10 Plus 256GB Negro','/static/img/img_producto/Samsung Note 10 Plus 256GB Negro.png',1,70,'2025-11-23 02:59:55'),(74,'Samsung Z Fold 5 5G 512GB 12GB Azul','/static/img/img_producto/Samsung Z Fold 5 5G 512GB 12GB Azul.png',1,71,'2025-11-23 02:59:55'),(75,'Samsung Z Fold 5 5G 512GB 12GB Crema','/static/img/img_producto/Samsung Z Fold 5 5G 512GB 12GB Crema.png',1,72,'2025-11-23 02:59:55'),(77,'Sixpack Leche Reconstituida Gloria Lata 395g','/static/img/img_producto/Sixpack Leche Reconstituida Gloria Lata 395g.png',1,74,'2025-11-23 02:59:55'),(78,'Soundbar Bluetooth Samsung 2.0 Ch HW-C400','/static/img/img_producto/Soundbar Bluetooth Samsung 2.0 Ch HW-C400.png',1,75,'2025-11-23 02:59:55'),(79,'Tablet LENOVO P11 (2nd Gen) 11 6GB 128GB (uMCP) Storm Grey','/static/img/img_producto/Tablet LENOVO P11 (2nd Gen) 11 6GB 128GB (uMCP) Storm Grey.png',1,76,'2025-11-23 02:59:55'),(80,'Tablet SAMSUNG S6 LITE 10.4 128GB HDD 4GB Gris','/static/img/img_producto/Tablet SAMSUNG S6 LITE 10.4 128GB HDD 4GB Gris.png',1,77,'2025-11-23 02:59:55'),(81,'Televisor SAMSUNG CRYSTAL UHD 65 UHD 4K Smart Tv UN65CU8000GXPE','/static/img/img_producto/Televisor SAMSUNG CRYSTAL UHD 65 UHD 4K Smart Tv UN65CU8000GXPE.png',1,78,'2025-11-23 02:59:55'),(82,'Televisor Samsung Smart TV 65 Crystal UHD 4K UN65CU7000GXPE','/static/img/img_producto/Televisor Samsung Smart TV 65 Crystal UHD 4K UN65CU7000GXPE.png',1,79,'2025-11-23 02:59:55'),(83,'Tricombo Oster Arrocera + Hervidor + Licuadora','/static/img/img_producto/Tricombo Oster Arrocera + Hervidor + Licuadora.png',1,80,'2025-11-23 02:59:55'),(84,'Tri-Combo Oster Licuadora BLSTKAGBPB + Olla Arrocera CKSTRC1700B + Hervidro BVSTKT3101','/static/img/img_producto/Tri-Combo Oster Licuadora BLSTKAGBPB + Olla Arrocera CKSTRC1700B + Hervidro BVSTKT3101.png',1,81,'2025-11-23 02:59:55'),(85,'Vino Tinto Malbec Finca Las Moras Botella 750ml','/static/img/img_producto/Vino Tinto Malbec Finca Las Moras Botella 750ml.png',1,82,'2025-11-23 02:59:55'),(86,'Whisky Johnnie Walker Blue Label Botella 750ml','/static/img/img_producto/Whisky Johnnie Walker Blue Label Botella 750ml.png',1,83,'2025-11-23 02:59:55'),(87,'Yogurt Bebible Gloria Fresa Botella 1kg','/static/img/img_producto/Yogurt Bebible Gloria Fresa Botella 1kg.png',1,84,'2025-11-23 02:59:55'),(88,'Yogurt Gloria Battimix Vainilla 146g','https://plazavea.vteximg.com.br/arquivos/ids/28884600-1000-1000/20295425.jpg',1,85,'2025-11-23 02:59:55');
/*!40000 ALTER TABLE `img_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `informacion_domus`
--

DROP TABLE IF EXISTS `informacion_domus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `informacion_domus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `correo` varchar(200) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `imglogo` text NOT NULL,
  `imgicon` text NOT NULL,
  `descripcion` text NOT NULL,
  `historia` text NOT NULL,
  `vision` text NOT NULL,
  `valores` text NOT NULL,
  `mision` text NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informacion_domus`
--

LOCK TABLES `informacion_domus` WRITE;
/*!40000 ALTER TABLE `informacion_domus` DISABLE KEYS */;
INSERT INTO `informacion_domus` VALUES (1,'servicioalcliente@domus.pe','074 606240','','','Con un enfoque meticuloso en la satisfacción del cliente y la excelencia en la oferta de productos, el Supermercado Domus sentó las bases de lo que se convertiría en una empresa líder en la industria de supermercados en el país.\r\n\r\n','Desde sus inicios, el Supermercado Domus se destacó por su compromiso con la calidad y la atención al cliente. Cultivó relaciones sólidas con proveedores locales y nacionales para garantizar la frescura y variedad de sus productos. Este enfoque se convirtió en el sello distintivo de Domus, estableciendo una base de confianza y lealtad entre la clientela. Con el tiempo, el Supermercado Domus identificó oportunidades de expansión y diversificación, ampliando tanto la variedad de productos como la infraestructura física de sus establecimientos. Esta expansión estratégica permitió a Domus atender a una base de clientes cada vez más amplia, consolidando su posición como referente en la industria.\r\n\r\n','Al año 2026 convertirnos en el supermercado preferido por las familias en la región Lambayeque, reconocido no solo por la calidad superior de nuestros productos y servicios, sino también por nuestra innovación constante, nuestro compromiso con la sostenibilidad y nuestro impacto positivo en las comunidades locales. Aspiramos a ser un ejemplo de excelencia en el comercio minorista, ofreciendo una experiencia de compra que no solo satisfaga, sino que deleite y fidelice a nuestros clientes.\r\n\r\n','- Responsabilidad\r\n- Colaboración\r\n- Integridad\r\n- Empatía\r\n- Prudencia\r\n- Fortaleza','Ofrecer a nuestros clientes una experiencia de compra única y agradable, caracterizada por una amplia variedad de productos frescos y de alta calidad, un servicio al cliente excepcional y un compromiso con la sostenibilidad y el apoyo a proveedores locales. Nos esforzamos por ser el supermercado preferido de las familias, ofreciendo precios competitivos y fomentando un entorno de trabajo inclusivo y respetuoso para nuestros empleados.\r\n\r\n','2024-12-06 22:59:46');
/*!40000 ALTER TABLE `informacion_domus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lista_deseos`
--

DROP TABLE IF EXISTS `lista_deseos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lista_deseos` (
  `productoid` int NOT NULL,
  `usuarioid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`productoid`,`usuarioid`),
  KEY `fklista_dese907029` (`usuarioid`),
  CONSTRAINT `fklista_dese59890` FOREIGN KEY (`productoid`) REFERENCES `producto` (`id`),
  CONSTRAINT `fklista_dese907029` FOREIGN KEY (`usuarioid`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lista_deseos`
--

LOCK TABLES `lista_deseos` WRITE;
/*!40000 ALTER TABLE `lista_deseos` DISABLE KEYS */;
INSERT INTO `lista_deseos` VALUES (5,12,'2024-12-07 01:49:06'),(6,12,'2024-12-07 01:29:10'),(8,20,'2024-12-07 03:19:43'),(9,20,'2024-12-07 03:19:46'),(10,20,'2024-12-07 03:19:48'),(17,3,'2025-11-23 04:40:22'),(17,35,'2025-11-22 17:30:14'),(71,3,'2025-11-23 16:35:54'),(76,3,'2025-11-23 16:35:51'),(77,3,'2025-11-23 16:35:51'),(78,3,'2025-11-23 16:35:52'),(79,3,'2025-11-23 16:35:50'),(85,39,'2025-11-23 05:53:06');
/*!40000 ALTER TABLE `lista_deseos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marca`
--

DROP TABLE IF EXISTS `marca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `img_logo` text NOT NULL,
  `img_banner` text,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marca`
--

LOCK TABLES `marca` WRITE;
/*!40000 ALTER TABLE `marca` DISABLE KEYS */;
INSERT INTO `marca` VALUES (1,'Samsung','/static/img/X.png','','2024-11-01 10:00:00',1,'2024-12-07 04:00:39'),(2,'Huawei','/static/img/X.png','','2024-09-17 10:00:00',1,'2024-12-07 04:00:53'),(3,'Tabernero','/static/img/X.png','','2024-09-10 10:00:00',1,'2024-12-07 04:00:54'),(4,'Primor','/static/img/X.png','','2024-09-01 10:00:00',1,'2024-12-07 04:03:56'),(5,'Pedigree','/static/img/X.png','','2024-08-22 10:00:00',1,'2024-12-07 04:03:56'),(6,'Gloria','/static/img/X.png','','2024-07-04 10:00:00',1,'2024-12-07 04:04:12'),(7,'Coca Cola','/static/img/X.png','','2024-09-17 10:00:00',1,'2024-12-07 04:04:13'),(8,'Nestle','/static/img/X.png','','2024-10-08 10:00:00',1,'2024-12-07 04:09:21'),(9,'LG','/static/img/X.png','','2024-07-05 10:00:00',1,'2024-12-07 04:04:26'),(10,'Hasbro','/static/img/X.png','','2024-10-10 10:00:00',1,'2024-12-07 04:04:52'),(12,'Adidas','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(13,'Artesco','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(14,'Pionier','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(15,'Inca Kola','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(16,'Braedt','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(17,'Lenovo','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(18,'Johnnie Walker','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(19,'Apple','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(20,'Costa','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(21,'Krea','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(22,'Nivea','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(23,'Oster','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(24,'Xiaomi','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(25,'Costeño','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(26,'Motorola','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(27,'Laive','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(28,'BlackLine','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(29,'Alacena','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(30,'HP','/static/img/X.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(31,'Imaco','/static/img/marca/31.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(32,'Ricocan','/static/img/marca/32.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(33,'Asus','/static/img/marca/33.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(34,'Kirma','/static/img/marca/34.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(35,'Suave','/static/img/marca/35.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(36,'Corona','/static/img/marca/36.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(37,'Nike','/static/img/marca/37.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(38,'San Carlos','/static/img/marca/38.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(39,'Pantene','/static/img/marca/39.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(40,'Don Vitorio','/static/img/marca/40.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(41,'SuperCat','/static/img/marca/41.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(42,'P&G','/static/img/marca/42.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(43,'Field','/static/img/marca/43.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(44,'North Star','/static/img/marca/44.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(45,'Standford','/static/img/marca/45.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(46,'Puma','/static/img/marca/46.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(47,'Oreo','/static/img/marca/47.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(48,'LEGO','/static/img/marca/48.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(49,'I-run','/static/img/marca/49.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(50,'Glacial','/static/img/marca/50.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(51,'Altomayo','/static/img/marca/51.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(52,'AXE','/static/img/marca/52.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(53,'Clorox','/static/img/marca/53.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(54,'Old Spice','/static/img/marca/54.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(55,'Pegafan','/static/img/marca/55.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(56,'Logitech','/static/img/marca/56.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(57,'Mattel','/static/img/marca/57.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(58,'Faber-Castell','/static/img/marca/58.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(59,'Sapolio','/static/img/marca/59.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(60,'Nintendo','/static/img/marca/60.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(61,'Sony','/static/img/marca/61.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(62,'Panasonic','/static/img/marca/62.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(63,'QuickSilver','/static/img/marca/63.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(64,'Frugos del Valle','/static/img/marca/64.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(65,'Paraiso','/static/img/marca/65.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19'),(66,'Walon','/static/img/marca/66.png','','2025-10-10 10:26:19',1,'2025-10-10 10:26:19');
/*!40000 ALTER TABLE `marca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metodo_pago`
--

DROP TABLE IF EXISTS `metodo_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodo_pago` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metodo_pago`
--

LOCK TABLES `metodo_pago` WRITE;
/*!40000 ALTER TABLE `metodo_pago` DISABLE KEYS */;
INSERT INTO `metodo_pago` VALUES (1,'Tarjeta de Débito',1,'2024-12-06 22:58:50'),(2,'Tarjeta de Crédito',1,'2024-12-06 22:58:50'),(3,'Yape',1,'2024-12-06 22:58:50'),(4,'Efectivo',0,'2024-12-06 22:58:50');
/*!40000 ALTER TABLE `metodo_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `motivo_comentario`
--

DROP TABLE IF EXISTS `motivo_comentario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `motivo_comentario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `motivo` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivo_comentario`
--

LOCK TABLES `motivo_comentario` WRITE;
/*!40000 ALTER TABLE `motivo_comentario` DISABLE KEYS */;
INSERT INTO `motivo_comentario` VALUES (1,'Queja o Reclamo',1,'2024-12-06 22:58:50'),(2,'Fallo en el Sistema',1,'2024-12-06 22:58:50'),(3,'Error al Iniciar Sesion',1,'2024-12-06 22:58:50'),(4,'Pagina No disponible',1,'2024-12-06 22:58:50'),(5,'Error al Comprar',1,'2024-12-06 22:58:50'),(6,'Pedido no Entregado',1,'2024-12-06 22:58:50');
/*!40000 ALTER TABLE `motivo_comentario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `novedad`
--

DROP TABLE IF EXISTS `novedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  KEY `fknovedad812313` (`tipo_novedadid`),
  KEY `fknovedad821851` (`subcategoriaid`),
  CONSTRAINT `fknovedad215901` FOREIGN KEY (`marcaid`) REFERENCES `marca` (`id`),
  CONSTRAINT `fknovedad812313` FOREIGN KEY (`tipo_novedadid`) REFERENCES `tipo_novedad` (`id`),
  CONSTRAINT `fknovedad821851` FOREIGN KEY (`subcategoriaid`) REFERENCES `subcategoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `novedad`
--

LOCK TABLES `novedad` WRITE;
/*!40000 ALTER TABLE `novedad` DISABLE KEYS */;
INSERT INTO `novedad` VALUES (1,'descuentos en Samsung','NUEVOS DESCUENTOS EN SAMSUNG','2025-10-10','2026-01-01','aaaaaaaaa','2025-11-26 22:50:47',1,1,NULL,3,'2024-12-06 23:19:22'),(2,'audifonos Samsung','Lo mejor de Samsung en Audifonos','2025-10-10','2026-01-01','aaaaa','2024-09-16 05:00:00',1,1,NULL,3,'2024-12-06 23:19:22'),(3,'televisores Samsung','DESCUENTOS EN TELEVISORES SAMSUNG','2025-10-10','2026-01-01','ecefweevwev','2024-10-09 05:00:00',1,1,NULL,3,'2024-12-06 23:19:22'),(4,'telefono Apple Ultimos dias','ULTIMOS DIAS en APPLE','2025-10-10','2026-01-01','','2024-11-05 05:00:00',1,19,NULL,3,'2024-12-06 23:19:22'),(5,'ultimos dias laptop lenovo','¡ULTIMOS DIAS en LENOVO!','2025-10-10','2026-01-01','','2024-08-14 05:00:00',1,17,NULL,3,'2024-12-06 23:19:22'),(6,'yogures Gloria','20% dsco en yogures GLORIA','2025-10-10','2026-01-01','yogurt barato','2024-07-24 05:00:00',1,6,NULL,3,'2024-12-06 23:19:22'),(7,'electrodomesticos Oster','Ofertas en Miles de Electrodomésticos','2025-10-10','2026-01-01','compra Oster','2024-09-03 05:00:00',1,23,19,3,'2024-12-06 23:19:22'),(9,'xiaomiProm','xiaomiProm','2025-01-01','2026-01-01','','2025-11-21 03:20:47',1,24,1,3,'2025-11-21 03:20:47'),(10,'huawei','huawei','2025-01-01','2026-01-01','huawei','2025-11-21 03:20:47',1,2,1,3,'2025-11-21 03:20:47');
/*!40000 ALTER TABLE `novedad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_compra` date DEFAULT NULL,
  `subtotal` decimal(9,2) DEFAULT NULL,
  `metodo_pagoid` int DEFAULT NULL,
  `usuarioid` int NOT NULL,
  `estado_pedidoid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `card_nro` varchar(255) DEFAULT NULL,
  `card_mmaa` varchar(255) DEFAULT NULL,
  `card_titular` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fkpedido259150` (`estado_pedidoid`),
  KEY `fkpedido787527` (`metodo_pagoid`),
  KEY `fkpedido832373` (`usuarioid`),
  CONSTRAINT `fkpedido259150` FOREIGN KEY (`estado_pedidoid`) REFERENCES `estado_pedido` (`id`),
  CONSTRAINT `fkpedido787527` FOREIGN KEY (`metodo_pagoid`) REFERENCES `metodo_pago` (`id`),
  CONSTRAINT `fkpedido832373` FOREIGN KEY (`usuarioid`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (16,'2025-11-22',150.50,1,12,2,'2024-12-07 02:13:03',NULL,NULL,NULL),(17,'2024-12-06',13.90,4,16,2,'2024-12-07 02:29:08',NULL,NULL,NULL),(18,'2024-12-06',33.78,1,18,2,'2024-12-07 02:32:43',NULL,NULL,NULL),(19,'2024-12-06',50.67,1,20,2,'2024-12-07 03:17:08',NULL,NULL,NULL),(20,'2024-12-07',1239.09,3,20,2,'2024-12-07 03:21:38',NULL,NULL,NULL),(21,'2025-11-22',150.50,1,33,2,'2024-12-07 03:53:36',NULL,NULL,NULL),(23,'2024-12-06',90.30,3,16,2,'2024-12-07 04:53:54',NULL,NULL,NULL),(24,'2025-09-01',1.00,1,3,2,'2024-12-08 08:26:52',NULL,NULL,NULL),(26,'2025-09-01',1.00,1,3,2,'2025-11-15 06:44:11',NULL,NULL,NULL),(27,'2025-11-22',150.50,1,3,2,'2025-11-15 12:38:54',NULL,NULL,NULL),(28,'2025-09-01',1.00,1,3,2,'2025-11-15 15:34:13',NULL,NULL,NULL),(29,'2025-09-01',1.00,1,3,2,'2025-11-15 16:48:43',NULL,NULL,NULL),(30,'2025-09-01',1.00,1,3,2,'2025-11-15 16:49:14',NULL,NULL,NULL),(31,'2025-09-01',1.00,1,3,2,'2025-11-15 16:49:19',NULL,NULL,NULL),(32,'2025-09-01',1.00,1,3,2,'2025-11-15 16:52:31',NULL,NULL,NULL),(33,'2025-09-01',1.00,1,3,2,'2025-11-15 17:03:48',NULL,NULL,NULL),(34,'2025-09-01',1.00,1,3,2,'2025-11-15 17:04:42',NULL,NULL,NULL),(35,'2025-09-01',1.00,1,3,2,'2025-11-15 17:08:47',NULL,NULL,NULL),(36,'2025-09-01',1.00,1,3,2,'2025-11-15 17:09:22',NULL,NULL,NULL),(37,'2025-09-01',1.00,1,3,2,'2025-11-15 17:10:40',NULL,NULL,NULL),(38,'2025-09-01',1.00,1,3,2,'2025-11-15 17:11:13',NULL,NULL,NULL),(39,'2025-11-20',30.40,3,3,2,'2025-11-15 17:18:12',NULL,NULL,NULL),(40,'2025-11-19',89.99,3,3,2,'2025-11-15 17:20:41',NULL,NULL,NULL),(41,'2025-11-19',2009.98,2,3,2,'2025-11-15 17:22:00',NULL,NULL,NULL),(42,'2025-11-20',240.88,3,3,2,'2025-11-20 03:47:59',NULL,NULL,NULL),(43,'2025-11-20',509.32,1,3,2,'2025-11-20 06:18:23',NULL,NULL,NULL),(44,'2025-11-20',132.70,3,3,2,'2025-11-20 13:44:11',NULL,NULL,NULL),(45,'2025-11-20',67.90,2,3,2,'2025-11-20 14:54:21',NULL,NULL,NULL),(46,'2025-11-20',1.00,1,3,2,'2025-11-20 14:58:43',NULL,NULL,NULL),(47,'2025-11-20',0.00,1,3,2,'2025-11-21 02:08:33',NULL,NULL,NULL),(48,'2025-11-21',116.88,3,3,2,'2025-11-21 22:42:40',NULL,NULL,NULL),(49,'2025-11-22',91.28,3,3,2,'2025-11-21 22:53:07',NULL,NULL,NULL),(50,'2025-11-22',99.99,3,3,2,'2025-11-22 00:29:48',NULL,NULL,NULL),(51,'2025-11-22',179.98,3,3,2,'2025-11-22 06:07:14',NULL,NULL,NULL),(52,'2025-11-22',1119.98,3,3,2,'2025-11-22 06:08:54',NULL,NULL,NULL),(53,'2025-11-22',99.99,3,3,2,'2025-11-22 06:40:25',NULL,NULL,NULL),(54,'2025-11-22',63.90,3,2,2,'2025-11-22 15:23:03',NULL,NULL,NULL),(55,'2025-11-22',53.78,1,2,2,'2025-11-22 15:26:31',NULL,NULL,NULL),(56,NULL,NULL,NULL,2,1,'2025-11-22 15:28:56',NULL,NULL,NULL),(57,'2025-11-22',0.00,3,3,2,'2025-11-22 15:35:16',NULL,NULL,NULL),(58,'2025-11-23',2248.00,2,3,2,'2025-11-22 15:43:09',NULL,NULL,NULL),(59,NULL,NULL,NULL,12,1,'2025-11-22 17:05:01',NULL,NULL,NULL),(60,NULL,NULL,NULL,12,1,'2025-11-22 17:06:02',NULL,NULL,NULL),(61,NULL,NULL,NULL,12,1,'2025-11-22 17:11:41',NULL,NULL,NULL),(62,NULL,NULL,NULL,33,1,'2025-11-22 17:15:30',NULL,NULL,NULL),(64,'2025-11-23',11.80,3,39,2,'2025-11-23 05:51:56',NULL,NULL,NULL),(65,NULL,NULL,NULL,39,1,'2025-11-23 05:53:26',NULL,NULL,NULL),(66,'2025-11-23',2.90,3,40,2,'2025-11-23 06:21:18',NULL,NULL,NULL),(67,NULL,NULL,NULL,40,1,'2025-11-23 06:21:33',NULL,NULL,NULL),(68,'2025-11-23',8547.00,2,3,2,'2025-11-23 22:34:38','gAAAAABpI4zcVZiN36tCTjNU5NMkM3ezAdWlajXClF89-QUuicUkrXYEXrzS3LKREyOk6VSAAAaAglO3WYshmgoSgGh_aD8UTVXVRYAcJl5xetzL_T-3DrY=','gAAAAABpI4zcBKVle7BXSB_lZVpXUEXdfFMh21t34rmafrqWEbBTUk6XUaKXrErh0OGROyp1DVv2iNvVliinP2xQ23EWySDvxg==','gAAAAABpI4zcb-OgZ9Wok97HZrFUBUV1dTQw4FI1YkJCocH0M5U6RBJ2yT97Ip4R32lBbCvPhT8myBH_E8WNPb9LnxpZCa3ulQ=='),(69,'2025-11-23',1049.00,3,3,2,'2025-11-23 22:38:20',NULL,NULL,NULL),(70,NULL,NULL,NULL,3,1,'2025-11-23 22:40:39',NULL,NULL,NULL);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  KEY `fkproducto953045` (`subcategoriaid`),
  KEY `fkproducto990798` (`marcaid`),
  CONSTRAINT `fkproducto953045` FOREIGN KEY (`subcategoriaid`) REFERENCES `subcategoria` (`id`),
  CONSTRAINT `fkproducto990798` FOREIGN KEY (`marcaid`) REFERENCES `marca` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro',1600.95,1289.99,999.99,NULL,11,'2024-10-06 10:00:00',1,1,1,'2024-12-07 04:25:17'),(2,'Televisor SAMSUNG CRYSTAL UHD 55\" UHD 4K Smart TV UN55DU8000GXPE',2299.00,1799.00,1699.00,NULL,232,'2024-10-01 10:00:00',1,1,7,'2024-12-07 04:25:17'),(3,'Celular Samsung Galaxy A15 256GB, 8GB ram, cámara principal 50MP + 5MP + 2MP, frontal 13MP, 6.5\", negro',799.00,589.00,NULL,NULL,1000,'2024-08-23 10:00:00',1,1,1,'2024-12-07 04:25:17'),(4,'Laptop LENOVO 15AMN8 15.6\" AMD Ryzen 5 (7000 series) 8GB 512GB W11',2259.00,1949.00,1849.00,NULL,204,'2024-09-12 10:00:00',1,17,5,'2024-12-07 04:25:17'),(5,'Yogurt Parcialmente Descremado GLORIA Sabor a Vainilla Botella 180g Paquete 6un',10.00,10.00,NULL,NULL,97,'2024-10-23 10:00:00',1,6,25,'2024-12-07 04:25:17'),(6,'Yogurt Bebible LAIVE Bio Sabor a Fresa Galonera 1.7Kg',11.50,11.50,NULL,NULL,96,'2024-10-23 10:00:00',1,27,25,'2024-12-07 04:25:17'),(7,'Café Instantáneo ALTOMAYO Gourmet Lata 190g',40.90,40.90,NULL,NULL,96,'2024-10-23 10:00:00',1,51,13,'2024-12-07 04:25:17'),(8,'Café Tostado Molido ALTOMAYO Gourmet Caja 450g + Prensa',37.90,37.90,NULL,NULL,98,'2024-10-23 10:00:00',1,51,13,'2024-12-07 04:25:17'),(9,'Pack Galleta Chocosoda FIELD Sixpack x 3un',18.00,16.89,NULL,NULL,94,'2024-10-23 10:00:00',1,43,11,'2024-12-07 04:25:17'),(10,'Pack Galletas FIELD Coronita Sixpack x 3un',15.00,12.48,NULL,NULL,99,'2024-10-23 10:00:00',1,43,11,'2024-12-07 04:25:17'),(11,'Galletas OREO sabor Cookies&Cream Paquete 6un',5.20,5.20,NULL,NULL,99,'2024-10-23 10:00:00',1,47,11,'2024-12-07 04:25:17'),(12,'Pack Galleta NABISCO Oreo Regular Sixpack x 3un',15.60,13.20,10.00,NULL,99,'2024-10-23 10:00:00',1,47,11,'2024-12-07 04:25:17'),(13,'Cereal CORN FLAKES Nestlé Sin Gluten Caja 405g',13.90,13.90,NULL,NULL,99,'2024-10-23 10:00:00',1,8,13,'2024-12-07 04:25:17'),(14,'Bombones NESTLE Multipack Surtido Bolsa 360g',26.90,26.90,24.00,NULL,99,'2024-10-23 10:00:00',1,8,21,'2024-12-07 04:25:17'),(15,'Producto de Prueba',109.99,99.99,89.99,NULL,100,'2025-10-31 03:32:07',1,1,1,'2025-10-31 03:32:07'),(16,'Producto de Prueba112',109.99,99.99,10.00,NULL,100,'2025-10-31 03:34:36',1,1,1,'2025-10-31 03:34:36'),(17,'Producto de Prueba',109.99,99.99,89.99,NULL,100,'2025-11-03 02:04:41',1,1,1,'2025-11-03 02:04:41'),(21,'Almendras con Cobertura de Chocolate Vizzio 69g',12.90,10.90,8.90,NULL,30,'2025-11-22 23:04:05',1,8,21,'2025-11-22 23:04:05'),(22,'Audífonos Inalámbricos In-Ear HUAWEI FreeBuds SE 2 Azul',179.00,149.00,129.00,NULL,30,'2025-11-22 23:04:05',1,2,3,'2025-11-22 23:04:05'),(23,'Audífonos inalámbricos verdaderos con cancelación de ruido Samsung Galaxy Buds Live (Mystic Black)',449.00,349.00,299.00,NULL,30,'2025-11-22 23:04:05',1,1,3,'2025-11-22 23:04:05'),(24,'Audífonos Samsung SM-R510NZAADBT Galaxy Buds 2 Pro',699.00,549.00,479.00,NULL,30,'2025-11-22 23:04:05',1,1,3,'2025-11-22 23:04:05'),(25,'Batería Krea 7 Piezas Antiadherente',189.00,159.00,139.00,NULL,30,'2025-11-22 23:04:05',1,21,19,'2025-11-22 23:04:05'),(26,'Bombones con Relleno de Avellanas Ferrero Rocher 8un',24.90,21.90,18.90,NULL,30,'2025-11-22 23:04:05',1,8,21,'2025-11-22 23:04:05'),(27,'Bombones Surtidos Nestlé Multipack 45un',54.90,47.90,42.90,NULL,30,'2025-11-22 23:04:05',1,8,21,'2025-11-22 23:04:05'),(28,'BZBGEAR Universal HDMI-SDI-USB Cámara PTZ de transmisión en vivo con zoom 12x (plata)',2899.00,2499.00,2299.00,NULL,30,'2025-11-22 23:04:05',1,56,6,'2025-11-22 23:04:05'),(29,'Cafetera OSTER 4 Tazas BVSTDCDR5B-053',149.00,129.00,109.00,NULL,30,'2025-11-22 23:04:05',1,23,19,'2025-11-22 23:04:05'),(30,'Casaca Diger Denim Stretch Hombre Pionier',189.00,159.00,139.00,NULL,30,'2025-11-22 23:04:05',1,14,49,'2025-11-22 23:04:05'),(31,'Celular Apple Iphone 13 128GB Negro',3299.00,2899.00,2699.00,NULL,30,'2025-11-23 02:59:38',1,19,1,'2025-11-23 02:59:38'),(32,'Celular Samsung Galaxy A34 5G 128GB Rom 6GB Ram NEGRO',1399.00,1199.00,1049.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(33,'Celular Samsung Galaxy A54 5G 256GB 8GB RAM Negro',1899.00,1649.00,1499.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(34,'Celular Samsung Galaxy S21 Plus 5G 128GB - Púrpura',2999.00,2599.00,2399.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(35,'Celular Samsung Galaxy S23 FE 6.4 256GB 8GB Morado',2499.00,2199.00,1999.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(36,'Celular Samsung S23 Ultra 5G 256GB 12GB Ram Color Lavender',5499.00,4799.00,4499.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(37,'Celular Xiaomi Redmi 13C 6.74 8GB RAM 256GB Negro',699.00,599.00,549.00,NULL,30,'2025-11-23 02:59:38',1,24,1,'2025-11-23 02:59:38'),(38,'Consola Nintendo Switch Modelo Oled Neón',1699.00,1499.00,1399.00,NULL,30,'2025-11-23 02:59:38',1,60,4,'2025-11-23 02:59:38'),(39,'Consola PS5 Slim Con Lector De Disco 1TB',2499.00,2299.00,2199.00,NULL,30,'2025-11-23 02:59:38',1,61,4,'2025-11-23 02:59:38'),(40,'Freidora de Aire OSTER 4L Digital Negro',399.00,349.00,299.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(41,'Freidora de Aire Oster CKSTAF18DDF-053 Digital 1.8L Negro',299.00,259.00,229.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(42,'Horno Microondas Oster POGGM3901M 700W 25 Litros',349.00,299.00,269.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(43,'Impresora Epson L4260 Ecotank',1099.00,949.00,849.00,NULL,30,'2025-11-23 02:59:38',1,30,5,'2025-11-23 02:59:38'),(44,'Iphone 11 6.1 4GB 64GB 12MP Blanco',1999.00,1799.00,1649.00,NULL,30,'2025-11-23 02:59:38',1,19,1,'2025-11-23 02:59:38'),(45,'Juego de Vajilla Krea Opal Flores 16 Piezas',129.00,109.00,94.90,NULL,30,'2025-11-23 02:59:38',1,21,19,'2025-11-23 02:59:38'),(47,'Laptop Lenovo IdeaPad Gaming3 15IAH7 i5-12450H 8GB RAM 512GB SSD RTX3060',4299.00,3799.00,3499.00,NULL,30,'2025-11-23 02:59:38',1,17,5,'2025-11-23 02:59:38'),(48,'Lavadora SAMSUNG Carga Superior 18Kg WA18T6260BV Negro',1899.00,1699.00,1549.00,NULL,30,'2025-11-23 02:59:38',1,1,19,'2025-11-23 02:59:38'),(49,'Leche Condensada GLORIA Doypack 200g',6.50,5.90,4.90,NULL,30,'2025-11-23 02:59:38',1,6,25,'2025-11-23 02:59:38'),(50,'Leche GLORIA UHT Chocolatada Caja 1L',7.90,6.90,5.90,NULL,30,'2025-11-23 02:59:38',1,6,25,'2025-11-23 02:59:38'),(51,'Leche Light GLORIA Lata 390g Paquete 6un',29.90,26.90,23.90,NULL,30,'2025-11-23 02:59:38',1,6,25,'2025-11-23 02:59:38'),(52,'Lenovo HE05 + Reloj Pulsera Digital de REGALO',79.00,69.00,59.00,NULL,30,'2025-11-23 02:59:38',1,17,3,'2025-11-23 02:59:38'),(53,'Licuadora Oster Xpert Series BLST3BCPG con Control de Textura',599.00,519.00,469.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(54,'Mantequilla con Sal Gloria 390g',18.90,16.90,14.90,NULL,30,'2025-11-23 02:59:38',1,6,25,'2025-11-23 02:59:38'),(55,'Mermelada de Fresa Gloria Frasco 1 kg',16.90,14.90,12.90,NULL,30,'2025-11-23 02:59:38',1,6,21,'2025-11-23 02:59:38'),(56,'Olla Arrocera OSTER 1.8L CKSTRC1700R Rojo',169.00,149.00,129.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(57,'Parlante Amazon Alexa Echo Dot 5ta Generación Smart Hub Blanco',249.00,199.00,179.00,NULL,30,'2025-11-23 02:59:38',1,56,3,'2025-11-23 02:59:38'),(58,'Plancha de vapor ligera Oster GCSTBS3802',129.00,109.00,94.90,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(59,'Samsung S22 Ultra 256GB 12GB Borgoña',4299.00,3799.00,3499.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(60,'Refrigeradora OSTER 559L No Frost OS-PSBSME20SSEBDI Black Inox',3499.00,3099.00,2899.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(61,'Refrigeradora Samsung Side by Side RS52B3000M9 PE 490L Gris Metal',3999.00,3599.00,3299.00,NULL,30,'2025-11-23 02:59:38',1,1,19,'2025-11-23 02:59:38'),(62,'Samsung A25 5G 256GB 8GB Negro',1199.00,1049.00,949.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(63,'Samsung Galaxy A25 128Gb 6Ram Blue Light',1099.00,949.00,849.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(64,'Samsung Galaxy S22 Ultra - 12GB RAM + 256GB + Cargador 45W - Borgoña',4499.00,3999.00,3699.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(65,'Samsung Galaxy S24 Plus 512gb 12gb Negro',5299.00,4699.00,4399.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(66,'Samsung Galaxy S24 Ultra 6.8 12GB RAM 256GB - Violeta Titanio+ CARGADOR 45w',5999.00,5399.00,4999.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(67,'Samsung Galaxy S24 Ultra 6.8 12GB RAM 512GB - Negro Titanio + CARGADOR 45w',6499.00,5899.00,5499.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(68,'Samsung Note 10 Plus 5G 256GB 12GB Aurora Glow',2499.00,2199.00,1999.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(69,'Samsung Note 10 Plus 5G 256GB 12GB Negro',2499.00,2199.00,1999.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(70,'Samsung Note 10 Plus 256GB Negro',2299.00,1999.00,1849.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(71,'Samsung Z Fold 5 5G 512GB 12GB Azul',7499.00,6799.00,6299.00,NULL,29,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(72,'Samsung Z Fold 5 5G 512GB 12GB Crema',7499.00,6799.00,6299.00,NULL,30,'2025-11-23 02:59:38',1,1,1,'2025-11-23 02:59:38'),(74,'Sixpack Leche Reconstituida Gloria Lata 395g',32.90,28.90,25.90,NULL,30,'2025-11-23 02:59:38',1,6,25,'2025-11-23 02:59:38'),(75,'Soundbar Bluetooth Samsung 2.0 Ch HW-C400',499.00,429.00,379.00,NULL,30,'2025-11-23 02:59:38',1,1,3,'2025-11-23 02:59:38'),(76,'Tablet LENOVO P11 (2nd Gen) 11 6GB 128GB (uMCP) Storm Grey',1299.00,1149.00,1049.00,NULL,27,'2025-11-23 02:59:38',1,17,2,'2025-11-23 02:59:38'),(77,'Tablet SAMSUNG S6 LITE 10.4 128GB HDD 4GB Gris',1499.00,1299.00,1199.00,NULL,28,'2025-11-23 02:59:38',1,1,2,'2025-11-23 02:59:38'),(78,'Televisor SAMSUNG CRYSTAL UHD 65 UHD 4K Smart Tv UN65CU8000GXPE',3299.00,2899.00,2699.00,NULL,30,'2025-11-23 02:59:38',1,1,7,'2025-11-23 02:59:38'),(79,'Televisor Samsung Smart TV 65 Crystal UHD 4K UN65CU7000GXPE',2999.00,2649.00,2449.00,NULL,30,'2025-11-23 02:59:38',1,1,7,'2025-11-23 02:59:38'),(80,'Tricombo Oster Arrocera + Hervidor + Licuadora',399.00,349.00,299.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(81,'Tri-Combo Oster Licuadora BLSTKAGBPB + Olla Arrocera CKSTRC1700B + Hervidro BVSTKT3101',429.00,379.00,329.00,NULL,30,'2025-11-23 02:59:38',1,23,19,'2025-11-23 02:59:38'),(82,'Vino Tinto Malbec Finca Las Moras Botella 750ml',39.90,34.90,29.90,NULL,30,'2025-11-23 02:59:38',1,3,10,'2025-11-23 02:59:38'),(83,'Whisky Johnnie Walker Blue Label Botella 750ml',899.00,799.00,749.00,NULL,30,'2025-11-23 02:59:38',1,18,10,'2025-11-23 02:59:38'),(84,'Yogurt Bebible Gloria Fresa Botella 1kg',12.90,10.90,8.90,NULL,29,'2025-11-23 02:59:38',1,6,25,'2025-11-23 02:59:38'),(85,'Yogurt Gloria Battimix Vainilla 146g',3.90,3.50,2.90,NULL,28,'2025-11-23 02:59:38',1,6,25,'2025-11-23 02:59:38');
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `redes_sociales`
--

DROP TABLE IF EXISTS `redes_sociales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `redes_sociales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomred` varchar(150) NOT NULL,
  `faicon_red` varchar(30) NOT NULL,
  `enlace` varchar(200) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `redes_sociales`
--

LOCK TABLES `redes_sociales` WRITE;
/*!40000 ALTER TABLE `redes_sociales` DISABLE KEYS */;
INSERT INTO `redes_sociales` VALUES (1,'Facebook','fa-brands fa-facebook','https://www.facebook.com','2024-12-06 22:58:56'),(2,'Twitter','fa-brands fa-twitter','https://www.twitter.com/','2024-12-06 22:58:56'),(3,'Instagram','fa-brands fa-instagram','https://www.instagram.com','2024-12-06 22:58:56'),(4,'Whatsapp','fa-brands fa-whatsapp','https://www.whatsapp.com','2024-12-06 22:58:56'),(5,'TikTok','fa-brands fa-tiktok','https://www.tiktok.com','2024-12-06 22:58:56'),(6,'YouTube','fa-brands fa-youtube','https://www.youtube.com','2024-12-06 22:58:56');
/*!40000 ALTER TABLE `redes_sociales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `secuencia_comprobante`
--

DROP TABLE IF EXISTS `secuencia_comprobante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `secuencia_comprobante` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` enum('boleta','factura') NOT NULL,
  `serie` varchar(4) NOT NULL,
  `ultimo_numero` int NOT NULL DEFAULT '0',
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tipo_serie` (`tipo`,`serie`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `secuencia_comprobante`
--

LOCK TABLES `secuencia_comprobante` WRITE;
/*!40000 ALTER TABLE `secuencia_comprobante` DISABLE KEYS */;
INSERT INTO `secuencia_comprobante` VALUES (1,'boleta','B001',3,'2025-11-22 15:38:43'),(2,'factura','F001',0,'2025-11-22 15:38:43');
/*!40000 ALTER TABLE `secuencia_comprobante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategoria`
--

DROP TABLE IF EXISTS `subcategoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `faicon_subcat` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `categoriaid` int NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fksubcategor822804` (`categoriaid`),
  CONSTRAINT `fksubcategor822804` FOREIGN KEY (`categoriaid`) REFERENCES `categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategoria`
--

LOCK TABLES `subcategoria` WRITE;
/*!40000 ALTER TABLE `subcategoria` DISABLE KEYS */;
INSERT INTO `subcategoria` VALUES (1,'Telefonia','fa-solid fa-mobile-screen-button',1,7,'2024-12-06 22:59:06'),(2,'Tablets','fa-solid fa-tablet',1,7,'2024-12-06 22:59:06'),(3,'Audio','fa-solid fa-headphones',1,7,'2024-12-06 22:59:06'),(4,'Zona Gamer','fa-solid fa-gamepad',1,7,'2024-12-06 22:59:06'),(5,'Computo','fa-solid fa-desktop',1,7,'2024-12-06 22:59:06'),(6,'Fotografia','fa-solid fa-camera',1,7,'2024-12-06 22:59:06'),(7,'Televisores','fa-solid fa-tv',1,7,'2024-12-06 22:59:06'),(8,'Accesorios','fa-solid fa-keyboard',1,7,'2024-12-06 22:59:06'),(9,'Frutas y Verduras','fa-solid fa-apple-whole',1,1,'2024-12-06 22:59:06'),(10,'Bebidas','fa-solid fa-wine-glass',1,1,'2024-12-06 22:59:06'),(11,'Snacks','fa-solid fa-cookie-bite',1,1,'2024-12-06 22:59:06'),(12,'Panaderia y Reposteria','fa-solid fa-bread-slice',1,1,'2024-12-06 22:59:06'),(13,'Desayunos','fa-solid fa-mug-saucer',1,1,'2024-12-06 22:59:06'),(14,'Limpieza','fa-solid fa-broom',1,3,'2024-12-06 22:59:06'),(15,'Cuidado personal','fa-regular fa-file',1,3,'2024-12-06 22:59:06'),(16,'Decoracion','fa-regular fa-file',1,3,'2024-12-06 22:59:06'),(17,'Dormitorio','fa-regular fa-file',1,3,'2024-12-06 22:59:06'),(18,'Juguetes y Juegos','fa-regular fa-file',1,3,'2024-12-06 22:59:06'),(19,'Electrodomésticos','fa-solid fa-blender-phone',1,3,'2024-12-06 22:59:06'),(20,'Papeleria','fa-solid fa-paperclip',1,4,'2024-12-06 22:59:06'),(21,'Abarrotes','fa-regular fa-file',1,1,'2024-12-06 22:59:06'),(22,'Comidas preparadas','fa-solid fa-utensils',1,1,'2024-12-06 22:59:06'),(23,'Congelados','fa-regular fa-file',1,1,'2024-12-06 22:59:06'),(24,'Carnes, Aves y Pescados','fa-regular fa-file',1,1,'2024-12-06 22:59:06'),(25,'Lacteos y Embutidos','fa-solid fa-cow',1,1,'2024-12-06 22:59:06'),(26,'Entrenamiento Y Fitness','fa-regular fa-file',1,2,'2024-12-06 22:59:06'),(27,'Bicicletas','fa-solid fa-bicycle',1,2,'2024-12-06 22:59:06'),(28,'Scooters Y Skates','fa-regular fa-file',1,2,'2024-12-06 22:59:06'),(29,'Accesorios Deportivos','fa-regular fa-file',1,2,'2024-12-06 22:59:06'),(30,'Camping','fa-solid fa-campground',1,2,'2024-12-06 22:59:06'),(31,'Individuales Y De Contacto','fa-solid fa-person',1,2,'2024-12-06 22:59:06'),(32,'En Equipo','fa-solid fa-people-group',1,2,'2024-12-06 22:59:06'),(33,'Acuáticos','fa-solid fa-person-swimming',1,2,'2024-12-06 22:59:06'),(34,'Libros','fa-solid fa-book',1,4,'2024-12-06 22:59:06'),(35,'Arte y Diseño','fa-solid fa-paintbrush',1,4,'2024-12-06 22:59:06'),(36,'Escritorio','fa-regular fa-file',1,4,'2024-12-06 22:59:06'),(37,'Alimento Para Perros','fa-regular fa-file',1,5,'2024-12-06 22:59:06'),(38,'Cuidado Y Limpieza Para Perros','fa-solid fa-shield-dog',1,5,'2024-12-06 22:59:06'),(39,'Accesorios Para Perros','fa-solid fa-dog',1,5,'2024-12-06 22:59:06'),(40,'Ropa Para Perros','fa-regular fa-file',1,5,'2024-12-06 22:59:06'),(41,'Artículos De Transporte Para Perros','fa-regular fa-file',1,5,'2024-12-06 22:59:06'),(42,'Alimento Para Gatos','fa-regular fa-file',1,5,'2024-12-06 22:59:06'),(43,'Cuidado Y Limpieza Para Gatos','fa-solid fa-shield-cat',1,5,'2024-12-06 22:59:06'),(44,'Accesorios Para Gatos','fa-solid fa-cat',1,5,'2024-12-06 22:59:06'),(45,'Ropa Para Gatos','fa-regular fa-file',1,5,'2024-12-06 22:59:06'),(46,'Artículos De Transporte Para Gatos','fa-regular fa-file',1,5,'2024-12-06 22:59:06'),(47,'Zapatillas','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(48,'Pantalones','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(49,'Chaquetas y Abrigos','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(50,'Sandalias','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(51,'Botas','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(52,'Faldas','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(53,'Vestidos','fa-solid fa-person-dress',1,6,'2024-12-06 22:59:06'),(54,'Polos','fa-solid fa-shirt',1,6,'2024-12-06 22:59:06'),(55,'Camisas','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(56,'Zapatos','fa-solid fa-shoe-prints',1,6,'2024-12-06 22:59:06'),(57,'Accesorios de vestimenta','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(58,'Trajes de Baño','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(59,'Poleras','fa-regular fa-file',1,6,'2024-12-06 22:59:06'),(60,'Shorts','fa-regular fa-file',1,6,'2024-12-06 22:59:06');
/*!40000 ALTER TABLE `subcategoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_contenido_info`
--

DROP TABLE IF EXISTS `tipo_contenido_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_contenido_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `faicon_cont` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_contenido_info`
--

LOCK TABLES `tipo_contenido_info` WRITE;
/*!40000 ALTER TABLE `tipo_contenido_info` DISABLE KEYS */;
INSERT INTO `tipo_contenido_info` VALUES (1,'Terminos y Condiciones','Infórmate sobre los términos y condiciones en Domus, incluyendo detalles sobre nuestras políticas de compra y venta.','fa-solid fa-file-contract',1,'2024-12-06 22:58:56'),(2,'Puntos de venta','Localiza nuestras tiendas físicas y conoce más sobre los servicios y productos disponibles en cada punto de venta.','fa-solid fa-store',1,'2024-12-06 22:58:56'),(3,'Pregunta Frecuentes','Encuentra respuestas a las preguntas más comunes sobre nuestra tienda para una mejor experiencia de compra.','fa-solid fa-circle-question',1,'2024-12-06 22:58:56'),(4,'Devoluciones y Cambios','Obtén información detallada sobre cómo realizar devoluciones y cambios de productos comprados en Domus Market.','fa-solid fa-undo-alt',1,'2024-12-06 22:58:56'),(5,'Garantias','Accede a la información acerca de garantía legal y garantía extendida de Domus Market, así como de otras marcas.','fa-solid fa-shield-alt',1,'2024-12-06 22:58:56'),(6,'Reclamos','Entérate sobre el proceso que seguimos para resolver cualquier inconveniente con nuestros productos o servicios.','fa-solid fa-bullhorn',1,'2024-12-06 22:58:56');
/*!40000 ALTER TABLE `tipo_contenido_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_img_novedad`
--

DROP TABLE IF EXISTS `tipo_img_novedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_img_novedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_img_novedad`
--

LOCK TABLES `tipo_img_novedad` WRITE;
/*!40000 ALTER TABLE `tipo_img_novedad` DISABLE KEYS */;
INSERT INTO `tipo_img_novedad` VALUES (1,'Banner',1,'2024-12-06 22:58:50'),(2,'Cuadro',1,'2024-12-06 22:58:50'),(3,'Rectangulo Vertical',1,'2024-12-06 22:58:50'),(4,'Rectangulo Horizontal',1,'2024-12-06 22:58:50'),(5,'Foto Adicional',1,'2024-12-06 22:58:50');
/*!40000 ALTER TABLE `tipo_img_novedad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_novedad`
--

DROP TABLE IF EXISTS `tipo_novedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_novedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomtipo` varchar(55) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_novedad`
--

LOCK TABLES `tipo_novedad` WRITE;
/*!40000 ALTER TABLE `tipo_novedad` DISABLE KEYS */;
INSERT INTO `tipo_novedad` VALUES (1,'Anuncios',1,'2024-12-06 22:58:50'),(2,'Avisos',1,'2024-12-06 22:58:50'),(3,'Promociones',1,'2024-12-06 22:58:50');
/*!40000 ALTER TABLE `tipo_novedad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_usuario`
--

DROP TABLE IF EXISTS `tipo_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(55) NOT NULL,
  `imagen` text NOT NULL,
  `descripcion` varchar(300) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL,
  `registro_auditoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_usuario`
--

LOCK TABLES `tipo_usuario` WRITE;
/*!40000 ALTER TABLE `tipo_usuario` DISABLE KEYS */;
INSERT INTO `tipo_usuario` VALUES (1,'Administrativo','','Administrador del sistema, no puede hacer compras, puede crear empleados',1,'2024-11-23 00:11:16'),(2,'Empleado','','Trabajador, solo puede gestionar marcas, productos y novedades',1,'2024-11-23 00:11:16'),(3,'Cliente','','Puede hacer compras, escoger productos para su lista de deseos, escoger su foto de perfil, cambiar su contraseña ',1,'2024-11-23 00:11:16');
/*!40000 ALTER TABLE `tipo_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `doc_identidad` varchar(15) NOT NULL,
  `img_usuario` text,
  `genero` tinyint(1) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Fabiana juas','Paucar Delgado','74125896',NULL,1,'2002-08-15','987654321','fabiana@mail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 23:00:32',3,'2024-12-06 23:00:32'),(2,'María','López Díaz','32434324324',NULL,0,'1985-08-22','555654321','maria.lopez@hotmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 23:00:32',3,'2024-12-06 23:00:32'),(3,'Carlos','Fernández Romerito','98765433',NULL,1,'2005-01-01','987654273','carlos.fernandez@yahoo.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',0,'2024-12-06 23:00:32',1,'2024-12-06 23:00:32'),(4,'Ana','Martínez Sánchez','72534282',NULL,0,'1988-12-30','555098765','ana.martinez@outlook.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 23:00:32',2,'2024-12-06 23:00:32'),(5,'Pedro','Gómez Ruiz','82340343',NULL,1,'1995-07-07','555876543','pedro.gomez@gmail.com','654321',1,'2024-12-06 23:00:32',3,'2024-12-06 23:00:32'),(6,'Franciso','Vazquez Fernanzdez','12356789',NULL,1,'2024-12-05','988838348','abc@xd.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 13:23:36',3,'2024-12-06 17:34:32'),(7,'Emilia','Paucar','33333333',NULL,0,'2024-12-03','987987585','aaaa@domus.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 14:17:05',2,'2024-12-06 16:13:07'),(8,'FULANO','bbbbbbb','99999999',NULL,1,'2024-12-12','944412121','fwefwef@DAWD.NB','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 18:30:41',3,'2024-12-06 20:20:44'),(9,'asdsa','dsaadsad','43434232',NULL,1,'2024-12-03','987654321','aaaa@eeee.es','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 20:28:26',3,'2024-12-06 20:29:37'),(10,'Carlos','Gómez','73546392',NULL,1,'1990-05-15','923743243','carlos_gomez@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 23:39:51',1,'2024-12-06 23:39:51'),(11,'Ana','López','73546387',NULL,2,'1985-08-20','923743233','ana_lopez@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 23:39:51',2,'2024-12-06 23:39:51'),(12,'Luis','Martínez','73946887',NULL,1,'2000-12-01','936743243','luis_martinez@hotmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-06 23:39:51',3,'2024-12-06 23:39:51'),(14,'María','Larrea','87958522',NULL,0,'2024-12-11','2324242423','maria@domus.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 00:13:48',2,'2024-12-07 00:13:48'),(16,'Franco','Cortez','87923563',NULL,1,'2005-01-01','954534654','franco@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 00:51:51',3,'2024-12-07 00:51:51'),(17,'Fabrizio','Curos','74185296',NULL,1,'2004-06-10','987654321','fabrizio@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 01:19:34',3,'2024-12-07 01:19:34'),(18,'Juan','Perez','73463743',NULL,1,'1995-01-19','974357353','juanperez@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 02:29:38',3,'2024-12-07 02:29:38'),(20,'Junior','Perez','74295872',NULL,1,'2004-09-14','948938578','perezdj0904@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 03:10:13',3,'2024-12-07 03:10:13'),(30,'Juan','Perez','99999999',NULL,1,'2024-12-12','944412121','juan_perez@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 03:31:12',1,'2024-12-07 03:31:12'),(31,'hola','adios','21321321',NULL,1,'2024-12-03','942342343','aaaa2a@sww','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 03:32:41',2,'2024-12-07 03:32:41'),(32,'Junior','yopsquienmas','12312311',NULL,1,'2000-12-12','946666666','yo@yo.yo','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 03:40:49',2,'2024-12-07 03:40:49'),(33,'ASDAS','ApellidosASDAS','74295872',NULL,1,'2024-11-19','952145632','pep@pep.pep','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 03:53:21',3,'2024-12-07 03:53:21'),(34,'Leonardo','Zuñiga','876833653',NULL,1,'2005-09-23','978541294','leozzzz@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2024-12-07 06:12:46',2,'2024-12-07 06:12:46'),(35,'Fabiana Lucía','Paucar Mejía','72428857',NULL,0,NULL,'999888777','fabianapm060126@gmail.com','84f307d9e4d62ba1b450c8bdeb539337fbee096622da09d1e33a486794e4634e',1,'2025-11-22 17:23:17',3,'2025-11-22 17:23:17'),(36,'Faustina','Mejía Alarcon','72422857',NULL,0,NULL,'999888707','faustina@gmail.com','ca48859a13f407975f7292107cf296409b91971fb2ff9f50e5950ed1279154dc',1,'2025-11-22 17:32:32',3,'2025-11-22 17:32:32'),(37,'Fiorela','Mejía Alarcon','72422857',NULL,0,NULL,'999888707','luana@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2025-11-22 17:33:08',3,'2025-11-22 17:33:08'),(38,'Jshsjs','Hbbbvv','64904844',NULL,0,NULL,'948484848','francocor0105@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2025-11-23 05:43:07',3,'2025-11-23 05:43:07'),(39,'Franxnxb','Coorkrb','94845484',NULL,0,NULL,'694840484','framcor0105@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2025-11-23 05:48:42',3,'2025-11-23 05:48:42'),(40,'Fr','Co','88555666',NULL,0,NULL,'996654178','franco05@gmail.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1,'2025-11-23 05:57:14',3,'2025-11-23 05:57:14'),(41,'Franco','Cortez','72567474',NULL,2,NULL,'941634214','francocr0105@gmail.com','3d66f31308c7159b94a83d1a81f1844e457b797292fa6b7918099813b9ef41e1',1,'2025-11-23 21:47:32',3,'2025-11-23 21:47:32');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-23 22:44:38
