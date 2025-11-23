

ALTER TABLE `pedido` ADD `card_nro` VARCHAR(255) NULL AFTER `registro_auditoria`, ADD `card_mmaa` VARCHAR(255) NULL AFTER `card_nro`, ADD `card_cvv` VARCHAR(255) NULL AFTER `card_mmaa`, ADD `card_titular` VARCHAR(255) NULL AFTER `card_cvv`;
