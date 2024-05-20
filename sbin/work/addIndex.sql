ALTER TABLE `Treatment` ADD INDEX `ClinicID` (`ClinicID`) USING BTREE;
ALTER TABLE `ClientReferrals` ADD INDEX `Client` (`ClientID`) USING BTREE;
