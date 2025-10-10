
INSERT INTO `tipo_usuario` (`id`, `tipo`, `imagen`, `descripcion`, `disponibilidad`, `registro_auditoria`) VALUES
(1, 'Administrativo', '', 'Administrador del sistema, no puede hacer compras, puede crear empleados', 1, '2024-11-22 19:11:16'),
(2, 'Empleado', '', 'Trabajador, solo puede gestionar marcas, productos y novedades', 1, '2024-11-22 19:11:16'),
(3, 'Cliente', '', 'Puede hacer compras, escoger productos para su lista de deseos, escoger su foto de perfil, cambiar su contraseña ', 1, '2024-11-22 19:11:16');

INSERT INTO `marca` (`id`, `marca`, `img_logo`, `img_banner`, `fecha_registro`, `disponibilidad`, `registro_auditoria`) VALUES
(1, 'Samsung', '', '', '2024-11-01 05:00:00', 1, '2024-12-06 23:00:39'),
(2, 'Huawei', '', '', '2024-09-17 05:00:00', 1, '2024-12-06 23:00:53'),
(3, 'Tabernero', '', '', '2024-09-10 05:00:00', 1, '2024-12-06 23:00:54'),
(4, 'Primor', '', '', '2024-09-01 05:00:00', 1, '2024-12-06 23:03:56'),
(5, 'Pedigree', '', '', '2024-08-22 05:00:00', 1, '2024-12-06 23:03:56'),
(6, 'Gloria', '', '', '2024-07-04 05:00:00', 1, '2024-12-06 23:04:12'),
(7, 'Coca Cola', '', '', '2024-09-17 05:00:00', 1, '2024-12-06 23:04:13'),
(8, 'Nestle', '', '', '2024-10-08 05:00:00', 1, '2024-12-06 23:09:21'),
(9, 'LG', '', '', '2024-07-05 05:00:00', 1, '2024-12-06 23:04:26'),
(10, 'Hasbro', '', '', '2024-10-10 05:00:00', 1, '2024-12-06 23:04:52'),
(12, 'Adidas', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(13, 'Artesco', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(14, 'Pionier', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(15, 'Inca Kola', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(16, 'Braedt', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(17, 'Lenovo', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(18, 'Johnnie Walker', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(19, 'Apple', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(20, 'Costa', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(21, 'Krea', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(22, 'Nivea', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(23, 'Oster', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(24, 'Xiaomi', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(25, 'Costeño', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(26, 'Motorola', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(27, 'Laive', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(28, 'BlackLine', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(29, 'Alacena', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(30, 'HP', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(31, 'Imaco', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(32, 'Ricocan', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(33, 'Asus', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(34, 'Kirma', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(35, 'Suave', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(36, 'Corona', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(37, 'Nike', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(38, 'San Carlos', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(39, 'Pantene', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(40, 'Don Vitorio', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(41, 'SuperCat', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(42, 'P&G', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(43, 'Field', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(44, 'North Star', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(45, 'Standford', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(46, 'Puma', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(47, 'Oreo', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(48, 'LEGO', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(49, 'I-run', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(50, 'Glacial', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(51, 'Altomayo', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(52, 'AXE', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(53, 'Clorox', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(54, 'Old Spice', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(55, 'Pegafan', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(56, 'Logitech', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(57, 'Mattel', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(58, 'Faber-Castell', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(59, 'Sapolio', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(60, 'Nintendo', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(61, 'Sony', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(62, 'Panasonic', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(63, 'QuickSilver', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(64, 'Frugos del Valle', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(65, 'Paraiso', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19'),
(66, 'Walon', '', '', '2025-10-10 05:26:19', 1, '2025-10-10 05:26:19');



INSERT INTO `usuario` VALUES 
(1,'Juan','Pérez García','73792534',NULL,1,'1990-05-15','555123456','juan.perez@gmail.com','password123',1,'2024-12-06 18:00:32',3,'2024-12-06 18:00:32'),
(2,'María','López Díaz','32434324324',NULL,0,'1985-08-22','555654321','maria.lopez@hotmail.com','securepass456',1,'2024-12-06 18:00:32',3,'2024-12-06 18:00:32'),
(3,'Carlos','Fernández Romero','32423434',NULL,1,'1992-02-10','555789012','carlos.fernandez@yahoo.com','carlospass789',0,'2024-12-06 18:00:32',1,'2024-12-06 18:00:32'),
(4,'Ana','Martínez Sánchez','72534282',NULL,0,'1988-12-30','555098765','ana.martinez@outlook.com','anapass987',1,'2024-12-06 18:00:32',2,'2024-12-06 18:00:32'),
(5,'Pedro','Gómez Ruiz','82340343',NULL,1,'1995-07-07','555876543','pedro.gomez@gmail.com','pedropass123',1,'2024-12-06 18:00:32',3,'2024-12-06 18:00:32'),
(6,'Franciso','Vazquez Fernanzdez','12356789',NULL,1,'2024-12-05','988838348','abc@xd.com','c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646',1,'2024-12-06 08:23:36',3,'2024-12-06 12:34:32'),
(7,'Emilia','Paucar','33333333',NULL,0,'2024-12-03','987987585','aaaa@domus.com','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5',1,'2024-12-06 09:17:05',2,'2024-12-06 11:13:07'),
(8,'FULANO','bbbbbbb','99999999',NULL,1,'2024-12-12','944412121','fwefwef@DAWD.NB','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5',1,'2024-12-06 13:30:41',3,'2024-12-06 15:20:44'),
(9,'asdsa','dsaadsad','43434232',NULL,1,'2024-12-03','987654321','aaaa@eeee.es','9a900403ac313ba27a1bc81f0932652b8020dac92c234d98fa0b06bf0040ecfd',1,'2024-12-06 15:28:26',3,'2024-12-06 15:29:37'),
(10,'Carlos','Gómez','73546392',NULL,1,'1990-05-15','923743243','carlos_gomez@gmail.com','73e98b7ae50347e4b92c61141f20da128ba062736d62e782cab425e0fc0115c8',1,'2024-12-06 18:39:51',1,'2024-12-06 18:39:51'),
(11,'Ana','López','73546387',NULL,2,'1985-08-20','923743233','ana_lopez@gmail.com','15bd809740b59f76f2686dd9bff0933ab70c52e4031e16da60947a5ec5165edc',1,'2024-12-06 18:39:51',2,'2024-12-06 18:39:51'),
(12,'Luis','Martínez','73946887',NULL,1,'2000-12-01','936743243','luis_martinez@hotmail.com','ff1e8003c35664806cdd7711061bcdc8922a77e4a835e556c2000af964a29998',1,'2024-12-06 18:39:51',3,'2024-12-06 18:39:51'),
(13,'Fabiana','Paucar Mejia','63278498',NULL,1,'2005-01-01','987567435','fabianapm060126@gmail.com','53ad146c33c33a8619e839edb7abd9638178287f39d82f35d41c17d96b62885f',1,'2024-12-06 19:09:19',3,'2024-12-06 19:09:19'),
(14,'María','Larrea','87958522',NULL,0,'2024-12-11','2324242423','maria@domus.com','054e3b308708370ea029dc2ebd1646c498d59d7203c9e1a44cf0484df98e581a',1,'2024-12-06 19:13:48',2,'2024-12-06 19:13:48'),
(16,'Franco','Cortez','87923563',NULL,1,'2005-01-01','954534654','franco@gmail.com','c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646',1,'2024-12-06 19:51:51',3,'2024-12-06 19:51:51'),
(17,'Fabrizio','Curos','74185296',NULL,1,'2004-06-10','987654321','fabrizio@gmail.com','819c52a063a8f4fc1095d661e35dd4b05d885882dcf6bdb81092c3debd6d398d',1,'2024-12-06 20:19:34',3,'2024-12-06 20:19:34'),
(18,'Juan','Perez','73463743',NULL,1,'1995-01-19','974357353','juanperez@gmail.com','46b2150accc75b4ae7b461fe4f5dde39512d2e034ee4d91df9c09b9bd0e090c9',1,'2024-12-06 21:29:38',3,'2024-12-06 21:29:38'),
(20,'Junior','Perez','74295872',NULL,1,'2004-09-14','948938578','perezdj0904@gmail.com','bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a',1,'2024-12-06 22:10:13',3,'2024-12-06 22:10:13'),
(30,'Juan','Perez','99999999',NULL,1,'2024-12-12','944412121','juan_perez@gmail.com','c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646',1,'2024-12-06 22:31:12',1,'2024-12-06 22:31:12'),
(31,'hola','adios','21321321',NULL,1,'2024-12-03','942342343','aaaa2a@sww','96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',1,'2024-12-06 22:32:41',2,'2024-12-06 22:32:41'),
(32,'Junior','yopsquienmas','12312311',NULL,1,'2000-12-12','946666666','yo@yo.yo','96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',1,'2024-12-06 22:40:49',2,'2024-12-06 22:40:49'),
(33,'ASDAS','ApellidosASDAS','74295872',NULL,1,'2024-11-19','952145632','pep@pep.pep','96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',1,'2024-12-06 22:53:21',3,'2024-12-06 22:53:21'),
(34,'Leonardo','Zuñiga','876833653',NULL,1,'2005-09-23','978541294','leozzzz@gmail.com','b02ac0aab6c3c1e025be26609555cf39b6e449e38e5a3f66ebdce1c1f4d10dfa',1,'2024-12-07 01:12:46',2,'2024-12-07 01:12:46');



INSERT INTO `categoria` VALUES 
(1,'Alimentos','fa-solid fa-drumstick-bite',1,'2024-12-06 17:59:06'),
(2,'Deportes','fa-solid fa-person-running',1,'2024-12-06 17:59:06'),
(3,'Hogar','fa-solid fa-house-chimney',1,'2024-12-06 17:59:06'),
(4,'Libreria y Oficina','fa-solid fa-book',1,'2024-12-06 17:59:06'),
(5,'Mascotas','fa-solid fa-paw',1,'2024-12-06 17:59:06'),
(6,'Ropa y Calzado','fa-solid fa-shirt',1,'2024-12-06 17:59:06'),
(7,'Tecnologia','fa-solid fa-microchip',1,'2024-12-06 17:59:06');


INSERT INTO `caracteristica` VALUES 
(1,'Carga rápida',1,'2024-12-06 17:59:17'),
(2,'Cámara Frontal',1,'2024-12-06 17:59:17'),
(3,'Color',1,'2024-12-06 17:59:17'),
(4,'Entrada carga',1,'2024-12-06 17:59:17'),
(5,'Pantalla',1,'2024-12-06 17:59:17'),
(6,'RAM',1,'2024-12-06 17:59:17'),(7,'Almacenamiento',1,'2024-12-06 17:59:17'),
(8,'Cámara posterior',1,'2024-12-06 17:59:17'),
(9,'Procesador',1,'2024-12-06 17:59:17'),(10,'Modelo',1,'2024-12-06 17:59:17'),(11,'Batería',1,'2024-12-06 17:59:17'),(12,'Sistema operativo',1,'2024-12-06 17:59:17'),
(13,'Resolución de pantalla',1,'2024-12-06 17:59:17'),
(14,'Tamaño de pantalla',1,'2024-12-06 17:59:17'),(15,'Capacidad de la batería',1,'2024-12-06 17:59:17'),
(16,'Tipo de red',1,'2024-12-06 17:59:17'),(17,'Capacidad de carga rápida',1,'2024-12-06 17:59:17'),
(18,'Sensor de huellas dactilares',1,'2024-12-06 17:59:17'),
(19,'Protección contra agua/polvo',1,'2024-12-06 17:59:17'),
(20,'Resolución de pantalla',1,'2024-12-06 17:59:17'),(21,'Tamaño de pantalla',1,'2024-12-06 17:59:17'),
(22,'Almacenamiento interno',1,'2024-12-06 17:59:17'),(23,'Memoria RAM',1,'2024-12-06 17:59:17'),
(24,'Conectividad',1,'2024-12-06 17:59:17'),
(25,'Duración de la batería',1,'2024-12-06 17:59:17'),
(26,'Soporte para lápiz óptico',1,'2024-12-06 17:59:17'),(27,'Sistema operativo',1,'2024-12-06 17:59:17'),(28,'Tipo de conectividad',1,'2024-12-06 17:59:17'),
(29,'Duración de la batería',1,'2024-12-06 17:59:17'),
(30,'Cancelación de ruido',1,'2024-12-06 17:59:17'),(31,'Compatibilidad con asistentes de voz',1,'2024-12-06 17:59:17'),(32,'Rango de frecuencia',1,'2024-12-06 17:59:17'),(33,'Potencia de salida',1,'2024-12-06 17:59:17'),(34,'Impermeabilidad',1,'2024-12-06 17:59:17'),(35,'Resolución de pantalla',1,'2024-12-06 17:59:17'),(36,'Tipo de teclado',1,'2024-12-06 17:59:17'),(37,'DPI',1,'2024-12-06 17:59:17'),(38,'Capacidad de respuesta',1,'2024-12-06 17:59:17'),(39,'Compatibilidad con consolas/PC',1,'2024-12-06 17:59:17'),(40,'Tipo de conexión',1,'2024-12-06 17:59:17'),(41,'Tipo de procesador',1,'2024-12-06 17:59:17'),(42,'Procesador',1,'2024-12-06 17:59:17'),(43,'Memoria RAM',1,'2024-12-06 17:59:17'),(44,'Disco duro',1,'2024-12-06 17:59:17'),(45,'Tarjeta gráfica',1,'2024-12-06 17:59:17'),(46,'Sistema operativo',1,'2024-12-06 17:59:17'),(47,'Tamaño de pantalla',1,'2024-12-06 17:59:17'),(48,'Resolución de pantalla',1,'2024-12-06 17:59:17'),(49,'Conectividad',1,'2024-12-06 17:59:17'),(50,'Resolución de cámara',1,'2024-12-06 17:59:17'),(51,'Tipo de lente',1,'2024-12-06 17:59:17'),(52,'Tamaño del sensor',1,'2024-12-06 17:59:17'),(53,'Capacidad de grabación en 4K',1,'2024-12-06 17:59:17'),(54,'Tipo de batería',1,'2024-12-06 17:59:17'),(55,'Almacenamiento compatible',1,'2024-12-06 17:59:17'),(56,'Modo manual/automático',1,'2024-12-06 17:59:17'),(57,'Tamaño de pantalla',1,'2024-12-06 17:59:17'),(58,'Resolución',1,'2024-12-06 17:59:17'),(59,'Tipo de panel',1,'2024-12-06 17:59:17'),(60,'Tasa de refresco',1,'2024-12-06 17:59:17'),(61,'Soporte para HDR',1,'2024-12-06 17:59:17'),(62,'Conectividad (HDMI, USB)',1,'2024-12-06 17:59:17'),(63,'Sistemas de sonido integrados',1,'2024-12-06 17:59:17'),(64,'Sistema operativo',1,'2024-12-06 17:59:17'),(65,'Tipo de conexión',1,'2024-12-06 17:59:17'),(66,'Compatibilidad (USB, Bluetooth)',1,'2024-12-06 17:59:17'),(67,'Autonomía de la batería',1,'2024-12-06 17:59:17'),(68,'Tamaño o dimensiones',1,'2024-12-06 17:59:17'),
(69,'Material de fabricación',1,'2024-12-06 17:59:17'),
(70,'Funciones adicionales (RGB, teclas programables)',1,'2024-12-06 17:59:17');



INSERT INTO `informacion_domus` VALUES 
(1,'servicioalcliente@domus.pe','074 606240', '' ,'' ,
'Con un enfoque meticuloso en la satisfacción del cliente y la excelencia en la oferta de productos, el Supermercado Domus sentó las bases de lo que se convertiría en una empresa líder en la industria de supermercados en el país.\r\n\r\n',
'Desde sus inicios, el Supermercado Domus se destacó por su compromiso con la calidad y la atención al cliente. Cultivó relaciones sólidas con proveedores locales y nacionales para garantizar la frescura y variedad de sus productos. Este enfoque se convirtió en el sello distintivo de Domus, estableciendo una base de confianza y lealtad entre la clientela. Con el tiempo, el Supermercado Domus identificó oportunidades de expansión y diversificación, ampliando tanto la variedad de productos como la infraestructura física de sus establecimientos. Esta expansión estratégica permitió a Domus atender a una base de clientes cada vez más amplia, consolidando su posición como referente en la industria.\r\n\r\n',
'Al año 2026 convertirnos en el supermercado preferido por las familias en la región Lambayeque, reconocido no solo por la calidad superior de nuestros productos y servicios, sino también por nuestra innovación constante, nuestro compromiso con la sostenibilidad y nuestro impacto positivo en las comunidades locales. Aspiramos a ser un ejemplo de excelencia en el comercio minorista, ofreciendo una experiencia de compra que no solo satisfaga, sino que deleite y fidelice a nuestros clientes.\r\n\r\n',
'- Responsabilidad\r\n- Colaboración\r\n- Integridad\r\n- Empatía\r\n- Prudencia\r\n- Fortaleza',
'Ofrecer a nuestros clientes una experiencia de compra única y agradable, caracterizada por una amplia variedad de productos frescos y de alta calidad, un servicio al cliente excepcional y un compromiso con la sostenibilidad y el apoyo a proveedores locales. Nos esforzamos por ser el supermercado preferido de las familias, ofreciendo precios competitivos y fomentando un entorno de trabajo inclusivo y respetuoso para nuestros empleados.\r\n\r\n',
'2024-12-06 17:59:46');


INSERT INTO `cupon` VALUES 
(1,'DOMUSESMICASA50','2025-01-01','2024-11-28',20.00,'2024-11-05 00:00:00',1,'2024-12-06 17:58:50');



INSERT INTO `estado_pedido` VALUES 
(1,'En proceso','2024-12-06 17:58:50'),
(2,'Comprado','2024-12-06 17:58:50');


INSERT INTO `metodo_pago` VALUES (1,'Tarjeta de Débito',1,'2024-12-06 17:58:50'),(2,'Tarjeta de Crédito',1,'2024-12-06 17:58:50'),(3,'Billetera Digital',1,'2024-12-06 17:58:50'),(4,'Efectivo',1,'2024-12-06 17:58:50');


INSERT INTO `motivo_comentario` VALUES (1,'Queja o Reclamo',1,'2024-12-06 17:58:50'),(2,'Fallo en el Sistema',1,'2024-12-06 17:58:50'),(3,'Error al Iniciar Sesion',1,'2024-12-06 17:58:50'),(4,'Pagina No disponible',1,'2024-12-06 17:58:50'),(5,'Error al Comprar',1,'2024-12-06 17:58:50'),(6,'Pedido no Entregado',1,'2024-12-06 17:58:50');


INSERT INTO `tipo_img_novedad` VALUES (1,'Banner',1,'2024-12-06 17:58:50'),(2,'Cuadro',1,'2024-12-06 17:58:50'),(3,'Rectangulo Vertical',1,'2024-12-06 17:58:50'),(4,'Rectangulo Horizontal',1,'2024-12-06 17:58:50'),(5,'Foto Adicional',1,'2024-12-06 17:58:50');





INSERT INTO `tipo_novedad` VALUES (1,'Anuncios',1,'2024-12-06 17:58:50'),(2,'Avisos',1,'2024-12-06 17:58:50'),(3,'Promociones',1,'2024-12-06 17:58:50');


INSERT INTO `tipo_contenido_info` VALUES (1,'Terminos y Condiciones','Infórmate sobre los términos y condiciones en Domus, incluyendo detalles sobre nuestras políticas de compra y venta.','fa-solid fa-file-contract',1,'2024-12-06 17:58:56'),(2,'Puntos de venta','Localiza nuestras tiendas físicas y conoce más sobre los servicios y productos disponibles en cada punto de venta.','fa-solid fa-store',1,'2024-12-06 17:58:56'),(3,'Pregunta Frecuentes','Encuentra respuestas a las preguntas más comunes sobre nuestra tienda para una mejor experiencia de compra.','fa-solid fa-circle-question',1,'2024-12-06 17:58:56'),(4,'Devoluciones y Cambios','Obtén información detallada sobre cómo realizar devoluciones y cambios de productos comprados en Domus Market.','fa-solid fa-undo-alt',1,'2024-12-06 17:58:56'),(5,'Garantias','Accede a la información acerca de garantía legal y garantía extendida de Domus Market, así como de otras marcas.','fa-solid fa-shield-alt',1,'2024-12-06 17:58:56'),(6,'Reclamos','Entérate sobre el proceso que seguimos para resolver cualquier inconveniente con nuestros productos o servicios.','fa-solid fa-bullhorn',1,'2024-12-06 17:58:56');


INSERT INTO `comentario` VALUES (1,'Junior','yopsquienmas','yuliver_max@hotmail.com','946666666','VENGO A RECLAMAR MIS DERECHOS COMO CONSUMIDOR','2024-12-06 22:30:07',0,1,NULL,'2024-12-06 22:30:07');


INSERT INTO `contenido_info` VALUES (1,'Generalidades','Estos términos y condiciones regulan el uso del sitio web de Domus Market y la compra de productos a través del mismo.\r\n\r\n',1,'2024-12-06 17:59:17'),(2,'Registro','Para realizar compras, debes registrarte proporcionando información veraz y actualizada. Es tu responsabilidad mantener la confidencialidad de tu cuenta.\r\n\r\n',1,'2024-12-06 17:59:17'),(3,'Pedidos','Todos los pedidos están sujetos a disponibilidad de stock. Nos reservamos el derecho de cancelar o rechazar un pedido por cualquier motivo.\r\n\r\n',1,'2024-12-06 17:59:17'),(4,'Precios y Pagos\r\n','Los precios están sujetos a cambios sin previo aviso. Aceptamos varios métodos de pago, incluyendo tarjetas de crédito y débito.\r\n\r\n',1,'2024-12-06 17:59:17'),(5,'Envíos y Entregas','Ofrecemos envíos a nivel nacional. Los tiempos de entrega pueden variar según la ubicación y disponibilidad del producto.',1,'2024-12-06 17:59:17'),(6,'Devoluciones y Cambios','Consulta nuestra política de devoluciones para más detalles sobre cómo devolver o cambiar un producto.',1,'2024-12-06 17:59:17'),(7,'Privacidad','Nos comprometemos a proteger tu privacidad. Consulta nuestra política de privacidad para más información.',1,'2024-12-06 17:59:17'),(8,'Modificaciones','Nos reservamos el derecho de modificar estos términos en cualquier momento. Los cambios serán efectivos una vez publicados en nuestro sitio web.',1,'2024-12-06 17:59:17'),(9,'Lima','Dirección: Av. Javier Prado 1234, San Isidro\r\n\r\nTeléfono: 01 2345678\r\n\r\nHorario: Lun-Sab 9:00am - 9:00pm, Dom 10:00am - 6:00pm',2,'2024-12-06 17:59:17'),(10,'Arequipa','Dirección: Av. Ejército 567, Cayma\r\n\r\nTeléfono: 054 234567\r\n\r\nHorario: Lun-Sab 9:00am - 8:00pm, Dom 10:00am - 5:00pm',2,'2024-12-06 17:59:17'),(11,'Trujillo','Dirección: Av. España 890, Trujillo\r\n\r\nTeléfono: 044 234567\r\n\r\nHorario: Lun-Sab 9:00am - 7:00pm, Dom 10:00am - 4:00pm',2,'2024-12-06 17:59:17'),(12,'¿Cómo puedo realizar una compra?\r\n','Para realizar una compra, simplemente navega por nuestro catálogo, añade los productos al carrito y sigue el proceso de pago. Asegúrate de estar registrado y haber iniciado sesión.',3,'2024-12-06 17:59:17'),(13,'¿Qué métodos de pago aceptan?','Aceptamos pagos con tarjetas de crédito y débito (Visa, MasterCard, American Express), así como pagos mediante transferencias bancarias y pagos contra entrega en algunas ubicaciones.',3,'2024-12-06 17:59:17'),(14,'¿Cuánto tiempo tarda en llegar mi pedido?','El tiempo de entrega varía según la ubicación. Generalmente, los pedidos se entregan entre 3 y 7 días hábiles. Durante promociones o eventos especiales, este tiempo puede extenderse.',3,'2024-12-06 17:59:17'),(15,'¿Puedo devolver un producto?','Sí, aceptamos devoluciones dentro de los 30 días posteriores a la compra. El producto debe estar en su estado original y con el empaque intacto. Consulta nuestra política de devoluciones para más detalles.',3,'2024-12-06 17:59:17'),(16,'¿Cómo puedo contactar al servicio al cliente?','Puedes contactarnos a través de nuestro formulario de contacto en la página web, enviándonos un correo electrónico a servicioalcliente@domus.pe o llamándonos al 074 606240.',3,'2024-12-06 17:59:17'),(17,'Devoluciones','Los productos pueden ser devueltos dentro de los 30 días posteriores a la compra. Deben estar en su estado original, sin signos de uso y en su empaque original.\r\n\r\n',4,'2024-12-06 17:59:17'),(18,'Cambios','Si necesitas cambiar un producto por otra talla, color o modelo, puedes hacerlo dentro de los 30 días posteriores a la compra. El producto debe estar en perfecto estado.',4,'2024-12-06 17:59:17'),(19,'Proceso de Devolución\r\n','Para iniciar una devolución, sigue estos pasos:\r\n\r\n- Contacta a nuestro servicio al cliente a través de servicioalcliente@domus.pe o al 074 606240.\r\n- Proporciona tu número de pedido y el motivo de la devolución.\r\n- Empaca el producto en su empaque original junto con todos los accesorios y etiquetas.\r\n- Envía el paquete a la dirección proporcionada por nuestro equipo de servicio al cliente.',4,'2024-12-06 17:59:17'),(20,'Reembolsos','Los reembolsos se procesarán una vez que hayamos recibido y revisado el producto devuelto. El reembolso se realizará a través del mismo método de pago utilizado en la compra original.\r\n\r\n',4,'2024-12-06 17:59:17'),(21,'Excepciones','Algunos productos, como los artículos personalizados o perecederos, no son elegibles para devoluciones o cambios. Consulta nuestra política completa para más detalles.\r\n\r\n',4,'2024-12-06 17:59:17'),(22,'Garantía Legal','Todos los productos cuentan con una garantía legal de 6 meses contra defectos de fabricación. Esta garantía cubre reparaciones y, en algunos casos, reemplazos del producto.\r\n\r\n\r\n',5,'2024-12-06 17:59:17'),(23,'Garantía del Fabricante','Adicionalmente, muchos de nuestros productos cuentan con una garantía del fabricante que puede variar entre 1 y 3 años. Consulta la documentación del producto para más detalles.',5,'2024-12-06 17:59:17'),(24,'Garantía Extendida','Ofrecemos la opción de adquirir garantías extendidas para ciertos productos. Estas garantías amplían la cobertura más allá del período estándar.\r\n\r\n',5,'2024-12-06 17:59:17'),(25,'Contacto Inicial','Contacta a nuestro servicio al cliente a través de servicioalcliente@domus.pe o al 074 606240 para reportar tu reclamo. Proporciona todos los detalles posibles, incluyendo tu número de pedido y una descripción del problema.\r\n\r\n',6,'2024-12-06 17:59:17'),(26,'Revisión del Reclamo','Nuestro equipo revisará tu reclamo y te proporcionará una respuesta dentro de los 5 días hábiles. En algunos casos, puede ser necesario solicitar información adicional o pruebas para procesar tu reclamo.',6,'2024-12-06 17:59:17'),(27,'Resolución','Una vez revisado, te ofreceremos una solución que puede incluir el reemplazo del producto, un reembolso, o cualquier otra medida correctiva que consideremos apropiada.\r\n\r\n',6,'2024-12-06 17:59:17');



INSERT INTO `subcategoria` VALUES (1,'Telefonia','fa-solid fa-mobile-screen-button',1,7,'2024-12-06 17:59:06'),(2,'Tablets','fa-solid fa-tablet',1,7,'2024-12-06 17:59:06'),(3,'Audio','fa-solid fa-headphones',1,7,'2024-12-06 17:59:06'),(4,'Zona Gamer','fa-solid fa-gamepad',1,7,'2024-12-06 17:59:06'),(5,'Computo','fa-solid fa-desktop',1,7,'2024-12-06 17:59:06'),(6,'Fotografia','fa-solid fa-camera',1,7,'2024-12-06 17:59:06'),(7,'Televisores','fa-solid fa-tv',1,7,'2024-12-06 17:59:06'),(8,'Accesorios','fa-solid fa-keyboard',1,7,'2024-12-06 17:59:06'),(9,'Frutas y Verduras','fa-solid fa-apple-whole',1,1,'2024-12-06 17:59:06'),(10,'Bebidas','fa-solid fa-wine-glass',1,1,'2024-12-06 17:59:06'),(11,'Snacks','fa-solid fa-cookie-bite',1,1,'2024-12-06 17:59:06'),(12,'Panaderia y Reposteria','fa-solid fa-bread-slice',1,1,'2024-12-06 17:59:06'),(13,'Desayunos','fa-solid fa-mug-saucer',1,1,'2024-12-06 17:59:06'),(14,'Limpieza','fa-solid fa-broom',1,3,'2024-12-06 17:59:06'),(15,'Cuidado personal','fa-regular fa-file',1,3,'2024-12-06 17:59:06'),(16,'Decoracion','fa-regular fa-file',1,3,'2024-12-06 17:59:06'),(17,'Dormitorio','fa-regular fa-file',1,3,'2024-12-06 17:59:06'),(18,'Juguetes y Juegos','fa-regular fa-file',1,3,'2024-12-06 17:59:06'),(19,'Electrodomésticos','fa-solid fa-blender-phone',1,3,'2024-12-06 17:59:06'),(20,'Papeleria','fa-solid fa-paperclip',1,4,'2024-12-06 17:59:06'),(21,'Abarrotes','fa-regular fa-file',1,1,'2024-12-06 17:59:06'),(22,'Comidas preparadas','fa-solid fa-utensils',1,1,'2024-12-06 17:59:06'),(23,'Congelados','fa-regular fa-file',1,1,'2024-12-06 17:59:06'),(24,'Carnes, Aves y Pescados','fa-regular fa-file',1,1,'2024-12-06 17:59:06'),(25,'Lacteos y Embutidos','fa-solid fa-cow',1,1,'2024-12-06 17:59:06'),(26,'Entrenamiento Y Fitness','fa-regular fa-file',1,2,'2024-12-06 17:59:06'),(27,'Bicicletas','fa-solid fa-bicycle',1,2,'2024-12-06 17:59:06'),(28,'Scooters Y Skates','fa-regular fa-file',1,2,'2024-12-06 17:59:06'),(29,'Accesorios Deportivos','fa-regular fa-file',1,2,'2024-12-06 17:59:06'),(30,'Camping','fa-solid fa-campground',1,2,'2024-12-06 17:59:06'),(31,'Individuales Y De Contacto','fa-solid fa-person',1,2,'2024-12-06 17:59:06'),(32,'En Equipo','fa-solid fa-people-group',1,2,'2024-12-06 17:59:06'),(33,'Acuáticos','fa-solid fa-person-swimming',1,2,'2024-12-06 17:59:06'),(34,'Libros','fa-solid fa-book',1,4,'2024-12-06 17:59:06'),(35,'Arte y Diseño','fa-solid fa-paintbrush',1,4,'2024-12-06 17:59:06'),(36,'Escritorio','fa-regular fa-file',1,4,'2024-12-06 17:59:06'),(37,'Alimento Para Perros','fa-regular fa-file',1,5,'2024-12-06 17:59:06'),(38,'Cuidado Y Limpieza Para Perros','fa-solid fa-shield-dog',1,5,'2024-12-06 17:59:06'),(39,'Accesorios Para Perros','fa-solid fa-dog',1,5,'2024-12-06 17:59:06'),(40,'Ropa Para Perros','fa-regular fa-file',1,5,'2024-12-06 17:59:06'),(41,'Artículos De Transporte Para Perros','fa-regular fa-file',1,5,'2024-12-06 17:59:06'),(42,'Alimento Para Gatos','fa-regular fa-file',1,5,'2024-12-06 17:59:06'),(43,'Cuidado Y Limpieza Para Gatos','fa-solid fa-shield-cat',1,5,'2024-12-06 17:59:06'),(44,'Accesorios Para Gatos','fa-solid fa-cat',1,5,'2024-12-06 17:59:06'),(45,'Ropa Para Gatos','fa-regular fa-file',1,5,'2024-12-06 17:59:06'),(46,'Artículos De Transporte Para Gatos','fa-regular fa-file',1,5,'2024-12-06 17:59:06'),(47,'Zapatillas','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(48,'Pantalones','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(49,'Chaquetas y Abrigos','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(50,'Sandalias','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(51,'Botas','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(52,'Faldas','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(53,'Vestidos','fa-solid fa-person-dress',1,6,'2024-12-06 17:59:06'),(54,'Polos','fa-solid fa-shirt',1,6,'2024-12-06 17:59:06'),(55,'Camisas','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(56,'Zapatos','fa-solid fa-shoe-prints',1,6,'2024-12-06 17:59:06'),(57,'Accesorios de vestimenta','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(58,'Trajes de Baño','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(59,'Poleras','fa-regular fa-file',1,6,'2024-12-06 17:59:06'),(60,'Shorts','fa-regular fa-file',1,6,'2024-12-06 17:59:06');



INSERT INTO `producto` VALUES (1,'Celular Samsung Galaxy A24 128GB 4GB RAM Negro',1600.95,1289.99,999.99,'¡Descubre el nuevo Galaxy A24 LTE! Pantalla brillante Super AMOLED, lentes triples con 50 MP para fotos y videos estables, una batería poderosa que se carga rápido. Almacenamiento y memoria grandes, el almacenamiento expandible te permite guardar más de todo. RAM plus para un aumento del rendimiento de manera virtual.\r\n\r\n- País de origen: China\r\n- Detalle de la garantía: 12 Meses\r\n- Pantalla Super Amoled 6.5\r\n- Memoria expandible Hasta 1TB\r\n- Procesador MT6769\r\n- Single Sim\r\n- Sensor de huella\r\n- Conectividad 4G\r\n- Carga rápida 25W\r\n- Plan Prepago\r\n- No incluye cargador\r\n- Procesador 2.0GHz, 2GHz',199,'2024-10-06 00:00:00',1,1,1,'2024-12-06 18:25:17'),(2,'Televisor SAMSUNG CRYSTAL UHD 55\" UHD 4K Smart TV UN55DU8000GXPE',2299.00,1799.00,1699.00,'aaa',232,'2024-10-01 00:00:00',1,1,7,'2024-12-06 18:25:17'),(3,'Celular Samsung Galaxy A15 256GB, 8GB ram, cámara principal 50MP + 5MP + 2MP, frontal 13MP, 6.5\", negro\r\n',799.00,589.00,NULL,'aaaaa',1000,'2024-08-23 00:00:00',1,1,1,'2024-12-06 18:25:17'),(4,'Laptop LENOVO 15AMN8 15.6\" AMD Ryzen 5 (7000 series) 8GB 512GB W11',2259.00,1949.00,1849.00,'- Aprovecha el rendimiento ágil gracias a sus procesadores móviles AMD\r\n- Disfruta de archivos multimedia enriquecidos en una pantalla nítida de 15″ y Dolby Audio™\r\n- Sus puertos opcionales versátiles te permitirán conectar todos tus periféricos favoritos\r\n- Lenovo AI Engine aprende tus hábitos informáticos y hace que tu laptop funcione mejor\r\n\r\nLa retroiluminación del teclado y algunos puertos/ranuras pueden ser opcionales o variar; colores sujetos a disponibilidad',204,'2024-09-12 00:00:00',1,17,5,'2024-12-06 18:25:17'),(5,'Yogurt Parcialmente Descremado GLORIA Sabor a Vainilla Botella 180g Paquete 6un',10.00,10.00,NULL,'',97,'2024-10-23 00:00:00',1,6,25,'2024-12-06 18:25:17'),(6,'Yogurt Bebible LAIVE Bio Sabor a Fresa Galonera 1.7Kg',11.50,11.50,NULL,'',96,'2024-10-23 00:00:00',1,27,25,'2024-12-06 18:25:17'),(7,'Café Instantáneo ALTOMAYO Gourmet Lata 190g',40.90,40.90,NULL,'',96,'2024-10-23 00:00:00',1,54,13,'2024-12-06 18:25:17'),(8,'Café Tostado Molido ALTOMAYO Gourmet Caja 450g + Prensa',37.90,37.90,NULL,'',98,'2024-10-23 00:00:00',1,51,13,'2024-12-06 18:25:17'),(9,'Pack Galleta Chocosoda FIELD Sixpack x 3un\r\n',18.00,16.89,NULL,'',94,'2024-10-23 00:00:00',1,43,11,'2024-12-06 18:25:17'),(10,'Pack Galletas FIELD Coronita Sixpack x 3un\r\n',15.00,12.48,NULL,'',99,'2024-10-23 00:00:00',1,43,11,'2024-12-06 18:25:17'),(11,'Galletas OREO sabor Cookies&Cream Paquete 6un',5.20,5.20,NULL,'',99,'2024-10-23 00:00:00',1,47,11,'2024-12-06 18:25:17'),(12,'Pack Galleta NABISCO Oreo Regular Sixpack x 3un',15.60,13.20,10.00,'',99,'2024-10-23 00:00:00',1,47,11,'2024-12-06 18:25:17'),(13,'Cereal CORN FLAKES Nestlé Sin Gluten Caja 405g',13.90,13.90,NULL,'Mezcla de cereales (94. 7%) [semolina de maíz (52. 1%), harina de maíz integral (42. 6%), azúcar, jarabe de azúcar morena parcialmente invertido, sal yodada, regulador de acidez (fosfato tricálcico, fosfato trisódico), antioxidantes (mezcla de tocoferoles). Vitaminas y minerales: carbonato de calcio, vitamina B3 (Niacina), Zinc, Hierro, Vitamina B5 (ácido pantoténico), vitamina B1 (tiamina), vitamina B6 (piridoxina), vitamina B2 (riboflavina), vitamina B9 (ácido fólico).',99,'2024-10-23 00:00:00',1,8,13,'2024-12-06 18:25:17'),(14,'Bombones NESTLE Multipack Surtido Bolsa 360g\r\n',26.90,26.90,24.00,'Sublime: lácteos, soja, cacahuate,\r\ngluten y frutos de cáscaras.\r\nTriángulo Donofrio: lácteos y soja.\r\nPuede contener gluten,\r\ncacahuate y frutos de cáscaras.\r\nPrincesa: lácteos y soja.\r\nPuede contener gluten y frutos de cáscaras',99,'2024-10-23 00:00:00',1,8,21,'2024-12-06 18:25:17');


INSERT INTO `redes_sociales` VALUES (1,'Facebook','fa-brands fa-facebook','https://www.facebook.com','2024-12-06 17:58:56'),(2,'Twitter','fa-brands fa-twitter','https://www.twitter.com/','2024-12-06 17:58:56'),(3,'Instagram','fa-brands fa-instagram','https://www.instagram.com','2024-12-06 17:58:56'),(4,'Whatsapp','fa-brands fa-whatsapp','https://www.whatsapp.com','2024-12-06 17:58:56'),(5,'TikTok','fa-brands fa-tiktok','https://www.tiktok.com','2024-12-06 17:58:56'),(6,'YouTube','fa-brands fa-youtube','https://www.youtube.com','2024-12-06 17:58:56');



INSERT INTO `novedad` VALUES (1,'descuentos en Samsung','NUEVOS DESCUENTOS EN SAMSUNG','2024-10-09','2025-01-01','aaaaaaaaa','0000-00-00 00:00:00',1,1,NULL,3,'2024-12-06 18:19:22'),(2,'audifonos Samsung','Lo mejor de Samsung en Audifonos','2024-08-14','2025-01-01','aaaaa','2024-09-16 00:00:00',1,1,NULL,3,'2024-12-06 18:19:22'),(3,'televisores Samsung','DESCUENTOS EN TELEVISORES SAMSUNG','2024-08-07','2025-01-01','ecefweevwev','2024-10-09 00:00:00',1,1,NULL,3,'2024-12-06 18:19:22'),(4,'telefono Apple Ultimos dias','ULTIMOS DIAS en APPLE','2024-11-28','2025-01-01','','2024-11-05 00:00:00',1,19,NULL,3,'2024-12-06 18:19:22'),(5,'ultimos dias laptop lenovo','¡ULTIMOS DIAS en LENOVO!','2024-10-02','2025-01-01','','2024-08-14 00:00:00',1,17,NULL,3,'2024-12-06 18:19:22'),(6,'yogures Gloria','20% dsco en yogures GLORIA','2024-08-19','2025-01-01','yogurt barato','2024-07-24 00:00:00',1,6,NULL,3,'2024-12-06 18:19:22'),(7,'electrodomesticos Oster','Ofertas en Miles de Electrodomésticos','2024-10-01','2025-01-01','compra Oster','2024-09-03 00:00:00',1,23,19,3,'2024-12-06 18:19:22');



INSERT INTO `img_novedad` (`id`, `nomimagen`, `imagen`, `tipo_img_novedadid`, `novedadid`, `registro_auditoria`) VALUES
(1, 'Celulares en cuadro azul', '', 2, 1, '2024-12-06 23:19:44'),
(2, 'Banner Samsung', '', 1, 1, '2024-12-06 23:20:34'),
(3, 'audifonos samsung', '', 4, 2, '2024-12-06 23:21:54'),
(4, 'tv samsung', '', 4, 3, '2024-12-06 23:22:10'),
(5, 'apple oferta', '', 3, 4, '2024-12-06 23:22:38'),
(6, 'lenovo oferta', '', 3, 5, '2024-12-06 23:22:48'),
(7, 'cuadro Oster licuadora', '', 2, 7, '2024-12-06 23:22:53'),
(8, 'cuadro Gloria Yogurt', '', 2, 6, '2024-12-06 23:22:59');




INSERT INTO `img_producto` (`id`, `img_nombre`, `imagen`, `imgprincipal`, `productoid`, `registro_auditoria`) VALUES
(1, 'foto1', '', 1, 1, '2024-12-06 23:25:56'),
(2, 'foto2', '', 0, 1, '2024-12-06 23:26:10'),
(3, 'foto 1', '', 1, 2, '2024-12-06 23:26:43'),
(4, 'aaa', '', 0, 1, '2024-12-06 23:26:43'),
(5, 'aaa', '', 0, 1, '2024-12-06 23:26:43'),
(6, 'aaa', '', 0, 1, '2024-12-06 23:26:43'),
(7, 'aaaa', '', 0, 1, '2024-12-06 23:26:43'),
(8, 'aaaa', '', 0, 1, '2024-12-06 23:26:43'),
(9, 'a15', '', 1, 3, '2024-12-06 23:27:03'),
(10, '15amn lenovo', '', 1, 4, '2024-12-06 23:27:04'),
(11, 'Chocolates Surtidos', '', 1, 14, '2024-12-06 23:27:21'),
(12, 'Cereal CORN FLAKES', '', 1, 13, '2024-12-06 23:27:23'),
(13, 'Pack Galleta NABISCO Oreo Regular Sixpack x 3un', '', 1, 12, '2024-12-06 23:27:35'),
(14, 'Galletas OREO sabor Cookies&Cream Paquete 6un', '', 1, 11, '2024-12-06 23:27:37'),
(15, 'Pack Galletas FIELD Coronita Sixpack x 3un\r\n', '', 1, 10, '2024-12-06 23:27:58'),
(16, 'Pack Galleta Chocosoda FIELD Sixpack x 3un\r\n', '', 1, 9, '2024-12-06 23:27:59'),
(17, 'Café Instantáneo ALTOMAYO Gourmet Lata 190g', '', 1, 7, '2024-12-06 23:28:06'),
(18, 'Café Tostado Molido ALTOMAYO Gourmet Caja 450g + Prensa', '', 1, 8, '2024-12-06 23:28:06'),
(19, 'Yogurt Bebible LAIVE Bio Sabor a Fresa Galonera 1.7Kg', '', 1, 6, '2024-12-06 23:28:14'),
(20, 'Yogurt Parcialmente Descremado GLORIA Sabor a Vainilla Botella 180g Paquete 6un', '', 1, 5, '2024-12-06 23:28:14');



INSERT INTO `caracteristica_subcategoria` VALUES 
(1,1,'2024-12-06 18:25:41'),(2,1,'2024-12-06 18:25:41'),(3,1,'2024-12-06 18:25:41'),(4,1,'2024-12-06 18:25:41'),(5,1,'2024-12-06 18:25:41'),(6,1,'2024-12-06 18:25:41'),(7,1,'2024-12-06 18:25:41'),(8,1,'2024-12-06 18:25:41'),(9,1,'2024-12-06 18:25:41'),(10,1,'2024-12-06 18:25:41'),(11,1,'2024-12-06 18:25:41'),(12,1,'2024-12-06 18:25:41'),(13,1,'2024-12-06 18:25:41'),(14,1,'2024-12-06 18:25:41'),(15,1,'2024-12-06 18:25:41'),(16,1,'2024-12-06 18:25:41'),(17,1,'2024-12-06 18:25:41'),(18,1,'2024-12-06 18:25:41'),(19,1,'2024-12-06 18:25:41'),(20,1,'2024-12-06 18:25:41'),(21,1,'2024-12-06 18:25:41'),(22,1,'2024-12-06 18:25:41'),(23,1,'2024-12-06 18:25:41'),(24,1,'2024-12-06 18:25:41'),(25,1,'2024-12-06 18:25:41'),(26,1,'2024-12-06 18:25:41'),(27,1,'2024-12-06 18:25:41'),(28,1,'2024-12-06 18:25:41'),(29,1,'2024-12-06 18:25:41'),(30,1,'2024-12-06 18:25:41'),(31,1,'2024-12-06 18:25:41'),(32,1,'2024-12-06 18:25:41'),(33,1,'2024-12-06 18:25:41'),(34,1,'2024-12-06 18:25:41'),(35,1,'2024-12-06 18:25:41'),(36,1,'2024-12-06 18:25:41'),(37,1,'2024-12-06 18:25:41'),(38,1,'2024-12-06 18:25:41'),(39,1,'2024-12-06 18:25:41'),(40,1,'2024-12-06 18:25:41'),(41,1,'2024-12-06 18:25:41'),(42,1,'2024-12-06 18:25:41'),(43,1,'2024-12-06 18:25:41'),(44,1,'2024-12-06 18:25:41'),(45,1,'2024-12-06 18:25:41'),(46,1,'2024-12-06 18:25:41'),(47,1,'2024-12-06 18:25:41'),(48,1,'2024-12-06 18:25:41'),(49,1,'2024-12-06 18:25:41'),(50,1,'2024-12-06 18:25:41'),(51,1,'2024-12-06 18:25:41'),(52,1,'2024-12-06 18:25:41'),(53,1,'2024-12-06 18:25:41'),(54,1,'2024-12-06 18:25:41'),(55,1,'2024-12-06 18:25:41'),(56,1,'2024-12-06 18:25:41'),(57,1,'2024-12-06 18:25:41'),(58,1,'2024-12-06 18:25:41'),(59,1,'2024-12-06 18:25:41'),(60,1,'2024-12-06 18:25:41'),(61,1,'2024-12-06 18:25:41'),(62,1,'2024-12-06 18:25:41'),(63,1,'2024-12-06 18:25:41'),(64,1,'2024-12-06 18:25:41'),(65,1,'2024-12-06 18:25:41'),(66,1,'2024-12-06 18:25:41'),(67,1,'2024-12-06 18:25:41'),(68,1,'2024-12-06 18:25:41'),
(69,1,'2024-12-06 18:25:41'),(70,1,'2024-12-06 18:25:41');



INSERT INTO `caracteristica_producto` VALUES 
(1,1,'25W',1,'2024-12-06 18:25:41'),
(7,1,'128GB',0,'2024-12-06 18:25:41'),
(12,1,'Android',0,'2024-12-06 18:25:41');


INSERT INTO `pedido` VALUES (16,'2024-12-06',20.00,1,12,2,'2024-12-06 21:13:03'),(17,'2024-12-06',13.90,4,16,2,'2024-12-06 21:29:08'),(18,'2024-12-06',33.78,1,18,2,'2024-12-06 21:32:43'),(19,'2024-12-06',50.67,1,20,2,'2024-12-06 22:17:08'),(20,'2024-12-07',1239.09,3,20,2,'2024-12-06 22:21:38'),(21,NULL,NULL,NULL,33,1,'2024-12-06 22:53:36'),(22,'2025-09-04',34.57,1,13,2,'2024-12-06 23:28:45'),(23,'2024-12-06',90.30,3,16,2,'2024-12-06 23:53:54'),(24,NULL,NULL,NULL,30,1,'2024-12-08 03:26:52'),(25,NULL,NULL,NULL,13,1,'2025-09-04 12:34:45');


INSERT INTO `lista_deseos` VALUES (5,12,'2024-12-06 20:49:06'),(6,12,'2024-12-06 20:29:10'),(8,20,'2024-12-06 22:19:43'),(9,13,'2025-09-04 13:08:19'),(9,20,'2024-12-06 22:19:46'),(10,20,'2024-12-06 22:19:48');


INSERT INTO `detalles_pedido` VALUES (1,20,1,'2024-12-06 22:36:16'),(5,16,2,'2024-12-06 21:13:03'),(5,20,1,'2024-12-07 00:44:05'),(6,20,3,'2024-12-07 00:43:23'),(6,21,1,'2024-12-06 22:53:36'),(6,23,1,'2024-12-06 23:53:54'),(6,24,1,'2024-12-08 03:26:52'),(7,20,3,'2024-12-06 22:21:38'),(7,23,1,'2024-12-06 23:53:55'),(8,20,1,'2024-12-06 22:52:15'),(8,23,1,'2024-12-06 23:53:56'),(9,18,2,'2024-12-06 21:32:43'),(9,19,3,'2024-12-06 22:17:08'),(9,22,1,'2024-12-06 23:28:50'),(9,25,1,'2025-09-04 13:08:14'),(10,22,1,'2024-12-06 23:28:45'),(11,22,1,'2024-12-06 23:28:48'),(11,25,7,'2025-09-04 12:34:45'),(12,20,1,'2024-12-07 00:43:55'),(13,17,1,'2024-12-06 21:42:41'),(14,20,1,'2024-12-07 01:06:04'),(14,25,1,'2025-09-04 13:08:11');




