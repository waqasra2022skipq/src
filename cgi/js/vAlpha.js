<!-- Cloak

function vAlpha(Str,Min,Max) 
{
  if ( Str.value == "" ) { return true; }

  var Alpha = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var tmp;
  var NewAlpha = "";
  for (var i=0; i<Str.value.length; i++) 
  { 
    tmp = Str.value.substring(i,i+1);
//alert("tmp=" + tmp );
    if (Alpha.indexOf(tmp) == "-1")
    {
      alert("Entry must be a A-Z or a-z ");
      Str.value = Str.defaultValue;
      Str.focus(); Str.select();
      return false;
    }
    else { NewAlpha = NewAlpha + tmp; }
//alert("NewAlpha=" + NewAlpha );
  }
  Str.value = NewAlpha;
  return true;
}

//  DeCloak -->
