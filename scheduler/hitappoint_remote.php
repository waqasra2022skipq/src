<?php
/*
this one can let you integrate hitAppoint into any other PHP page, even on a different server.
1) Copy this file to your site where you will have your appointments page
2) Include it and initiate the Hitappoint_Remote class giving it the URL of your hitAppoint install:

make sure this code goes on the very top of your PHP page, before any output is sent to the browser

include_once( dirname(__FILE__) . '/hitappoint_remote.php' );
$haremote = new Hitappoint_Remote( 'http://www.anothersite.com/appointments/' );

then the second piece of code goes in just in place where you need your appointment system, normally in the content area of your page:

echo $haremote->display();

Also make sure that your page has the <head> part as it is important to the script to include hitAppoint style and JavaScript files.

Here is a short example of the final page:

[sample code starts]
<?php
include_once( dirname(__FILE__) . '/hitappoint_remote.php' );
$haremote = new Hitappoint_Remote( 'http://www.anothersite.com/appointments/' );
?>
<html>
<head>
<title>Our Appointments</title>
</head>

<body>
<p>
Some header staff
</p>

And now goes hitAppoint:
<?php  echo $haremote->display(); ?>

<p>
Some footer staff
</p>
</body>

</html>

[sample code ends]

*/

class Hitappoint_Remote {
	var $url = '';
	var $web_path = '';
	var $result = array();

	public function __construct( 
		$url, // or local file path if on the same server
		$web_path = '' // for css and js if local file
		)
	{
		ob_start();

		if( ! isset($_SESSION) )
		{
//			session_name( NTS_SESSION_NAME );
			session_start();
		}

		$this->url = $url;
		$this->web_path = $web_path;

		if( // REQUEST VIA HTTP
			( substr($url, 0, strlen('http://')) == 'http://' ) OR
			( substr($url, 0, strlen('https://')) == 'https://' )
			)
		{
			$url_details = parse_url( $url );
			$host = $url_details['host'];
			$this->client = new hcHttpClient( $host );
//		$this->client->setDebug( TRUE );
			$this->client->setHandleRedirects( TRUE );
			$this->init_cookies();

			$out = $this->get_there();
			$this->result = json_decode( $out, TRUE );

//		print_r( $this->result );

		// if push download
			if( isset($this->client->headers['content-disposition']) )
			{
				if( ob_get_contents() )
					ob_end_clean();

				reset( $this->client->headers );
				foreach( $this->client->headers as $k => $v )
				{
					header($k . ': ' . $v);
				}
				echo $out;
				exit;
			}
			elseif( $this->is_ajax() )
			{
				echo isset($this->result['content']) ? $this->result['content'] : '';
				exit;
			}
		}
		else // LOCAL FILE
		{
			if( ! $web_path )
			{
				$out['content'] = "WEB PATH IS REQUIRED WHEN CALLING LOCAL FILE!";
				$out = json_encode( $out );
			}
			else
			{
				$this_url = $this->prepare_return_url( $web_path );
				$_REQUEST['nts-integrate-file'] = $web_path;
				ob_start();
				require( $this->url );
				$out = ob_get_contents();
				ob_end_clean();
			}
		}

		$this->result = json_decode( $out, TRUE );
	}

	protected function prepare_return_url( $url )
	{
		$return = $url;
		$return = preg_replace( '/https?\:\/\//', '', $return );

		if( substr($url, 0, strlen('https://')) == 'https://' )
		{
			$return = 's:' . $return;
		}
		return $return;
	}

	function init_cookies()
	{
		if( isset($_SESSION['hrp_cookies']) )
		{
			$this->client->cookies = $_SESSION['hrp_cookies'];
		}
	}

	function save_cookies()
	{
		$_SESSION['hrp_cookies'] = $this->client->cookies;
	}

	public function display()
	{
	// add header
		$already_shown = ob_get_contents();
		ob_end_clean();

		$head = $this->head();

		$pos1 = strpos( $already_shown, '<head' );
		if( $pos1 !== FALSE )
		{
			$pos2 = strpos( $already_shown, '>', $pos1 );
//			$already_shown = substr($already_shown, 0, $pos2 + 1 ) . $head . substr($already_shown, $pos2 + 1);
			$already_shown = str_replace( '</head>', $head . '</head>', $already_shown );
		}

		$return = '';
		$return .= $already_shown;
		$return .= $this->content();
		return $return;
	}

	public function head()
	{
		$return = isset($this->result['head']) ? $this->result['head'] : '';
		return $return;
	}

	public function content()
	{
		$return = isset($this->result['content']) ? $this->result['content'] : '';
		return $return;
	}

