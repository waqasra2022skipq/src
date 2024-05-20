<!-- Cloak
function validate(form)
{
//alert('in validate: form='+form);
  if ( !vEntry("notnull",form.Treatment_ClinicID_1
                        ,form.Treatment_SCID_1
                        ,form.Treatment_POS_1
                        ,form.Treatment_ContLogDate_1
                        ,form.Treatment_ContLogBegTime_1
                        ,form.Treatment_ContLogEndTime_1
                        ,form.NoteProblems
                        ,form.NoteTrPlanPG
                        ,form.ProgNotes_Methods_1
                        ,form.ProgNotes_Progress_1
                        ,form.ProgNotes_ProgEvidence_1
              )
     ) { return false; }
  var CurType = form.CurType.value;
//alert('in validate: CurType='+CurType);
  if ( CurType == "GC" || CurType == "GR" )
  { if ( !vEntry("notnull",form.ProgNotes_GrpSize_1) ) { return false; } }
  else if ( CurType == "CI" )
  { 
    if ( !vEntry("notnull",form.ProgNotes_CrisisText_1
                          ,form.ProgNotes_GAFCurrent_1
                          ,form.ProgNotes_GAFRecent_1
                )
       ) { return false; }
  }
  return true;
}
//  DeCloak -->
