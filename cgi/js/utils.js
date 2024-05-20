// Browser.js
var isDOM=document.getElementById?1:0;
var isIE=document.all?1:0;
var isIE4=((document.all && !isDOM)?1:0);
var isNS=(navigator.appName=='Netscape');
var isNS4=navigator.appName=='Netscape'&&!isDOM?1:0;
var isOp=window.opera?1:0;
var isWin=navigator.platform.indexOf('Win')!=-1?1:0;
var isMac=navigator.platform.indexOf('Mac')!=-1?1:0;
var isDyn=isDOM||isIE||isNS4;
// myClock.js
function myClock()
{
  var runTime = new Date();
  var hours = runTime.getHours();
  var minutes = runTime.getMinutes();
  var seconds = runTime.getSeconds();
  var dn = "AM";
  if (hours >= 12) { dn = "PM"; hours = hours - 12; }
  if (hours == 0) { hours = 12; }
  if (minutes <= 9) { minutes = "0" + minutes; }
  if (seconds <= 9) { seconds = "0" + seconds; }
  movingtime = "<b>"+ hours + ":" + minutes + ":" + seconds + " " + dn + "</b>";
  if (document.layers)
  {
    document.layers.clock.document.write(movingtime);
    document.layers.clock.document.close();
  }
  else { document.getElementById("clock").innerHTML = movingtime; }
  setTimeout("myClock()", 1000)
}
// popupMsg.js
function getRef(id, par)
{
 par=!par?document:(par.navigator?par.document:par);
 return isIE ? par.all[id] :
  (isDOM ? (par.getElementById?par:par.ownerDocument).getElementById(id) :
  (isNS4 ? par.layers[id] : null));
}
function getSty(id, par)
{
 var r=getRef(id, par);
 return r?(isNS4?r:r.style):null;
}
if (!window.LayerObj) var LayerObj = new Function('id', 'par','this.ref=getRef(id, par); this.sty=getSty(id, par); return this');
function getLyr(id, par) { return new LayerObj(id, par) }
function LyrFn(fn, fc)
{
 LayerObj.prototype[fn] = new Function('var a=arguments,p=a[0],px=isNS4||isOp?0:"px"; ' +
  'with (this) { '+fc+' }');
}
LyrFn('x','if (!isNaN(p)) sty.left=p+px; else return parseInt(sty.left)');
LyrFn('y','if (!isNaN(p)) sty.top=p+px; else return parseInt(sty.top)');
LyrFn('w','if (p) (isNS4?sty.clip:sty).width=p+px; ' +
 'else return (isNS4?ref.document.width:ref.offsetWidth)');
LyrFn('h','if (p) (isNS4?sty.clip:sty).height=p+px; ' +
 'else return (isNS4?ref.document.height:ref.offsetHeight)');
LyrFn('vis','sty.visibility=p');
LyrFn('write','if (isNS4) with (ref.document){write(p);close()} else ref.innerHTML=p');
LyrFn('alpha','var f=ref.filters,d=(p==null); if (f) {' +
 'if (!d&&sty.filter.indexOf("alpha")==-1) sty.filter+=" alpha(opacity="+p+")"; ' +
 'else if (f.length&&f.alpha) with(f.alpha){if(d)enabled=false;else{opacity=p;enabled=true}} }' +
 'else if (isDOM) sty.MozOpacity=d?"":p+"%"');
var CSSmode=document.compatMode;
CSSmode=(CSSmode&&CSSmode.indexOf('CSS')!=-1)||isDOM&&!isIE||isOp?1:0;
if (!window.page) var page = { win: window, minW: 0, minH: 0, MS: isIE&&!isOp,
 db: CSSmode?'documentElement':'body' }
page.winW=function()
 { with (this) return Math.max(minW, MS?win.document[db].clientWidth:win.innerWidth) }
page.winH=function()
 { with (this) return Math.max(minH, MS?win.document[db].clientHeight:win.innerHeight) }
page.scrollY=function()
 { with (this) return MS?win.document[db].scrollTop:win.pageYOffset }
page.scrollX=function()
 { with (this) return MS?win.document[db].scrollLeft:win.pageXOffset }

// *** TIP FUNCTIONS AND OBJECT ***

