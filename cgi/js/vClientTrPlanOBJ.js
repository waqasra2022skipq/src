<!-- Cloak
function validate(form)
{
  if ( !vEntry("notnull",form.ClientTrPlanOBJ_Obj_1
                        ,form.ClientTrPlanOBJ_InitiatedDate_1
               )
     ) { return false; }
  var field = form.ClientTrPlanOBJ_ProvID1_1;
  if ( !chkBoth(form.ClientTrPlanOBJ_Service1_1,field) )
  { return vOK(field,"Input is required in Provider 1"); }
  var field = form.ClientTrPlanOBJ_ProvID2_1;
  if ( !chkBoth(form.ClientTrPlanOBJ_Service2_1,field) )
  { return vOK(field,"Input is required in Provider 2"); }
  var field = form.ClientTrPlanOBJ_ProvID3_1;
  if ( !chkBoth(form.ClientTrPlanOBJ_Service3_1,field) )
  { return vOK(field,"Input is required in Provider 3"); }
}
function chkBoth(obj1,obj2)
{
//alert("opt1 value="+obj1.options[obj1.selectedIndex].value);
  if ( obj1.options[obj1.selectedIndex].value )
  {
//alert("opt2 value="+obj2.options[obj2.selectedIndex].value);
    if ( obj2.options[obj2.selectedIndex].value )
    { return true; }
    else
    { return false; }
  }
  return true;
}
//  DeCloak -->
