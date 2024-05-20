<?php
$om =& ntsObserverManager::getInstance();

$post = $_NTS['REQ']->getPostParams();
$post_params = array_keys($post);

$enable_prefix = 'enable_';
$param_prefix = 'param_';

$enabled = array();
$params = array();
foreach( $post as $pn => $pv )
{
	if( substr($pn, 0, strlen($enable_prefix)) == $enable_prefix )
	{
		$obs_name = substr($pn, strlen($enable_prefix));
		$enabled[] = $obs_name;

		$this_param_prefix = $param_prefix . $obs_name . '_';
		reset( $post_params );
		foreach( $post_params as $pn2 )
		{
			if( substr($pn2, 0, strlen($this_param_prefix)) == $this_param_prefix )
			{
				$param_name = substr($pn2, strlen($this_param_prefix));
				$params[ $obs_name . '_' . $param_name ] = $post[$pn2];
			}
		}
	}
}

$om->set_enabled( $enabled );
$om->set_params( $params );

$msg = join( ': ', array(M('Event Actions'), M('Update'), M('OK')) );
ntsView::addAnnounce( $msg, 'ok' );

//_print_r( $post );
$forwardTo = ntsLink::makeLink( '-current-' );
ntsView::redirect( $forwardTo );
exit;
?>