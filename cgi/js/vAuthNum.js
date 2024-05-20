<!-- Cloak

function vAuthNum(AuthNum,InsTAG) 
{

  if ( AuthNum.value == "" ) { return true; }
  if ( InsTAG != 'medicaid' && InsTAG != 'medicare' ) { return true; }

  var AuthPat = /^(\d{10})$/;
  var matchArray = AuthNum.value.match(AuthPat); 
  if (matchArray == null)       // is the format ok?
  {
    var AuthPat = /^M(\d{9})$/;
    var matchArray = AuthNum.value.match(AuthPat); 
    if (matchArray == null)       // is the format ok?
    {
      var AuthPat = /^PB(\d{8})$/;
      var matchArray = AuthNum.value.match(AuthPat); 
      if (matchArray == null)       // is the format ok?
      {
        var AuthPat = /\d{12}/;
        var matchArray = AuthNum.value.match(AuthPat); 
        if (matchArray == null)       // is the format ok?
        {
          alert("Invalid Number!\nMust be\n10 digits\nor\nM followed by 9 digits\nor\nPB followed by 8 digits.");
          AuthNum.value = AuthNum.defaultValue;
          AuthNum.focus(); AuthNum.select();
          return false;
        }
      }
    }
  }
  var Num = matchArray[1];
  return true;
}

//  DeCloak -->
