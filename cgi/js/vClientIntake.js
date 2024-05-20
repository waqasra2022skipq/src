<!-- Cloak
function validate(form)
{
  if(!checkAgeAndHarmFulIntent(form.Client_Age.value, form.ClientReferrals_Harmfulintent_1.value)) {
    return false
  }
  var ventry;
  if (form.Client_Homeless_1.checked === true) {
    ventry = vEntry("notnull",form.ClientReferrals_RefDate_1
                         ,form.Client_FName_1
                         ,form.Client_LName_1
                         ,form.Client_Addr1_1
                         ,form.Client_Zip_1
                         ,form.Client_SSN_1
                         ,form.Client_DOB_1
                         ,form.Client_Gend_1
                         ,form.Client_Race_1
                         ,form.Client_Ethnicity_1
                         ,form.Client_clinicClinicID_1
                         ,form.Insurance_InsID_1
                         ,form.Insurance_InsIDNum_1
                         ,form.Insurance_InsNumEffDate_1
                         ,form.Insurance_Deductible_1
                         ,form.Insurance_Copay_1
               );
  } else {
    ventry = vEntry("notnull",form.ClientReferrals_RefDate_1
                         ,form.Client_FName_1
                         ,form.Client_LName_1
                         ,form.Client_Addr1_1
                         ,form.Client_City_1
                         ,form.Client_County_1
                         ,form.Client_ST_1
                         ,form.Client_Zip_1
                         ,form.Client_SSN_1
                         ,form.Client_DOB_1
                         ,form.Client_Gend_1
                         ,form.Client_Race_1
                         ,form.Client_Ethnicity_1
                         ,form.Client_clinicClinicID_1
                         ,form.Insurance_InsID_1
                         ,form.Insurance_InsIDNum_1
                         ,form.Insurance_InsNumEffDate_1
                         ,form.Insurance_Deductible_1
                         ,form.Insurance_Copay_1
               );
  }
  if ( ventry )
   {
     if ( form.ClientReferrals_ReferredBy1Type_1.value == 8 || form.ClientReferrals_ReferredBy1Type_1.value == 41 
       || form.ClientReferrals_ReferredBy2Type_1.value == 8 || form.ClientReferrals_ReferredBy2Type_1.value == 41 )
     {
      return ( vEntry("notnull",form.ClientReferrals_InPatientProcCode_1
                               ,form.ClientReferrals_InPatientDisStatus_1
                     )
             );
     }
   }
   else { return(false); }
}
//  DeCloak -->
const checkAgeAndHarmFulIntent = (clientAge, harmFulIntent) => {
  if(clientAge < 8 && harmFulIntent > 1) {
    alert('Harmful intent cannot be Homicidal or Both for clients under age 8')
    return false
  }
  return true
}