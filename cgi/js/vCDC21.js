<!-- Cloak
function validate(form,ok,no)
{
  if(!checkAgeAndHarmFulIntent(form.Client_Age.value, form.ClientReferrals_Harmfulintent_1.value)) {
    return false
  }
  return vEntry("notnull",form.Client_FName_1
                         ,form.Client_LName_1
                         ,form.Client_Addr1_1
                         ,form.Client_City_1
                         ,form.Client_County_1
                         ,form.Client_ST_1
                         ,form.Client_Zip_1
                         ,form.ClientPrAuthCDC_TransType_1
                         ,form.ClientPrAuthCDC_TransDate_1
                         ,form.ClientPrAuthCDC_TransTime_1
                         ,form.Client_DOB_1
                         ,form.ClientIntake_ServiceFocus_1
                         ,form.Client_Race_1
                         ,form.Client_Ethnicity_1
                         ,form.Client_SSN_1
                         ,form.Client_Gend_1
                         ,form.ClientReferrals_ReferredBy1Type_1
                         ,form.ClientRelations_Residence_1
                         ,form.ClientRelations_LivesWith_1
                         ,form.ClientRelations_HomelessLong_1
                         ,form.ClientRelations_HomelessMany_1
                         ,form.Client_EmplStat_1
                         ,form.Client_EmplType_1
                         ,form.ClientIntake_SchoolLast3_1
                         ,form.ClientIntake_MilFlag_1
                         ,form.ClientRelations_MarStat_1
                         ,form.ClientResources_IncomeDeps_1
                         ,form.ClientSocial_SpeakEnglish_1
                         ,form.ClientSocial_PreLang_1
                         ,form.ClientLegal_LegalStatus_1
                         ,form.ClientIntake_LOC_1
                         ,form.PDDom_Dom1Score_1
                         ,form.PDDom_Dom2Score_1
                         ,form.PDDom_Dom3Score_1
                         ,form.PDDom_Dom4Score_1
                         ,form.PDDom_Dom5Score_1
                         ,form.PDDom_Dom6Score_1
                         ,form.PDDom_Dom7Score_1
                         ,form.PDDom_Dom8Score_1
                         ,form.PDDom_Dom9Score_1
                         ,form.ClientLegal_Arrest1_1
                         ,form.ClientLegal_Arrested_1
                         ,form.ClientResources_SelfHelp30_1
                         ,form.ClientLegal_CustAgency_1
                         ,form.MedHx_RestrictivePlacement_1
                         ,form.MedHx_SelfHarm_1
                         ,form.ClientIntake_AbsentSchool_1
                         ,form.ClientIntake_SuspendedSchool_1
                         ,form.ClientIntake_AbsentDayCare_1
               );
}
//  DeCloak -->
const checkAgeAndHarmFulIntent = (clientAge, harmFulIntent) => {
  if(clientAge < 8 && harmFulIntent > 1) {
    alert('Harmful intent cannot be Homicidal or Both for clients under age 8')
    return false
  }
  return true
}