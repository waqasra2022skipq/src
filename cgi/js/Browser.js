// *** Check for Browser Version ***
var isDOM=document.getElementById?1:0;
var isIE=document.all?1:0;
var isIE4=((document.all && !isDOM)?1:0);
var isNS=(navigator.appName=='Netscape');
var isNS4=navigator.appName=='Netscape'&&!isDOM?1:0;
var isOp=window.opera?1:0;
var isWin=navigator.platform.indexOf('Win')!=-1?1:0;
var isMac=navigator.platform.indexOf('Mac')!=-1?1:0;
var isDyn=isDOM||isIE||isNS4;
