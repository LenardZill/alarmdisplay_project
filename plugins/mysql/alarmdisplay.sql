/*
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `alarmitems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `ric` varchar(7) NOT NULL DEFAULT '0',
  `funktion` int(1) NOT NULL,
	`funktionChar` text(1) NOT NULL,
  `msg` text NOT NULL,
	`bitrate` int(4) NOT NULL,
	`description` text NOT NULL,
  KEY `ID` (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
*/

CREATE TABLE IF NOT EXISTS `alarmitems` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`time` datetime NOT NULL,
 	`ric` varchar(7) NOT NULL DEFAULT '0',
 	`funktion` int(1) NOT NULL,
	`funktionChar` text(1) NOT NULL,
  	`msg` text NOT NULL,
	`bitrate` int(4) NOT NULL,
	`description` text NOT NULL,
	`alarmnumber` text NOT NULL,
	`category` text NOT NULL,
	`keyword` text NOT NULL,
	`street` text NOT NULL,
	`street_addition` text NOT NULL,
	`country` text NOT NULL,
	`caller` text NOT NULL,
	`message` text NOT NULL,
  	KEY `ID` (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;