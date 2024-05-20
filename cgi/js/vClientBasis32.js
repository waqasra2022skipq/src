<!--
function validate(form)
{
  return vEntry("notnull",form.ClientBasis32_B01_1
                         ,form.ClientBasis32_B02_1
                         ,form.ClientBasis32_B03_1
                         ,form.ClientBasis32_B04_1
                         ,form.ClientBasis32_B05_1
                         ,form.ClientBasis32_B06_1
                         ,form.ClientBasis32_B07_1
                         ,form.ClientBasis32_B08_1
                         ,form.ClientBasis32_B09_1
                         ,form.ClientBasis32_B10_1
                         ,form.ClientBasis32_B11_1
                         ,form.ClientBasis32_B12_1
                         ,form.ClientBasis32_B13_1
                         ,form.ClientBasis32_B14_1
                         ,form.ClientBasis32_B15_1
                         ,form.ClientBasis32_B16_1
                         ,form.ClientBasis32_B17_1
                         ,form.ClientBasis32_B18_1
                         ,form.ClientBasis32_B19_1
                         ,form.ClientBasis32_B20_1
                         ,form.ClientBasis32_B21_1
                         ,form.ClientBasis32_B22_1
                         ,form.ClientBasis32_B23_1
                         ,form.ClientBasis32_B24_1
                         ,form.ClientBasis32_B25_1
                         ,form.ClientBasis32_B26_1
                         ,form.ClientBasis32_B27_1
                         ,form.ClientBasis32_B28_1
                         ,form.ClientBasis32_B29_1
                         ,form.ClientBasis32_B30_1
                         ,form.ClientBasis32_B31_1
                         ,form.ClientBasis32_B32_1
               );
}
function validateScore(form,Field)
{
  if ( !vNum(Field,0,4) )
  { return false; }
  return vTotal("not0",form.ClientBasis32_Tot_1,form.ClientBasis32_Avg_1
                         ,form.ClientBasis32_B01_1
                         ,form.ClientBasis32_B02_1
                         ,form.ClientBasis32_B03_1
                         ,form.ClientBasis32_B04_1
                         ,form.ClientBasis32_B05_1
                         ,form.ClientBasis32_B06_1
                         ,form.ClientBasis32_B07_1
                         ,form.ClientBasis32_B08_1
                         ,form.ClientBasis32_B09_1
                         ,form.ClientBasis32_B10_1
                         ,form.ClientBasis32_B11_1
                         ,form.ClientBasis32_B12_1
                         ,form.ClientBasis32_B13_1
                         ,form.ClientBasis32_B14_1
                         ,form.ClientBasis32_B15_1
                         ,form.ClientBasis32_B16_1
                         ,form.ClientBasis32_B17_1
                         ,form.ClientBasis32_B18_1
                         ,form.ClientBasis32_B19_1
                         ,form.ClientBasis32_B20_1
                         ,form.ClientBasis32_B21_1
                         ,form.ClientBasis32_B22_1
                         ,form.ClientBasis32_B23_1
                         ,form.ClientBasis32_B24_1
                         ,form.ClientBasis32_B25_1
                         ,form.ClientBasis32_B26_1
                         ,form.ClientBasis32_B27_1
                         ,form.ClientBasis32_B28_1
                         ,form.ClientBasis32_B29_1
                         ,form.ClientBasis32_B30_1
                         ,form.ClientBasis32_B31_1
                         ,form.ClientBasis32_B32_1
               );
}
function vTotal(type,TotField,AvgField)
{
  var args = vTotal.arguments;
  var TotAmt = 0;
  var AvgAmt = 0;
  var Cnt = 0;
  for (var i=3; i<args.length; i++)
  {
    var Amt = 0;
    var CheckField = args[i];
    if ( CheckField.value != "" ) 
    { Amt = parseFloat(CheckField.value); }
    TotAmt += Amt;

    if ( type == "all" ) { Cnt++; }
    else
    { if ( Amt > 0 ) { Cnt++; } }

    if ( Cnt == 0 ) { AvgAmt = 0; }
    else
    { AvgAmt = TotAmt / Cnt; }
  }
  TotField.value = TotAmt;
  AvgField.value = AvgAmt;
  return true;
}
// DeCloak -->
