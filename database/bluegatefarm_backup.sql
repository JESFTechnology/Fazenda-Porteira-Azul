-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.32-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para bluegatefarm
CREATE DATABASE IF NOT EXISTS `bluegatefarm` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `bluegatefarm`;

-- Copiando estrutura para tabela bluegatefarm.costtypes
CREATE TABLE IF NOT EXISTS `costtypes` (
  `id_cost_type` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `cost_value` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_cost_type`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.costtypes: ~4 rows (aproximadamente)
DELETE FROM `costtypes`;
INSERT INTO `costtypes` (`id_cost_type`, `name`, `cost_value`) VALUES
	(1, 'Fertilizante', 850.00),
	(2, 'Semente', 320.00),
	(3, 'Defensivo', 1200.00),
	(4, 'Mão de Obra', 10.00);

-- Copiando estrutura para tabela bluegatefarm.crops
CREATE TABLE IF NOT EXISTS `crops` (
  `id_crop` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `area_hectares` decimal(10,2) DEFAULT NULL,
  `current_season` year(4) DEFAULT NULL,
  PRIMARY KEY (`id_crop`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.crops: ~4 rows (aproximadamente)
DELETE FROM `crops`;
INSERT INTO `crops` (`id_crop`, `name`, `area_hectares`, `current_season`) VALUES
	(1, 'SEDE', 0.00, '2025'),
	(2, 'Soja', 150.00, '2025'),
	(3, 'Milho', 85.50, '2025'),
	(4, 'Trigo', 60.75, '2024');

-- Copiando estrutura para tabela bluegatefarm.employees
CREATE TABLE IF NOT EXISTS `employees` (
  `id_employee` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `cpf` int(13) NOT NULL,
  `job` varchar(100) DEFAULT NULL,
  `base_salary` decimal(10,2) DEFAULT NULL,
  `weekly_hours` int(11) DEFAULT NULL,
  `hire_date` date DEFAULT NULL,
  `id_crop_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_employee`),
  KEY `id_crop_fk` (`id_crop_fk`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`id_crop_fk`) REFERENCES `crops` (`id_crop`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.employees: ~5 rows (aproximadamente)
DELETE FROM `employees`;
INSERT INTO `employees` (`id_employee`, `name`, `cpf`, `job`, `base_salary`, `weekly_hours`, `hire_date`, `id_crop_fk`) VALUES
	(1, 'Johann Estevão Sacconi Ferreira', 2147483647, 'Desenvolvedor Back-end', 4000.00, 44, '2025-10-28', 1),
	(2, 'João Silva', 2147483647, 'Gerente Agrícola', 6500.00, 44, '2020-03-15', NULL),
	(3, 'Maria Oliveira', 2147483647, 'Operador de Máquinas', 3200.50, 40, '2022-08-20', 1),
	(4, 'Pedro Souza', 2147483647, 'Técnico Agrônomo', 4800.75, 44, '2021-05-10', 2),
	(5, 'Ana Pereira', 2147483647, 'Auxiliar Geral', 2500.00, 40, '2023-01-05', 1);

-- Copiando estrutura para tabela bluegatefarm.grains
CREATE TABLE IF NOT EXISTS `grains` (
  `id_grain` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_grain`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.grains: ~4 rows (aproximadamente)
DELETE FROM `grains`;
INSERT INTO `grains` (`id_grain`, `name`, `type`) VALUES
	(1, 'Café', 'Burbon'),
	(2, 'Soja', 'Oleaginosa'),
	(3, 'Milho', 'Cereal'),
	(4, 'Trigo', 'Cereal');

-- Copiando estrutura para tabela bluegatefarm.machinery
CREATE TABLE IF NOT EXISTS `machinery` (
  `id_machinery` int(11) NOT NULL AUTO_INCREMENT,
  `model` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `total_worked_hours` int(11) DEFAULT NULL,
  `total_fuel_consumption` decimal(10,2) DEFAULT NULL,
  `id_machinery_brand_fk` int(11) DEFAULT NULL,
  `id_machinery_type_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_machinery`),
  KEY `id_machinery_brand_fk` (`id_machinery_brand_fk`),
  KEY `id_machinery_type_fk` (`id_machinery_type_fk`),
  CONSTRAINT `machinery_ibfk_1` FOREIGN KEY (`id_machinery_brand_fk`) REFERENCES `machinerybrand` (`id_machinery_brand`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `machinery_ibfk_2` FOREIGN KEY (`id_machinery_type_fk`) REFERENCES `machinerytype` (`id_machinery_type`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.machinery: ~4 rows (aproximadamente)
DELETE FROM `machinery`;
INSERT INTO `machinery` (`id_machinery`, `model`, `year`, `total_worked_hours`, `total_fuel_consumption`, `id_machinery_brand_fk`, `id_machinery_type_fk`) VALUES
	(1, 'JD 7815', 2018, 3500, 15500.50, 1, 1),
	(2, 'Axial-Flow 7250', 2020, 1200, 8900.25, 2, 2),
	(3, 'MF 4292', 2015, 4200, 18000.00, 3, 1),
	(4, 'TL5.80', 2022, 500, 2500.70, 4, 3);

-- Copiando estrutura para tabela bluegatefarm.machinerybrand
CREATE TABLE IF NOT EXISTS `machinerybrand` (
  `id_machinery_brand` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_machinery_brand`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.machinerybrand: ~4 rows (aproximadamente)
DELETE FROM `machinerybrand`;
INSERT INTO `machinerybrand` (`id_machinery_brand`, `name`) VALUES
	(1, 'John Deere'),
	(2, 'Case IH'),
	(3, 'Massey Ferguson'),
	(4, 'New Holland');

-- Copiando estrutura para tabela bluegatefarm.machinerytype
CREATE TABLE IF NOT EXISTS `machinerytype` (
  `id_machinery_type` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_machinery_type`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.machinerytype: ~4 rows (aproximadamente)
DELETE FROM `machinerytype`;
INSERT INTO `machinerytype` (`id_machinery_type`, `name`) VALUES
	(1, 'Trator'),
	(2, 'Colheitadeira'),
	(3, 'Pulverizador'),
	(4, 'Plantadeira');

-- Copiando estrutura para tabela bluegatefarm.machineryusage
CREATE TABLE IF NOT EXISTS `machineryusage` (
  `id_machinery_usage` int(11) NOT NULL AUTO_INCREMENT,
  `usage_date` date DEFAULT NULL,
  `hours_usage` decimal(10,2) DEFAULT NULL,
  `fuel_consumed` decimal(10,2) DEFAULT NULL,
  `observation` varchar(255) DEFAULT NULL,
  `id_machinery_fk` int(11) DEFAULT NULL,
  `id_employee_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_machinery_usage`),
  KEY `id_machinery_fk` (`id_machinery_fk`),
  KEY `id_employee_fk` (`id_employee_fk`),
  CONSTRAINT `machineryusage_ibfk_1` FOREIGN KEY (`id_machinery_fk`) REFERENCES `machinery` (`id_machinery`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `machineryusage_ibfk_2` FOREIGN KEY (`id_employee_fk`) REFERENCES `employees` (`id_employee`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.machineryusage: ~3 rows (aproximadamente)
DELETE FROM `machineryusage`;
INSERT INTO `machineryusage` (`id_machinery_usage`, `usage_date`, `hours_usage`, `fuel_consumed`, `observation`, `id_machinery_fk`, `id_employee_fk`) VALUES
	(1, '2025-10-25', 8.50, 45.20, 'Preparo de solo para o Milho.', 1, 2),
	(2, '2025-10-26', 10.00, 55.00, 'Plantio de Soja, talhão B.', 1, 2),
	(3, '2025-04-15', 7.20, 85.30, 'Colheita de Milho, finalização.', 2, 2);

-- Copiando estrutura para tabela bluegatefarm.marketquotes
CREATE TABLE IF NOT EXISTS `marketquotes` (
  `id_market_quotes` int(11) NOT NULL AUTO_INCREMENT,
  `price_per_bag` decimal(10,2) DEFAULT NULL,
  `quote_date` date DEFAULT NULL,
  `observation` varchar(200) DEFAULT NULL,
  `id_grain_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_market_quotes`),
  KEY `id_grain_fk` (`id_grain_fk`),
  CONSTRAINT `marketquotes_ibfk_1` FOREIGN KEY (`id_grain_fk`) REFERENCES `grains` (`id_grain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.marketquotes: ~3 rows (aproximadamente)
DELETE FROM `marketquotes`;
INSERT INTO `marketquotes` (`id_market_quotes`, `price_per_bag`, `quote_date`, `observation`, `id_grain_fk`) VALUES
	(1, 135.50, '2025-10-30', 'Cotação da bolsa de Chicago, Dólar a 5.10', 1),
	(2, 65.20, '2025-10-30', 'Cotação interna, alta demanda', 2),
	(3, 78.90, '2025-10-28', 'Fechamento do dia, mercado estável', 3);

-- Copiando estrutura para tabela bluegatefarm.productioncosts
CREATE TABLE IF NOT EXISTS `productioncosts` (
  `id_production_cost` int(11) NOT NULL AUTO_INCREMENT,
  `cost_date` date DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `id_cost_type_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_production_cost`),
  KEY `id_cost_type_fk` (`id_cost_type_fk`),
  CONSTRAINT `productioncosts_ibfk_1` FOREIGN KEY (`id_cost_type_fk`) REFERENCES `costtypes` (`id_cost_type`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.productioncosts: ~3 rows (aproximadamente)
DELETE FROM `productioncosts`;
INSERT INTO `productioncosts` (`id_production_cost`, `cost_date`, `description`, `id_cost_type_fk`) VALUES
	(1, '2025-09-01', 'Compra de NPK para Soja (150 un)', 1),
	(2, '2025-09-05', 'Compra de semente de Milho Híbrido (85 un)', 2),
	(3, '2025-10-20', 'Aplicação de Herbicida no Milho', 3);

-- Copiando estrutura para tabela bluegatefarm.storage
CREATE TABLE IF NOT EXISTS `storage` (
  `id_storage` int(11) NOT NULL AUTO_INCREMENT,
  `quantity_bags` int(11) DEFAULT NULL,
  `entry_date` date DEFAULT NULL,
  `id_grain_fk` int(11) DEFAULT NULL,
  `id_location_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_storage`),
  KEY `id_grain_fk` (`id_grain_fk`),
  KEY `id_location_fk` (`id_location_fk`),
  CONSTRAINT `storage_ibfk_1` FOREIGN KEY (`id_grain_fk`) REFERENCES `grains` (`id_grain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `storage_ibfk_2` FOREIGN KEY (`id_location_fk`) REFERENCES `storagelocations` (`id_storage_location`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.storage: ~4 rows (aproximadamente)
DELETE FROM `storage`;
INSERT INTO `storage` (`id_storage`, `quantity_bags`, `entry_date`, `id_grain_fk`, `id_location_fk`) VALUES
	(2, 5000, '2025-06-10', 2, 4),
	(3, 8000, '2025-05-20', 1, 4),
	(4, 1200, '2024-12-01', 3, 3),
	(6, 2001, '2025-11-05', 1, 1);

-- Copiando estrutura para tabela bluegatefarm.storagelocations
CREATE TABLE IF NOT EXISTS `storagelocations` (
  `id_storage_location` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_storage_location`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.storagelocations: ~4 rows (aproximadamente)
DELETE FROM `storagelocations`;
INSERT INTO `storagelocations` (`id_storage_location`, `name`) VALUES
	(1, 'Armazem R1'),
	(2, 'Silo Principal - Leste'),
	(3, 'Silo Auxiliar - Oeste'),
	(4, 'Armazém de Bagagem');

-- Copiando estrutura para tabela bluegatefarm.users
CREATE TABLE IF NOT EXISTS `users` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `activity` tinyint(1) DEFAULT NULL,
  `id_user_type_fk` int(11) NOT NULL,
  `id_employee_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  KEY `id_user_type_fk` (`id_user_type_fk`),
  KEY `id_employee_fk` (`id_employee_fk`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_user_type_fk`) REFERENCES `usertype` (`id_user_type`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`id_employee_fk`) REFERENCES `employees` (`id_employee`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.users: ~4 rows (aproximadamente)
DELETE FROM `users`;
INSERT INTO `users` (`id_user`, `name`, `email`, `password`, `activity`, `id_user_type_fk`, `id_employee_fk`) VALUES
	(1, 'Johann', 'johannsacconi@gmail.com', '1234', 1, 4, 1),
	(2, 'Admin', 'admin@bluegate.com', 'hash_admin_123', 1, 1, 5),
	(3, 'joaoSilva', 'joao.silva@bluegate.com', 'hash_joao_456', 1, 2, 2),
	(4, 'Maria', 'maria.o@bluegate.com', 'hash_maria_789', 1, 3, 3);

-- Copiando estrutura para tabela bluegatefarm.usertype
CREATE TABLE IF NOT EXISTS `usertype` (
  `id_user_type` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_user_type`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela bluegatefarm.usertype: ~8 rows (aproximadamente)
DELETE FROM `usertype`;
INSERT INTO `usertype` (`id_user_type`, `description`) VALUES
	(1, 'Operador'),
	(2, 'Motorista'),
	(3, 'Engenheiro de manutenção'),
	(4, 'Tecnologia & Inovação'),
	(5, 'Administrador do Sistema'),
	(6, 'Gerente'),
	(7, 'Operacional'),
	(8, 'Visitante');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
