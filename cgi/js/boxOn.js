
<!-- TWO STEPS TO INSTALL INDENT MENU:

  1.  Copy the coding into the HEAD of your HTML document
  2.  Add the last code into the BODY of your HTML document  -->

<!-- STEP ONE: Paste this code into the HEAD of your HTML document  -->

<HEAD>

<!-- Original:  CodeLifter.com (support@codelifter.com) -->
<!-- Web Site:  http://www.codelifter.com -->

<!-- This script and many more are available free online at -->
<!-- The JavaScript Source!! http://javascript.internet.com -->

<style>
<!-- Begin
.BorderOn  { width:90px;
             margin-left:10px;
             border:1px solid #456789 }
.BorderOff { width:90px;
             margin-left:0px;
             border:1px solid #444444 }
A.mBlue:link      {color:#00CCFF; text-decoration:none;}
A.mBlue:visited   {color:#00CCFF; text-decoration:none;}
A.mBlue:active    {color:#00CCFF; text-decoration:none;}
A.mBlue:hover     {color:#FF0000; text-decoration:underline;}        
A.mGreen:link     {color:#00FF80; text-decoration:none;}
A.mGreen:visited  {color:#00FF80; text-decoration:none;}
A.mGreen:active   {color:#00FF80; text-decoration:none;}
A.mGreen:hover    {color:#FF0000; text-decoration:underline;} 
A.mYellow:link    {color:#FFFF00; text-decoration:none;}
A.mYellow:visited {color:#FFFF00; text-decoration:none;}
A.mYellow:active  {color:#FFFF00; text-decoration:none;}
A.mYellow:hover   {color:#FF0000; text-decoration:underline;}          
//-->             
</style>
<script language="JavaScript1.2">
<!-- Begin
offMessage = "Add this menu to your site!"
function boxOn(which,message) {
if (document.all||document.getElementById) {
which.className = 'BorderOn';
if (document.getElementById) {
document.getElementById("Message").innerHTML = message
}
else {
Message.innerHTML = message;
      }
   }
}
function boxOff(which) {
if (document.all||document.getElementById) {
which.className = 'BorderOff';
if (document.getElementById) {
document.getElementById("Message").innerHTML = offMessage
}
else {
Message.innerHTML = offMessage;
      }
   }
}
//  End -->
</script>

</HEAD>

<!-- STEP TWO: Copy this code into the BODY of your HTML document  -->

<BODY>

<!-- Outer Container Table //-->
<table cellpadding="0" cellspacing="0" width="100">
<tr>
<td align="center">
<!-- Header Table // -->
<table cellpadding="3" cellspacing="0" bgcolor="#000000" class="BorderOff">
<tr>
<td>
<font color="#FEDCBA" size="2" face="Arial">Heading</font>
</td>
</tr>
</table>
<!-- End Header Table //-->
<!-- Menu Items Tables
   - To add more, just follow the pattern
   - Note class= in each <a href> to attach link style colors
//-->
<!-- Menu Item One Table //-->
<table cellpadding="3" cellspacing="0" class="BorderOff" onMouseover="boxOn(this,'Visit the JavaScript Source')" onMouseout="boxOff(this)">
<tr>
<td>
<font color="#00FF80" size="2" face="Arial"><a class="mBlue" href="http://www.javascriptsource.com" target="_blank">Item One</a></font>
</td>
</tr>
</table>  
<!-- Menu Item Two Table //-->
<table cellpadding="3" cellspacing="0" class="BorderOff" onMouseover="boxOn(this,'Description 2')" onMouseout="boxOff(this)">
<tr>
<td>
<font color="#00FF80" size="2" face="Arial"><a class="mBlue" href="http://www.your-link-here.com" target="_blank">Item Two</a></font>
</td>
</tr>
</table>
<!-- Menu Item Three Table //-->
<table cellpadding="3" cellspacing="0" class="BorderOff" onMouseover="boxOn(this,'Description 3')" onMouseout="boxOff(this)">  
<tr>
<td>
<font color="#00FF80" size="2" face="Arial"><a class="mGreen" href="http://www.your-link-here.com" target="_blank">Item Three</a></font>
</td>
</tr>
</table>
<!-- Menu Item Four Table //-->
<table cellpadding="3" cellspacing="0" class="BorderOff" onMouseover="boxOn(this,'Description 4')" onMouseout="boxOff(this)">  
<tr>
<td>
<font color="#00FF80" size="2" face="Arial"><a class="mYellow" href="http://www.your-link-here.com" target="_blank">Item Four</a></font>
</td>
</tr>
</table>
<!-- End Menu Items Tables //-->
<!-- Message Table //-->
<!-- Set the width= of this table the same as the overall width in the <style> //-->
<table cellpadding="1" cellspacing="0" bgcolor="#444444" width="90">
<tr>
<td>
<!-- Set the width= of this table to the overall width
     in the style table minus 2x the border width; set
     the height= long (large) enough to accommodate your
     longest message //-->
<table cellpadding="3" cellspacing="0" bgcolor="#000000" width="88" height="100">
<tr>
<td align="left" valign="top">
<font id="Message" color="#CBA987" size="2" face="Arial">Move your mouse over the menu items.</font>
</td>
</tr>
</table>
</td>
</tr>
</table>
<!-- End Message Table //-->
</td>
</tr>
</table>
<!-- End Outer Container Table //-->
<!-- END OF MENU //-->

<p><center>
<font face="arial, helvetica" size"-2">Free JavaScripts provided<br>
by <a href="http://javascriptsource.com">The JavaScript Source</a></font>
</center><p>

<!-- Script Size:  5.35 KB -->