function msgTrack(evt, always) { with (this)
{
 // Reference the correct event object.
 evt=evt?evt:window.event;

 // Figure out the mouse co-ordinates and call the position function.
 // Also set sX and sY as the scroll position of the document.
 sX = page.scrollX();
 sY = page.scrollY();
 mX = isNS4 ? evt.pageX : sX + evt.clientX;
 mY = isNS4 ? evt.pageY : sY + evt.clientY;

 // If we've set message tracking, call the position function.
 if (msgStick == 1) position();
}}
function msgPosition(forcePos) { with (this)
{
 // Can't position a message if there isn't one available...
 if (!activeMsg) return;

 // Pull the window sizes from the page object.
 // In NS we size down the window a little as it includes scrollbars.
 var wW = page.winW()-(isIE?0:15), wH = page.winH()-(isIE?0:15);

 // Pull the compulsory information out of the message array.
 var t=message[activeMsg], msgX=eval(t[0]), msgY=eval(t[1]), msgW=div.w(), msgH=div.h(), adjY = 1;

 // Add mouse position onto relatively positioned message.
 if (typeof(t[0])=='number') msgX += mX;
 if (typeof(t[1])=='number') msgY += mY;

 // Check the message is not within 5px of the screen boundaries.
 if (msgX + msgW + 5 > sX + wW) { msgX = sX + wW - msgW - 5; adjY = 2 }
 if (msgY + msgH + 5 > sY + wH) msgY = sY + wH - (adjY*msgH) - 5;
 if (msgX < sX+ 5) msgX = sX + 5;
 if (msgY < sY + 5) msgY = sY + 5;

 // If the message is currently invisible, show at the calculated position.
 // Also do this if we're passed the 'forcePos' parameter.
 if ((!showMsg && (doFades ? !alpha : true)) || forcePos)
 {
  xPos = msgX;
  yPos = msgY;
 }

 // Otherwise move the message towards the calculated position by the stickiness factor.
 // Low stickinesses will result in slower catchup times.
 xPos += (msgX - xPos) * msgStick;
 yPos += (msgY - yPos) * msgStick;

 div.x(xPos);
 div.y(yPos);
}}
function msgShow(msgName) { with (this)
{
 if (!isDyn) return;

 // If this message is nested, call the 'show' function of its parent too.
 if (message[msgName].parentObj) message[msgName].parentObj.show(message[msgName].parentObj);

 // My layer object we use.
 if (!div) div = getLyr(myName + 'Layer');
 
 // IE4 requires a small width set otherwise message divs expand to full body size.
 if (isDOM) div.sty.width = 'auto';

 // If we're mousing over a different or new message...
 if (activeMsg != msgName)
 {
  // Remember this message number as active, for the other functions.
  activeMsg = msgName;

  // Set message's onmouseover and onmouseout handlers for static message.
  if (msgStick == 0)
  {
   if (isNS4) div.ref.captureEvents(Event.MOUSEOVER | Event.MOUSEOUT);
   div.ref.onmouseover = new Function('evt', myName + '.show("' + msgName + '"); ' +
    'if (isNS4) return this.routeEvent(evt)');
   div.ref.onmouseout = new Function('evt', myName + '.hide(); ' +
   'if (isNS4) return this.routeEvent(evt)');
  }

  // Place it somewhere onscreen - pass true to force a complete reposition.
  position(true);

  // Go through and replace %0% with the array's 0 index, %1% with message[msgName][1] etc...
  var str = template;
  for (var i=0; i<message[msgName].length; i++) str = str.replace('%'+i+'%', message[msgName][i]);
  // Write the proper content... the last <br> strangely helps IE5/Mac...?
  div.write(str + ((document.all && !isWin) ? '<small><br></small>' : ''));
 }

 // For non-integer stickiness values, we need to use setInterval to animate the message,
 // if it's 0 or 1 we can just use onmousemove to position it.
 clearInterval(trackTimer);
 if (msgStick != parseInt(msgStick)) trackTimer = setInterval(myName+'.position()', 50);

 // Finally either fade in immediately or after 'showDelay' milliseconds.
 // NS4 must always delay by a small amount as sometimes hide events come before show events
 // from a previous mouseout (when two message triggers overlap), because it's a weird browser.
 // So, this show call can cancel a (slightly later) hide.
 clearTimeout(fadeTimer);
 if (showDelay || isNS4)
  fadeTimer = setTimeout('with ('+myName+') { showMsg = true; fade() }', showDelay + 10);
 else { showMsg = true; fade() }
}}
function msgHide() { with (this)
{
 // We've got to be a DHTML-capable browser that has a message currently active.
 if (!isDyn || !activeMsg) return;

 // If the mouse position is within the message boundaries, we know NS4 is telling us stories
 // as often it makes hide events unaccompanied by overs or in a weird order.
 // Only applies to static message that we want the user to mouseover...
 if (isNS4 && msgStick==0 && xPos<=mX && mX<=xPos+div.w() && yPos<=mY && mY<=yPos+div.h())
  return;

 // If this message is nested, call the 'hide' function of its parent too.
 if (message[activeMsg].parentObj) message[activeMsg].parentObj.hide();

 // Fade out after a delay so another mouseover can cancel this fade.
 // This allows the user to mouseover a static message before its hides.
 clearTimeout(fadeTimer);
 fadeTimer = setTimeout('with (' + myName + ') { showMsg=false; fade() }', hideDelay);
}}
function msgFade() { with (this)
{
 // Clear to stop existing fades.
 clearTimeout(fadeTimer);

 // Show it and optionally increment alpha from minAlpha to maxAlpha or back again.
 if (showMsg)
 {
  div.vis('visible');
  if (doFades)
  {
   alpha += fadeSpeed;
   if (alpha > maxAlpha) alpha = maxAlpha;
   div.alpha(alpha);
   // Call this function again shortly, fading message in further.
   if (alpha < maxAlpha) fadeTimer = setTimeout(myName + '.fade()', 50);
  }
  window.status = message[activeMsg][3];
 }
 else
 {
  // Similar to before but counting down and hiding at the end.
  if (doFades && alpha > minAlpha)
  {
   alpha -= fadeSpeed;
   if (alpha < minAlpha) alpha = minAlpha;
   div.alpha(alpha);
   fadeTimer = setTimeout(myName + '.fade()', 50);
   return;
  }
  div.vis('hidden');
  // Clear the active message flag so it is repositioned next time.
  activeMsg = '';
  // Stop any sticky-message tracking if it's invisible.
  clearInterval(trackTimer);
  window.status = '';
 }
}}
function MsgObj(myName)
{
 // Holds the properties the functions above use.
 this.myName = myName;
 this.message = new Array();
 this.template = '';
 this.activeMsg = '';
 this.showMsg = false;
 this.msgStick = 1;
 this.showDelay = 50;
 this.hideDelay = 250;
 this.xPos = this.yPos = this.sX = this.sY = this.mX = this.mY = 0;

 this.track = msgTrack;
 this.position = msgPosition;
 this.show = msgShow;
 this.hide = msgHide;
 this.fade = msgFade;
 
 this.div = null;
 this.trackTimer = this.fadeTimer = 0;
 this.alpha = 0;
 this.doFades = true;
 this.minAlpha = 0;
 this.maxAlpha = 100;
 this.fadeSpeed = 10;
}

