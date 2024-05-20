<?php
include_once( dirname(__FILE__) . '/container.php' );
class HC_Html_Widget_Tabs
{
	protected $tabs = array();
	protected $active = NULL;
	protected $id = NULL;

	function __construct()
	{
		$id = 'nts' . hc_random();
		$this->set_id( $id );
	}

	function set_id($id)
	{
		$this->id = $id;
	}
	function id()
	{
		return $this->id;
	}

	function set_active( $active )
	{
		$this->active = $active;
	}
	function active()
	{
		$return = NULL;
		if( $this->active ){
			$return = $this->active;
		}
		elseif( count($this->tabs) ){
			$tabs = array_keys($this->tabs);
			$return = $tabs[0];
		}
		return $return;
	}

	function add_tab( $key, $label, $content )
	{
		$this->tabs[ $key ] = array( $label, $content );
	}
	function tabs()
	{
		return $this->tabs;
	}

	function render_content()
	{
		$active = $this->active();
		$my_tabs = $this->tabs();

		$content = HC_Html_Factory::element('div')
			->add_attr('class', 'hc-tab-content')
			->add_attr('style', 'overflow: visible;')
			;
		reset( $my_tabs );
		foreach( $my_tabs as $key => $tab_array ){
			list( $tab_label, $tab_content ) = $tab_array;
			$tab = HC_Html_Factory::element('div')
				->add_attr('class', 'hc-tab-pane')
				->add_attr('id', $key)
				->add_attr('data-tab-id', $key)
				;
			if( $active == $key ){
				$tab->add_attr('class', 'active');
			}
			$tab->add_child( $tab_content );
			$content->add_child( $tab );
		}
		return $content;
	}

	function render()
	{
		$return = '';
		$my_tabs = $this->tabs();

		if( count($my_tabs) == 1 ){
			foreach( $my_tabs as $key => $tab_array ){
				list( $tab_label, $tab_content ) = $tab_array;
				$return = $tab_content;
				break;
			}
			return $return;
		}

	/* tabs */
		$id = $this->id();

		$tabs = HC_Html_Factory::widget('list')
			->add_attr('class', array('nav'))
			->add_attr('class', array('nav-tabs'))
			->add_attr('class', array('hc-tab-links'))
			->add_attr('id', $id) 
			;


		reset( $my_tabs );
		foreach( $my_tabs as $key => $tab_array ){
			list( $tab_label, $tab_content ) = $tab_array;
			$tabs->add_item( $key, 
				HC_Html_Factory::widget('titled', 'a')
					->add_attr('href', '#' . $key)
					// ->add_attr('data-toggle', 'tab')
					->add_attr('class', 'hc-tab-toggler')
					->add_attr('data-toggle-tab', $key)
					->add_child( $tab_label )
				);
		}
		$active = $this->active();
		$tabs->add_item_attr($active, 'class', 'active');

	/* content */
		$content = $this->render_content();

	/* out */
		$out = HC_Html_Factory::widget('list')
			->add_attr('class', array('list-unstyled'))
			->add_attr('class', array('hc-tabs'))
			;
		$out->add_item( $tabs );
		$out->add_item( $content );

		return $out->render();
	}
}
?>