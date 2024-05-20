// ** INCLUDES **
// xLibrary scripts: credit - Michael Foster - http://www.cross-browser.com
// PUBLIC NOTICE: These scripts covered by the GNU Lesser public license:
// Local Copy: http://www.realtruth.org/include/xLibrary/license.html
var script = document.createElement("script");
script.setAttribute("type", "text/javascript");
script.setAttribute("src", "/include/xLibrary/x/x_core.js");
var script2 = document.createElement("script");
script2.setAttribute("type", "text/javascript");
script2.setAttribute("src", "/include/xLibrary/x/x_event.js");
var script3 = document.createElement("script");
script3.setAttribute("type", "text/javascript");
script3.setAttribute("src", "/include/xLibrary/x/x_drag.js");
document.getElementsByTagName("head")[0].appendChild(script);
document.getElementsByTagName("head")[0].appendChild(script2);
document.getElementsByTagName("head")[0].appendChild(script3);
		
// End Scripts covered by GNU Lesser public license. 
// All other code, Copyright 2007 © The Restored Church of God. All Rights Reserved.
// ** FUNCTIONS **
// create window
function CreateWindow(x,y,strID,title,content)
	{
	// -- Create outer Window ---------
	var divWin=document.createElement('div');
	divWin.id = strID;
	divWin.className = 'winBox';
	// --------------------------------
		
	// Close
	var divClose=document.createElement('div');
	divClose.id = strID + 'CloseBtn';
	divClose.className = 'winBtn';		
	divClose.innerHTML = 'X';
	divClose.title = 'Close';
	
	// Next Verse
	var divNext=document.createElement('div');
	divNext.id = strID + 'NextBtn';
	divNext.className = 'winBtnInvert';
	divNext.innerHTML = '>';
	divNext.title = 'Next Verse';
	divNext.disabled = false;
	// Previous Verse
	var divPrevious=document.createElement('div');
	divPrevious.id = strID + 'PreviousBtn';
	divPrevious.className = 'winBtnInvert';
	if (xIE4Up)
		divPrevious.innerHTML = '<<';
	else
		divPrevious.innerHTML = '<';
	divPrevious.title = 'Previous Verse';
	divPrevious.disabled = false;
	// Next Chapter
	var divNextChapter=document.createElement('div');
	divNextChapter.id = strID + 'NextChapterBtn';
	divNextChapter.className = 'winBtnInvert';
	divNextChapter.innerHTML = '>>';
	divNextChapter.title = 'Next Chapter';	
	divNextChapter.disabled = false;
	
	// Previous Chapter
	var divPreviousChapter=document.createElement('div');
	divPreviousChapter.id = strID + 'PreviousChapterBtn';
	divPreviousChapter.className = 'winBtnInvert';
	if (xIE4Up)	
		divPreviousChapter.innerHTML = '<<<';
	else
		divPreviousChapter.innerHTML = '<<';
	divPreviousChapter.title = 'Previous Chapter';	
	divPreviousChapter.disabled = false;
	
	// --
	// Content Area
	var divContent = document.createElement('div');
	divContent.id = strID + 'Content';
	divContent.className = 'winContent';
	divContent.innerHTML = content;
	divContent.Tag = strID;
	// --
	// Title Bar
	var divBar = document.createElement('div');
	divBar.id = strID + 'Bar';
	divBar.className = 'winBar';
	divBar.innerHTML = title;
	
	// Footer Bar
	var divFooter = document.createElement('div');
	divFooter.id = strID + 'Footer';
	divFooter.className = 'winFooterBar';
	
	// -- Assemble Window Components --
	divWin.appendChild(divFooter);
	divWin.appendChild(divClose);	
	divWin.appendChild(divBar);
	
	
	var divSlicknav = document.createElement('div');
	divSlicknav.className = 'slicknav';
	
	divSlicknav.appendChild(divPreviousChapter);	
	divSlicknav.appendChild(divPrevious);
	divSlicknav.appendChild(divNext);
	divSlicknav.appendChild(divNextChapter);	
	
	divWin.appendChild(divSlicknav);	
	divWin.appendChild(divContent);	
	// --------------------------------
	
	// !! Attach Window to Document !!
	document.getElementsByTagName('body')[0].appendChild(divWin);
	// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	
	// Set Up Window
	xMoveTo(divWin,x,y);
	
	// Attach Drag Scripts
	xEnableDrag(strID + 'Bar', SubDivOnDragStart, BarOnDrag, null);
	
	// Attach Close Script
	divClose.onclick = WinClose;
	divNext.onclick = NextVerse;
	divPrevious.onclick = PreviousVerse;
	divNextChapter.onclick = NextChapter;
	divPreviousChapter.onclick = PreviousChapter;
		
	// !! Show !!
	xShow(divWin);
	return divWin;
}
function ViewContent(strID,intHeight,intWidth,bolSizable,strTitle)
{
	var strWinID = 'SlickContentWindow-' + strID;
	
	var divWin = xGetElementById(strWinID);
	if (divWin)
		{
		// This makes window appear at mouse location
		lngToX = lngX - 15 - (intWidth / 3);
		lngToY = lngY - 8 - (intHeight / 3);	
		
		if (lngToX < 50)
			lngToX = 50;
		if (lngToY < 50)
			lngToY = 50;
		//lngToX = 150;
		//lngToY = 150;	
	
		var lngMaxX = xWidth(document.body)-10;
		var lngMaxY = xHeight(document.body)-40 + xScrollTop();
	
		if (lngToX > lngMaxX - intWidth)
			lngToX = lngMaxX - intWidth;
		if (lngToY > lngMaxY - intHeight)
			lngToY = lngMaxY - intHeight;			
		
		
		xShow(divWin);
		xMoveTo(divWin,lngToX, lngToY);
		return;
		}
	
	divWin=document.createElement('div');
	divWin.id = strWinID;
	divWin.className = 'winDynamicBox';
	
	var divClose=document.createElement('div');
	divClose.id = strWinID + 'CloseBtn';
	divClose.className = 'winBtn';		
	divClose.innerHTML = 'X';
	divClose.title = 'Close';
	
	// Content Area
	var divContent = document.createElement('div');
	divContent.id = strWinID + 'Content';
	divContent.className = 'winDynamicContent';
	divContent.innerHTML = 'Loading...';
	
	// --
	// Title Bar
	var divBar = document.createElement('div');
	divBar.id = strWinID + 'Bar';
	divBar.className = 'winBar';
	
	if (strTitle != '' && strTitle != undefined)
		divBar.innerHTML = strTitle;
	else
		divBar.innerHTML = '&nbsp;';	
	if (bolSizable)
		{
		var divResize=document.createElement('div');
		divResize.id = strWinID + 'ResizeBtn';
		divResize.className = 'winBtnResize';		
		divResize.innerHTML = '&frasl;';
		divResize.title = 'Resize';
		// Footer Bar
		var divFooter = document.createElement('div');
		divFooter.id = strWinID + 'Footer';
		divFooter.className = 'winDynamicFooterBar';
		divFooter.innerHTML = '&nbsp;';
		}
	divWin.appendChild(divClose);	
	divWin.appendChild(divBar);
	divWin.appendChild(divContent);
	
	if (bolSizable)
		{
		divWin.appendChild(divResize);			
		divWin.appendChild(divFooter);
		}
	// !! Attach Window to Document !!
	document.getElementsByTagName('body')[0].appendChild(divWin);	
	
	if (intWidth == 0 || intWidth == '')
		intWidth = 400;
	divWin.style.width = intWidth + 'px';
	if (intHeight == 0 || intHeight == '')
		intHeight = 400;
	divContent.style.height = intHeight + 'px';
	
	// This makes window appear at mouse location
	lngToX = lngX - 15 - (intWidth / 3);
	lngToY = lngY - 8 - (intHeight / 3);
	
	if (lngToX < 50)
		lngToX = 50;
	if (lngToY < 50)
		lngToY = 50;
	//lngToX = 150;
	//lngToY = 150;	
	var lngMaxX = xWidth(document.body)-10;
	var lngMaxY = xHeight(document.body)-40 + xScrollTop();
	if (lngToX > lngMaxX - intWidth)
		lngToX = lngMaxX - intWidth;
	if (lngToY > lngMaxY - intHeight)
		lngToY = lngMaxY - intHeight;		
	// Set Up Window
	xMoveTo(divWin,lngToX,lngToY);
	
	/*
	intWidth = parseInt(intWidth) + 9;
	divWin.style.width = intWidth + 'px';
	*/
	
	xEnableDrag(strWinID + 'Bar', SubDivOnDragStart, BarOnDrag, null);
	if (bolSizable)
		xEnableDrag(strWinID + 'ResizeBtn', SubDivOnDragStart, ResizeOnDrag, null);	
	
	// Attach Close Script
	divClose.onclick = WinClose;	
	// !! Show !!
	xShow(divWin);	
	
	AjaxReadContent(strID);		
	
	return divWin;	
}
function ViewIMG(strID, strFilename, intWidth, intHeight, title, strSource, strCaption)
{
	divWin = xGetElementById(strID);
	if (divWin)
		{
		// This makes window appear at mouse location
		lngToX = lngX - 15 - (intWidth / 3);
		lngToY = lngY - 8 - (intHeight / 3);				
		xShow(divWin);
		xMoveTo(divWin,lngToX, lngToY);
		return;
		}
	
	divWin=document.createElement('div');
	divWin.id = strID;
	divWin.className = 'winIMGBox';
	
	var divClose=document.createElement('div');
	divClose.id = strID + 'CloseBtn';
	divClose.className = 'winBtn';		
	divClose.innerHTML = 'X';
	divClose.title = 'Close';	
	
	// Content Area
	var divContent = document.createElement('div');
	divContent.id = strID + 'Content';
	divContent.className = 'winIMGContent';
	divContent.innerHTML = '<img src="' + strFilename + '" width="' + intWidth + '" height="' + intHeight + '" />';
	divContent.Tag = strID;
	
	divWin.width = intWidth;
	
	// --
	// Title Bar
	var divBar = document.createElement('div');
	divBar.id = strID + 'Bar';
	divBar.className = 'winBar';
	if (title != '')
		divBar.innerHTML = title;
	else
		divBar.innerHTML = '&nbsp;';
		
	if (strCaption != '')
		{
		var pCaption = document.createElement('p');
		pCaption.className = "caption";
		pCaption.innerHTML = strCaption;
		divContent.appendChild(pCaption);
		}		
	if (strSource != '')
		{
		var pSource = document.createElement('p');
		pSource.className = "source";
		pSource.innerHTML = strSource;
		divContent.appendChild(pSource);
		}			
	
	// Footer Bar
	var divFooter = document.createElement('div');
	divFooter.id = strID + 'Footer';
	divFooter.className = 'winFooterBar';	
	
	divWin.appendChild(divClose);	
	divWin.appendChild(divBar);
	divWin.appendChild(divContent);
	divWin.appendChild(divFooter);
	
	// !! Attach Window to Document !!
	document.getElementsByTagName('body')[0].appendChild(divWin);	
	
	// This makes window appear at mouse location
	lngToX = lngX - 15 - (intWidth / 3);
	lngToY = lngY - 8 - (intHeight / 3);	
		
	// Set Up Window
	xMoveTo(divWin,lngToX,lngToY);
	
	intWidth = parseInt(intWidth) + 9;
	divWin.style.width = intWidth + 'px';
	
	xEnableDrag(strID + 'Bar', SubDivOnDragStart, BarOnDrag, null);
	
	// Attach Close Script
	divClose.onclick = WinClose;	
	
	// !! Show !!
	xShow(divWin);	
	
	return divWin;	
}
function SubDivOnDragStart(ele, mx, my)
{
 	xZIndex(ele.parentNode.id, highZ++);
}
function BarOnDrag(ele, mdx, mdy)
{
	strID = ele.parentNode.id;
	
	var lngMaxX = xWidth(document.body);
	var lngMaxY = xHeight(document.body)-40;
	
	var lngNewX = xLeft(strID) + mdx;
	var lngNewY = xTop(strID) + mdy;
	
	if ((lngNewX) > (lngMaxX - xWidth(strID))) // Greater than max
		{
		lngNewX = lngMaxX - xWidth(strID);
		}
//	if ((xTop(strID) + mdy) > (lngMaxY - xHeight(strID))-34) // Greater than max
//		{
//		alert(xTop(strID) + ' + ' + mdy + ' > ' + lngMaxY + ' - ' + xHeight(strID)-34);
//		return;
//		}
	if (lngNewX < 0) // Less than min
		{
		lngNewX = 0;		
		}
	if ((lngNewY) < 0) // Less than min
		{
		lngNewY = 0;				
		}
		
	xMoveTo(strID, lngNewX, lngNewY);
}
function ResizeOnDrag(ele, mdx, mdy)
{
	strID = ele.parentNode.id;
	strContent = strID + 'Content';
	xWidth(strID, xWidth(strID) + mdx);
	intHeight = xHeight(strContent);
	intHeight = intHeight + 0; // Adjustment value
	xHeight(strContent, intHeight + mdy);
}
function MaxBtnOnClick()
{
	strID = this.parentNode.id;
	var div = xGetElementById(strID);
	if (div.maximized) 
		{
	    div.maximized = false;
		this.title = 'Maximize';
    	xResizeTo(div, div.prevW, div.prevH);
	    xMoveTo(div, div.prevX, div.prevY);
    	WinPaint(strID);
		}
	else 
		{
		this.title = 'Restore';
    	div.prevW = xWidth(div);
	    div.prevH = xHeight(div);
    	div.prevX = xLeft(div);
	    div.prevY = xTop(div);
    	xMoveTo(div, xScrollLeft(), xScrollTop());
	    div.maximized = true;
    	xResizeTo(div, xClientWidth(), xClientHeight());
	    WinPaint(strID);
		}
}
function WinClose()
	{
  	var divWin = xGetElementById(this.parentNode.id);
	xHide(divWin);  
	}