// Capture the onmousemove event so message can follow the mouse. Add in all your message objects here
// and also any functions from other scripts that need this event (e.g. my DHTML Scroller) too.
if (isNS4) document.captureEvents(Event.MOUSEMOVE);
document.onmousemove = function(evt)
{

 // Add or remove message objects from here!
 textMsg.track(evt);
 if (isNS4) return document.routeEvent(evt);
}
// A small function that refreshes NS4 on horizontal resize.
var nsWinW = window.innerWidth, nsWinH = window.innerHeight;
function ns4BugCheck()
{
 if (isNS4 && (nsWinW!=innerWidth || nsWinH!=innerHeight)) location.reload()
}
window.onresize = function()
{
 ns4BugCheck();
}

// *** START EDITING HERE ***

var textMsg = new MsgObj('textMsg');
textMsg.template = '<table bgcolor="green" cellpadding="1" cellspacing="0" width="%2%" border="0">' +
    '<tr><td><table bgcolor="lightgreen" cellpadding="3" cellspacing="0" width="100%" border="0">' +
    '<tr><td class="msgText">%3%</td></tr></table></td></tr></table>';
textMsg.doFades = false;
function newtextMsg(msgName,MsgInfo)
{
  textMsg.message[msgName] = new Array(-75, 15, 300, MsgInfo);
//alert("Name=" + msgName + ", Info=" + MsgInfo);
//alert("message.info=" + textMsg.message.info);
//showProps(textMsg,"textMsg");
  return 1
}
function showProps(obj,objName)
{
  var result = "";
  var count = 0;
  for (var i in obj)
  { result += objName + "." + i + " = " + obj[i] + "\n";
    count++;
    if (count == 5) { alert(result); result = ""; count = 0; }
  }
  alert(result);       
}
// ImgSwitch.js
var ImgName; 
function ImgShow(Name)
{
  ImgName = Name;
  NewImg = "/images/" + ImgName + "_show.gif"; 
  document.images[ImgName].src=NewImg;
} 
function ImgHide()
{
  NewImg = "/images/" + ImgName + "_hide.gif";
  document.images[ImgName].src=NewImg;
} 
// DHTML.js
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
// vEntry.js
function vEntry(type)
{
  var args = vEntry.arguments;
//alert("BEGIN: vEntry ");
  for (var i=1; i<args.length; i++)
  {
    var CheckField = args[i];
//alert("type=" + type + " CheckField=" + CheckField + " name=" + CheckField.name + " type=" + CheckField.type);
    if ( type == "notnull" && isEmpty( CheckField ) )
    { 
      var FieldName = CheckField.name;
      if ( !FieldName ) { FieldName = CheckField[0].name; }
      var field = FieldName;
      var NamePat = /^(.+)_(.+)_(\d+)/;
//alert("field = " + field + ", NamePat=" + NamePat + ", FieldName=" + FieldName);
      var matchArray = FieldName.match(NamePat); 
      if ( matchArray ) { var field = matchArray[2]; }
      return vOK(CheckField,"Input is required in " + field + " field."); 
    }
    else if ( type == "setnull" )
    { CheckField.value = ""; }
  }
//alert("END: vEntry = true");
  return true;
}
// Check for field empty.
function isEmpty( Str )
{
//alert("value=" + Str.value + ", length=" + Str.length + ", type=" + Str.type + ", index=" + Str.selectedIndex + ", idx=" + Str.index);
  if ( Str.type == "text" || Str.type == "textarea" || Str.type == "hidden" || Str.type == "password" )
  { CheckStr = Str; }
  else if ( Str.type == "select-one" || Str.type == "select-multiple" )
  { CheckStr = Str.options[Str.selectedIndex]; }
  else if ( Str.length > 0 )
  {
    for (var i=0; i<Str.length; i++)
    { if ( Str[i].checked ) { return false; } }
    return true;
  }
  else if ( Str.type == "checkbox" )
  { 
//alert("type=" + Str.type);
    if ( Str.checked ) { return false; }
    return true;
  }
  else
  { return false; }
//alert("Name=" + CheckStr.name + ", value=" + CheckStr.value );
  if( CheckStr.value == "" ) { return true; }
  return false;
}
// Allows for clean return on error.
function vOK(Field,errmsg)
{
  var args = vOK.arguments;
  var confirmError = args[2];

// It is an ERROR if not ok, so return true.
//alert("value=" + Field.value + ", type=" + Field.type + ", index=" + Field.selectedIndex + ", def=" +  + Field.defaultValue);
  if ( confirmError && confirm(errmsg) ) { return true; }
  alert(errmsg);

  if( Field.type == "text" || Field.type == "textarea" || Field.type == "hidden" || Field.type == "password" )
  {
    Field.value = Field.defaultValue;
    Field.focus(); 
    Field.select();
  }
  else if ( Field.type == "select-one" || Field.type == "select-multiple" )
  {
    Field.focus(); 
  }
  else if ( Field.type == "checkbox" )    
  { 
    Field.checked = Field.defaultChecked;
    Field.focus(); 
  }
  else                                   // radio button?
  {
    Field[0].focus(); 
  }
  return false;
}
// Keeps a Field from changing.
function vUNDO(Field,errmsg)
{
//alert("value=" + Field.value + ", type=" + Field.type + ", index=" + Field.selectedIndex + ", def=" +  + Field.defaultValue);
  alert(errmsg + "\nField cannot be changed.");
  if( Field.type == "text" || Field.type == "textarea" )
  { Field.value = Field.defaultValue; Field.focus(); Field.select(); }
  else if ( Field.type == "select-one" || Field.type == "select-multiple" )
  { Field.focus(); }
  else if ( Field.type == "checkbox" )    
  { Field.checked = Field.defaultChecked; Field.focus(); }
  else                                   // radio button?
  { Field[0].focus(); }
  return false;
}
function vDELETE(delmsg)
{ 
  if ( confirm(delmsg) ) { return true; }
  return false; 
} 
function togglediv(divid)
{ 
  if(document.getElementById(divid).style.display == 'none')
  { document.getElementById(divid).style.display = 'block'; }
  else
  { document.getElementById(divid).style.display = 'none'; } 
} 
function togglefld(f1,f2,divid)
{ 
  var t1 = eval("document.all." + f1);
  var t2 = eval("document.all." + f2);
  var tmp = t1.value;
  t1.value = t2.value;
  t2.value = tmp;
  document.getElementById(divid).innerHTML = t1.value; 
} 
function stringFilter (fldString,badValues,u1,q1,q2)
{
  s = fldString.value;
  badValues += "<>";       // never allowed.
  if ( q1 > 0 ) { badValues += "'"; }
  if ( q2 > 0 ) { badValues += '"'; }
  var badChar = "";
  var rtnString = "";
  var i;
  for (i = 0; i < s.length; i++)
  {
    var c = s.charAt(i);
    if (badValues.indexOf(c) > -1)
    { 
      if ( c == " " ) {  badChar += "/space/"; }
      else if ( c == '"' && q1 == 0 ) { rtnString += "'"; }    // allow single, but not double.
      else if ( c == "'" && q2 == 0 ) { rtnString += '"'; }    // allow double, but not single.
      else if ( c == "'" || c == '"' ) { badChar += "/quote/"; }
      else { badChar += c; }
    }
    else if ( i == 0 && u1 == 1 ) { rtnString += c.toUpperCase(); }
    else { rtnString += c; }
  }
  fldString.value = rtnString;
  if ( badChar.length > 0 )
  {
    alert("'" + badChar + "' character(s) invalid!\nDo not use the following characters '" + badValues + "'.");
    fldString.focus();
    return false;
  }
}
// ReportWindow.js
var ScreenWindowObj="";
function ScreenWindow(newURL,newName)
{
  ScreenWindowObj = window.open(newURL,newName);
  ScreenWindowObj.focus();
}
var ReportWindowObj="";
function ReportWindow(newURL,newName,h,w)
{
  if (h==undefined) { h = '700'; }
  if (w==undefined) { w = '1000'; }
//alert("h=" + h + ", w=" + w);
  ReportWindowObj = window.open(newURL,newName,'HEIGHT='+h+',WIDTH='+w+',SCROLLBARS=yes,RESIZABLE=yes,STATUS=yes');
  ReportWindowObj.focus();
}
var InputWindowObj="";
function InputWindow(url,title,h,w) {
  if (h==undefined) { h = '700'; }
  if (w==undefined) { w = '1000'; }
  var left = (screen.width/2)-(w/2);
  var top = (screen.height/2)-(h/2);
  InputWindowObj = window.open(url, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, SCROLLBARS=yes, resizable=no, copyhistory=no, WIDTH='+w+', HEIGHT='+h+', TOP='+top+', LEFT='+left);
  InputWindowObj.focus();
}
function checkInputWindow() 
{  
  if (!InputWindowObj.closed && InputWindowObj.location) { InputWindowObj.close(); }
}
function printDiv(tag)
{
  var contents = document.getElementById(tag).innerHTML;
  var frame1 = document.createElement('iframe');
  frame1.name = "frame1";
  frame1.style.position = "absolute";
  frame1.style.top = "-1000000px";
  document.body.appendChild(frame1);
  var frameDoc = frame1.contentWindow ? frame1.contentWindow : frame1.contentDocument.document ? frame1.contentDocument.document : frame1.contentDocument;
  frameDoc.document.open();
  frameDoc.document.write('<html><head><title>DIV Contents</title>');
  frameDoc.document.write('</head><body>');
  frameDoc.document.write(contents);
  frameDoc.document.write('</body></html>');
  frameDoc.document.close();
  setTimeout(function ()
  {
    window.frames["frame1"].focus();
    window.frames["frame1"].print();
    document.body.removeChild(frame1);
  }, 500);
  return false;
}
//  DeCloak -->
function LoadInParent(url, closeSelf)
{
  self.opener.location = url;
  self.opener.window.focus;
  if(closeSelf) self.close();
}
function addHidden(theForm, key, value) {
//alert("addHidden: key="+key+" value="+value);
    // Create a hidden input element, and append it to the form:
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = value;
    theForm.appendChild(input);
}
function parseQueryString(theForm,queryString)
{
//alert("pQS: queryString="+queryString);
    var queries, temp, i, l;
    // Split into key/value pairs
    queries = queryString.split("&");
    // Convert the array of strings into an object
    for ( i = 0, l = queries.length; i < l; i++ ) {
        temp = queries[i].split('=');
//alert("pQS: 0="+temp[0]+" 1="+temp[1]);
        addHidden(theForm,temp[0],temp[1]);
    }
}
function setTotals(type,TotField,AvgField)
{
  var args = setTotals.arguments;
  var TotAmt = 0;
  var AvgAmt = 0;
  var Cnt = 0;
  for (var i=3; i<args.length; i++)
  {
    var Amt = 0;
    var CheckField = args[i];
    if ( CheckField.value != "" ) 
    { Amt = parseFloat(CheckField.value); }
    TotAmt += Amt;

    if ( type == "all" ) { Cnt++; }
    else
    { if ( Amt > 0 ) { Cnt++; } }

    if ( Cnt == 0 ) { AvgAmt = 0; }
    else { AvgAmt = TotAmt / Cnt; }
  }
  TotField.value = TotAmt;
  if ( typeof AvgField !== "undefined" ) { AvgField.value = AvgAmt; }
  return true;
}
function doDisableCheck(id,o1,o2)
{
// find the value, then Disable the others
//alert("doDisableCheck: id="+id);
  var radios = document.getElementsByName(o1);
  for (var i = 0; i < radios.length; i++) 
  {       
//alert("doDisableCheck: i="+i+" value="+radios[i].value+" checked="+radios[i].checked+" disabled="+radios[i].disabled);
    if ( radios[i].value == id ) { doDisable(radios[i],o1,o2); }
  }
}
function doDisable(e1,o1,o2)
{
// Disable the others
//alert("doDisable: e1="+e1.value+", "+e1.checked);
  var radios = document.getElementsByName(o1);
  for (var i = 0; i < radios.length; i++) 
  {       
//alert("doDisable: i="+i+" value="+radios[i].value+" checked="+radios[i].checked+" disabled="+radios[i].disabled);
    if ( radios[i].value == e1.value ) { null; }
    else
    {
      if ( e1.checked ) { radios[i].checked = false; radios[i].disabled = true; }
      else { radios[i].disabled = false; }
    }
//alert("doDisable: i="+i+" value="+radios[i].value+" checked="+radios[i].checked+" disabled="+radios[i].disabled);
  }
  doShow(o1,o2);
}
function doShow(o1,o2)
{
//alert("o1="+o1);
//alert("o2="+o2);
  var a1 = o1.split('_');
  var radios = document.getElementsByName(o1);
  var mylist = a1[1]+':<BR>';
  for (var i = 0; i < radios.length; i++) 
  {       
    if (radios[i].checked) { mylist += radios[i].id+'<BR>'; }
  }
  document.getElementById(o2).innerHTML=mylist;
}
function setCheckBox(checkValue,boxName)
{
//alert("checkValue="+checkValue+" ENTER");
  var element = document.getElementsByName(boxName);
//alert("length="+element.length);
  for(var i=0; i < element.length; i++)
  {
    if (element[i].type == "checkbox")
    { element[i].checked = checkValue; }
  }
}