	static function currentPageUrl()
	{
		$pageURL = 'http';
		if( isset($_SERVER['HTTPS']) && ( $_SERVER['HTTPS'] == 'on' ) ){
			$pageURL .= 's';
			}
		$pageURL .= "://";
		if( isset($_SERVER['SERVER_PORT']) && $_SERVER['SERVER_PORT'] != '80'){
			$pageURL .= $_SERVER['SERVER_NAME'] . ':' . $_SERVER['SERVER_PORT'];
			}
		else {
			$pageURL .= $_SERVER['SERVER_NAME'];
			}

		if ( ! empty($_SERVER['REQUEST_URI']) )
			$pageURL .= $_SERVER['REQUEST_URI'];
		else
			$pageURL .= $_SERVER['SCRIPT_NAME'];
		return $pageURL;
	}

	static function pureUrl( $url )
	{
		preg_match( "/(.+)\?.*$/", $url, $matches );
		if( isset($matches[ 1 ]) ) 
			$url = $matches[ 1 ];
		return $url;
	}

	public function is_ajax()
	{
		$return = FALSE;
		if( isset($_SERVER['HTTP_X_REQUESTED_WITH']) && ($_SERVER['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest') )
		{
			$return = TRUE;
		}
		if( ! $return )
		{
			if( isset($_REQUEST['nts-view-mode']) && ($_REQUEST['nts-view-mode'] == 'ajax') )
			{
				$return = TRUE;
			}
		}
		return $return;
	}

	protected function get_there()
	{
		$return_url = self::pureUrl( self::currentPageUrl() );
		$url = $this->url;

		$pref = 'nts-';
	// check if we have GET and POST
		reset( $_POST );

		$get_params = array();
		reset( $_GET );
		foreach( $_GET as $k => $v )
		{
			if( substr($k, 0, strlen($pref)) )
			{
				$get_params[ $k ] = $v;
			}
		}

		$post_params = array();
		reset( $_POST );
		foreach( $_POST as $k => $v )
		{
			if( substr($k, 0, strlen($pref)) )
			{
				$post_params[ $k ] = $v;
			}
		}

		$url_details = parse_url($url);
		$url = $url_details['path'];

//		$this->client->setDebug(TRUE);
		$this_params = $post_params ? $post_params : $get_params;

	// strip started http:// as apache seems to have troubles with it
		$return_url = $this->prepare_return_url( $return_url );
		$this_params['nts-integrate-url'] = $return_url;

		if( $this->is_ajax() )
		{
			$this_params['nts-view-mode'] = 'ajax';
		}

		if( $post_params )
		{
			if( ! $this->client->post($url, $this_params) )
			{
				die('An error occurred: ' . $this->client->getError());
			}
			$out = $this->client->getContent();
		}
		else
		{
			$q = http_build_query( $this_params );
			$url .= '?' . $q;

			if( ! $this->client->get($url) )
			{
				die('An error occurred: ' . $this->client->getError());
			}
			$out = $this->client->getContent();
		}
		$this->save_cookies();
		return $out;
	}
}

class hcHttpClient {
	// Request vars
	var $host;
	var $port;
	var $path;
	var $method;
	var $postdata = '';
	var $cookies = array();
	var $referer;
	var $accept = 'text/xml,application/xml,application/xhtml+xml,text/html,text/plain,image/png,image/jpeg,image/gif,*/*';
	var $accept_encoding = 'gzip';
	var $accept_language = 'en-us';
	var $user_agent = 'Incutio HttpClient v0.9';
	// Options
	var $timeout = 20;
	var $use_gzip = true;
	var $persist_cookies = true;  // If true, received cookies are placed in the $this->cookies array ready for the next request
								  // Note: This currently ignores the cookie path (and time) completely. Time is not important, 
								  //	   but path could possibly lead to security problems.
	var $persist_referers = true; // For each request, sends path of last request as referer
	var $debug = false;
	var $handle_redirects = true; // Auaomtically redirect if Location or URI header is found
	var $max_redirects = 5;
	var $headers_only = false;	// If true, stops receiving once headers have been read.
	// Basic authorization variables
	var $username;
	var $password;
	// Response vars
	var $status;
	var $headers = array();
	var $content = '';
	var $errormsg;
	// Tracker variables
	var $redirect_count = 0;
	var $cookie_host = '';
	function __construct($host, $port=80) {
		$this->host = $host;
		$this->port = $port;
		$this->cookie_host = $this->host;
	}
	function get($path, $data = false) {
		$this->path = $path;
		$this->method = 'GET';
		if ($data) {
			$this->path .= '?'.$this->buildQueryString($data);
		}
		return $this->doRequest();
	}
	function post($path, $data) {
		$this->path = $path;
		$this->method = 'POST';
		$this->postdata = $this->buildQueryString($data);
		return $this->doRequest();
	}
	function buildQueryString($data) {
		$querystring = '';
		if (is_array($data)) {
			// Change data in to postable data
			foreach ($data as $key => $val) {
				if (is_array($val)) {
					foreach ($val as $val2) {
						$querystring .= urlencode($key).'='.urlencode($val2).'&';
					}
				} else {
					$querystring .= urlencode($key).'='.urlencode($val).'&';
				}
			}
			$querystring = substr($querystring, 0, -1); // Eliminate unnecessary &
		} else {
			$querystring = $data;
		}
		return $querystring;
	}
	function doRequest() {
		// Performs the actual HTTP request, returning true or false depending on outcome
		if (!$fp = @fsockopen($this->host, $this->port, $errno, $errstr, $this->timeout)) {
			// Set error message
			switch($errno) {
				case -3:
					$this->errormsg = 'Socket creation failed (-3)';
				case -4:
					$this->errormsg = 'DNS lookup failure (-4)';
				case -5:
					$this->errormsg = 'Connection refused or timed out (-5)';
				default:
					$this->errormsg = 'Connection failed ('.$errno.')';
				$this->errormsg .= ' '.$errstr;
				$this->debug($this->errormsg);
			}
			return false;
		}
		socket_set_timeout($fp, $this->timeout);
		$request = $this->buildRequest();
		$this->debug('Request', $request);
		fwrite($fp, $request);
		// Reset all the variables that should not persist between requests
		$this->headers = array();
		$this->content = '';
		$this->errormsg = '';
		// Set a couple of flags
		$inHeaders = true;
		$atStart = true;
		// Now start reading back the response
		while (!feof($fp)) {
			$line = fgets($fp, 4096);
			if ($atStart) {
				// Deal with first line of returned data
				$atStart = false;
				if (!preg_match('/HTTP\/(\\d\\.\\d)\\s*(\\d+)\\s*(.*)/', $line, $m)) {
					$this->errormsg = "Status code line invalid: ".htmlentities($line);
					$this->debug($this->errormsg);
					return false;
				}
				$http_version = $m[1]; // not used
				$this->status = $m[2];
				$status_string = $m[3]; // not used
				$this->debug(trim($line));
				continue;
			}
			if ($inHeaders) {
				if (trim($line) == '') {
					$inHeaders = false;
					$this->debug('Received Headers', $this->headers);
					if ($this->headers_only) {
						break; // Skip the rest of the input
					}
					continue;
				}
				if (!preg_match('/([^:]+):\\s*(.*)/', $line, $m)) {
					// Skip to the next header
					continue;
				}
				$key = strtolower(trim($m[1]));
				$val = trim($m[2]);
				// Deal with the possibility of multiple headers of same name
				if (isset($this->headers[$key])) {
					if (is_array($this->headers[$key])) {
						$this->headers[$key][] = $val;
					} else {
						$this->headers[$key] = array($this->headers[$key], $val);
					}
				} else {
					$this->headers[$key] = $val;
				}
				continue;
			}
			// We're not in the headers, so append the line to the contents
			$this->content .= $line;
		}
		fclose($fp);
		// If data is compressed, uncompress it
		if (isset($this->headers['content-encoding']) && $this->headers['content-encoding'] == 'gzip') {
			$this->debug('Content is gzip encoded, unzipping it');
			$this->content = substr($this->content, 10); // See http://www.php.net/manual/en/function.gzencode.php
			$this->content = gzinflate($this->content);
		}

		// If $persist_cookies, deal with any cookies
		if ($this->persist_cookies && isset($this->headers['set-cookie']) && $this->host == $this->cookie_host) {
			$cookies = $this->headers['set-cookie'];
			if (!is_array($cookies)) {
				$cookies = array($cookies);
			}
			foreach ($cookies as $cookie) {
				if (preg_match('/([^=]+)=([^;]+);/', $cookie, $m)) {
					$this->cookies[$m[1]] = $m[2];
				}
			}
			// Record domain of cookies for security reasons
			$this->cookie_host = $this->host;
		}
		// If $persist_referers, set the referer ready for the next request
		if ($this->persist_referers) {
			$this->debug('Persisting referer: '.$this->getRequestURL());
			$this->referer = $this->getRequestURL();
		}
		// Finally, if handle_redirects and a redirect is sent, do that
		if ($this->handle_redirects) {
			if (++$this->redirect_count >= $this->max_redirects) {
				$this->errormsg = 'Number of redirects exceeded maximum ('.$this->max_redirects.')';
				$this->debug($this->errormsg);
				$this->redirect_count = 0;
				return false;
			}
			$location = isset($this->headers['location']) ? $this->headers['location'] : '';
			$uri = isset($this->headers['uri']) ? $this->headers['uri'] : '';
			if ($location || $uri) {
				$url = parse_url($location.$uri);
				$to = $url['path'];
				if( isset($url['query']) && strlen($url['query']) )
				{
					$to .= '?' . $url['query'];
				}
				// This will FAIL if redirect is to a different site
				return $this->get( $to );
			}
		}
		return true;
	}
	function buildRequest() {
		$headers = array();
		$headers[] = "{$this->method} {$this->path} HTTP/1.0"; // Using 1.1 leads to all manner of problems, such as "chunked" encoding
		$headers[] = "Host: {$this->host}";
		$headers[] = "User-Agent: {$this->user_agent}";
		$headers[] = "Accept: {$this->accept}";
		if ($this->use_gzip) {
			$headers[] = "Accept-encoding: {$this->accept_encoding}";
		}
		$headers[] = "Accept-language: {$this->accept_language}";
		if ($this->referer) {
			$headers[] = "Referer: {$this->referer}";
		}
		// Cookies
		if ($this->cookies) {
			$cookie = 'Cookie: ';
			foreach ($this->cookies as $key => $value) {
				$cookie .= "$key=$value; ";
			}
			$headers[] = $cookie;
		}
		// Basic authentication
		if ($this->username && $this->password) {
			$headers[] = 'Authorization: BASIC '.base64_encode($this->username.':'.$this->password);
		}
		// If this is a POST, set the content type and length
		if ($this->postdata) {
			$headers[] = 'Content-Type: application/x-www-form-urlencoded';
			$headers[] = 'Content-Length: '.strlen($this->postdata);
		}
		$request = implode("\r\n", $headers)."\r\n\r\n".$this->postdata;
		return $request;
	}
	function getStatus() {
		return $this->status;
	}
	function getContent() {
		return $this->content;
	}
	function getHeaders() {
		return $this->headers;
	}
	function getHeader($header) {
		$header = strtolower($header);
		if (isset($this->headers[$header])) {
			return $this->headers[$header];
		} else {
			return false;
		}
	}
	function getError() {
		return $this->errormsg;
	}
	function getCookies() {
		return $this->cookies;
	}
	function getRequestURL() {
		$url = 'http://'.$this->host;
		if ($this->port != 80) {
			$url .= ':'.$this->port;
		}			
		$url .= $this->path;
		return $url;
	}
	// Setter methods
	function setUserAgent($string) {
		$this->user_agent = $string;
	}
	function setAuthorization($username, $password) {
		$this->username = $username;
		$this->password = $password;
	}
	function setCookies($array) {
		$this->cookies = $array;
	}
	// Option setting methods
	function useGzip($boolean) {
		$this->use_gzip = $boolean;
	}
	function setPersistCookies($boolean) {
		$this->persist_cookies = $boolean;
	}
	function setPersistReferers($boolean) {
		$this->persist_referers = $boolean;
	}
	function setHandleRedirects($boolean) {
		$this->handle_redirects = $boolean;
	}
	function setMaxRedirects($num) {
		$this->max_redirects = $num;
	}
	function setHeadersOnly($boolean) {
		$this->headers_only = $boolean;
	}
	function setDebug($boolean) {
		$this->debug = $boolean;
	}
	// "Quick" static methods
	function quickGet($url) {
		$bits = parse_url($url);
		$host = $bits['host'];
		$port = isset($bits['port']) ? $bits['port'] : 80;
		$path = isset($bits['path']) ? $bits['path'] : '/';
		if (isset($bits['query'])) {
			$path .= '?'.$bits['query'];
		}
		$client = new HttpClient($host, $port);
		if (!$client->get($path)) {
			return false;
		} else {
			return $client->getContent();
		}
	}
	function quickPost($url, $data) {
		$bits = parse_url($url);
		$host = $bits['host'];
		$port = isset($bits['port']) ? $bits['port'] : 80;
		$path = isset($bits['path']) ? $bits['path'] : '/';
		$client = new HttpClient($host, $port);
		if (!$client->post($path, $data)) {
			return false;
		} else {
			return $client->getContent();
		}
	}
	function debug($msg, $object = false) {
		if ($this->debug) {
			print '<div style="border: 1px solid red; padding: 0.5em; margin: 0.5em;"><strong>HttpClient Debug:</strong> '.$msg;
			if ($object) {
				ob_start();
				print_r($object);
				$content = htmlentities(ob_get_contents());
				ob_end_clean();
				print '<pre>'.$content.'</pre>';
			}
			print '</div>';
		}
	}   
}
?>