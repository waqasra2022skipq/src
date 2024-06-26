<?php
if( file_exists(dirname(__FILE__) . '/../../db.php') )
{
	$nts_no_db = TRUE;
	include_once( dirname(__FILE__) . '/../../db.php' );
}

if( ! defined('NTS_NO_CSRF_CHECK') ){
	define( 'NTS_NO_CSRF_CHECK', TRUE );
}

if( defined('NTS_DEVELOPMENT') )
	$happ_path = NTS_DEVELOPMENT;
else
	$happ_path = dirname(__FILE__) . '/../happ';

include_once( $happ_path . '/hclib/hcWpBase.php' );
if( file_exists($happ_path . '/hclib/hcWpPremiumPlugin.php') )
{
	include_once( $happ_path . '/hclib/hcWpPremiumPlugin.php' );
}

if( ! class_exists('ntsWpBase5') )
{
class ntsWpBase2 extends hcWpBase5
{
	public function __construct( 
		$real_class,
		$real_class_file,
		$hc_product = ''
		)
	{
		$this->happ_path = defined('NTS_DEVELOPMENT') ? NTS_DEVELOPMENT : dirname(__FILE__) . '/../happ';;
		$this->happ_web_dir = defined('NTS_DEVELOPMENT') ? plugins_url('', $this->happ_path) : plugins_url('core6', $real_class_file);

		$app = strtolower( $real_class );
		$slug = $app;
		$db_prefix = 'ha';

		$dev_app_file = dirname(__FILE__) . '/../../_app.php';
		if( file_exists($dev_app_file) ){
			require( $dev_app_file ); /* $app defined there */
		}
		else {
			$dev_app_file = dirname(__FILE__) . '/../version_' . $slug . '_salon_pro.php';
			if( file_exists($dev_app_file) ){
				$app = $slug . '_salon_pro';
			}
			else {
				$dev_app_file = dirname(__FILE__) . '/../version_' . $slug . '_pro.php';
				if( file_exists($dev_app_file) ){
					$app = $slug . '_pro';
				}
			}
		}

		$this->happ_files_file = dirname(__FILE__) . '/../assets/happ_files.php';
		parent::__construct(
			$app,
			$real_class_file,
			$hc_product,
			'nts',
			array(),
			$slug,
			$db_prefix
			);

		$this->dir = dirname(__FILE__);
		$this->require_shortcode = TRUE;
		$this->query_prefix = '';

		add_action( 'joebooking_cron', array($this, 'cron') );
		$next_scheduled = wp_next_scheduled('joebooking_cron');
		if ( ! $next_scheduled ){
			$start_time = time();
			$start_time = $start_time + 10 * 60;
			wp_schedule_event( $start_time, 'hourly', 'joebooking_cron' );
		}
		register_deactivation_hook( $real_class_file, array($this, 'remove_cron') );
	}

	public function remove_cron()
	{
		wp_clear_scheduled_hook('joebooking_cron');
	}

	public function cron()
	{
		include_once( dirname(__FILE__) . '/../model/init.php' );

		$conf =& ntsConf::getInstance();
		$currentVersion = $conf->get('currentVersion');
		if( ! $currentVersion ){
			return;
		}

		require( dirname(__FILE__) . '/../panels/cron.php' );

		// $now = time();
		// $conf->set( 'cronLastRunWp', $now );
	}

	public function _continue_init()
	{
		parent::_continue_init();

		require( dirname(__FILE__) . '/../assets/files.php' );
		reset( $css_files );
		foreach( $css_files as $f ){
			$this->register_admin_style($f);
		}

		reset( $js_files );
		foreach( $js_files as $f ){
			$this->register_admin_script($f);
		}

//		$shortcode = $slug . '6';
		$shortcode = $this->slug;
		add_shortcode( $shortcode, array($this, 'front_view'));
		add_action('wp', array($this, 'front_init') );
		add_action( 'admin_init', array($this, 'admin_init') );
		add_action( 'admin_menu', array($this, 'admin_menu') );
	}

	public function admin_menu()
	{
		parent::admin_menu();

		$default_title = $this->app;
		$default_title = str_replace( '_', ' ', $default_title );
		$default_title = ucwords( $default_title );
		$menu_title = get_site_option( $this->app . '_menu_title', $default_title );

		$page = add_menu_page(
			$menu_title,
			$menu_title,
			'read',
			$this->slug,
			array( $this, 'admin_view' ),
			'dashicons-calendar'
			);
	}

	public function front_init()
	{
		if( ! is_admin() )
		{
			if( parent::front_init() )
			{
				// if language param supplied
				if( isset($GLOBALS['NTS_CONFIG'][$this->app]['DEFAULT_PARAMS']) ){
					$params = $GLOBALS['NTS_CONFIG'][$this->app]['DEFAULT_PARAMS'];
					if( isset($params['lang']) && (! defined('NTS_DEFAULT_LANGUAGE')) ){
						define( 'NTS_DEFAULT_LANGUAGE', $params['lang'] );
					}
				}

			// action
				$file = $this->dir . '/../controller.php';
				require( $file );
				$GLOBALS['NTS_CONFIG'][$this->app]['ACTION_STARTED'] = 1;
			}
		}
	}

	public function admin_init()
	{
		if( $this->is_me_admin() )
		{
			parent::admin_init();

			$file = $this->dir . '/../controller.php';
			require( $file );

			if( $this->require_shortcode )
			{
				if( ! $this->pages )
				{
					$announceText = "You have not yet added the <strong>&#91;" . $this->slug . "&#93;</strong> shortcode to any of your posts or pages, the customer booking interface will not work!";
					ntsView::setAdminAnnounce( $announceText, 'alert' );
				}
			}
		}
	}

	public function admin_view()
	{
		$file = $this->dir . '/../view.php';
		require( $file );
	}

	public function _install()
	{
		parent::_install();

		/* make the current user the admin in our app */
		$currentUser = wp_get_current_user();
		$currentUserId = $currentUser->ID;

		global $NTS_SETUP_ADMINS;
		$NTS_SETUP_ADMINS = array();

		$roles = array( 'Developer', 'Administrator' );
		reset( $roles );
		foreach( $roles as $role )
		{
			$wp_user_search = new WP_User_Search( '', '', $role);
			$NTS_SETUP_ADMINS = array_merge( $NTS_SETUP_ADMINS, $wp_user_search->get_results() );
		}

/* database */
		$file = $this->dir . '/../model/init.php';
		include_once( $file );

		$app_info = ntsLib::getAppInfo();
		if( ! $app_info['installed_version'] )
		{
			require( $this->dir . '/../setup/create-database.php' );
			require( $this->dir . '/../setup/populate.php' );

		/* reset some settings */
			$conf =& ntsConf::getInstance();
			$email_from = get_bloginfo('admin_email');
			$email_from_name = get_bloginfo('name');
			$conf->set( 'emailSentFrom', $email_from );
			$conf->set( 'emailSentFromName', $email_from_name );
		}
	}
}
}
?>