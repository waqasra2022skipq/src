// <!-- Cloak

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
  var ws = "HEIGHT="+h+",WIDTH="+w+",SCROLLBARS=yes,RESIZABLE=yes,STATUS=yes";
  ReportWindowObj = window.open(newURL,newName,ws);
  ReportWindowObj.focus();
}
var PopupWindowObj="";
function ActionWindow(newURL,newName,h,w)
{
  if (h==undefined) { h = '700'; }
  if (w==undefined) { w = '1000'; }
  var ws = "HEIGHT=" + h + ",WIDTH=" + w + ",SCROLLBARS=yes";
  PopupWindowObj = window.open(newURL,newName,ws);
  PopupWindowObj.focus();
}
function PopupWindow(newName,h,w,t)
{
  var ws = "HEIGHT=" + h + ",WIDTH=" + w + ",SCROLLBARS=yes";
  PopupWindowObj = window.open('',newName,ws);
  PopupWindowObj.document.write('<html><head><title>' + newName + '</title>');
  PopupWindowObj.document.write('</head><body onload="window.focus();" >');
  PopupWindowObj.document.write('<p style="text-align: right; vertical-align: top;" ><a href="javascript:window.close()">Close</a></p>');
  PopupWindowObj.document.write(t);
  PopupWindowObj.document.write('</body></html>');
  PopupWindowObj.focus();
}
function checkPopupWindow() 
{  
  if (!PopupWindowObj.closed && PopupWindowObj.location) { PopupWindowObj.close(); }
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
