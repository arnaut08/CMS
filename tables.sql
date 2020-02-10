-- Access Permission Table
CREATE TABLE `accessPermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `canRead` tinyint(4) DEFAULT '0',
  `canWrite` tinyint(4) DEFAULT '0',
  `description` varchar(255) DEFAULT NULL,
  `projectId` int(11) DEFAULT NULL,
  `credentialId` varchar(8) DEFAULT NULL,
  `isOwner` tinyint(4) DEFAULT '0',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

-- CMS Events Table
CREATE TABLE `cmsEvents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comments` varchar(255) NOT NULL,
  `credentialId` varchar(8) DEFAULT NULL,
  `projectId` int(11) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

-- Credential Table
CREATE TABLE `credential` (
  `id` varchar(8) NOT NULL,
  `name` varchar(45) NOT NULL,
  `projectId` int(11) NOT NULL,
  `createdBy` int(11) NOT NULL,
  `version` int(11) DEFAULT '1',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `description` varchar(255) DEFAULT NULL,
  `starredBy` json DEFAULT NULL,
  KEY `pk_credentialId` (`id`),
  KEY `fk_createdBy` (`createdBy`),
  KEY `fk_projectId` (`projectId`)
);

-- Credential Fields Table
CREATE TABLE `field` (
  `id` varchar(8) NOT NULL,
  `credentialId` varchar(8) NOT NULL,
  `fieldType` set('username','password','file','key','software','link') NOT NULL,
  `label` varchar(45) DEFAULT NULL,
  `value` varchar(255) NOT NULL,
  `version` int(11) DEFAULT '1',
  KEY `pk_fieldId` (`id`),
  KEY `fk_credentialId` (`credentialId`)
);
