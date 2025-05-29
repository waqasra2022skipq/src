
// *** COMMON CROSS-BROWSER COMPATIBILITY CODE ***

//var isDOM=document.getElementById?1:0;
//var isIE=document.all?1:0;
//var isNS4=navigator.appName=='Netscape'&&!isDOM?1:0;
//var isOp=window.opera?1:0;
//var isWin=navigator.platform.indexOf('Win')!=-1?1:0;
//var isDyn=isDOM||isIE||isNS4;
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

if (!window.LayerObj) var LayerObj = new Function('id', 'par',
 'this.ref=getRef(id, par); this.sty=getSty(id, par); return this');
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
alert("Name=" + msgName + ", Info=" + MsgInfo);
alert("message.info=" + textMsg.message.info);
showProps(textMsg,"textMsg");
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
