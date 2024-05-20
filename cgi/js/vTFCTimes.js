<!--Cloak
function validate(form)
{
//if ( '11:30:00' >= '12:00:00' ) { flag = true; }
//else { flag = false; }
//alert("validate: flag=" + flag);
  for (var i=0; i < form.length; i++) 
  { 
//alert("i=" + i);
    var obj = form.elements[i];
    if( obj.type == "select-one" || obj.type == "select-multiple" )
    {
      var val = obj.options[obj.selectedIndex].value;
      if ( val != '' ) { if ( !chkFields(form,val,i) ) { return false; } }
    }
  }
}
function chkFields(form, str, idx)
{
//alert("chkRange: str=" + str + " idx=" + idx);
  var start=1;            // check Begtime to Begtimes and Endtime to Endtimes.
  if ( parseInt(idx/2,10) == parseFloat(idx/2,10) ) { start=0; }
  for (var f=start; f<form.length; f+=2)
  {
//alert("idx=" + idx + ", f=" + f + ", name=" + form.elements[f].name);
    if ( idx != f )
    {
      if( form.elements[f].type == "select-one" || form.elements[f].type == "select-multiple" )
      { if ( !chkRange(form,idx,str,f) ) { return false; } }
    }
  }
  return true;
}
function chkRange(form, idx, str, fld)
{
// check idx is even, then Begin Time check
//   otherwise End Time check
  if ( parseInt(idx/2,10) == parseFloat(idx/2,10) )
  { 
    var fld1 = form.elements[fld].options[form.elements[fld].selectedIndex].value;
    var fld2 = form.elements[fld+1].options[form.elements[fld+1].selectedIndex].value;
    if ( fld1 == '' || fld2 == '' ) { return true; }
//alert("idx=" + idx + ", str=" + str + ", fld=" + fld + ", fld1=" + fld1 + ", fld2=" + fld2);
    if ( str < fld1 || str >= fld2 ) { return true; }
    alert("START TIME CONFLICT: " + str + " conflicts with " + fld1 + " and " + fld2);
  }
  else
  {
    var beg1 = form.elements[idx-1].options[form.elements[idx-1].selectedIndex].value;
    var fld1 = form.elements[fld-1].options[form.elements[fld-1].selectedIndex].value;
    var fld2 = form.elements[fld].options[form.elements[fld].selectedIndex].value;
    if ( beg1 == '' ) { return true; }
    if ( str > beg1 )
    {
      if ( fld1 == '' || fld2 == '' ) { return true; }
//alert("idx=" + idx + ", str=" + str + ", fld=" + fld + ", beg1=" + beg1 + ", fld1=" + fld1 + ", fld2=" + fld2);
      if (str <= fld1 || str > fld2 ) { return true; }
      alert("END TIME CONFLICT: " + str + " conflicts with " + fld1 + " thru " + fld2);
    }
    else
    {
      alert("CONFLICT: END TIME '" + str + "' less than or equal to '" + beg1 + "'");
    }
  }
  return false;
}
//  End -->
