ALTER TABLE `Client` ADD `addressVerified` TINYINT NULL DEFAULT NULL ;
ALTER TABLE `ClientReferrals` ADD `addressVerified` TINYINT NULL DEFAULT NULL ;
ALTER TABLE `ClientLegalPP` ADD `addressVerified` TINYINT NULL DEFAULT NULL ;
ALTER TABLE `ClientFamily` ADD `addressVerified` TINYINT NULL DEFAULT NULL ;
ALTER TABLE `Guarantor` ADD `addressVerified` TINYINT NULL DEFAULT NULL ;
ALTER TABLE `Provider` ADD `addressVerified` TINYINT NULL DEFAULT NULL ;
ALTER TABLE `xInsurance` ADD `addressVerified` TINYINT NULL DEFAULT NULL ;