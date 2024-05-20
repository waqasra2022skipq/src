
<!--Cloak

function vSSN(field)
{

  var SSNStr = field.value;
  var errmsg;

  if (SSNStr == "") { return true; }       

  var valid = "0123456789-";
  var del1 = 0; del2 = 0;
  var temp;
  for (var i=0; i< SSNStr.length; i++)
  { temp = "" + SSNStr.substring(i, i+1);
    if (valid.indexOf(temp) == "-1")
    { alert("SSN has invalid characters!"); 
      field.value = field.defaultValue;
      field.focus(); field.select(); return false;
    }
    if ( temp == "-" )
    { 
      if ( i == 0 )
      { alert("Invalid 1st character in SSN!");
        field.value = field.defaultValue;
        field.focus(); field.select(); return false;
      }
      else if ( del1 == 0 ) { del1 = i; }
      else if ( del2 == 0 ) { del2 = i; }
      else
      { alert("Too many delimeters in SSN!");
        field.value = field.defaultValue;
        field.focus(); field.select(); return false;
      }
    }
  }
  if ( del1 == 0 && del2 == 0 )
  {
    var part1 = SSNStr.substring(0,3);
    var part2 = SSNStr.substring(3,5);
    var part3 = SSNStr.substring(5,SSNStr.length);
  }
  else if ( del1 == 0 || del2 == 0 )
  { alert("Missing a '-'!");
    field.value = field.defaultValue;
    field.focus();
    field.select();
    return false;
  }
  else
  { 
    var part1 = SSNStr.substring(0,del1);
    var part2 = SSNStr.substring(del1+1,del2);
    var part3 = SSNStr.substring(del2+1,SSNStr.length);
  }
  if ( part1.length < 3 )
  { errmsg = "1st part of SSN to short! Make sure it is 3 digits."; }
  else if ( part1.length > 3 )
  { errmsg = "1st part of SSN to long! Make sure it is 3 digits."; }
  else if ( part2.length < 2 )
  { errmsg = "2nd part of SSN to short! Make sure it is 2 digits."; }
  else if ( part2.length > 2 )
  { errmsg = "2nd part of SSN to long! Make sure it is 2 digits."; }
  else if ( part3.length < 4 )
  { errmsg = "3rd part of SSN to short! Make sure it is 4 digits."; }
  else if ( part3.length > 4 )
  { errmsg = "3rd part of SSN to long! Make sure it is 4 digits."; }
  else
  { field.value = part1 + "-" + part2 + "-" + part3; return true; }

  alert(errmsg);
  field.value = field.defaultValue;
  field.focus();
  field.select();
  return false;
}
//  DeCloak -->
