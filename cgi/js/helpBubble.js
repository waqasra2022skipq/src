<!--
/* Pop up information box. Keith L. Stephenson */
Xoffset=-60;    // modify these values to ...
Yoffset= 20;    // change the popup position.

var nav,old,iex=(document.all),yyy=-1000;
if (navigator.appName=="Netscape") { (document.layers)?nav=true:old=true; }

if (!old)
{
  var skn=(nav)?document.dek:dek.style;
  if(nav)document.captureEvents(Event.MOUSEMOVE);
  document.onmousemove=get_mouse;
}

function showHelp(msg,color)
{
  var content="<TABLE WIDTH=150 BORDER=1 BORDERCOLOR=black CELLPADDING=2 CELLSPACING=0 "+ "BGCOLOR="+color+"><TR><TD ALIGN=center><FONT COLOR=black SIZE=2>"+msg+"</FONT></TD></TR></TABLE>";
  if (old) 
  { alert(msg); return; } 
  else
  { yyy=Yoffset;
    if (nav) 
    { skn.document.write(content);
      skn.document.close();
      skn.visibility="visible";
    }
    else if (iex) 
    { document.all("dek").innerHTML=content;
      skn.visibility="visible";
    }
  }
}

function get_mouse(e)
{
  var x=(nav)?e.pageX:event.x+document.body.scrollLeft;skn.left=x+Xoffset;
  var y=(nav)?e.pageY:event.y+document.body.scrollTop;skn.top=y+yyy;
}

function hideHelp()
{ if (!old) { yyy=-1000; skn.visibility="hidden";} }
//-->
