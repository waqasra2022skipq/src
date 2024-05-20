<?php
class HC_Html_Widget_Container extends HC_Html_Element
{
	protected $items = array();
	protected $items_attr = NULL;

	function __construct()
	{
		parent::__construct( 'container' );
	}

	/* add to all items */
	function add_items_attr( $key, $value )
	{
		if( ! isset($this->items_attr) ){
			$this->items_attr = HC_Html_Factory::element('a');
		}
		$this->items_attr->add_attr( $key, $value );
		return $this;
	}
	function items_attr( $key = '' )
	{
		if( ! isset($this->items_attr) ){
			$this->items_attr = HC_Html_Factory::element('a');
		}
		return $this->items_attr->attr( $key );
	}

	function add_item( $item, $item_value = NULL )
	{
		if( $item_value === NULL )
			$this->items[] = $item;
		else
			$this->items[$item] = $item_value;
		return $this;
	}

	function remove_item( $key )
	{
		unset( $this->items[$key] );
		return $this;
	}

	function set_items( $items )
	{
		$this->items = $items;
		return $this;
	}
	function items()
	{
		return $this->items;
	}
	function item( $key )
	{
		return isset($this->items[$key]) ? $this->items[$key] : NULL;
	}

	function render()
	{
		$out = '';

		$items = $this->items();
		foreach( $items as $item ){
			if( is_object($item) ){
				$out .= $item->render();
			}
			else {
				$out .= $item;
			}
		}
		return $out;
	}
}
?>