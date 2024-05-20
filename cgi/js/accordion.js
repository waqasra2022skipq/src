var accordionItems = new Array();
var accordionImages = new Array();
function init_accordion(start_open) 
{
  // Grab the accordion items from the page
  var theItems = document.getElementsByClassName( 'accordionItem' );
  for ( var i = 0; i < theItems.length; i++ ) 
  {
    theItems[i].id = i;
    accordionItems.push( theItems[i] );
//        if ( theItems[i].className == 'accordionItem' ) accordionItems.push( theItems[i] );
  }

  // Assign onclick events to the accordion item headings
  for ( var i = 0; i < accordionItems.length; i++ ) 
  {
    var h2 = getFirstChildWithTagName( accordionItems[i], 'H2' );
    h2.onclick = toggleItem;
  }

  // Hide all accordion item bodies (except the first i = 1)?
  // show them? start_open
  var hideit = 'hide';
  if ( start_open == 1 ) { hideit = ''; }
  for ( var i = 0; i < accordionItems.length; i++ ) 
  {
//alert("i="+i+" id="+accordionItems[i].id+" Name="+accordionItems[i].className);
    accordionItems[i].className = 'accordionItem '+hideit;
  }

  // Grab the accordion images from the page
  var theImages = document.getElementsByClassName( 'accordionImage' );
  for ( var i = 0; i < theImages.length; i++ ) 
  {
    accordionImages.push( theImages[i] );
//alert("i="+i+" Name="+accordionImages[i].className);
  }

}

function toggleItem() 
{
  var itemClass = this.parentNode.className;

  // Hide all items
  for ( var i = 0; i < accordionItems.length; i++ ) 
  {
    accordionItems[i].className = 'accordionItem hide';
  }

  // Change the images
  for ( var i = 0; i < accordionImages.length; i++ ) 
  {
//alert("i="+i+" Name="+accordionImages[i].className+" src="+accordionImages[i].src);
    accordionImages[i].src = "/images/sorted_down.gif";
  }

  // Show this item if it was previously hidden
  if ( itemClass == 'accordionItem hide' ) 
  {
//alert(" parent id="+this.parentNode.id);
    this.parentNode.className = 'accordionItem';
    accordionImages[this.parentNode.id].src = "/images/sorted_up.gif";
  }
  this.parentNode.scrollIntoView();
}

function getFirstChildWithTagName( element, tagName ) 
{
  for ( var i = 0; i < element.childNodes.length; i++ ) 
  {
    if ( element.childNodes[i].nodeName == tagName ) return element.childNodes[i];
  }
}