function ReEnable(strWin)
	{
	divWin = xGetElementById(strWin);
	divWin.disabled = false;
	}	
function NextVerse()
	{
	if (this.disabled == false)
		{
		this.disabled = true;
		setTimeout("ReEnable('" + this.id + "')", 600);		
		var strWin = this.parentNode.parentNode.id
		var divWin = xGetElementById(strWin);		
		strBook = divWin.strBook;
		strChapter = divWin.strChapter
		strVerse = divWin.strVerse;
		AjaxNextVerse('/dynamic_content/nextverse.php?strBook=' + strBook + '&strChapter=' + strChapter + '&strVerse=' + strVerse, strWin);
		}
	}
function PreviousVerse()
	{
	if (this.disabled == false)
		{
		this.disabled = true;
		setTimeout("ReEnable('" + this.id + "')", 600);		
		var strWin = this.parentNode.parentNode.id
		var divWin = xGetElementById(strWin);		
		strBook = divWin.strBook;
		strChapter = divWin.strChapter
		strVerse = divWin.strVerse;
		AjaxNextVerse('/dynamic_content/previousverse.php?strBook=' + strBook + '&strChapter=' + strChapter + '&strVerse=' + strVerse, strWin);
		}		
	}
function NextChapter()
	{
	if (this.disabled == false)
		{
		this.disabled = true;
		setTimeout("ReEnable('" + this.id + "')", 600);		
		var strWin = this.parentNode.parentNode.id
		var divWin = xGetElementById(strWin);		
		strBook = divWin.strBook;
		strChapter = divWin.strChapter
		strVerse = divWin.strVerse;
		AjaxNextVerse('/dynamic_content/nextchapter.php?strBook=' + strBook + '&strChapter=' + strChapter + '&strVerse=' + strVerse, strWin);
		}		
	}
