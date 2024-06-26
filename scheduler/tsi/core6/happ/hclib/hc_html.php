<?php
class Hc_Renderer
{
	function render( $view_file, $view_params = array() )
	{
		if( $view_params ){
			extract($view_params);
		}

		ob_start();
		require( $view_file );
		$output = ob_get_contents();
		ob_end_clean();
		$output = trim( $output );
		return $output;
	}
}

class HC_View_Layout
{
	protected $partials = array();
	protected $template = '';
	protected $params = array();

	function set_partial( $key, $value )
	{
		$this->partials[$key] = $value;
	}
	function partial( $key )
	{
		$return = '';
		if( isset($this->partials[$key]) ){
			if( is_array($this->partials[$key]) ){
				$return = join( '', $this->partials[$key] );
			}
			else {
				$return = $this->partials[$key];
			}
		}
		return $return;
	}

	function has_partial( $key )
	{
		return (isset($this->partials[$key]) && $this->partials[$key]) ? TRUE : FALSE;
	}

	function set_template( $template )
	{
		$this->template = $template;
	}
	function template()
	{
		return $this->template;
	}

	function set_params( $params )
	{
		foreach( $params as $param => $value )
		{
			$this->set_param( $param, $value );
		}
	}
	function set_param( $param, $value )
	{
		$this->params[ $param ] = $value;
	}
	function params()
	{
		return $this->params;
	}
	function param( $key )
	{
		$return = isset($this->params[$key]) ? $this->params[$key] : '';
		return $return;
	}

	public function __toString()
	{
		return $this->render();
    }
}

class HC_Html_Factory
{
	public static function element( $element )
	{
		$return = new HC_Html_Element( $element );
		return $return;
	}

	public static function input( $element, $name = '' )
	{
		static $classes = array();
		$class_key = 'input_' . $element;

		if( isset($classes[$class_key]) ){
			$class = $classes[$class_key];
		}
		else {
			$widget_locations = HC_App::widget_locations();
			foreach( $widget_locations as $prfx => $locations ){
				$class = strtoupper($prfx) . '_Form_Input_' . ucfirst($element);
				if( ! class_exists($class) ){
					/* attempt to load the file */
					if( ! is_array($locations) ){
						$locations = array( $locations );
					}
					foreach( $locations as $location ){
						$file = $location . '/form/' . $element . '.php';
// echo "ATTEMPT TO LOAD '$class' IN '$file'<br>";
						if( file_exists($file) ){
							include_once( $file );
							break;
						}
					}
				}
				if( class_exists($class) ){
					$classes[$class_key] = $class;
					break;
				}
			}
		}

		if( class_exists($class) ){
			if( $name )
				$return = new $class( $name );
			else
				$return = new $class;
			return $return;
		}
		else {
			throw new Exception( "No class defined: '$class'" );
		}
	}

	public static function widget( $element )
	{
		static $classes = array();
		$class_key = 'widget_' . $element;

		if( isset($classes[$class_key]) ){
			$class = $classes[$class_key];
		}
		else
		{
			$widget_locations = HC_App::widget_locations();
			foreach( $widget_locations as $prfx => $locations ){
				$class = strtoupper($prfx) . '_Html_Widget_' . ucfirst($element);
				if( ! class_exists($class) ){
					/* attempt to load the file */
					if( ! is_array($locations) ){
						$locations = array( $locations );
					}
					foreach( $locations as $location ){
//echo "ATTEMPT TO LOAD '$class'<br>";
						$file = $location . '/html/' . $element . '.php';
						if( file_exists($file) ){
							include_once( $file );
							break;
						}
					}
				}
				if( class_exists($class) ){
					$classes[$class_key] = $class;
					break;
				}
			}
		}

		$args = func_get_args();
		if( class_exists($class) ){
			$return = new $class();
			array_shift( $args );
			if( $args ){
				call_user_func_array( array($return, "init"), $args );
			}
			return $return;
		}
		else {
			throw new Exception( "No class defined: '$class'" );
		}
	}
}

class HC_Html_Element
{
	protected $tag = 'input';
	protected $attr = array();
	protected $children = array();
	protected $addon = array();
	protected $wrap = array();

