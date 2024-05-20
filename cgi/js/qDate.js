<!-- Cloak

function qDate(DateStr) 
{
  if ( DateStr.value == "" ) { return true; }

  // Checks for the following valid date formats:
  // Also separates date into month, day, and year variables
  // YYYY/MM/DD   YYYY-MM-DD
  var DatePat = /^(\?{4}|\d{4})(\/|-)(\?{2}|\d{1,2})\2(\?{2}|\d{1,2})$/;
  var matchArray = DateStr.value.match(DatePat); 
  if (matchArray == null)         // is the format ok?
  {
    // MM/DD/YY   MM/DD/YYYY   MM-DD-YY   MM-DD-YYYY
    var DatePat = /^(\?{2}|\d{1,2})(\/|-)(\?{2}|\d{1,2})\2(\?{4}|\d{4})$/;
    var matchArray = DateStr.value.match(DatePat); 
    if (matchArray == null)       // is the format ok?
    {
      alert("Date is not in a valid format.\n(yyyy/mm/dd or mm/dd/yyyy)\nMake sure year is 4 digits.\nNote: use ?? for unknown month or day, ???? for year.");
      DateStr.value = DateStr.defaultValue;
      DateStr.focus(); DateStr.select();
      return false;
    }
    month = matchArray[1];        // parse date into variables
    day = matchArray[3];
    year = matchArray[4];
  }
  else                            // parse date into variables
  {
    year = matchArray[1];
    month = matchArray[3];
    day = matchArray[4];
  }
  if (month < 1 || month > 12)    // check month range
  {
    alert("Month must be between 1 and 12.");
    DateStr.value = DateStr.defaultValue;
    DateStr.focus(); DateStr.select();
    return false;
  }
  if (day < 1 || day > 31) 
  {
    alert("Day must be between 1 and 31.");
    DateStr.value = DateStr.defaultValue;
    DateStr.focus(); DateStr.select();
    return false;
  }
  if ((month==4 || month==6 || month==9 || month==11) && day==31) 
  {
    alert("Month "+month+" doesn't have 31 days!")
    DateStr.value = DateStr.defaultValue;
    DateStr.focus(); DateStr.select();
    return false;
  }
  if (month == 2)                 // check for february 29th
  { 
    var isleap = (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0));
    if (day>29 || (day==29 && !isleap)) 
    {
      alert("February doesn't have " + day + " days!");
      DateStr.value = DateStr.defaultValue;
      DateStr.focus(); DateStr.select();
      return false;
    }
  }
                                  // date is valid
  DateStr.value = year + "-" + month + "-" + day;
  return true;
}

//  DeCloak -->