function PreviousChapter()
	{
	if (this.disabled == false)
		{
		this.disabled = true;
		setTimeout("ReEnable('" + this.id + "')", 600);		
		var strWin = this.parentNode.parentNode.id
		var divWin = xGetElementById(strWin);		
		strBook = divWin.strBook;
		strChapter = divWin.strChapter
		strVerse = divWin.strVerse;
		AjaxNextVerse('/dynamic_content/previouschapter.php?strBook=' + strBook + '&strChapter=' + strChapter + '&strVerse=' + strVerse, strWin);
		}			
	}
function slickWindow(strBook,strChapter,strVerse)
	{
    strID = strBook + '-' + strChapter + '-' + strVerse;
	strWinID = 'Win' + strID;
	if (strVerse == 'ALL')
		strDisplay = strBook + ' ' + strChapter + ' (KJV)';
	else
	    strDisplay = strBook + ' ' + strChapter + ':' + strVerse + ' (KJV)';
	
	// This makes window appear at mouse location
	lngToX = lngX - 15;
	lngToY = lngY - 8;
	
	var objWin = xGetElementById(strWinID);
	if (!objWin)
		{
		objWin = CreateWindow(lngToX, lngToY, strWinID, strDisplay, 'Loading...');
		
		// basically storing as variables (who wants to use a class, anyway? :P)
		objWin.strBook = strBook;
		objWin.strChapter = strChapter;
		objWin.strVerse = strVerse;
		AjaxReadVerse('/dynamic_content/readverse.php?strBook=' + strBook + '&strChapter=' + strChapter + '&strVerse=' + strVerse, strWinID);		
		}
	else
		{
		xShow(objWin);
		xMoveTo(objWin,lngToX, lngToY);
		objWin.strBook = strBook;
		objWin.strChapter = strChapter;
		objWin.strVerse = strVerse;		
		AjaxReadVerse('/dynamic_content/readverse.php?strBook=' + strBook + '&strChapter=' + strChapter + '&strVerse=' + strVerse, strWinID);
		RefreshTitle(strWinID, strBook, strChapter, strVerse);
		}
		
	lngDocWidth = xWidth(document);
	lngWinWidth = xWidth(objWin);
	lngWinHeight = xHeight(objWin);
	
	if (lngToX > (lngDocWidth - lngWinWidth))
		xMoveTo(objWin, lngDocWidth-lngWinWidth, lngToY);
	}
	