	function __construct( $tag = '' )
	{
		if( strlen($tag) )
			$this->set_tag( $tag );
	}

	public function __toString()
	{
		return $this->render();
    }

	function init( $smth = NULL )
	{
	}

	function set_tag( $tag )
	{
		$this->tag = $tag;
		return $this;
	}
	function tag()
	{
		return $this->tag;
	}

	function attr( $key = '' )
	{
		$return = array();
		if( $key === '' ){
			$return = $this->attr;
		}
		elseif( isset($this->attr[$key]) ){
			$return = $this->attr[$key];
		}
		return $return;
	}

	protected function prep_attr( $key, $value )
	{
		switch( $key ){
			case 'title':
				if( is_string($value) ){
					$value = strip_tags($value);
					$value = trim($value);
				}
				break;
		}
		return $value;
	}

	function add_attr( $key, $value = NULL )
	{
		if( count(func_get_args()) == 1 ){
			// supplied as array
			foreach( $key as $key => $value ){
				$this->add_attr( $key, $value );
			}
		}
		else {
			if( is_array($value) ){
				foreach( $value as $v ){
					$this->add_attr( $key, $v );
				}
			}
			else {
				$value = $this->prep_attr( $key, $value );
				if( isset($this->attr[$key]) ){
					$this->attr[$key][] = $value;
				}
				else {
					if( ! is_array($value) )
						$value = array( $value ); 
					$this->attr[$key] = $value;
				}
			}
		}
		return $this;
	}

	function add_child( $child )
	{
		$this->children[] = $child;
		return $this;
	}
	function prepend_child( $child )
	{
		array_unshift( $this->children, $child );
		return $this;
	}
	function remove_children()
	{
		$this->children = array();
		return $this;
	}
	function children()
	{
		return $this->children;
	}

	function add_wrap( $wrap )
	{
		$this->wrap[] = $wrap;
		return $this;
	}
	function wrap()
	{
		return $this->wrap;
	}

	function add_addon( $addon )
	{
		$this->addon[] = $addon;
		return $this;
	}
	function addon()
	{
		return $this->addon;
	}

	protected function _prepare_children()
	{
		$return = '';

		$children = $this->children();
		if( $children ){
			reset( $children );
			foreach( $children as $child ){
//				$return .= "\n";
				if( is_array($child) ){
					foreach( $child as $subchild ){
						if( is_object($subchild) ){
							$return .= $subchild->render();
						}
						else {
							$return .= $subchild;
						}
					}
				}
				elseif( is_object($child) ){
					$return .= $child->render();
				}
				else {
					$return .= $child;
				}
			}
		}
		return $return;
	}

	function render()
	{
		$return = '';
		$return .= '<' . $this->tag();

		$attr = $this->attr();
		foreach( $attr as $key => $val ){
			switch( $key ){
				case 'class':
					if( defined('HC_SKIP_CSS_PREFIX') && HC_SKIP_CSS_PREFIX ){
						continue;
					}
					$skip = array('fa', 'hc-');
					$append = 'hc-';

					for( $ii = 0; $ii < count($val); $ii++ ){
						if( substr($val[$ii], 0, strlen($append)) != $append ){
							$append_this = TRUE;
							reset( $skip );
							foreach( $skip as $sk ){
								if( substr($val[$ii], 0, strlen($sk)) == $sk ){
									$append_this = FALSE;
									break;
								}
							}
							if( $append_this ){
								$val[$ii] = $append . $val[$ii];
							}
						}
					}
					break;

				case 'value':
					for( $ii = 0; $ii < count($val); $ii++ ){
						$val[$ii] = htmlspecialchars( $val[$ii] );
						$val[$ii] = str_replace( array("'", '"'), array("&#39;", "&quot;"), $val[$ii] );
					}
					break;
			}

			$val = join(' ', $val);
			if( strlen($val) ){
				$return .= ' ' . $key . '="' . $val . '"';
			}
		}

		$children_return = $this->_prepare_children();
		if( strlen($children_return) ){
			$return .= '>';
			$return .= $children_return;
//			$return .= "\n";
			$return .= '</' . $this->tag() . '>';
		}
		else {
			if( in_array($this->tag(), array('br', 'input')) ){
				$return .= '/>';
			}
			else {
				$return .= '></' . $this->tag() . '>';
			}
		}

		$addon = $this->addon();
		if( $addon ){
			reset( $addon );
			foreach( $addon as $ao ){
				if( is_object($ao) ){
					$return .= $ao->render();
				}
				else {
					$return .= $ao;
				}
			}
		}

		if( $wrap = $this->wrap() ){
			foreach( $wrap as $wr ){
				$return = $wr->add_child($return)->render();
			}
		}

		return $return;
	}
}

