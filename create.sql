-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: testdb
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `AS`
--

DROP TABLE IF EXISTS `AS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AS` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asn` int(11) DEFAULT NULL,
  `name` varchar(260) DEFAULT NULL,
  `descr` varchar(260) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `changed` datetime DEFAULT NULL,
  `approved` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asn` (`asn`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `descr` (`descr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AS`
--

LOCK TABLES `AS` WRITE;
/*!40000 ALTER TABLE `AS` DISABLE KEYS */;
/*!40000 ALTER TABLE `AS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ASContacts`
--

DROP TABLE IF EXISTS `ASContacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ASContacts` (
  `as_id` int(11) DEFAULT NULL,
  `contact_id` int(11) DEFAULT NULL,
  KEY `as_id` (`as_id`),
  KEY `contact_id` (`contact_id`),
  CONSTRAINT `ASContacts_ibfk_1` FOREIGN KEY (`as_id`) REFERENCES `AS` (`id`),
  CONSTRAINT `ASContacts_ibfk_2` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ASContacts`
--

LOCK TABLES `ASContacts` WRITE;
/*!40000 ALTER TABLE `ASContacts` DISABLE KEYS */;
/*!40000 ALTER TABLE `ASContacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CommunityASs`
--

DROP TABLE IF EXISTS `CommunityASs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CommunityASs` (
  `community_id` int(11) DEFAULT NULL,
  `AS_id` int(11) DEFAULT NULL,
  KEY `community_id` (`community_id`),
  KEY `AS_id` (`AS_id`),
  CONSTRAINT `CommunityASs_ibfk_1` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`),
  CONSTRAINT `CommunityASs_ibfk_2` FOREIGN KEY (`AS_id`) REFERENCES `AS` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CommunityASs`
--

LOCK TABLES `CommunityASs` WRITE;
/*!40000 ALTER TABLE `CommunityASs` DISABLE KEYS */;
/*!40000 ALTER TABLE `CommunityASs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CommunityCEs`
--

DROP TABLE IF EXISTS `CommunityCEs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CommunityCEs` (
  `community_id` int(11) DEFAULT NULL,
  `CustomerEdge_id` int(11) DEFAULT NULL,
  KEY `community_id` (`community_id`),
  KEY `CustomerEdge_id` (`CustomerEdge_id`),
  CONSTRAINT `CommunityCEs_ibfk_1` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`),
  CONSTRAINT `CommunityCEs_ibfk_2` FOREIGN KEY (`CustomerEdge_id`) REFERENCES `customer_edge` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CommunityCEs`
--

LOCK TABLES `CommunityCEs` WRITE;
/*!40000 ALTER TABLE `CommunityCEs` DISABLE KEYS */;
/*!40000 ALTER TABLE `CommunityCEs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CommunityContacts`
--

DROP TABLE IF EXISTS `CommunityContacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CommunityContacts` (
  `community_id` int(11) DEFAULT NULL,
  `contact_id` int(11) DEFAULT NULL,
  KEY `community_id` (`community_id`),
  KEY `contact_id` (`contact_id`),
  CONSTRAINT `CommunityContacts_ibfk_1` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`),
  CONSTRAINT `CommunityContacts_ibfk_2` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CommunityContacts`
--

LOCK TABLES `CommunityContacts` WRITE;
/*!40000 ALTER TABLE `CommunityContacts` DISABLE KEYS */;
/*!40000 ALTER TABLE `CommunityContacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PrefixNameServers`
--

DROP TABLE IF EXISTS `PrefixNameServers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PrefixNameServers` (
  `prefix_id` int(11) DEFAULT NULL,
  `name_server_id` int(11) DEFAULT NULL,
  KEY `prefix_id` (`prefix_id`),
  KEY `name_server_id` (`name_server_id`),
  CONSTRAINT `PrefixNameServers_ibfk_1` FOREIGN KEY (`prefix_id`) REFERENCES `prefix` (`id`),
  CONSTRAINT `PrefixNameServers_ibfk_2` FOREIGN KEY (`name_server_id`) REFERENCES `name_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PrefixNameServers`
--

LOCK TABLES `PrefixNameServers` WRITE;
/*!40000 ALTER TABLE `PrefixNameServers` DISABLE KEYS */;
/*!40000 ALTER TABLE `PrefixNameServers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `community`
--

DROP TABLE IF EXISTS `community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `community` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(260) DEFAULT NULL,
  `short` varchar(6) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `short` (`short`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `community`
--

LOCK TABLES `community` WRITE;
/*!40000 ALTER TABLE `community` DISABLE KEYS */;
/*!40000 ALTER TABLE `community` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mail` varchar(260) DEFAULT NULL,
  `nickname` varchar(260) DEFAULT NULL,
  `xmpp` varchar(260) DEFAULT NULL,
  `firstname` varchar(260) DEFAULT NULL,
  `lastname` varchar(260) DEFAULT NULL,
  `login` varchar(260) DEFAULT NULL,
  `password` varchar(260) DEFAULT NULL,
  `handle` varchar(260) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mail` (`mail`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `xmpp` (`xmpp`),
  UNIQUE KEY `firstname` (`firstname`),
  UNIQUE KEY `lastname` (`lastname`),
  UNIQUE KEY `login` (`login`),
  UNIQUE KEY `password` (`password`),
  UNIQUE KEY `handle` (`handle`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_edge`
--

DROP TABLE IF EXISTS `customer_edge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_edge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(260) DEFAULT NULL,
  `fqdn` varchar(260) DEFAULT NULL,
  `ipv4` varchar(260) DEFAULT NULL,
  `ipv6` varchar(260) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `fqdn` (`fqdn`),
  UNIQUE KEY `ipv4` (`ipv4`),
  UNIQUE KEY `ipv6` (`ipv6`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_edge`
--

LOCK TABLES `customer_edge` WRITE;
/*!40000 ALTER TABLE `customer_edge` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_edge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `name_server`
--

DROP TABLE IF EXISTS `name_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `name_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fqdn` varchar(260) DEFAULT NULL,
  `community_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fqdn` (`fqdn`),
  KEY `community_id` (`community_id`),
  CONSTRAINT `name_server_ibfk_1` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `name_server`
--

LOCK TABLES `name_server` WRITE;
/*!40000 ALTER TABLE `name_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `name_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peering_session`
--

DROP TABLE IF EXISTS `peering_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `peering_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pe_id` int(11) DEFAULT NULL,
  `ce_id` int(11) DEFAULT NULL,
  `pe_v4` varchar(260) DEFAULT NULL,
  `pe_v6` varchar(260) DEFAULT NULL,
  `ce_v4` varchar(260) DEFAULT NULL,
  `ce_v6` varchar(260) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `tunneltype_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pe_v4` (`pe_v4`),
  UNIQUE KEY `pe_v6` (`pe_v6`),
  UNIQUE KEY `ce_v4` (`ce_v4`),
  UNIQUE KEY `ce_v6` (`ce_v6`),
  KEY `pe_id` (`pe_id`),
  KEY `ce_id` (`ce_id`),
  KEY `tunneltype_id` (`tunneltype_id`),
  CONSTRAINT `peering_session_ibfk_1` FOREIGN KEY (`pe_id`) REFERENCES `provider_edge` (`id`),
  CONSTRAINT `peering_session_ibfk_2` FOREIGN KEY (`ce_id`) REFERENCES `customer_edge` (`id`),
  CONSTRAINT `peering_session_ibfk_3` FOREIGN KEY (`tunneltype_id`) REFERENCES `tunnel_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peering_session`
--

LOCK TABLES `peering_session` WRITE;
/*!40000 ALTER TABLE `peering_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `peering_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prefix`
--

DROP TABLE IF EXISTS `prefix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prefix` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prefix` varchar(260) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `community_id` int(11) DEFAULT NULL,
  `site_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prefix` (`prefix`),
  KEY `community_id` (`community_id`),
  KEY `site_id` (`site_id`),
  CONSTRAINT `prefix_ibfk_1` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`),
  CONSTRAINT `prefix_ibfk_2` FOREIGN KEY (`site_id`) REFERENCES `site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prefix`
--

LOCK TABLES `prefix` WRITE;
/*!40000 ALTER TABLE `prefix` DISABLE KEYS */;
/*!40000 ALTER TABLE `prefix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `provider_edge`
--

DROP TABLE IF EXISTS `provider_edge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `provider_edge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(260) DEFAULT NULL,
  `fqdn` varchar(260) DEFAULT NULL,
  `ipv4` varchar(260) DEFAULT NULL,
  `ipv6` varchar(260) DEFAULT NULL,
  `asn_id` int(11) DEFAULT NULL,
  `site_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `fqdn` (`fqdn`),
  UNIQUE KEY `ipv4` (`ipv4`),
  UNIQUE KEY `ipv6` (`ipv6`),
  KEY `asn_id` (`asn_id`),
  KEY `site_id` (`site_id`),
  CONSTRAINT `provider_edge_ibfk_1` FOREIGN KEY (`asn_id`) REFERENCES `AS` (`id`),
  CONSTRAINT `provider_edge_ibfk_2` FOREIGN KEY (`site_id`) REFERENCES `site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provider_edge`
--

LOCK TABLES `provider_edge` WRITE;
/*!40000 ALTER TABLE `provider_edge` DISABLE KEYS */;
/*!40000 ALTER TABLE `provider_edge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site`
--

DROP TABLE IF EXISTS `site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(260) DEFAULT NULL,
  `country` varchar(2) DEFAULT NULL,
  `city` varchar(5) DEFAULT NULL,
  `datacenter` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site`
--

LOCK TABLES `site` WRITE;
/*!40000 ALTER TABLE `site` DISABLE KEYS */;
/*!40000 ALTER TABLE `site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tunnel_type`
--

DROP TABLE IF EXISTS `tunnel_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tunnel_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tunnel_type`
--

LOCK TABLES `tunnel_type` WRITE;
/*!40000 ALTER TABLE `tunnel_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `tunnel_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-30  0:34:15
