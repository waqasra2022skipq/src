function validate(form)
{
  return vEntry("notnull",form.ClientAUDITC_TestDate_1
                         ,form.ClientAUDITC_q1_1
                         ,form.ClientAUDITC_q2_1
                         ,form.ClientAUDITC_q3_1
               );
}
function validateScore(form,Field,min,max)
{
  // if ( !vNum(Field,min,max) ) { return false; }
  // setTotals("not0",form.ClientAUDITC_Score_1,form.Average
  //                        ,form.ClientAUDITC_q1_1
  //                        ,form.ClientAUDITC_q2_1
  //                        ,form.ClientAUDITC_q3_1
  //              );
  // form.ClientAUDITC_Result_1.value = 'Negative';
  // if ( form.ClientAUDITC_Score_1.value >= 8 ) { form.ClientAUDITC_Result_1.value = 'Positive'; }
  return true;
}
