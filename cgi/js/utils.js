function ReportWindow(url, windowName, height, width) {
    window.open(url, windowName, `height=${height},width=${width},resizable=yes,scrollbars=yes`);
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
function stringTrim(str)
{
  str.value=str.value.replace(/^\s+|\s+$/g,"");
  return true;
}
function is_numeric(NumStr) 
{
  var Num = "0123456789.-";
  for (var i=0; i<NumStr.length; i++) 
  { 
    tmp = NumStr.substring(i,i+1);
    if (tmp == "$") { null; }
    else if (tmp == ",") { null; }
    else if (Num.indexOf(tmp) == "-1") { return false; }
  }
  return true;
}
