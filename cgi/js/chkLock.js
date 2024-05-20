<!-- Cloak
function chkLock(fld,msg,locked)
{
//alert("fld=" + fld + " msg=" + msg + " locked=" + locked);
//  if ( locked == 0 ) { fld.focus(); }
//  else
  if ( locked != 0 )
  { 
    alert("\n" + msg + "\nNo changes permitted.\nUpdates will be ignored.\n"); 
//    fld.form[(getFormIndex(fld)+1) % fld.form.length].focus();
    fld.blur();
  }
}
//  DeCloak -->
function getFormIndex(fld)
{
  var index = -1, i = 0, found = false;
  while (i < fld.form.length && index == -1)
  if (fld.form[i] == fld)index = i;
  else i++;
  return index;
}
