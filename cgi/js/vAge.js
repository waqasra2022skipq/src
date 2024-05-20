<!-- Cloak

function vAge(AgeStr) 
{
  var args = vAge.arguments;
  var emptyok = args[1];

  if ( AgeStr.value == '' )
  { return true; }

  // Checks for the following valid Age formats:
  // Also separates date into years and months variables
  // patern = yrs/mos
  var AgePat = /^(\d{1,2})(\/|-)(\d{1,2})$/;
  var matchArray = AgeStr.value.match(AgePat); 
  if (matchArray == null)         // is the format ok?
  {
    alert("Age is not in a valid format.\n(yrs/mos)\nMake sure format is 1or2digits/1or2digits.");
    AgeStr.value = AgeStr.defaultValue;
    AgeStr.focus(); AgeStr.select();
    return false;
  }
  year = matchArray[1];
  month = matchArray[3];
  if (year < 1 || year > 99)    // check year range
  {
    alert("Month must be between 1 and 99.");
    AgeStr.value = AgeStr.defaultValue;
    AgeStr.focus(); AgeStr.select();
    return false;
  }
  if (month < 1 || month > 12)    // check month range
  {
    alert("Month must be between 1 and 12.");
    AgeStr.value = AgeStr.defaultValue;
    AgeStr.focus(); AgeStr.select();
    return false;
  }
  return true;
}
//  DeCloak -->
