<!--Cloak

function vPhone(PhoneStr)
{

  if (PhoneStr.value == "") { return true; }       

  var PhonePat = /\S?(\d{3})\S?[\s|\-|\.]?(\d{3})[\s|\-|\.]?(\d{4})[\s|\-|\.|\x]?(\d{0,5})$/;
  var matchArray = PhoneStr.value.match(PhonePat); 
  if (matchArray == null)         // is the format ok?
  {
    alert("Invalid phone number format!");
    PhoneStr.value = PhoneStr.defaultValue;
    PhoneStr.focus(); PhoneStr.select(); 
    return false;
  }
  else
  {
    AC = matchArray[1];
    PF = matchArray[2];
    BD = matchArray[3];
    EX = matchArray[4];
  }
  if ( EX.length > 0 ) { EX = "x" + EX; }
//  PhoneStr.value = "(" + AC + ") " + PF + "-" + BD + " " + EX;
  PhoneStr.value = AC + "-" + PF + "-" + BD + EX;
  return true;
}
//  DeCloak -->
