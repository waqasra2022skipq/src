<?php
class ntsSmsTemplateManager extends ntsEmailTemplateManager {
	function __construct(){
		$this->defaultFolder = dirname(__FILE__) . '/../defaults/language';
		$this->languageFolder = NTS_EXTENSIONS_DIR . '/languages';

		$this->fileName = 'sms.xml';
		$this->dbKeyPrefix = 'sms-';

		$this->templates = array();
		$this->tags = array();
		$this->init();
		}

	// Singleton stuff
	static function &getInstance(){
		return ntsLib::singletonFunction( 'ntsSmsTemplateManager' );
		}
	}
?>