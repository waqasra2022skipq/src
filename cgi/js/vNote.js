<!-- Cloak
function getProbAddrd()
{
  var ProbBit = 0; 
  var Bit = 1; 
//alert("ProbBit=" + ProbBit +" Bit=" + Bit);
  var Probs = getElementsWithId('ProbAddrd');
  for ( var i=0; i<Probs.length; i++ )
  {
//alert("ProbBit=" + ProbBit +" Bit=" + Bit + " i=" + i);
//alert('id='+Probs[i].id+', name='+Probs[i].name);
//alert("checked "+i+"="+Probs[i].checked);
    if ( Probs[i].checked ) { ProbBit += Bit; }
    Bit *= 2;
  }
//alert("return ProbBit=" + ProbBit);
  return ProbBit;
}
//  DeCloak -->
