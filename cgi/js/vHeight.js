var vHeightFeet;
var vHeightInch;
function sBMI(height,weight,bmi) 
{
  var matchpat = /^(\d+)'? ?(\d+(\.(\d)*)?)\"?$/;
  var matcharr = height.value.match(matchpat);
  if ( matcharr == null ) { return false; }
  vHeightFeet = matcharr[1]; vHeightInch = matcharr[2]; 
  if ( !vNum(weight,1,1000) ) { return false; }
  var h = (parseFloat(vHeightFeet) * 12) + parseFloat(vHeightInch);
  var b = 0;
  if ( h > 0 ) { b = ( weight.value / ( h * h ) ) * 703; }
  bmi.value = b.toFixed(2);
}
function vHeight(height,weight,bmi) 
{
  if ( tHeight(height.value) )
  {
    if ( parseFloat(vHeightFeet,10) > 9 )
    {
      alert(height.value+" Invalid! Feet greater than 9! use feet'"+' inch"');
      height.value = height.defaultValue;
      height.focus(); height.select();
      return false;
    } 
    else if ( parseFloat(vHeightInch,10) > 12 )
    {
      alert(height.value+" Invalid! Inches greater than 12! use feet'"+' inch"');
      height.value = height.defaultValue;
      height.focus(); height.select();
      return false;
    } 
    height.value = vHeightFeet+"' "+vHeightInch+'"';   // reset to standard
    sBMI(height,weight,bmi);
  }
  else
  { 
    alert(height.value+" Invalid! use feet'"+' inch"');
    height.value = height.defaultValue;
    height.focus(); height.select();
    return false;
  } 
  return true;
}
function tHeight(h) 
{
  var matchpat = /^(\d+)'? ?(\d+(\.(\d)*)?)\"?$/;
  var matcharr = h.match(matchpat);
  if ( matcharr != null ) { vHeightFeet = matcharr[1]; vHeightInch = matcharr[2]; return true; }
  else if ( isNaN(h) ) { return false; }
  else if ( is_numeric(h) )     // take it as inches
  {
    vHeightFeet = Math.floor(h/12);
    vHeightInch = h%12;
    return true;
  }
  return false;
}
function vWeight(height,weight,bmi) 
{
  if ( vNum(weight) )
  { sBMI(height,weight,bmi); }
  else
  { 
    alert(weight.value+" Invalid! enter only numbers.");
    weight.value = weight.defaultValue;
    weight.focus(); weight.select();
    return false;
  } 
  return true;
}
//  DeCloak -->