function WriteContent(strWinID, strContent)
	{
	divContent = xGetElementById(strWinID + 'Content');
	divContent.innerHTML = strContent;
	}
function InitSlick(strID)
	{
	objWin = xGetElementById(strID);
	objBar = xGetElementById(strID + 'Bar');
	objFooter = xGetElementById(strID + 'Footer');
	objContent = xGetElementById(strID + 'Content');
	xResizeTo(objWin, xWidth(objWin), xHeight(objContent) + xHeight(objBar) + xHeight(objFooter));
	}
	
function RefreshTitle(strID, strBook, strChapter, strVerse)
	{
	objWin = xGetElementById(strID);
	objWin.strBook = strBook;
	objWin.strChapter = strChapter;
	objWin.strVerse = strVerse;
	objBar = xGetElementById(strID + 'Bar');
	if (objWin.strVerse == 'ALL')
		objBar.innerHTML = objWin.strBook + ' ' + objWin.strChapter + ' (KJV)';	
	else
		objBar.innerHTML = objWin.strBook + ' ' + objWin.strChapter + ':' + objWin.strVerse + ' (KJV)';	
	}
	
function DynamicContentWrite(strID, strContent)
	{
	var strWinID = 'SlickContentWindow-' + strID;
	var strContentID = strWinID + 'Content';	
	var divContent = xGetElementById(strContentID);
	divContent.innerHTML = strContent;
	}

