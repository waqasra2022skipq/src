<!-- Cloak

function vNum(NumStr,Min,Max) 
{
  if ( NumStr.value == "" ) { return true; }
  if ( NumStr.value == "A" ) { NumStr.value = Max; return true; }
  if ( NumStr.value == "a" ) { NumStr.value = Max; return true; }
  var args = vNum.arguments;
  var argsmsg = '';
  for (var i=3; i<args.length; i++)
  {
    var a = args[i];
    if ( NumStr.value == a ) { NumStr.value = a; return true; }
    argsmsg = argsmsg + ',' + a;
  }

  var Num = "0123456789.-";
  var tmp;
  var NewNum = "";
  for (var i=0; i<NumStr.value.length; i++) 
  { 
    tmp = NumStr.value.substring(i,i+1);
//alert("tmp=" + tmp );
    if (tmp == "$") { null; }
    else if (tmp == ",") { null; }
    else if (Num.indexOf(tmp) == "-1")
    {
      alert("Entry must be a valid number " + argsmsg);
      NumStr.value = NumStr.defaultValue;
      NumStr.focus(); NumStr.select();
      return false;
    }
    else { NewNum = NewNum + tmp; }
//alert("NewNum=" + NewNum );
  }
  NumStr.value = NewNum;
//alert("val=" + parseFloat(NumStr.value,10) + " min=" + parseFloat(Min,10) + " max=" + parseFloat(Max,10) );
  if (parseFloat(NumStr.value,10) < parseFloat(Min,10) 
   || parseFloat(NumStr.value,10) > parseFloat(Max,10))    // check range
  {
    alert("Number must be between '" + Min + "' and '" + Max + "' \nor enter an 'A' for maximun value " + Max + ".");
    NumStr.value = NumStr.defaultValue;
    NumStr.focus(); NumStr.select();
    return false;
  }
  return true;
}

//  DeCloak -->
