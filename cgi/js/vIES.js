function validate(form)
{
  return(true);
}
function validateScore(form,Field)
{
  if ( !vNum(Field,0,4) ) { return false; }
  return setTotals("not0",form.IES_Score_1,form.IES_Average_1
                         ,form.IES_AnyReminder_1
                         ,form.IES_TroubleSleeping_1
                         ,form.IES_ThinkAbout_1
                         ,form.IES_Irritable_1
                         ,form.IES_AvoidedUpset_1
                         ,form.IES_ThoughtsAbout_1
                         ,form.IES_WasntReal_1
                         ,form.IES_AvoidReminders_1
                         ,form.IES_PicturesAbout_1
                         ,form.IES_EasilyStartled_1
                         ,form.IES_NotThinkAbout_1
                         ,form.IES_DidntDeal_1
                         ,form.IES_KindOfNumb_1
                         ,form.IES_BackAtTime_1
                         ,form.IES_TroubleAsleep_1
                         ,form.IES_StrongFeelings_1
                         ,form.IES_RemoveMemory_1
                         ,form.IES_TroubleCon_1
                         ,form.IES_PhysicalReactions_1
                         ,form.IES_DreamsAbout_1
                         ,form.IES_Watchful_1
                         ,form.IES_NotTalk_1
               );
}
