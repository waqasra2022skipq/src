<!-- Cloak
function vDate(DateStr) 
{
  var args = vDate.arguments;
  var emptyok = args[1];
  var form = args[2];
  var AgeField = args[3];
  var BegDate = args[4];
  var EndDate = args[5];

  if ( DateStr.value == '' )
  { if ( emptyok ) 
    { return true; }
    else 
    { alert("Date Required!");
      DateStr.value = DateStr.defaultValue;
      DateStr.focus(); DateStr.select();
      return false;
    }
  }
  if ( DateStr.value == 't'  || DateStr.value == 'T' )
  { 
    var today = new Date();
    var year = today.getYear();
    if ( year < 1900 ) { year += 1900; }
    var month = today.getMonth() + 1;
    var day = today.getDate();
    DateStr.value = year + "-" + month + "-" + day;
  }

  // Checks for the following valid date formats:
  // Also separates date into month, day, and year variables
  // YYYY/MM/DD   YYYY-MM-DD
  var DatePat = /^(\d{4})(\/|-)(\d{1,2})\2(\d{1,2})$/;
  var matchArray = DateStr.value.match(DatePat); 
  if (matchArray == null)         // is the format ok?
  {
    // MM/DD/YY   MM/DD/YYYY   MM-DD-YY   MM-DD-YYYY
//    var DatePat = /^(\d{1,2})(\/|-)(\d{1,2})\2(\d{2}|\d{4})$/;
    var DatePat = /^(\d{1,2})(\/|-)(\d{1,2})\2(\d{4})$/;
    var matchArray = DateStr.value.match(DatePat); 
    if (matchArray == null)       // is the format ok?
    {
      alert("Date is not in a valid format.\n(yyyy/mm/dd or mm/dd/yyyy)\nMake sure year is 4 digits.\nYou can use a 'T' for todays date.");
      DateStr.value = DateStr.defaultValue;
      DateStr.focus(); DateStr.select();
      return false;
    }
    month = matchArray[1];        // parse date into variables
    day = matchArray[3];
    year = matchArray[4];
//    if ( year >= 55 && year <= 99 ) { year = '19' + year; }
//    if ( year < 55 ) { year = '20' + year; }
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
  if (year < 1900 ) 
  {
    alert("Year must be greater than 1900.");
    DateStr.value = DateStr.defaultValue;
    DateStr.focus(); DateStr.select();
    return false;
  }
// date is valid
  if ( month.length < 2 ) { month = '0' + month; }
  if ( day.length < 2 ) { day = '0' + day; }
  DateStr.value = year + "-" + month + "-" + day;
  if ( BegDate )
  {
    if ( DateStr.value < BegDate )
    {
      alert("Date cannot be before " + BegDate + "!");
      DateStr.value = DateStr.defaultValue;
      DateStr.focus(); DateStr.select();
      return false;
    }
  }
  if ( EndDate )
  {
    if ( DateStr.value > EndDate )
    {
      alert("Date cannot be after " + EndDate + "!");
      DateStr.value = DateStr.defaultValue;
      DateStr.focus(); DateStr.select();
      return false;
    }
  }
  if ( AgeField ) { getAge(form,DateStr,AgeField); }
  return true;
}
function setToday(fld)
{
  if ( fld.value == '' || fld.value == 't' || fld.value == 'T' )
  {
    var today = new Date();
    var year = today.getYear();
    if ( year < 1900 ) { year += 1900; }
    var month = today.getMonth() + 1;
    var day = today.getDate();
    if ( month < 10 ) { month = '0' + month; }
    if ( day < 10 ) { day = '0' + day; }
//    alert("month=" + month + ", day=" + day);
    fld.value = year + "-" + month + "-" + day;
    fld.select();
  }
  return true;
}
function getAge(form,DateStr,AgeField)
{
  var now = new Date();
  var curyear = now.getYear();
  if ( curyear < 1900 ) { curyear += 1900; }
  var curmonth = now.getMonth();
  curmonth++;
  var curday = now.getDate();

  // must be a 4-digit year.
  var YYYYMMDD = /^(\d{4})-(\d{1,2})-(\d{1,2})$/;
  var dateArray = DateStr.value.match(YYYYMMDD);
  if ( dateArray == null )
  { form[AgeField].value = 'null';
    return true;
  }
  year = dateArray[1];
  month = dateArray[2];
  day = dateArray[3];

  var Age = curyear - year;
  if ( curmonth < month ) { Age--; }
  if ( curmonth == month && curday < day ) { Age--; }
  form[AgeField].value = Age;
  document.getElementById(AgeField).value = Age;
  return true;
}
//  DeCloak -->
