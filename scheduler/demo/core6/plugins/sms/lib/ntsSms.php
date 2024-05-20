<?php
class ntsSms {
	public $body;
	public $from;
	public $debug;
	public $disabled = false;
	public $error;
	public $params = array();

	function addLog(){
		}

	function _realSend( $to, $msg, $from = '' ){
		$return = 0;

		$this->setError( '' );
		$plugin = 'sms';

		$plm =& ntsPluginManager::getInstance();

		/* process $to if we have any rules */
		$convert = $plm->getPluginSetting( $plugin, 'convert' );
		switch( $convert )
		{
			case 'us':
				/* if length is 10 then add +1 */
				if( strlen($to) == 10 )
				{
					$to = '1' . $to;
				}
				break;

			case 'aus':
				/* if starts with 0 then change it to +61 */
				if( substr($to, 0, 1) == '0' )
				{
					$to = substr_replace( $to, '61', 0, 1 );
				}
				break;
		}

		$gateway = $plm->getPluginSetting( $plugin, 'gateway' );

	/* the send file should return $success and $response vars */
		$sendFile = dirname(__FILE__) . '/../gateways/' . $gateway . '/send.php';
		require( $sendFile );

		if( ! is_array($success) )
			$success = array($success);
		if( ! is_array($response) )
			$response = array($response);
		if( ! is_array($msg) )
			$msg = array($msg);

	/* add log */
		$nolog = $plm->getPluginSetting( $plugin, 'nolog' );
		if( ! $nolog )
		{
			$ntsdb =& dbWrapper::getInstance();
			$tblName = 'smslog';

			for( $ii = 0; $ii < count($success); $ii++ )
			{
				$paramsArray = array(
					'sent_at'		=> time(),
					'to_number'		=> $to,
					'from_number'	=> $from,
					'message'		=> $msg[$ii],
					'success'		=> $success[$ii],
					'response'		=> $response[$ii],
					'gateway'		=> $gateway,
					);
				$ntsdb->insert( $tblName, $paramsArray, array('to' => 'string', 'from' => 'string') );
			}
		}
	/* end of log */

		$return = is_array($success) ? $success[0] : $success;
		return $return;
		}

	function __construct(){
		$plugin = 'sms';
		$this->body = '';
		$this->error = '';

		$this->disabled = false;

	/* from, from name, and debug settings */
		$plm =& ntsPluginManager::getInstance();
		$this->disabled = ( $plm->getPluginSetting( $plugin, 'disabled' ) ) ? true : false;
		$this->debug = ( $plm->getPluginSetting( $plugin, 'debug' ) ) ? true : false;
		}

	function setParam( $k, $v )
	{
		$this->params[$k] = $v;
	}

	function getParam( $k )
	{
		$return = isset($this->params[$k]) ? $this->params[$k] : NULL;
		return $return;
	}

	function setBody( $body ){
		$this->body = $body;
		}
	function setFrom( $from ){
		$this->from = $from;
		}

	function sendToOne( $toEmail ){
		$toArray = array( $toEmail );
		return $this->_send( $toArray );
		}

	function getBody(){
		return $this->body;
		}

	function _send( $toArray = array() ){
		if( $this->disabled )
			return true;

		$plugin = 'sms';
		$plm =& ntsPluginManager::getInstance();
		$settings = $plm->getPluginSettings( $plugin );
		if( isset($settings['from']) ){
			$this->setFrom( $settings['from'] );
			}

		$from = $this->from;
		$msg = $this->getBody();

		reset( $toArray );

		if( defined('NTS_DEVELOPMENT') && NTS_DEVELOPMENT )
		{
			$announce = 'SMS to ' . join( ', ', $toArray );
			ntsView::addAnnounce( $announce, 'info' );
		}
		elseif( $this->debug ){
			$text = '';
			$text .= "\n-------------------------------------------\n";
			$text .= "SMS MESSAGE";
			$text .= "\n-------------------------------------------\n";
			foreach( $toArray as $to ){
				$text .= "To:<I>$to</I>\n";
				}
			$text .= "From: $from\n";
			$text .= "Msg:\n" . $msg . "\n";
			$text .= "\n-------------------------------------------\n";

			$outFile = NTS_APP_DIR . '/../smslog.txt';
			if( file_exists($outFile) ){
				$fp = fopen( $outFile, 'a' );
				fwrite( $fp, $text . "\n\n" );
				fclose($fp);
				}
			else {
				echo nl2br($text);
				}
			}
		else {
			foreach( $toArray as $to ){
				$this->_realSend( $to, $msg, $from );
				}
			}

		return true;
		}

	function isError(){
		$return = $this->error ? true : false;
		return $return;
		}

	function getError(){
		return $this->error;
		}

	function setError( $error ){
		$this->error = $error;
		}
	}
?>