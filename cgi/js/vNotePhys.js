<!-- Cloak
function validate(form)
{
//alert('in validate: form='+form);
  if ( !vEntry("notnull",form.Treatment_ClinicID_1
                        ,form.Treatment_SCID_1
                        ,form.Treatment_SCID2_1
                        ,form.Treatment_SCID4_1
                        ,form.Treatment_SCID5_1
                        ,form.Treatment_SCID6_1
                        ,form.Treatment_POS_1
                        ,form.Treatment_ContLogDate_1
                        ,form.Treatment_ContLogBegTime_1
                        ,form.Treatment_ContLogEndTime_1
                        ,form.NoteProblems
                        ,form.NoteTrPlanPG
                        ,form.PhysNotes_Progress_1
                        ,form.PhysNotes_ProgEvidence_1
              )
     ) { return false; }
  return true;
}
//  DeCloak -->
