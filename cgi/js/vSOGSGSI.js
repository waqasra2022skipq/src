<!--
function validate(form)
{
  return vEntry("notnull",form.SOGSGSI_TransDate_1
                         ,form.SOGSGSI_TransType_1
                         ,form.SOGSGSI_A1_1
                         ,form.SOGSGSI_A2_1
                         ,form.SOGSGSI_A3_1
                         ,form.SOGSGSI_A4_1
                         ,form.SOGSGSI_A5_1
                         ,form.SOGSGSI_A6_1
                         ,form.SOGSGSI_A7_1
                         ,form.SOGSGSI_A8_1
                         ,form.SOGSGSI_A9_1
                         ,form.SOGSGSI_A10_1
                         ,form.SOGSGSI_A11_1
                         ,form.SOGSGSI_A12_1
                         ,form.SOGSGSI_A13_1
                         ,form.SOGSGSI_G1D_1
                         ,form.SOGSGSI_G1Y_1
                         ,form.SOGSGSI_G2D_1
                         ,form.SOGSGSI_G2Y_1
                         ,form.SOGSGSI_G3D_1
                         ,form.SOGSGSI_G3Y_1
                         ,form.SOGSGSI_G4D_1
                         ,form.SOGSGSI_G4Y_1
                         ,form.SOGSGSI_G5D_1
                         ,form.SOGSGSI_G5Y_1
                         ,form.SOGSGSI_G6D_1
                         ,form.SOGSGSI_G6Y_1
                         ,form.SOGSGSI_G7D_1
                         ,form.SOGSGSI_G7Y_1
                         ,form.SOGSGSI_G8D_1
                         ,form.SOGSGSI_G8Y_1
                         ,form.SOGSGSI_G9D_1
                         ,form.SOGSGSI_G9Y_1
                         ,form.SOGSGSI_G10D_1
                         ,form.SOGSGSI_G10Y_1
                         ,form.SOGSGSI_G11D_1
                         ,form.SOGSGSI_G11Y_1
                         ,form.SOGSGSI_G12D_1
                         ,form.SOGSGSI_G12Y_1
                         ,form.SOGSGSI_G13D_1
                         ,form.SOGSGSI_G13Y_1
                         ,form.SOGSGSI_G14D_1
                         ,form.SOGSGSI_G14Y_1
                         ,form.SOGSGSI_G15D_1
                         ,form.SOGSGSI_G15Y_1
                         ,form.SOGSGSI_G16D_1
                         ,form.SOGSGSI_G16Y_1
                         ,form.SOGSGSI_G17_1
                         ,form.SOGSGSI_G18_1
                         ,form.SOGSGSI_G19_1
                         ,form.SOGSGSI_G20_1
                         ,form.SOGSGSI_G21_1
                         ,form.SOGSGSI_G22_1
                         ,form.SOGSGSI_G24x1_1
                         ,form.SOGSGSI_G24x2_1
                         ,form.SOGSGSI_G24x3_1
                         ,form.SOGSGSI_G24x4_1
                         ,form.SOGSGSI_G24x5_1
                         ,form.SOGSGSI_G24x6_1
                         ,form.SOGSGSI_G24x7_1
                         ,form.SOGSGSI_G24x8_1
                         ,form.SOGSGSI_G25L_1
                         ,form.SOGSGSI_G25M_1
                         ,form.SOGSGSI_G26L_1
                         ,form.SOGSGSI_G26M_1
                         ,form.SOGSGSI_G27L_1
                         ,form.SOGSGSI_G27M_1
                         ,form.SOGSGSI_G28L_1
                         ,form.SOGSGSI_G28M_1
                         ,form.SOGSGSI_G29L_1
                         ,form.SOGSGSI_G29M_1
                         ,form.SOGSGSI_G30L_1
                         ,form.SOGSGSI_G30M_1
                         ,form.SOGSGSI_G31L_1
                         ,form.SOGSGSI_G31M_1
                         ,form.SOGSGSI_G32L_1
                         ,form.SOGSGSI_G32M_1
                         ,form.SOGSGSI_G33L_1
                         ,form.SOGSGSI_G33M_1
                         ,form.SOGSGSI_G34L_1
                         ,form.SOGSGSI_G34M_1
                         ,form.SOGSGSI_G35L_1
                         ,form.SOGSGSI_G35M_1
                         ,form.SOGSGSI_G36L_1
                         ,form.SOGSGSI_G36M_1
                         ,form.SOGSGSI_G37aL_1
                         ,form.SOGSGSI_G37aM_1
                         ,form.SOGSGSI_G37bL_1
                         ,form.SOGSGSI_G37bM_1
                         ,form.SOGSGSI_G37cL_1
                         ,form.SOGSGSI_G37cM_1
                         ,form.SOGSGSI_G37dL_1
                         ,form.SOGSGSI_G37dM_1
                         ,form.SOGSGSI_G37eL_1
                         ,form.SOGSGSI_G37eM_1
                         ,form.SOGSGSI_G37fL_1
                         ,form.SOGSGSI_G37fM_1
                         ,form.SOGSGSI_G37gL_1
                         ,form.SOGSGSI_G37gM_1
                         ,form.SOGSGSI_G37hL_1
                         ,form.SOGSGSI_G37hM_1
                         ,form.SOGSGSI_G37iL_1
                         ,form.SOGSGSI_G37iM_1
                         ,form.SOGSGSI_G38_1
                         ,form.SOGSGSI_G39_1
                         ,form.SOGSGSI_G41_1
                         ,form.SOGSGSI_G42a_1
                         ,form.SOGSGSI_G42b_1
               );
}
function validateLost(form,Field)
{
  if ( !vNum(Field,0,9999999) )
  { return false; }
  return vTotal("text",form.SOGSGSI_TotalLost_1,form.SOGSGSI_AvgLost_1,7
                         ,form.SOGSGSI_A7_1
                         ,form.SOGSGSI_A8_1
                         ,form.SOGSGSI_A9_1
                         ,form.SOGSGSI_A10_1
                         ,form.SOGSGSI_A11_1
                         ,form.SOGSGSI_A12_1
                         ,form.SOGSGSI_A13_1
               );
}
function validatePast(form,Field)
{
  if ( !vNum(Field,0,1) )
  { return false; }
//alert("Field v=" + Field.value + ", c=" + Field.checked);
//alert("form.SOGSGSI_G37aM_1 0 v=" + form.SOGSGSI_G37aM_1[0].value + " c=" + form.SOGSGSI_G37aM_1[0].checked);
//alert("form.SOGSGSI_G37aM_1 1 v=" + form.SOGSGSI_G37aM_1[1].value + " c=" + form.SOGSGSI_G37aM_1[1].checked);
  return vTotal("radio",form.SOGSGSI_TotalPast_1,form.SOGSGSI_AvgPast_1,9
                         ,form.SOGSGSI_G37aM_1[0]
                         ,form.SOGSGSI_G37aM_1[1]
                         ,form.SOGSGSI_G37bM_1[0]
                         ,form.SOGSGSI_G37bM_1[1]
                         ,form.SOGSGSI_G37cM_1[0]
                         ,form.SOGSGSI_G37cM_1[1]
                         ,form.SOGSGSI_G37dM_1[0]
                         ,form.SOGSGSI_G37dM_1[1]
                         ,form.SOGSGSI_G37eM_1[0]
                         ,form.SOGSGSI_G37eM_1[1]
                         ,form.SOGSGSI_G37fM_1[0]
                         ,form.SOGSGSI_G37fM_1[1]
                         ,form.SOGSGSI_G37gM_1[0]
                         ,form.SOGSGSI_G37gM_1[1]
                         ,form.SOGSGSI_G37hM_1[0]
                         ,form.SOGSGSI_G37hM_1[1]
                         ,form.SOGSGSI_G37iM_1[0]
                         ,form.SOGSGSI_G37iM_1[1]
               );
}
function vTotal(type,TotField,AvgField,Cnt)
{
  var args = vTotal.arguments;
  var TotAmt = 0;
  var AvgAmt = 0;
  for (var i=4; i<args.length; i++)
  {
    var Amt = 0;
    var CheckField = args[i];
    if ( type == "radio" ) { if ( CheckField.checked ) { Amt = parseFloat(CheckField.value); } }
    else if ( CheckField.value != "" ) 
    { Amt = parseFloat(CheckField.value); }
    TotAmt += Amt;
//alert("CheckField value=" + CheckField.value + " checked=" + CheckField.checked + " Amt =" + Amt + " Cnt=" + Cnt + " Tot=" + TotAmt);
  }
  AvgAmt = TotAmt / Cnt;
  TotField.value = TotAmt;
  AvgField.value = AvgAmt;
  return true;
}
// DeCloak -->
