<!-- Cloak
function validate(form)
{
  if(!isEmpty( form.ClientGDSS_Score_1 ) && !isEmpty(form.ClientGDSS_TestDate_1)) {
    return 1;
  }
  return vEntry("notnull",form.ClientGDSS_TestDate_1
                         ,form.ClientGDSS_q1_1
                         ,form.ClientGDSS_q2_1
                         ,form.ClientGDSS_q3_1
                         ,form.ClientGDSS_q4_1
                         ,form.ClientGDSS_q5_1
                         ,form.ClientGDSS_q6_1
                         ,form.ClientGDSS_q7_1
                         ,form.ClientGDSS_q8_1
                         ,form.ClientGDSS_q9_1
                         ,form.ClientGDSS_q10_1
                         ,form.ClientGDSS_q11_1
                         ,form.ClientGDSS_q12_1
                         ,form.ClientGDSS_q13_1
                         ,form.ClientGDSS_q14_1
                         ,form.ClientGDSS_q15_1
               );
}
//  DeCloak -->
