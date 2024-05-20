<!-- Cloak
function vZip(Zip) 
{

  if ( Zip.value == "" ) { return true; }
  var AuthPat = /(^\d{5}$)/;
  var matchArray = Zip.value.match(AuthPat); 
  if (matchArray == null)       // is the format ok?
  {
    var AuthPat = /^(\d{5})\-(\d{4})$/;
    var matchArray = Zip.value.match(AuthPat); 
    if (matchArray == null)       // is the format ok?
    {
      alert("Invalid Number!\nMust be in 1 of 2 formats\n12345-6789\nor\n12345\ndigits only.");
      Zip.value = Zip.defaultValue;
      Zip.focus(); Zip.select();
      return false;
    }
  }
  return true;
}
//  DeCloak -->
