function validate(form)
{
  return vEntry("notnull",form.ClientAUDIT_TestDate_1
                         ,form.ClientAUDIT_q1_1
                         ,form.ClientAUDIT_q9_1
                         ,form.ClientAUDIT_q10_1
               );
}
function validateInputs(form)
{
  if (form.ClientAUDIT_q1_1.value == 0) {
    setDisableInputs(form.ClientAUDIT_q2_1, true);
    setDisableInputs(form.ClientAUDIT_q3_1, true);
    setDisableInputs(form.ClientAUDIT_q4_1, true);
    setDisableInputs(form.ClientAUDIT_q5_1, true);
    setDisableInputs(form.ClientAUDIT_q6_1, true);
    setDisableInputs(form.ClientAUDIT_q7_1, true);
    setDisableInputs(form.ClientAUDIT_q8_1, true);
  } else {
    setDisableInputs(form.ClientAUDIT_q2_1, false);
    setDisableInputs(form.ClientAUDIT_q3_1, false);
    setDisableInputs(form.ClientAUDIT_q4_1, false);
    setDisableInputs(form.ClientAUDIT_q5_1, false);
    setDisableInputs(form.ClientAUDIT_q6_1, false);
    setDisableInputs(form.ClientAUDIT_q7_1, false);
    setDisableInputs(form.ClientAUDIT_q8_1, false);

    if (form.ClientAUDIT_q2_1.value == 0 && form.ClientAUDIT_q3_1.value == 0) {
      setDisableInputs(form.ClientAUDIT_q4_1, true);
      setDisableInputs(form.ClientAUDIT_q5_1, true);
      setDisableInputs(form.ClientAUDIT_q6_1, true);
      setDisableInputs(form.ClientAUDIT_q7_1, true);
      setDisableInputs(form.ClientAUDIT_q8_1, true);
    } else {
      setDisableInputs(form.ClientAUDIT_q4_1, false);
      setDisableInputs(form.ClientAUDIT_q5_1, false);
      setDisableInputs(form.ClientAUDIT_q6_1, false);
      setDisableInputs(form.ClientAUDIT_q7_1, false);
      setDisableInputs(form.ClientAUDIT_q8_1, false);
    }
  }
}
function setDisableInputs(inputs, disabled)
{
  for (var i=0; i<inputs.length; i++) {
    inputs[i].disabled = disabled;
  }
}
function validateScore(form,Field,min,max)
{
  // if ( !vNum(Field,min,max) ) { return false; }
  // setTotals("not0",form.ClientAUDIT_Score_1,form.Average
  //                        ,form.ClientAUDIT_q1_1
  //                        ,form.ClientAUDIT_q2_1
  //                        ,form.ClientAUDIT_q3_1
  //                        ,form.ClientAUDIT_q4_1
  //                        ,form.ClientAUDIT_q5_1
  //                        ,form.ClientAUDIT_q6_1
  //                        ,form.ClientAUDIT_q7_1
  //                        ,form.ClientAUDIT_q8_1
  //                        ,form.ClientAUDIT_q9_1
  //                        ,form.ClientAUDIT_q10_1
  //              );
  // form.ClientAUDIT_Result_1.value = 'Negative';
  // if ( form.ClientAUDIT_Score_1.value >= 8 ) { form.ClientAUDIT_Result_1.value = 'Positive'; }
  return true;
}
