function clearObj(form,idx,locked)
{
//alert('idx=' + idx + ' locked=' + locked);
  if ( locked == 1 ) { return false; }
  var Obj = eval("form.TrPlanIP_Obj" + idx + "_1");
  Obj.value = '';
  var Init = eval("form.TrPlanIP_Init" + idx + "_1");
  Init.value = '';
  var Date = eval("form.TrPlanIP_Date" + idx + "_1");
  Date.value = '';
  var Help = eval("form.TrPlanIP_Help" + idx + "_1");
  Help.value = '';
  var Serv = eval("form.TrPlanIP_Serv" + idx + "_1");
  Serv.value = '';
  var Freq = eval("form.TrPlanIP_Freq" + idx + "_1");
  Freq.value = '';
  var Cred = eval("form.TrPlanIP_Cred" + idx + "_1");
  Cred.value = '';
  var Prog = eval("form.TrPlanIP_Prog" + idx + "_1");
  Prog.value = '';
  return true;
}
function deleteObj(form,idx,locked)
{
//alert('idx=' + idx + ' locked=' + locked);
  if ( locked == 1 ) { return false; }
  for (var i=idx; i<5; i++)
  {
    var j=i+1;
    var x = eval("form.TrPlanIP_Obj" + i + "_1");
    var y = eval("form.TrPlanIP_Obj" + j + "_1");
    x.value = y.value;
//alert('i=' + i + ', j=' + j + ', x=' + x + ', y=' + y);
    var x = eval("form.TrPlanIP_Init" + i + "_1");
    var y = eval("form.TrPlanIP_Init" + j + "_1");
    x.value = y.value;
    var x = eval("form.TrPlanIP_Date" + i + "_1");
    var y = eval("form.TrPlanIP_Date" + j + "_1");
    x.value = y.value;
    var x = eval("form.TrPlanIP_Help" + i + "_1");
    var y = eval("form.TrPlanIP_Help" + j + "_1");
    x.value = y.value;
    var x = eval("form.TrPlanIP_Serv" + i + "_1");
    var y = eval("form.TrPlanIP_Serv" + j + "_1");
    x.value = y.value;
    var x = eval("form.TrPlanIP_Freq" + i + "_1");
    var y = eval("form.TrPlanIP_Freq" + j + "_1");
    x.value = y.value;
    var x = eval("form.TrPlanIP_Cred" + i + "_1");
    var y = eval("form.TrPlanIP_Cred" + j + "_1");
    x.value = y.value;
    var x = eval("form.TrPlanIP_Prog" + i + "_1");
    var y = eval("form.TrPlanIP_Prog" + j + "_1");
    x.value = y.value;
  }

  form.TrPlanIP_Obj5_1.value = '';
  form.TrPlanIP_Init5_1.value = '';
  form.TrPlanIP_Help5_1.value = '';
  form.TrPlanIP_Date5_1.value = '';
  form.TrPlanIP_Serv5_1.value = '';
  form.TrPlanIP_Freq5_1.value = '';
  form.TrPlanIP_Cred5_1.value = '';
  form.TrPlanIP_Prog5_1.value = '';
  return true;
}