class HC_Html
{
	static function label( $class, $label = '' )
	{
		$return = '';
		if( ! strlen($label) )
			$label ='&nbsp;';

		$return = HC_Html_Factory::element('span')
			->add_attr('class', 'label')
			->add_child($label)
			;
		if( ! is_array($class) ){
			$class = array($class);
		}
		foreach( $class as $cla ){
			$return->add_attr('class', 'label-' . $cla);
		}
		return $return;
	}

	static function icon_stack( $icons )
	{
		$icon1 = array_shift($icons);
		$icon2 = array_shift($icons);

		$return = HC_Html_Factory::element('span')
			->add_attr('class', 'fa-stack')
			->add_attr('class', 'fa-fw')
//			->add_attr('class', 'fa-lg')
			// ->add_attr('style', 'border: red 1px solid;')
			;

		if( ! is_array($icon1) ){
			$icon1 = array($icon1);
		}
		if( ! is_array($icon2) ){
			$icon2 = array($icon2);
		}

		$step1 = HC_Html::icon( array_shift($icon1), FALSE );
		foreach( $icon1 as $ic1 ){
			$step1->add_attr('class', $ic1);
		}
		$step2 = HC_Html::icon( array_shift($icon2), FALSE );
		foreach( $icon2 as $ic2 ){
			$step2->add_attr('class', $ic2);
		}

		$step1->add_attr('class', 'fa-stack-1x');
		// $step1->add_attr('class', 'align-right');

		$step2->add_attr('class', 'fa-stack-15x');
		// $step2->add_attr('class', 'align-right');

		$return->add_child($step1);
		$return->add_child($step2);

		return $return;
	}

	static function icon( $icon, $fw = TRUE, $inside = '' )
	{
		if( substr($icon, 0, 2) == '<i' )
			return $icon;

		$return = HC_Html_Factory::element('i');
		if( strlen($icon) ){
			$return
				->add_attr('class', array('fa', 'fa-' . $icon))
				;
		}
		elseif( strlen($inside) ){
			$return
				->add_attr('class', array('fa'))
				;
			$return->add_child( $inside );
		}

		if( $fw ){
			$return->add_attr('class', 'fa-fw');
		}
		return $return;
	}

	static function page_header( $header )
	{
		$wrap = HC_Html_Factory::element('div')
			->add_attr( 'class', 'page-header' )
			->add_child( $header )
			;
		return $wrap->render();
	}

	/**
	* input
	*
	* Outputs HTML code for input
	*
	* @param	array $input ('value', 'error', 'type', 'name')
	* @return	string
	*/
	static function input( $input_array, $more = array() )
	{
		$return = '';

		$value = isset($input_array['value']) ? $input_array['value'] : '';
		$el = HC_Html_Factory::input(
			$input_array['type'],
			$input_array['name'],
			$value,
			$more
			);

		$error = isset($input_array['error']) ? $input_array['error'] : '';
		if( $error )
		{
			$el->set_error( $error );
		}

		return $el->render();
	}

	static function dropdown_menu( $menu, $class = 'dropdown-menu', $more_li_class = '' )
	{
		$renderer = new Hc_renderer;
		$view_file = dirname(__FILE__) . '/view/dropdown_menu.php';
		return $renderer->render( 
			$view_file, 
			array(
				'menu'			=> $menu,
				'class'			=> $class,
				'more_li_class'	=> $more_li_class,
				)
			);
	}
}