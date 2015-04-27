-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Máquina: localhost
-- Data de Criação: 27-Fev-2014 às 20:02
-- Versão do servidor: 5.5.33
-- versão do PHP: 5.4.4-14+deb7u7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de Dados: `HousePi`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `Agendamento`
--

CREATE TABLE IF NOT EXISTS `Agendamento` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `DataHoraInicial` datetime NOT NULL,
  `DataHoraFinal` datetime NOT NULL,
  `Ativo` int(11) NOT NULL DEFAULT '1',
  `Nome` varchar(60) NOT NULL,
  `Alarme` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------
--
-- Estrutura da tabela `Camera`
--

CREATE TABLE IF NOT EXISTS `Camera` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `Device` varchar(100) NOT NULL,
  `Porta` int(11) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Extraindo dados da tabela `Camera`
--

INSERT INTO `Camera` (`Id`, `Nome`, `Device`, `Porta`) VALUES
(1, 'Camera 1', '/dev/video0', 2343);

-- --------------------------------------------------------

--
-- Estrutura da tabela `ConfiguracaoAlarme`
--

CREATE TABLE IF NOT EXISTS `ConfiguracaoAlarme` (
  `Id` int(11) NOT NULL,
  `EnviarEmail` int(11) NOT NULL,
  `UsarSirene` int(11) NOT NULL,
  `DesligarDisparoConsecutivo` int(11) NOT NULL,
  `TempoDisparo` int(11) NOT NULL,
  `StatusAlarme` int(11) NOT NULL DEFAULT '0',
  `StatusPanico` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `ConfiguracaoAlarme`
--

INSERT INTO `ConfiguracaoAlarme` (`Id`, `EnviarEmail`, `UsarSirene`, `DesligarDisparoConsecutivo`, `TempoDisparo`, `StatusAlarme`, `StatusPanico`) VALUES
(1, 1, 1, 1, 60, 0, 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `ConfiguracaoEmail`
--

CREATE TABLE IF NOT EXISTS `ConfiguracaoEmail` (
  `Id` int(11) NOT NULL,
  `Remetente` varchar(100) DEFAULT NULL,
  `Senha` varchar(60) DEFAULT NULL,
  `Destinatario` varchar(500) DEFAULT NULL,
  `ServidorSMTP` varchar(100) DEFAULT NULL,
  `PortaSMTP` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `ConfiguracaoEmail`
--

INSERT INTO `ConfiguracaoEmail` (`Id`, `Remetente`, `Senha`, `Destinatario`, `ServidorSMTP`, `PortaSMTP`) VALUES
(1, '', '', '', '', 587);

-- --------------------------------------------------------

--
-- Estrutura da tabela `DiaAgendamento`
--

CREATE TABLE IF NOT EXISTS `DiaAgendamento` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `IdAgendamento` int(11) NOT NULL,
  `Dia` int(11) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `Dias_do_Agendamento` (`IdAgendamento`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `Rele`
--

CREATE TABLE IF NOT EXISTS `Rele` (
  `Id` int(11) NOT NULL,
  `Nome` varchar(60) DEFAULT NULL,
  `Status` int(11) NOT NULL,
  `NumeroGPIO` int(11) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `Rele`
--

INSERT INTO `Rele` (`Id`, `Nome`, `Status`, `NumeroGPIO`) VALUES
(0, 'Rele 1', 0, 0),
(1, 'Rele 2', 0, 1),
(2, 'Rele 3', 0, 2),
(3, 'Rele 4', 0, 3),
(4, 'Rele 5', 0, 4),
(5, 'Rele 6', 0, 5),
(6, 'Rele 7', 0, 6),
(7, 'Rele 8', 0, 7),
(8, 'Rele 9', 0, 8),
(9, 'Rele 10', 0, 9),
(10, '12 Volts - GPB2', 0, 10),
(11, '12 Volts - GPB3', 0, 11),
(12, '12 Volts - GPB4', 0, 12);

-- --------------------------------------------------------

--
-- Estrutura da tabela `ReleAgendamento`
--

CREATE TABLE IF NOT EXISTS `ReleAgendamento` (
  `IdAgendamento` int(11) NOT NULL,
  `IdRele` int(11) NOT NULL,
  PRIMARY KEY (`IdAgendamento`,`IdRele`),
  KEY `Reles` (`IdRele`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estrutura da tabela `RFID`
--

CREATE TABLE IF NOT EXISTS `RFID` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Tag` varchar(50) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;


-- --------------------------------------------------------

--
-- Estrutura da tabela `SensorAlarme`
--

CREATE TABLE IF NOT EXISTS `SensorAlarme` (
  `Id` int(11) NOT NULL,
  `Nome` varchar(60) DEFAULT NULL,
  `Ativo` int(11) NOT NULL,
  `NumeroGPIO` int(11) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `SensorAlarme`
--

INSERT INTO `SensorAlarme` (`Id`, `Nome`, `Ativo`, `NumeroGPIO`) VALUES
(0, 'Sensor 0', 0, 17),
(1, 'Sensor 1', 0, 18),
(2, 'Sensor 2', 0, 27),
(3, 'Sensor 3', 0, 22),
(4, 'Sensor 4', 0, 23),
(5, 'Sensor 5', 0, 24),
(6, 'Sensor 6', 0, 25),
(7, 'Sensor 7', 0, 4);

-- --------------------------------------------------------

--
-- Estrutura da tabela `Usuario`
--

CREATE TABLE IF NOT EXISTS `Usuario` (
  `Id` int(11) NOT NULL,
  `Usuario` varchar(60) NOT NULL,
  `Senha` varchar(60) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `Usuario`
--

INSERT INTO `Usuario` (`Id`, `Usuario`, `Senha`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Estrutura da tabela `DisparoAlarme`
--

CREATE TABLE IF NOT EXISTS `DisparoAlarme` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `IdSensorAlarme` int(11) NOT NULL,
  `DataHora` datetime NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `Sensor_Disparo` (`IdSensorAlarme`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `DiaAgendamento`
--
ALTER TABLE `DiaAgendamento`
  ADD CONSTRAINT `Dias_do_Agendamento` FOREIGN KEY (`IdAgendamento`) REFERENCES `Agendamento` (`Id`);

--
-- Limitadores para a tabela `ReleAgendamento`
--
ALTER TABLE `ReleAgendamento`
  ADD CONSTRAINT `Agendamento` FOREIGN KEY (`IdAgendamento`) REFERENCES `Agendamento` (`Id`),
  ADD CONSTRAINT `Reles` FOREIGN KEY (`IdRele`) REFERENCES `Rele` (`Id`);

-- Limitadores para a tabela `DisparoAlarme`
--
ALTER TABLE `DisparoAlarme`
  ADD CONSTRAINT `Sensor_Disparo` FOREIGN KEY (`IdSensorAlarme`) REFERENCES `SensorAlarme` (`Id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
