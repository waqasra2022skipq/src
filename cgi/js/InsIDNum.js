<!-- Cloak

function vInsIDNum(InsIDNum,InsID) 
{

  if ( InsID.value == '100' || InsID.value == '101' )
  { return true; }

  InsIDNumPat =~ /[ABCDMU]\d{6}(?:-| +)\d{2}/;
  var matchArray = InsIDNum.value.match(InsIDNumPat);
  if (matchArray) { return true; }

  InsIDNumPat =~ /R\d{9}-?00/;
  var matchArray = InsIDNum.value.match(InsIDNumPat);
  if (matchArray) { return true; }

  InsIDNumPat =~ /MRH\d{5}(?:-| +)\d{2}/;
  var matchArray = InsIDNum.value.match(InsIDNumPat);
  if (matchArray) { return true; }

  InsIDNumPat =~ /MRE\d{5}(?:-| +)\d{2}/;
  var matchArray = InsIDNum.value.match(InsIDNumPat);
  if (matchArray) { return true; }

  InsIDNumPat =~ /MRP\d{5}(?:-| +)\d{2}/;
  var matchArray = InsIDNum.value.match(InsIDNumPat);
  if (matchArray) { return true; }

  InsIDNumPat =~ /RL\d+(?:-| +)\d{2}/;
  var matchArray = InsIDNum.value.match(InsIDNumPat);
  if (matchArray) { return true; }

  InsIDNumPat =~ /RA\d+(?:-| +)\d{2}/;
  var matchArray = InsIDNum.value.match(InsIDNumPat);
  if (matchArray == null) 
  { return vOK(InsIDNum,"Medicaid Number is not valid."); }
}
// DeCloak -->
