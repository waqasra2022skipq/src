<!--
/* Dynamic HTML library.  Keith L. Stephenson */
var mouseX;
var mouseY;
function getObject(obj)
{
  var theObj;
  if ( typeof obj == "string" )
  {
    if ( isNS4 ) { theObj = eval("document." + obj); }
    else if ( isIE4 ) { theObj = eval("document.all." + obj); }
    else if ( isDOM )
    { var objMain = obj.substring(0, obj.indexOf("."));
      var objRest = obj.substring(obj.indexOf("."), obj.length);
//alert("objMain=" + objMain + ", objRest=" + objRest);
      if ( objMain == "" ) 
      { theObj = document.getElementById(obj); }
      else 
      { theObj = eval("document.getElementById(objMain)" + objRest);
      }
    }
  }
  else
  { theObj = obj; }
  return theObj;
}
function show(obj)
{
  var theObj = getObject(obj);
  if ( isNS4 ) { theObj.visibility = "visible"; }
  else { theObj.style.visibility = "visible"; }
}
function hide(obj)
{
  var theObj = getObject(obj);
  if ( isNS4 ) { theObj.visibility = "hidden"; }
  else { theObj.style.visibility = "hidden"; }
}
function moveObj(x, y, obj)
{
  var theObj = getObject(obj);
//alert("Browser=" + BrowserID + ", " + isNS4);
//alert("x=" + x + ", y=" + y);
  var ExtraSpace     = 20;
  var WindowLeftEdge = (isIE) ? document.body.scrollLeft   : window.pageXOffset;
  var WindowTopEdge  = (isIE) ? document.body.scrollTop    : window.pageYOffset;
  var WindowWidth    = (isIE) ? document.body.clientWidth  : window.innerWidth;
  var WindowHeight   = (isIE) ? document.body.clientHeight : window.innerHeight;
  var WindowRightEdge  = (WindowLeftEdge + WindowWidth) - ExtraSpace;
  var WindowBottomEdge = (WindowTopEdge + WindowHeight) - ExtraSpace;
  var ObjectHeight   = (isNS4) ? theObj.clip.height : theObj.offsetHeight;
  var ObjectWidth    = (isNS4) ? theObj.clip.width : theObj.offsetWidth;
//alert("re=" + WindowRightEdge + ", be=" + WindowBottomEdge);
//alert("w=" + ObjectWidth + ", h=" + ObjectHeight);
//showProps(theObj,"helpBox");
  if ( y + ObjectHeight > WindowBottomEdge )
  { y = WindowBottomEdge - ObjectHeight; 
    x += ObjectWidth/2;
  }
  if ( x + ObjectWidth > WindowRightEdge )
  { x = WindowRightEdge - ObjectWidth; }
  if ( y < ExtraSpace ) { y = ExtraSpace; }
  if ( x < ExtraSpace ) { x = ExtraSpace; }
//alert("x=" + x + ", y=" + y);
  if ( isNS4 )
  { theObj.moveTo(x,y); }
  else
  { theObj.style.left = x + "px";
    theObj.style.top  = y + "px";
  }
//showProps(theObj,theObj.id);
//alert("pixelLeft=" + theObj.style.pixelLeft + ", pixelTop=" + theObj.style.pixelTop);
}
function getMouse(e)
{
  mouseX=(isIE) ? event.x+document.body.scrollLeft : e.pageX;
  mouseY=(isIE) ? event.y+document.body.scrollTop : e.pageY;
//alert("x=" + mouseX + ", y=" + mouseY);
}
function getElementsWithId( id ) {
  var children = document.body.getElementsByTagName('*');
  var elements = [], child;
  for (var i = 0, length = children.length; i < length; i++) {
    child = children[i];
    if (child.id.substr(0, id.length) == id)
      elements.push(child);
  }
  return elements;
}
function showProps(obj,objName)
{
  var result = "";
  var count = 0;
  for (var i in obj)
  { result += objName + "." + i + " = " + obj[i] + "\n";
    count++;
    if (count == 25)
    { alert(result); result = ""; count = 0; }
  }
  alert(result);       
}
//  DeCloak -->
