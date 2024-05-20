<!-- Cloak
function mDate(DateStr,aMonth,aDay)
{
//alert("indate is " + DateStr + " & " + DateStr.value + " m=" + aMonth + " d=" + aDay);
  var DatePat = /^(\d{4})-(\d{1,2})-(\d{1,2})$/;
  var matchArray = DateStr.value.match(DatePat); 
//alert("match is " + matchArray );
  var year = parseInt(matchArray[1],10);
  var month = parseInt(matchArray[2],10);
  var day = parseInt(matchArray[3],10);

//alert("0. date is " + year + "-" + month + "-" + day);
  month += parseInt(aMonth);
//alert("1. date is " + year + "-" + month + "-" + day);
  while ( month > 12 ) { month-=12; year+=1; }
  while ( month < 1 ) { month+=12; year-=1; }
  var isleap = (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0));
  if ( month==4 || month==6 || month==9 || month==11 ) { maxDay = 30; }
  else if ( month == 2 ) { if ( isleap ) { maxDay = 29; } else { maxDay = 28 }; }
  else { maxDay = 31; }
// if we want month to stay within next month
//  while ( day > maxDay ) { day -= 1; }
  day += parseInt(aDay);
//alert("2. date is " + year + "-" + month + "-" + day);
  while ( day > maxDay ) 
  { day -= maxDay; 
    month+=1;
    if ( month > 12 ) { month-=12; year+=1; }
    isleap = (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0));
    if ( month==4 || month==6 || month==9 || month==11 ) { maxDay = 30; }
    else if ( month == 2 ) { if ( isleap ) { maxDay = 29; } else { maxDay = 28 }; }
    else { maxDay = 31; }
  }
  while ( day < 1 ) 
  { month-=1;
    if ( month < 1 ) { month+=12; year-=1; }
    isleap = (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0));
    if ( month==4 || month==6 || month==9 || month==11 ) { maxDay = 30; }
    else if ( month == 2 ) { if ( isleap ) { maxDay = 29; } else { maxDay = 28 }; }
    else { maxDay = 31; }
    day += maxDay; 
  }

  if ( month < 10 ) { month = '0' + month; }
  if ( day < 10 ) { day = '0' + day; }
//alert("3. date is " + year + "-" + month + "-" + day);
  return year + "-" + month + "-" + day;
}
function vSetDate(DateStr) 
{
  var args = vSetDate.arguments;
  var emptyok = args[1];
  var form = args[2];
  var DateField = args[3];
  var months = args[4];
  var days = args[5];
  if ( ! vDate(DateStr,emptyok) ) { return false; }
  form[DateField].value = mDate(DateStr,months,days);
  return true;
}
//  DeCloak -->
