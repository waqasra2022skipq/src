[[myHTML->newPage(%form+Mental Health)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientDevl.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/qDate.js"> </SCRIPT>

<FORM NAME="Devl" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Developmental History Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port heading" COLSPAN="2" >DEVELOPMENTAL HISTORY</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="50%" >
      Were developmental age factors, motor development and functioning accomplished within appropriate time frames?
    </TD>
    <TD CLASS="strcol" WIDTH="50%" >
      <INPUT TYPE="radio" NAME="MedHx_DevlFlag_1" VALUE="1" <<MedHx_DevlFlag_1=1>> > Yes
      <INPUT TYPE="radio" NAME="MedHx_DevlFlag_1" VALUE="0" <<MedHx_DevlFlag_1=0>> > No
      <INPUT TYPE="radio" NAME="MedHx_DevlFlag_1" VALUE="U" <<MedHx_DevlFlag_1=U>> > Unknown
      [<A HREF="#AdjDis" >If YES or UNKNOWN, skip to Handicaps/Disabilities/Limitations/Challenges</A>]
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >Prenatal (Mother's condition while pregnant)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Prenatal_1" VALUE="N" <<ClientDevl_Prenatal_1=N>> > Normal
      <INPUT TYPE="radio" NAME="ClientDevl_Prenatal_1" VALUE="U" <<ClientDevl_Prenatal_1=U>> > Unknown
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_PrematureContractions_1" VALUE="1" <<ClientDevl_PrematureContractions_1=checkbox>> > Premature Contractions
      <INPUT TYPE="checkbox" NAME="ClientDevl_GestationalDiabetes_1" VALUE="1" <<ClientDevl_GestationalDiabetes_1=checkbox>> > Gestational Diabetes 
      <INPUT TYPE="checkbox" NAME="ClientDevl_Anemia_1" VALUE="1" <<ClientDevl_Anemia_1=checkbox>> > Anemia
      <INPUT TYPE="checkbox" NAME="ClientDevl_Allergies_1" VALUE="1" <<ClientDevl_Allergies_1=checkbox>> > Allergies 
      <INPUT TYPE="checkbox" NAME="ClientDevl_EmotionalStrain_1" VALUE="1" <<ClientDevl_EmotionalStrain_1=checkbox>> > Emotional Strain
      <INPUT TYPE="checkbox" NAME="ClientDevl_Bleeding_1" VALUE="1" <<ClientDevl_Bleeding_1=checkbox>> > Bleeding
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_EdemaSwelling_1" VALUE="1" <<ClientDevl_EdemaSwelling_1=checkbox>> > Edema / Swelling 
      <INPUT TYPE="checkbox" NAME="ClientDevl_Hypertension_1" VALUE="1" <<ClientDevl_Hypertension_1=checkbox>> > Hypertension 
      <INPUT TYPE="checkbox" NAME="ClientDevl_Convulsions_1" VALUE="1" <<ClientDevl_Convulsions_1=checkbox>> > Convulsions
      <INPUT TYPE="checkbox" NAME="ClientDevl_ExcessNausea_1" VALUE="1" <<ClientDevl_ExcessNausea_1=checkbox>> > Excess Nausea
      <INPUT TYPE="checkbox" NAME="ClientDevl_RubellaMeasles_1" VALUE="1" <<ClientDevl_RubellaMeasles_1=checkbox>> > Rubella/Measles
      <INPUT TYPE="checkbox" NAME="ClientDevl_Surgery_1" VALUE="1" <<ClientDevl_Surgery_1=checkbox>> > Surgery 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_HeartInfection_1" VALUE="1" <<ClientDevl_HeartInfection_1=checkbox>> > Heart Infection 
      <INPUT TYPE="checkbox" NAME="ClientDevl_ViralInfection_1" VALUE="1" <<ClientDevl_ViralInfection_1=checkbox>> > Viral Infection 
      <INPUT TYPE="checkbox" NAME="ClientDevl_HighFever_1" VALUE="1" <<ClientDevl_HighFever_1=checkbox>> > High Fever 
      <INPUT TYPE="checkbox" NAME="ClientDevl_Toxemia_1" VALUE="1" <<ClientDevl_Toxemia_1=checkbox>> > Toxemia 
      <INPUT TYPE="checkbox" NAME="ClientDevl_AmnioticFluidLoss_1" VALUE="1" <<ClientDevl_AmnioticFluidLoss_1=checkbox>> > Amniotic Fluid Loss
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_SeriousInjury_1" VALUE="1" <<ClientDevl_SeriousInjury_1=checkbox>> > Serious Injury
      <INPUT TYPE="checkbox" NAME="ClientDevl_SmokedLTpack_1" VALUE="1" <<ClientDevl_SmokedLTpack_1=checkbox>> > Smoked < 1 pack/day
      <INPUT TYPE="checkbox" NAME="ClientDevl_SmokedGTpack_1" VALUE="1" <<ClientDevl_SmokedGTpack_1=checkbox>> > Smoked > 1 pack/day
      <INPUT TYPE="checkbox" NAME="ClientDevl_UsedIllegalDrugs_1" VALUE="1" <<ClientDevl_UsedIllegalDrugs_1=checkbox>> > Used Illegal Drugs
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_AlcoholInfrequently_1" VALUE="1" <<ClientDevl_AlcoholInfrequently_1=checkbox>> > Drank Alcohol Infrequently
      <INPUT TYPE="checkbox" NAME="ClientDevl_AlcoholFrequently_1" VALUE="1" <<ClientDevl_AlcoholFrequently_1=checkbox>> > Drank Alcohol Frequently
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_UsedPrescription_1" VALUE="1" <<ClientDevl_UsedPrescription_1=checkbox>> > Used Prescription Drugs: 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientDevl_UsedPrescriptionText_1" COLS="90" ROWS="2" WRAP=virtual ><<ClientDevl_UsedPrescriptionText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >Perinatal (Condition at birth)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Perinatal_1" VALUE="N" <<ClientDevl_Perinatal_1=N>> > Normal / Full term
      <INPUT TYPE="radio" NAME="ClientDevl_Perinatal_1" VALUE="P" <<ClientDevl_Perinatal_1=P>> > Premature 
      <INPUT TYPE="text" NAME="ClientDevl_PerinatalWks_1" VALUE="<<ClientDevl_PerinatalWks_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" > wks
      <INPUT TYPE="radio" NAME="ClientDevl_Perinatal_1" VALUE="U" <<ClientDevl_Perinatal_1=U>> > Unknown
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_EpiduralAnesthesia_1" VALUE="1" <<ClientDevl_EpiduralAnesthesia_1=checkbox>> > Epidural Anesthesia
      <INPUT TYPE="checkbox" NAME="ClientDevl_GeneralAnesthesia_1" VALUE="1" <<ClientDevl_GeneralAnesthesia_1=checkbox>> > General Anesthesia 
      <INPUT TYPE="checkbox" NAME="ClientDevl_Longlabor_1" VALUE="1" <<ClientDevl_Longlabor_1=checkbox>> > Long labor 
      <INPUT TYPE="checkbox" NAME="ClientDevl_Motherill_1" VALUE="1" <<ClientDevl_Motherill_1=checkbox>> > Mother ill
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_RhFactorProblems_1" VALUE="1" <<ClientDevl_RhFactorProblems_1=checkbox>> > Rh Factor Problems
      <INPUT TYPE="checkbox" NAME="ClientDevl_Transfusion_1" VALUE="1" <<ClientDevl_Transfusion_1=checkbox>> > Required Blood Transfusion
      <INPUT TYPE="checkbox" NAME="ClientDevl_Breech_1" VALUE="1" <<ClientDevl_Breech_1=checkbox>> > Breech  
      <INPUT TYPE="checkbox" NAME="ClientDevl_UseForceps_1" VALUE="1" <<ClientDevl_UseForceps_1=checkbox>> > Use of Forceps 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_PlannedCesarean_1" VALUE="1" <<ClientDevl_PlannedCesarean_1=checkbox>> > Planned Cesarean
      <INPUT TYPE="checkbox" NAME="ClientDevl_EmergencyCesarean_1" VALUE="1" <<ClientDevl_EmergencyCesarean_1=checkbox>> > Emergency Cesarean
      <INPUT TYPE="checkbox" NAME="ClientDevl_CordAroundNeck_1" VALUE="1" <<ClientDevl_CordAroundNeck_1=checkbox>> > Cord Around Neck 
      <INPUT TYPE="checkbox" NAME="ClientDevl_SlowHeartRate_1" VALUE="1" <<ClientDevl_SlowHeartRate_1=checkbox>> > Slow Heart Rate  
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_DelayedBreathing_1" VALUE="1" <<ClientDevl_DelayedBreathing_1=checkbox>> > Delayed Breathing
      <INPUT TYPE="checkbox" NAME="ClientDevl_RequiredOxygen_1" VALUE="1" <<ClientDevl_RequiredOxygen_1=checkbox>> > Required Oxygen 
      <INPUT TYPE="checkbox" NAME="ClientDevl_LowWeight_1" VALUE="1" <<ClientDevl_LowWeight_1=checkbox>> > Low Weight 
      <INPUT TYPE="checkbox" NAME="ClientDevl_FeedingTube_1" VALUE="1" <<ClientDevl_FeedingTube_1=checkbox>> > Required Feeding Tube 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Jaundice_1" VALUE="1" <<ClientDevl_Jaundice_1=checkbox>> > Jaundice
      <INPUT TYPE="checkbox" NAME="ClientDevl_Incubator_1" VALUE="1" <<ClientDevl_Incubator_1=checkbox>> > Required Incubator 
      <INPUT TYPE="checkbox" NAME="ClientDevl_LimpFloppy_1" VALUE="1" <<ClientDevl_LimpFloppy_1=checkbox>> > Limp / Floppy
      <INPUT TYPE="checkbox" NAME="ClientDevl_CongenitalDefects_1" VALUE="1" <<ClientDevl_CongenitalDefects_1=checkbox>> > Congenital Defects
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Fever_1" VALUE="1" <<ClientDevl_Fever_1=checkbox>> > Fever
      <INPUT TYPE="checkbox" NAME="ClientDevl_PerinatalOther_1" VALUE="1" <<ClientDevl_PerinatalOther_1=checkbox>> > Other: 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientDevl_PerinatalOtherText_1" COLS="90" ROWS="2" WRAP=virtual ><<ClientDevl_PerinatalOtherText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      Weight: 
      <INPUT TYPE="text" NAME="ClientDevl_Weightlbs_1" VALUE="<<ClientDevl_Weightlbs_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" > lbs
      <INPUT TYPE="text" NAME="ClientDevl_Weightozs_1" VALUE="<<ClientDevl_Weightozs_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2"> oz.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_FeedComplications_1" VALUE="1" <<ClientDevl_FeedComplications_1=checkbox>> > Feeding Complications
      <INPUT TYPE="checkbox" NAME="ClientDevl_BreastFed_1" VALUE="1" <<ClientDevl_BreastFed_1=checkbox>> > Breast Fed
      <INPUT TYPE="checkbox" NAME="ClientDevl_BreastSupplement_1" VALUE="1" <<ClientDevl_BreastSupplement_1=checkbox>> > Breast with Supplement
      <INPUT TYPE="checkbox" NAME="ClientDevl_BottleFed_1" VALUE="1" <<ClientDevl_BottleFed_1=checkbox>> > Bottle Fed
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >Postnatal (Early Life)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Postnatal_1" VALUE="1" <<ClientDevl_Postnatal_1=1>> > Known
      <INPUT TYPE="radio" NAME="ClientDevl_Postnatal_1" VALUE="U" <<ClientDevl_Postnatal_1=U>> > Unknown
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Alert_1" VALUE="1" <<ClientDevl_Alert_1=checkbox>> > Alert 
      <INPUT TYPE="checkbox" NAME="ClientDevl_ExtremelyActive_1" VALUE="1" <<ClientDevl_ExtremelyActive_1=checkbox>> > Extremely Active 
      <INPUT TYPE="checkbox" NAME="ClientDevl_Inactive_1" VALUE="1" <<ClientDevl_Inactive_1=checkbox>> > Inactive / Sluggish 
      <INPUT TYPE="checkbox" NAME="ClientDevl_ExcessiveSleeper_1" VALUE="1" <<ClientDevl_ExcessiveSleeper_1=checkbox>> > Excessive Sleeper 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_DiffToAwake_1" VALUE="1" <<ClientDevl_DiffToAwake_1=checkbox>> > Difficult to Awake
      <INPUT TYPE="checkbox" NAME="ClientDevl_DiffFallAsleep_1" VALUE="1" <<ClientDevl_DiffFallAsleep_1=checkbox>> > Difficulty Falling Asleep
      <INPUT TYPE="checkbox" NAME="ClientDevl_FrequentAwaking_1" VALUE="1" <<ClientDevl_FrequentAwaking_1=checkbox>> > Frequent awaking
      <INPUT TYPE="checkbox" NAME="ClientDevl_LittleSleep_1" VALUE="1" <<ClientDevl_LittleSleep_1=checkbox>> > Little Sleep but Comfortable
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_ParentToSleep_1" VALUE="1" <<ClientDevl_ParentToSleep_1=checkbox>> > Needs Parent Present to Sleep
      <INPUT TYPE="checkbox" NAME="ClientDevl_SleepsWithParent_1" VALUE="1" <<ClientDevl_SleepsWithParent_1=checkbox>> > Often Sleeps with Parent 
      <INPUT TYPE="checkbox" NAME="ClientDevl_PhysActiveSleep_1" VALUE="1" <<ClientDevl_PhysActiveSleep_1=checkbox>> > Physically Active Sleep
      <INPUT TYPE="checkbox" NAME="ClientDevl_SleepWalking_1" VALUE="1" <<ClientDevl_SleepWalking_1=checkbox>> > Sleep Walking
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Nightmares_1" VALUE="1" <<ClientDevl_Nightmares_1=checkbox>> > Frequent Nightmares
      <INPUT TYPE="checkbox" NAME="ClientDevl_OccasionalCrying_1" VALUE="1" <<ClientDevl_OccasionalCrying_1=checkbox>> > Occasional Crying 
      <INPUT TYPE="checkbox" NAME="ClientDevl_FrequentCrying_1" VALUE="1" <<ClientDevl_FrequentCrying_1=checkbox>> > Frequent Crying 
      <INPUT TYPE="checkbox" NAME="ClientDevl_DiffToComfort_1" VALUE="1" <<ClientDevl_DiffToComfort_1=checkbox>> > Difficult to Comfort 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Sociable_1" VALUE="1" <<ClientDevl_Sociable_1=checkbox>> > Sociable
      <INPUT TYPE="checkbox" NAME="ClientDevl_ReachesOutPickedUp_1" VALUE="1" <<ClientDevl_ReachesOutPickedUp_1=checkbox>> > Reaches Out to be Picked Up
      <INPUT TYPE="checkbox" NAME="ClientDevl_WantsHeldFreq_1" VALUE="1" <<ClientDevl_WantsHeldFreq_1=checkbox>> > Wants to be Held Freq.
      <INPUT TYPE="checkbox" NAME="ClientDevl_NotBeHeld_1" VALUE="1" <<ClientDevl_NotBeHeld_1=checkbox>> > Does Not Want to be Held
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Happy_1" VALUE="1" <<ClientDevl_Happy_1=checkbox>> > Happy
      <INPUT TYPE="checkbox" NAME="ClientDevl_Playful_1" VALUE="1" <<ClientDevl_Playful_1=checkbox>> > Playful
      <INPUT TYPE="checkbox" NAME="ClientDevl_Angry_1" VALUE="1" <<ClientDevl_Angry_1=checkbox>> > Angry
      <INPUT TYPE="checkbox" NAME="ClientDevl_Fearful_1" VALUE="1" <<ClientDevl_Fearful_1=checkbox>> > Fearful 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Withdrawn_1" VALUE="1" <<ClientDevl_Withdrawn_1=checkbox>> > Withdrawn
      <INPUT TYPE="checkbox" NAME="ClientDevl_FoodAllergies_1" VALUE="1" <<ClientDevl_FoodAllergies_1=checkbox>> > Food Allergies 
      <INPUT TYPE="checkbox" NAME="ClientDevl_PoorAppetite_1" VALUE="1" <<ClientDevl_PoorAppetite_1=checkbox>> > Poor Appetite
      <INPUT TYPE="checkbox" NAME="ClientDevl_RefusesMostFood_1" VALUE="1" <<ClientDevl_RefusesMostFood_1=checkbox>> > Refuses Most Food 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_DiffSucking_1" VALUE="1" <<ClientDevl_DiffSucking_1=checkbox>> > Difficulty Sucking
      <INPUT TYPE="checkbox" NAME="ClientDevl_DiffSwallowing_1" VALUE="1" <<ClientDevl_DiffSwallowing_1=checkbox>> > Difficulty Swallowing
      <INPUT TYPE="checkbox" NAME="ClientDevl_Chokes_1" VALUE="1" <<ClientDevl_Chokes_1=checkbox>> > Chokes
      <INPUT TYPE="checkbox" NAME="ClientDevl_Colic_1" VALUE="1" <<ClientDevl_Colic_1=checkbox>> > Colic
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_Reflux_1" VALUE="1" <<ClientDevl_Reflux_1=checkbox>> > Reflux
      <INPUT TYPE="checkbox" NAME="ClientDevl_FreqSpitsUp_1" VALUE="1" <<ClientDevl_FreqSpitsUp_1=checkbox>> > Frequently Spits Up
      <INPUT TYPE="checkbox" NAME="ClientDevl_WandersFromTable_1" VALUE="1" <<ClientDevl_WandersFromTable_1=checkbox>> > Wanders from Table
      <INPUT TYPE="checkbox" NAME="ClientDevl_FoodTextures_1" VALUE="1" <<ClientDevl_FoodTextures_1=checkbox>> > Dislikes Certain Food Textures
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_EarInfections_1" VALUE="1" <<ClientDevl_EarInfections_1=checkbox>> > Ear Infections
      <INPUT TYPE="checkbox" NAME="ClientDevl_PostnatalOther_1" VALUE="1" <<ClientDevl_PostnatalOther_1=checkbox>> > Other:  
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientDevl_PostnatalOtherText_1" COLS="90" ROWS="2" WRAP=virtual ><<ClientDevl_PostnatalOtherText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR > <TD CLASS="port hdrtxt" >Toileting</TD></TR> <TR>
    <TD CLASS="strcol" COLSPAN="2" >
Problems: 
      <INPUT TYPE="radio" NAME="ClientDevl_ToiletProblems_1" VALUE="1" <<ClientDevl_ToiletProblems_1=1>> > Bladder
      <INPUT TYPE="radio" NAME="ClientDevl_ToiletProblems_1" VALUE="2" <<ClientDevl_ToiletProblems_1=2>> > Bowel
      <INPUT TYPE="radio" NAME="ClientDevl_ToiletProblems_1" VALUE="3" <<ClientDevl_ToiletProblems_1=3>> > Both
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
Severity:
      <INPUT TYPE="radio" NAME="ClientDevl_ToiletSeverity_1" VALUE="1" <<ClientDevl_ToiletSeverity_1=1>> > Mild
      <INPUT TYPE="radio" NAME="ClientDevl_ToiletSeverity_1" VALUE="2" <<ClientDevl_ToiletSeverity_1=2>> > Moderate
      <INPUT TYPE="radio" NAME="ClientDevl_ToiletSeverity_1" VALUE="3" <<ClientDevl_ToiletSeverity_1=3>> > Severe
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      Age Achieved: 
      Daytime: <INPUT TYPE="text" NAME="ClientDevl_ToiletDaytime_1" VALUE="<<ClientDevl_ToiletDaytime_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
      Nighttime: <INPUT TYPE="text" NAME="ClientDevl_ToiletNighttime_1" VALUE="<<ClientDevl_ToiletNighttime_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >Emergency Room</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_EmergencyRoom_1" VALUE="1" <<ClientDevl_EmergencyRoom_1=U>> > Unknown
      <INPUT TYPE="radio" NAME="ClientDevl_EmergencyRoom_1" VALUE="1" <<ClientDevl_EmergencyRoom_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_EmergencyRoom_1" VALUE="1" <<ClientDevl_EmergencyRoom_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Dates / Reason:
      <TEXTAREA NAME="ClientDevl_EmergencyRoomText_1" COLS="90" ROWS="2" WRAP=virtual ><<ClientDevl_EmergencyRoomText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >Motor Milestones (Age when accomplished)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_MotorMilestones_1" VALUE="1" <<ClientDevl_MotorMilestones_1=1>> > Known
      <INPUT TYPE="radio" NAME="ClientDevl_MotorMilestones_1" VALUE="U" <<ClientDevl_MotorMilestones_1=U>> > Unknown
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_MMSitAlone_1" VALUE="1" <<ClientDevl_MMSitAlone_1=checkbox>> > Sit Alone 
      <INPUT TYPE="checkbox" NAME="ClientDevl_MMCrawl_1" VALUE="1" <<ClientDevl_MMCrawl_1=checkbox>> > Crawl 
      <INPUT TYPE="checkbox" NAME="ClientDevl_MMWalk_1" VALUE="1" <<ClientDevl_MMWalk_1=checkbox>> > Walk 
      <INPUT TYPE="checkbox" NAME="ClientDevl_MMGoDownStairs_1" VALUE="1" <<ClientDevl_MMGoDownStairs_1=checkbox>> > Go Down Stairs 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientDevl_MMRideTricycle_1" VALUE="1" <<ClientDevl_MMRideTricycle_1=checkbox>> > Ride Tricycle  
      <INPUT TYPE="checkbox" NAME="ClientDevl_MMRideBicycle_1" VALUE="1" <<ClientDevl_MMRideBicycle_1=checkbox>> > Ride bicycle without Training Wheels 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Gross Motor and Fine Motor</TD></TR>
  <TR>
    <TD CLASS="strcol" >Difficulty riding a riding toy, with feet pushing or propelling</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_RidingToy_1" VALUE="1" <<ClientDevl_RidingToy_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_RidingToy_1" VALUE="0" <<ClientDevl_RidingToy_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_RidingToy_1" VALUE="S" <<ClientDevl_RidingToy_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty pumping self on swing</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PumpingSelfOnSwing_1" VALUE="1" <<ClientDevl_PumpingSelfOnSwing_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PumpingSelfOnSwing_1" VALUE="0" <<ClientDevl_PumpingSelfOnSwing_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PumpingSelfOnSwing_1" VALUE="S" <<ClientDevl_PumpingSelfOnSwing_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty learning how to ride a bike</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_LearningHowRideBike_1" VALUE="1" <<ClientDevl_LearningHowRideBike_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_LearningHowRideBike_1" VALUE="0" <<ClientDevl_LearningHowRideBike_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_LearningHowRideBike_1" VALUE="S" <<ClientDevl_LearningHowRideBike_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dislikes coloring or paper and pencil tasks</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ColoringPaperPencilTasks_1" VALUE="1" <<ClientDevl_ColoringPaperPencilTasks_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ColoringPaperPencilTasks_1" VALUE="0" <<ClientDevl_ColoringPaperPencilTasks_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ColoringPaperPencilTasks_1" VALUE="S" <<ClientDevl_ColoringPaperPencilTasks_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dislikes playing with puzzles or becomes easily frustrated</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_EasilyFrustrated_1" VALUE="1" <<ClientDevl_EasilyFrustrated_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_EasilyFrustrated_1" VALUE="0" <<ClientDevl_EasilyFrustrated_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_EasilyFrustrated_1" VALUE="S" <<ClientDevl_EasilyFrustrated_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty playing with small manipulative toys (i.e. Legos, etc.)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PlayingSmallToys_1" VALUE="1" <<ClientDevl_PlayingSmallToys_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PlayingSmallToys_1" VALUE="0" <<ClientDevl_PlayingSmallToys_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PlayingSmallToys_1" VALUE="S" <<ClientDevl_PlayingSmallToys_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty using scissors or learning how to use scissors</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_UsingScissors_1" VALUE="1" <<ClientDevl_UsingScissors_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_UsingScissors_1" VALUE="0" <<ClientDevl_UsingScissors_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_UsingScissors_1" VALUE="S" <<ClientDevl_UsingScissors_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems weaker and tires more easily that other children his/her age</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Weaker_1" VALUE="1" <<ClientDevl_Weaker_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_Weaker_1" VALUE="0" <<ClientDevl_Weaker_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_Weaker_1" VALUE="S" <<ClientDevl_Weaker_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Appears stiff, awkward, or clumsy in movement</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AppearsStiff_1" VALUE="1" <<ClientDevl_AppearsStiff_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AppearsStiff_1" VALUE="0" <<ClientDevl_AppearsStiff_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AppearsStiff_1" VALUE="S" <<ClientDevl_AppearsStiff_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems to have great difficulty learning new motor tasks</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_NewMotorTasks_1" VALUE="1" <<ClientDevl_NewMotorTasks_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_NewMotorTasks_1" VALUE="0" <<ClientDevl_NewMotorTasks_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_NewMotorTasks_1" VALUE="S" <<ClientDevl_NewMotorTasks_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty catching a ball</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CatchingBall_1" VALUE="1" <<ClientDevl_CatchingBall_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CatchingBall_1" VALUE="0" <<ClientDevl_CatchingBall_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CatchingBall_1" VALUE="S" <<ClientDevl_CatchingBall_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty kicking a ball</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_KickingBall_1" VALUE="1" <<ClientDevl_KickingBall_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_KickingBall_1" VALUE="0" <<ClientDevl_KickingBall_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_KickingBall_1" VALUE="S" <<ClientDevl_KickingBall_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty learning how to swim</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_LearningHowSwim_1" VALUE="1" <<ClientDevl_LearningHowSwim_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_LearningHowSwim_1" VALUE="0" <<ClientDevl_LearningHowSwim_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_LearningHowSwim_1" VALUE="S" <<ClientDevl_LearningHowSwim_1=S>> > Sometimes
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Self-Help Skills</TD></TR>
  <TR>
    <TD CLASS="strcol" >Difficulty with the use of a spoon (messy eater)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_UseOfSpoon_1" VALUE="1" <<ClientDevl_UseOfSpoon_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_UseOfSpoon_1" VALUE="0" <<ClientDevl_UseOfSpoon_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_UseOfSpoon_1" VALUE="S" <<ClientDevl_UseOfSpoon_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty cutting with a knife</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CuttingWithKnife_1" VALUE="1" <<ClientDevl_CuttingWithKnife_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CuttingWithKnife_1" VALUE="0" <<ClientDevl_CuttingWithKnife_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CuttingWithKnife_1" VALUE="S" <<ClientDevl_CuttingWithKnife_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty with dressing self</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DressingSelf_1" VALUE="1" <<ClientDevl_DressingSelf_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DressingSelf_1" VALUE="0" <<ClientDevl_DressingSelf_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DressingSelf_1" VALUE="S" <<ClientDevl_DressingSelf_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty with clothing fasteners (buttons, zippers)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ClothingFasteners_1" VALUE="1" <<ClientDevl_ClothingFasteners_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ClothingFasteners_1" VALUE="0" <<ClientDevl_ClothingFasteners_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ClothingFasteners_1" VALUE="S" <<ClientDevl_ClothingFasteners_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty tying shoes</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TyingShoes_1" VALUE="1" <<ClientDevl_TyingShoes_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TyingShoes_1" VALUE="0" <<ClientDevl_TyingShoes_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TyingShoes_1" VALUE="S" <<ClientDevl_TyingShoes_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty brushing teeth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_BrushingTeeth_1" VALUE="1" <<ClientDevl_BrushingTeeth_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_BrushingTeeth_1" VALUE="0" <<ClientDevl_BrushingTeeth_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_BrushingTeeth_1" VALUE="S" <<ClientDevl_BrushingTeeth_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty making a simple sandwich</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_MakingSimpleSandwich_1" VALUE="1" <<ClientDevl_MakingSimpleSandwich_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_MakingSimpleSandwich_1" VALUE="0" <<ClientDevl_MakingSimpleSandwich_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_MakingSimpleSandwich_1" VALUE="S" <<ClientDevl_MakingSimpleSandwich_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty completing chores</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CompletingChores_1" VALUE="1" <<ClientDevl_CompletingChores_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CompletingChores_1" VALUE="0" <<ClientDevl_CompletingChores_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CompletingChores_1" VALUE="S" <<ClientDevl_CompletingChores_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty making bed</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_MakingBed_1" VALUE="1" <<ClientDevl_MakingBed_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_MakingBed_1" VALUE="0" <<ClientDevl_MakingBed_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_MakingBed_1" VALUE="S" <<ClientDevl_MakingBed_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty taking a bath or shower (washing self)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TakingBathShower_1" VALUE="1" <<ClientDevl_TakingBathShower_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TakingBathShower_1" VALUE="0" <<ClientDevl_TakingBathShower_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TakingBathShower_1" VALUE="S" <<ClientDevl_TakingBathShower_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty washing hair</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_WashingHair_1" VALUE="1" <<ClientDevl_WashingHair_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_WashingHair_1" VALUE="0" <<ClientDevl_WashingHair_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_WashingHair_1" VALUE="S" <<ClientDevl_WashingHair_1=S>> > Sometimes
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Movement and Balance</TD></TR>
  <TR>
    <TD CLASS="strcol" >Car sick frequently</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CarSickFrequently_1" VALUE="1" <<ClientDevl_CarSickFrequently_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CarSickFrequently_1" VALUE="0" <<ClientDevl_CarSickFrequently_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CarSickFrequently_1" VALUE="S" <<ClientDevl_CarSickFrequently_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Nausea or vomits from other movement (i.e. swings, playground, merry-go-round)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_NauseaVomitsFromMovement_1" VALUE="1" <<ClientDevl_NauseaVomitsFromMovement_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_NauseaVomitsFromMovement_1" VALUE="0" <<ClientDevl_NauseaVomitsFromMovement_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_NauseaVomitsFromMovement_1" VALUE="S" <<ClientDevl_NauseaVomitsFromMovement_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is unable to give adequate warning about feeling of nausea</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_WarningFeelingNausea_1" VALUE="1" <<ClientDevl_WarningFeelingNausea_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_WarningFeelingNausea_1" VALUE="0" <<ClientDevl_WarningFeelingNausea_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_WarningFeelingNausea_1" VALUE="S" <<ClientDevl_WarningFeelingNausea_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seeks quantities of twirling or spinning</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_SeeksSpinning_1" VALUE="1" <<ClientDevl_SeeksSpinning_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_SeeksSpinning_1" VALUE="0" <<ClientDevl_SeeksSpinning_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_SeeksSpinning_1" VALUE="S" <<ClientDevl_SeeksSpinning_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seeks quantity of stimulation on amusement park rides/swings</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_SeeksParkrides_1" VALUE="1" <<ClientDevl_SeeksParkrides_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_SeeksParkrides_1" VALUE="0" <<ClientDevl_SeeksParkrides_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_SeeksParkrides_1" VALUE="S" <<ClientDevl_SeeksParkrides_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Hesitates to climb or play on playground equipment</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HesitatesPlayground_1" VALUE="1" <<ClientDevl_HesitatesPlayground_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HesitatesPlayground_1" VALUE="0" <<ClientDevl_HesitatesPlayground_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HesitatesPlayground_1" VALUE="S" <<ClientDevl_HesitatesPlayground_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has trouble or hesitancy in learning to climb or descend stairs</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasTroubleClimb_1" VALUE="1" <<ClientDevl_HasTroubleClimb_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasTroubleClimb_1" VALUE="0" <<ClientDevl_HasTroubleClimb_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasTroubleClimb_1" VALUE="S" <<ClientDevl_HasTroubleClimb_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dislikes being lifted up and gently tossed in the air by parent</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_LiftedUp_1" VALUE="1" <<ClientDevl_LiftedUp_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_LiftedUp_1" VALUE="0" <<ClientDevl_LiftedUp_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_LiftedUp_1" VALUE="S" <<ClientDevl_LiftedUp_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Did not / does not like being placed on stomach or back as infant</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PlacedOnAsInfant_1" VALUE="1" <<ClientDevl_PlacedOnAsInfant_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PlacedOnAsInfant_1" VALUE="0" <<ClientDevl_PlacedOnAsInfant_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PlacedOnAsInfant_1" VALUE="S" <<ClientDevl_PlacedOnAsInfant_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Rocks self when stressed</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_RocksSelfWhenStressed_1" VALUE="1" <<ClientDevl_RocksSelfWhenStressed_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_RocksSelfWhenStressed_1" VALUE="0" <<ClientDevl_RocksSelfWhenStressed_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_RocksSelfWhenStressed_1" VALUE="S" <<ClientDevl_RocksSelfWhenStressed_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Period of crawling absent or very brief</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PeriodCrawling_1" VALUE="1" <<ClientDevl_PeriodCrawling_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PeriodCrawling_1" VALUE="0" <<ClientDevl_PeriodCrawling_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PeriodCrawling_1" VALUE="S" <<ClientDevl_PeriodCrawling_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Walks on toes, now or in the past</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_WalksOnToes_1" VALUE="1" <<ClientDevl_WalksOnToes_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_WalksOnToes_1" VALUE="0" <<ClientDevl_WalksOnToes_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_WalksOnToes_1" VALUE="S" <<ClientDevl_WalksOnToes_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is always on the "go" or constantly moving</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ConstantlyMoving_1" VALUE="1" <<ClientDevl_ConstantlyMoving_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ConstantlyMoving_1" VALUE="0" <<ClientDevl_ConstantlyMoving_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ConstantlyMoving_1" VALUE="S" <<ClientDevl_ConstantlyMoving_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Trips or falls frequently</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TripsFallsFrequently_1" VALUE="1" <<ClientDevl_TripsFallsFrequently_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TripsFallsFrequently_1" VALUE="0" <<ClientDevl_TripsFallsFrequently_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TripsFallsFrequently_1" VALUE="S" <<ClientDevl_TripsFallsFrequently_1=S>> > Sometimes
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Touch</TD></TR>
  <TR>
    <TD CLASS="strcol" >Seems unaware of being touched</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareBeingTouched_1" VALUE="1" <<ClientDevl_UnawareBeingTouched_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareBeingTouched_1" VALUE="0" <<ClientDevl_UnawareBeingTouched_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareBeingTouched_1" VALUE="S" <<ClientDevl_UnawareBeingTouched_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems unaware of being hurt/pain in comparison to others</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareBeingHurt_1" VALUE="1" <<ClientDevl_UnawareBeingHurt_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareBeingHurt_1" VALUE="0" <<ClientDevl_UnawareBeingHurt_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareBeingHurt_1" VALUE="S" <<ClientDevl_UnawareBeingHurt_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems overly sensitive to being touched, pulls away from light touch</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_OverlySensitive_1" VALUE="1" <<ClientDevl_OverlySensitive_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_OverlySensitive_1" VALUE="0" <<ClientDevl_OverlySensitive_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_OverlySensitive_1" VALUE="S" <<ClientDevl_OverlySensitive_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems excessively ticklish or strong dislike to being tickled</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ExcessivelyTicklish_1" VALUE="1" <<ClientDevl_ExcessivelyTicklish_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ExcessivelyTicklish_1" VALUE="0" <<ClientDevl_ExcessivelyTicklish_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ExcessivelyTicklish_1" VALUE="S" <<ClientDevl_ExcessivelyTicklish_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dislikes the feeling of certain clothing or tags</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ClothingTags_1" VALUE="1" <<ClientDevl_ClothingTags_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ClothingTags_1" VALUE="0" <<ClientDevl_ClothingTags_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ClothingTags_1" VALUE="S" <<ClientDevl_ClothingTags_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Resists wearing short sleeve shirts or short pants</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsShorts_1" VALUE="1" <<ClientDevl_ResistsShorts_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsShorts_1" VALUE="0" <<ClientDevl_ResistsShorts_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsShorts_1" VALUE="S" <<ClientDevl_ResistsShorts_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty transitioning clothes to reflect seasons (summer to winter clothing or vise versa)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TransitioningSeasons_1" VALUE="1" <<ClientDevl_TransitioningSeasons_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TransitioningSeasons_1" VALUE="0" <<ClientDevl_TransitioningSeasons_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TransitioningSeasons_1" VALUE="S" <<ClientDevl_TransitioningSeasons_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Continues to examine objects by putting them in the mouth (past age 1.5 yrs)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PuttingObjectsInMouth_1" VALUE="1" <<ClientDevl_PuttingObjectsInMouth_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PuttingObjectsInMouth_1" VALUE="0" <<ClientDevl_PuttingObjectsInMouth_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PuttingObjectsInMouth_1" VALUE="S" <<ClientDevl_PuttingObjectsInMouth_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dislikes being cuddled or hugged, unless on his/her terms</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_BeingCuddled_1" VALUE="1" <<ClientDevl_BeingCuddled_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_BeingCuddled_1" VALUE="0" <<ClientDevl_BeingCuddled_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_BeingCuddled_1" VALUE="S" <<ClientDevl_BeingCuddled_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Avoids putting hands in messy substances</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AvoidsMessy_1" VALUE="1" <<ClientDevl_AvoidsMessy_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AvoidsMessy_1" VALUE="0" <<ClientDevl_AvoidsMessy_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AvoidsMessy_1" VALUE="S" <<ClientDevl_AvoidsMessy_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems unaware that face and hands are messy</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareMessy_1" VALUE="1" <<ClientDevl_UnawareMessy_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareMessy_1" VALUE="0" <<ClientDevl_UnawareMessy_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_UnawareMessy_1" VALUE="S" <<ClientDevl_UnawareMessy_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Strongly dislikes hair cutting or washing</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesHairCutting_1" VALUE="1" <<ClientDevl_DislikesHairCutting_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesHairCutting_1" VALUE="0" <<ClientDevl_DislikesHairCutting_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesHairCutting_1" VALUE="S" <<ClientDevl_DislikesHairCutting_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Strongly dislikes bath or shower time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesBath_1" VALUE="1" <<ClientDevl_DislikesBath_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesBath_1" VALUE="0" <<ClientDevl_DislikesBath_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesBath_1" VALUE="S" <<ClientDevl_DislikesBath_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Very sensitive to water temperature (it must be "just right")</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_VerySensitiveWater_1" VALUE="1" <<ClientDevl_VerySensitiveWater_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_VerySensitiveWater_1" VALUE="0" <<ClientDevl_VerySensitiveWater_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_VerySensitiveWater_1" VALUE="S" <<ClientDevl_VerySensitiveWater_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Strongly dislikes toe or finger nail cutting</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesNailCutting_1" VALUE="1" <<ClientDevl_DislikesNailCutting_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesNailCutting_1" VALUE="0" <<ClientDevl_DislikesNailCutting_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DislikesNailCutting_1" VALUE="S" <<ClientDevl_DislikesNailCutting_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Pinches, bites, or otherwise hurt self</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PinchesBites_1" VALUE="1" <<ClientDevl_PinchesBites_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PinchesBites_1" VALUE="0" <<ClientDevl_PinchesBites_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PinchesBites_1" VALUE="S" <<ClientDevl_PinchesBites_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Frequently bangs head repeatedly</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_BangsHeadRepeatedly_1" VALUE="1" <<ClientDevl_BangsHeadRepeatedly_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_BangsHeadRepeatedly_1" VALUE="0" <<ClientDevl_BangsHeadRepeatedly_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_BangsHeadRepeatedly_1" VALUE="S" <<ClientDevl_BangsHeadRepeatedly_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Crawled with fisted hands</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CrawledFistedHands_1" VALUE="1" <<ClientDevl_CrawledFistedHands_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CrawledFistedHands_1" VALUE="0" <<ClientDevl_CrawledFistedHands_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CrawledFistedHands_1" VALUE="S" <<ClientDevl_CrawledFistedHands_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems overly sensitive to slight bumps or scrapes</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_SensitiveSlightBumpsScrapes_1" VALUE="1" <<ClientDevl_SensitiveSlightBumpsScrapes_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_SensitiveSlightBumpsScrapes_1" VALUE="0" <<ClientDevl_SensitiveSlightBumpsScrapes_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_SensitiveSlightBumpsScrapes_1" VALUE="S" <<ClientDevl_SensitiveSlightBumpsScrapes_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Tendency to touch things constantly</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TendencyTouchThingsConstantly_1" VALUE="1" <<ClientDevl_TendencyTouchThingsConstantly_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TendencyTouchThingsConstantly_1" VALUE="0" <<ClientDevl_TendencyTouchThingsConstantly_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TendencyTouchThingsConstantly_1" VALUE="S" <<ClientDevl_TendencyTouchThingsConstantly_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Frequently pushes, bites, or hits other children</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_FrequentlyPushesBitesHits_1" VALUE="1" <<ClientDevl_FrequentlyPushesBitesHits_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_FrequentlyPushesBitesHits_1" VALUE="0" <<ClientDevl_FrequentlyPushesBitesHits_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_FrequentlyPushesBitesHits_1" VALUE="S" <<ClientDevl_FrequentlyPushesBitesHits_1=S>> > Sometimes
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Auditory / Language</TD></TR>
  <TR>
    <TD CLASS="strcol" >Has or has had repeated ear infections</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_RepeatedEarInfections_1" VALUE="1" <<ClientDevl_RepeatedEarInfections_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_RepeatedEarInfections_1" VALUE="0" <<ClientDevl_RepeatedEarInfections_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_RepeatedEarInfections_1" VALUE="S" <<ClientDevl_RepeatedEarInfections_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Particularly distracted by sounds, seeming to hear sounds that go unnoticed by others</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DistractedBySounds_1" VALUE="1" <<ClientDevl_DistractedBySounds_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DistractedBySounds_1" VALUE="0" <<ClientDevl_DistractedBySounds_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DistractedBySounds_1" VALUE="S" <<ClientDevl_DistractedBySounds_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Often fails to listen or pay attention to what is said to him/her</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_OftenFailsListen_1" VALUE="1" <<ClientDevl_OftenFailsListen_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_OftenFailsListen_1" VALUE="0" <<ClientDevl_OftenFailsListen_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_OftenFailsListen_1" VALUE="S" <<ClientDevl_OftenFailsListen_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is overly sensitive to mildly loud noises</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_SensitiveMildlyLoudNoises_1" VALUE="1" <<ClientDevl_SensitiveMildlyLoudNoises_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_SensitiveMildlyLoudNoises_1" VALUE="0" <<ClientDevl_SensitiveMildlyLoudNoises_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_SensitiveMildlyLoudNoises_1" VALUE="S" <<ClientDevl_SensitiveMildlyLoudNoises_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Frequently covers ears when sounds are loud</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CoversEarsWhenSoundsAreLoud_1" VALUE="1" <<ClientDevl_CoversEarsWhenSoundsAreLoud_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CoversEarsWhenSoundsAreLoud_1" VALUE="0" <<ClientDevl_CoversEarsWhenSoundsAreLoud_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CoversEarsWhenSoundsAreLoud_1" VALUE="S" <<ClientDevl_CoversEarsWhenSoundsAreLoud_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is afraid of some noises</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AfraidSomeNoises_1" VALUE="1" <<ClientDevl_AfraidSomeNoises_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AfraidSomeNoises_1" VALUE="0" <<ClientDevl_AfraidSomeNoises_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AfraidSomeNoises_1" VALUE="S" <<ClientDevl_AfraidSomeNoises_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Enjoys hearing own voice echo or make loud noises</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_EnjoysHearingOwnVoice_1" VALUE="1" <<ClientDevl_EnjoysHearingOwnVoice_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_EnjoysHearingOwnVoice_1" VALUE="0" <<ClientDevl_EnjoysHearingOwnVoice_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_EnjoysHearingOwnVoice_1" VALUE="S" <<ClientDevl_EnjoysHearingOwnVoice_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >History of delayed speech development</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DelayedSpeechDevelopment_1" VALUE="1" <<ClientDevl_DelayedSpeechDevelopment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DelayedSpeechDevelopment_1" VALUE="0" <<ClientDevl_DelayedSpeechDevelopment_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DelayedSpeechDevelopment_1" VALUE="S" <<ClientDevl_DelayedSpeechDevelopment_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is difficult to understand</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultUnderstand_1" VALUE="1" <<ClientDevl_DifficultUnderstand_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultUnderstand_1" VALUE="0" <<ClientDevl_DifficultUnderstand_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultUnderstand_1" VALUE="S" <<ClientDevl_DifficultUnderstand_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Stammers or stutters</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Stammers_1" VALUE="1" <<ClientDevl_Stammers_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_Stammers_1" VALUE="0" <<ClientDevl_Stammers_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_Stammers_1" VALUE="S" <<ClientDevl_Stammers_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Speaks in incomplete sentences</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_SpeaksIncompleteSentences_1" VALUE="1" <<ClientDevl_SpeaksIncompleteSentences_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_SpeaksIncompleteSentences_1" VALUE="0" <<ClientDevl_SpeaksIncompleteSentences_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_SpeaksIncompleteSentences_1" VALUE="S" <<ClientDevl_SpeaksIncompleteSentences_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems confused as to the location or direction of sound</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ConfusedLocationSound_1" VALUE="1" <<ClientDevl_ConfusedLocationSound_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ConfusedLocationSound_1" VALUE="0" <<ClientDevl_ConfusedLocationSound_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ConfusedLocationSound_1" VALUE="S" <<ClientDevl_ConfusedLocationSound_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has difficulty paying attention in proximity to other noises</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasDifficultyPayingAttention_1" VALUE="1" <<ClientDevl_HasDifficultyPayingAttention_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasDifficultyPayingAttention_1" VALUE="0" <<ClientDevl_HasDifficultyPayingAttention_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasDifficultyPayingAttention_1" VALUE="S" <<ClientDevl_HasDifficultyPayingAttention_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Does not seem to understand what is said to him/her</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotSeemUnderstand_1" VALUE="1" <<ClientDevl_DoesNotSeemUnderstand_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotSeemUnderstand_1" VALUE="0" <<ClientDevl_DoesNotSeemUnderstand_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotSeemUnderstand_1" VALUE="S" <<ClientDevl_DoesNotSeemUnderstand_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Talks constantly</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TalksConstantly_1" VALUE="1" <<ClientDevl_TalksConstantly_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TalksConstantly_1" VALUE="0" <<ClientDevl_TalksConstantly_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TalksConstantly_1" VALUE="S" <<ClientDevl_TalksConstantly_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has a diagnosis of hearing loss</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DiagnosisHearingLoss_1" VALUE="1" <<ClientDevl_DiagnosisHearingLoss_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DiagnosisHearingLoss_1" VALUE="0" <<ClientDevl_DiagnosisHearingLoss_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DiagnosisHearingLoss_1" VALUE="S" <<ClientDevl_DiagnosisHearingLoss_1=S>> > Sometimes
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Emotional</TD></TR>
  <TR>
    <TD CLASS="strcol" >Does not accept changes in routine easily</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotAcceptChange_1" VALUE="1" <<ClientDevl_DoesNotAcceptChange_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotAcceptChange_1" VALUE="0" <<ClientDevl_DoesNotAcceptChange_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotAcceptChange_1" VALUE="S" <<ClientDevl_DoesNotAcceptChange_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Becomes easily frustrated</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_BecomesEasilyFrustrated_1" VALUE="1" <<ClientDevl_BecomesEasilyFrustrated_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_BecomesEasilyFrustrated_1" VALUE="0" <<ClientDevl_BecomesEasilyFrustrated_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_BecomesEasilyFrustrated_1" VALUE="S" <<ClientDevl_BecomesEasilyFrustrated_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Apt to be impulsive, heedless, accident-prone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AptBeImpulsive_1" VALUE="1" <<ClientDevl_AptBeImpulsive_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AptBeImpulsive_1" VALUE="0" <<ClientDevl_AptBeImpulsive_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AptBeImpulsive_1" VALUE="S" <<ClientDevl_AptBeImpulsive_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Marked mood variations, tendency to outbursts or tantrums</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_MarkedMoodVariations_1" VALUE="1" <<ClientDevl_MarkedMoodVariations_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_MarkedMoodVariations_1" VALUE="0" <<ClientDevl_MarkedMoodVariations_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_MarkedMoodVariations_1" VALUE="S" <<ClientDevl_MarkedMoodVariations_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Tends to withdraw from groups, plays on the outskirts</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TendsWithdrawFromGroups_1" VALUE="1" <<ClientDevl_TendsWithdrawFromGroups_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TendsWithdrawFromGroups_1" VALUE="0" <<ClientDevl_TendsWithdrawFromGroups_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TendsWithdrawFromGroups_1" VALUE="S" <<ClientDevl_TendsWithdrawFromGroups_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Seems to do things the hard way</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DoThingsHardway_1" VALUE="1" <<ClientDevl_DoThingsHardway_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DoThingsHardway_1" VALUE="0" <<ClientDevl_DoThingsHardway_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DoThingsHardway_1" VALUE="S" <<ClientDevl_DoThingsHardway_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Changes activities frequently</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ChangesActivitiesFrequently_1" VALUE="1" <<ClientDevl_ChangesActivitiesFrequently_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ChangesActivitiesFrequently_1" VALUE="0" <<ClientDevl_ChangesActivitiesFrequently_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ChangesActivitiesFrequently_1" VALUE="S" <<ClientDevl_ChangesActivitiesFrequently_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Frequently breaks toys or is overly rough on toys</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_BreaksToys_1" VALUE="1" <<ClientDevl_BreaksToys_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_BreaksToys_1" VALUE="0" <<ClientDevl_BreaksToys_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_BreaksToys_1" VALUE="S" <<ClientDevl_BreaksToys_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is impatient, cannot wait</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Impatient_1" VALUE="1" <<ClientDevl_Impatient_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_Impatient_1" VALUE="0" <<ClientDevl_Impatient_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_Impatient_1" VALUE="S" <<ClientDevl_Impatient_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cannot tolerate frustration</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTolerateFrustration_1" VALUE="1" <<ClientDevl_CannotTolerateFrustration_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTolerateFrustration_1" VALUE="0" <<ClientDevl_CannotTolerateFrustration_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTolerateFrustration_1" VALUE="S" <<ClientDevl_CannotTolerateFrustration_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Hums or taps fingers</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HumsTapsFingers_1" VALUE="1" <<ClientDevl_HumsTapsFingers_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HumsTapsFingers_1" VALUE="0" <<ClientDevl_HumsTapsFingers_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HumsTapsFingers_1" VALUE="S" <<ClientDevl_HumsTapsFingers_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Does not finish what is started</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotFinish_1" VALUE="1" <<ClientDevl_DoesNotFinish_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotFinish_1" VALUE="0" <<ClientDevl_DoesNotFinish_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotFinish_1" VALUE="S" <<ClientDevl_DoesNotFinish_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Takes a long time to settle down</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TakesLongTimeSettledown_1" VALUE="1" <<ClientDevl_TakesLongTimeSettledown_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TakesLongTimeSettledown_1" VALUE="0" <<ClientDevl_TakesLongTimeSettledown_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TakesLongTimeSettledown_1" VALUE="S" <<ClientDevl_TakesLongTimeSettledown_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Insists that bedroom/toys must be in precise order</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ToysInOrder_1" VALUE="1" <<ClientDevl_ToysInOrder_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ToysInOrder_1" VALUE="0" <<ClientDevl_ToysInOrder_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ToysInOrder_1" VALUE="S" <<ClientDevl_ToysInOrder_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is generally disorganized</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_GenerallyDisorganized_1" VALUE="1" <<ClientDevl_GenerallyDisorganized_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_GenerallyDisorganized_1" VALUE="0" <<ClientDevl_GenerallyDisorganized_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_GenerallyDisorganized_1" VALUE="S" <<ClientDevl_GenerallyDisorganized_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is unable to put things in order</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_UnablePutThingsInOrder_1" VALUE="1" <<ClientDevl_UnablePutThingsInOrder_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_UnablePutThingsInOrder_1" VALUE="0" <<ClientDevl_UnablePutThingsInOrder_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_UnablePutThingsInOrder_1" VALUE="S" <<ClientDevl_UnablePutThingsInOrder_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cannot sit through a board game</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CannotSitThroughBoardgame_1" VALUE="1" <<ClientDevl_CannotSitThroughBoardgame_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CannotSitThroughBoardgame_1" VALUE="0" <<ClientDevl_CannotSitThroughBoardgame_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CannotSitThroughBoardgame_1" VALUE="S" <<ClientDevl_CannotSitThroughBoardgame_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Does things without thinking</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DoesThingsWithoutThinking_1" VALUE="1" <<ClientDevl_DoesThingsWithoutThinking_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DoesThingsWithoutThinking_1" VALUE="0" <<ClientDevl_DoesThingsWithoutThinking_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DoesThingsWithoutThinking_1" VALUE="S" <<ClientDevl_DoesThingsWithoutThinking_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cannot play quietly for 20 minutes</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CannotPlayQuietly_1" VALUE="1" <<ClientDevl_CannotPlayQuietly_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CannotPlayQuietly_1" VALUE="0" <<ClientDevl_CannotPlayQuietly_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CannotPlayQuietly_1" VALUE="S" <<ClientDevl_CannotPlayQuietly_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is always on the go</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AlwaysOnGo_1" VALUE="1" <<ClientDevl_AlwaysOnGo_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AlwaysOnGo_1" VALUE="0" <<ClientDevl_AlwaysOnGo_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AlwaysOnGo_1" VALUE="S" <<ClientDevl_AlwaysOnGo_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Runs rather than walks</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_RunsRatherThanWalks_1" VALUE="1" <<ClientDevl_RunsRatherThanWalks_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_RunsRatherThanWalks_1" VALUE="0" <<ClientDevl_RunsRatherThanWalks_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_RunsRatherThanWalks_1" VALUE="S" <<ClientDevl_RunsRatherThanWalks_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fidgets or squirms</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Fidgets_1" VALUE="1" <<ClientDevl_Fidgets_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_Fidgets_1" VALUE="0" <<ClientDevl_Fidgets_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_Fidgets_1" VALUE="S" <<ClientDevl_Fidgets_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cannot keep hands to self</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CannotKeepHandsSelf_1" VALUE="1" <<ClientDevl_CannotKeepHandsSelf_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CannotKeepHandsSelf_1" VALUE="0" <<ClientDevl_CannotKeepHandsSelf_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CannotKeepHandsSelf_1" VALUE="S" <<ClientDevl_CannotKeepHandsSelf_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is difficult to take to visit friends / relatives / shopping</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultVisit_1" VALUE="1" <<ClientDevl_DifficultVisit_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultVisit_1" VALUE="0" <<ClientDevl_DifficultVisit_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultVisit_1" VALUE="S" <<ClientDevl_DifficultVisit_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Resists changes in routine</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsChangesInRoutine_1" VALUE="1" <<ClientDevl_ResistsChangesInRoutine_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsChangesInRoutine_1" VALUE="0" <<ClientDevl_ResistsChangesInRoutine_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsChangesInRoutine_1" VALUE="S" <<ClientDevl_ResistsChangesInRoutine_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is difficult to leave with a babysitter</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultLeaveWithBabysitter_1" VALUE="1" <<ClientDevl_DifficultLeaveWithBabysitter_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultLeaveWithBabysitter_1" VALUE="0" <<ClientDevl_DifficultLeaveWithBabysitter_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DifficultLeaveWithBabysitter_1" VALUE="S" <<ClientDevl_DifficultLeaveWithBabysitter_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is overly cautious</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_OverlyCautious_1" VALUE="1" <<ClientDevl_OverlyCautious_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_OverlyCautious_1" VALUE="0" <<ClientDevl_OverlyCautious_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_OverlyCautious_1" VALUE="S" <<ClientDevl_OverlyCautious_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cries for the slightest reason</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CriesSlightestReason_1" VALUE="1" <<ClientDevl_CriesSlightestReason_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CriesSlightestReason_1" VALUE="0" <<ClientDevl_CriesSlightestReason_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CriesSlightestReason_1" VALUE="S" <<ClientDevl_CriesSlightestReason_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Forget social expectations</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ForgetSocialExpectations_1" VALUE="1" <<ClientDevl_ForgetSocialExpectations_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ForgetSocialExpectations_1" VALUE="0" <<ClientDevl_ForgetSocialExpectations_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ForgetSocialExpectations_1" VALUE="S" <<ClientDevl_ForgetSocialExpectations_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cannot tolerate noisy, busy places</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTolerateNoisy_1" VALUE="1" <<ClientDevl_CannotTolerateNoisy_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTolerateNoisy_1" VALUE="0" <<ClientDevl_CannotTolerateNoisy_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTolerateNoisy_1" VALUE="S" <<ClientDevl_CannotTolerateNoisy_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Needs a calm, quiet atmosphere in order to concentrate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_NeedsCalm_1" VALUE="1" <<ClientDevl_NeedsCalm_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_NeedsCalm_1" VALUE="0" <<ClientDevl_NeedsCalm_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_NeedsCalm_1" VALUE="S" <<ClientDevl_NeedsCalm_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Does sloppy work in spite of effort</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DoesSloppyWork_1" VALUE="1" <<ClientDevl_DoesSloppyWork_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DoesSloppyWork_1" VALUE="0" <<ClientDevl_DoesSloppyWork_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DoesSloppyWork_1" VALUE="S" <<ClientDevl_DoesSloppyWork_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Ignores social rules of modesty</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_IgnoresSocialRules_1" VALUE="1" <<ClientDevl_IgnoresSocialRules_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_IgnoresSocialRules_1" VALUE="0" <<ClientDevl_IgnoresSocialRules_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_IgnoresSocialRules_1" VALUE="S" <<ClientDevl_IgnoresSocialRules_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has no guilt for wrongdoing</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasNoGuilt_1" VALUE="1" <<ClientDevl_HasNoGuilt_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasNoGuilt_1" VALUE="0" <<ClientDevl_HasNoGuilt_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasNoGuilt_1" VALUE="S" <<ClientDevl_HasNoGuilt_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Believes rules apply only to others</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_BelievesRulesApplyOnlyOthers_1" VALUE="1" <<ClientDevl_BelievesRulesApplyOnlyOthers_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_BelievesRulesApplyOnlyOthers_1" VALUE="0" <<ClientDevl_BelievesRulesApplyOnlyOthers_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_BelievesRulesApplyOnlyOthers_1" VALUE="S" <<ClientDevl_BelievesRulesApplyOnlyOthers_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Does not seem to learn from experience</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotSeemLearn_1" VALUE="1" <<ClientDevl_DoesNotSeemLearn_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotSeemLearn_1" VALUE="0" <<ClientDevl_DoesNotSeemLearn_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DoesNotSeemLearn_1" VALUE="S" <<ClientDevl_DoesNotSeemLearn_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cannot tell right from wrong</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTellRight_1" VALUE="1" <<ClientDevl_CannotTellRight_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTellRight_1" VALUE="0" <<ClientDevl_CannotTellRight_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CannotTellRight_1" VALUE="S" <<ClientDevl_CannotTellRight_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Always has an excuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AlwaysHasExcuse_1" VALUE="1" <<ClientDevl_AlwaysHasExcuse_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AlwaysHasExcuse_1" VALUE="0" <<ClientDevl_AlwaysHasExcuse_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AlwaysHasExcuse_1" VALUE="S" <<ClientDevl_AlwaysHasExcuse_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Complains of unfair treatment</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ComplainsUnfairTreatment_1" VALUE="1" <<ClientDevl_ComplainsUnfairTreatment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ComplainsUnfairTreatment_1" VALUE="0" <<ClientDevl_ComplainsUnfairTreatment_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ComplainsUnfairTreatment_1" VALUE="S" <<ClientDevl_ComplainsUnfairTreatment_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has poor self-image, feels worthless</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasPoorSelfimage_1" VALUE="1" <<ClientDevl_HasPoorSelfimage_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasPoorSelfimage_1" VALUE="0" <<ClientDevl_HasPoorSelfimage_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasPoorSelfimage_1" VALUE="S" <<ClientDevl_HasPoorSelfimage_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is overly concerned about performance</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_OverlyConcerned_1" VALUE="1" <<ClientDevl_OverlyConcerned_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_OverlyConcerned_1" VALUE="0" <<ClientDevl_OverlyConcerned_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_OverlyConcerned_1" VALUE="S" <<ClientDevl_OverlyConcerned_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is irritable</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Irritable_1" VALUE="1" <<ClientDevl_Irritable_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_Irritable_1" VALUE="0" <<ClientDevl_Irritable_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_Irritable_1" VALUE="S" <<ClientDevl_Irritable_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has short fuse, explodes at any little thing</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasShortFuse_1" VALUE="1" <<ClientDevl_HasShortFuse_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasShortFuse_1" VALUE="0" <<ClientDevl_HasShortFuse_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasShortFuse_1" VALUE="S" <<ClientDevl_HasShortFuse_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has hurt someone such that medical attention was necessary</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HurtSome_1" VALUE="1" <<ClientDevl_HurtSome_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HurtSome_1" VALUE="0" <<ClientDevl_HurtSome_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HurtSome_1" VALUE="S" <<ClientDevl_HurtSome_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is insensitive to feelings of others</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_InsensitiveFeelingsOthers_1" VALUE="1" <<ClientDevl_InsensitiveFeelingsOthers_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_InsensitiveFeelingsOthers_1" VALUE="0" <<ClientDevl_InsensitiveFeelingsOthers_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_InsensitiveFeelingsOthers_1" VALUE="S" <<ClientDevl_InsensitiveFeelingsOthers_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Resists authority</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsAuthority_1" VALUE="1" <<ClientDevl_ResistsAuthority_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsAuthority_1" VALUE="0" <<ClientDevl_ResistsAuthority_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsAuthority_1" VALUE="S" <<ClientDevl_ResistsAuthority_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is defiant/belligerent when disciplined</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DefiantWhenDisciplined_1" VALUE="1" <<ClientDevl_DefiantWhenDisciplined_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DefiantWhenDisciplined_1" VALUE="0" <<ClientDevl_DefiantWhenDisciplined_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DefiantWhenDisciplined_1" VALUE="S" <<ClientDevl_DefiantWhenDisciplined_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Purposely does the opposite of what is told</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PurposelyDoesOpposite_1" VALUE="1" <<ClientDevl_PurposelyDoesOpposite_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PurposelyDoesOpposite_1" VALUE="0" <<ClientDevl_PurposelyDoesOpposite_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PurposelyDoesOpposite_1" VALUE="S" <<ClientDevl_PurposelyDoesOpposite_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Makes up untruths</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_MakesUpUntruths_1" VALUE="1" <<ClientDevl_MakesUpUntruths_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_MakesUpUntruths_1" VALUE="0" <<ClientDevl_MakesUpUntruths_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_MakesUpUntruths_1" VALUE="S" <<ClientDevl_MakesUpUntruths_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Picks only on people smaller than him/her</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PicksOnSmaller_1" VALUE="1" <<ClientDevl_PicksOnSmaller_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PicksOnSmaller_1" VALUE="0" <<ClientDevl_PicksOnSmaller_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PicksOnSmaller_1" VALUE="S" <<ClientDevl_PicksOnSmaller_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Cannot be trusted alone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_CannotBeTrustedAlone_1" VALUE="1" <<ClientDevl_CannotBeTrustedAlone_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_CannotBeTrustedAlone_1" VALUE="0" <<ClientDevl_CannotBeTrustedAlone_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_CannotBeTrustedAlone_1" VALUE="S" <<ClientDevl_CannotBeTrustedAlone_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Wants friends but is rejected by others</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_WantsFriends_1" VALUE="1" <<ClientDevl_WantsFriends_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_WantsFriends_1" VALUE="0" <<ClientDevl_WantsFriends_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_WantsFriends_1" VALUE="S" <<ClientDevl_WantsFriends_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has a few friends, seems disliked</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasFewFriends_1" VALUE="1" <<ClientDevl_HasFewFriends_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasFewFriends_1" VALUE="0" <<ClientDevl_HasFewFriends_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasFewFriends_1" VALUE="S" <<ClientDevl_HasFewFriends_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has no close friends</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasNoCloseFriends_1" VALUE="1" <<ClientDevl_HasNoCloseFriends_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasNoCloseFriends_1" VALUE="0" <<ClientDevl_HasNoCloseFriends_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasNoCloseFriends_1" VALUE="S" <<ClientDevl_HasNoCloseFriends_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Prefers to play with older children</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayOlderChildren_1" VALUE="1" <<ClientDevl_PrefersPlayOlderChildren_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayOlderChildren_1" VALUE="0" <<ClientDevl_PrefersPlayOlderChildren_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayOlderChildren_1" VALUE="S" <<ClientDevl_PrefersPlayOlderChildren_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Prefers to play with adults</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayAdults_1" VALUE="1" <<ClientDevl_PrefersPlayAdults_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayAdults_1" VALUE="0" <<ClientDevl_PrefersPlayAdults_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayAdults_1" VALUE="S" <<ClientDevl_PrefersPlayAdults_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Prefers to play with younger children</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayYoungerChildren_1" VALUE="1" <<ClientDevl_PrefersPlayYoungerChildren_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayYoungerChildren_1" VALUE="0" <<ClientDevl_PrefersPlayYoungerChildren_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PrefersPlayYoungerChildren_1" VALUE="S" <<ClientDevl_PrefersPlayYoungerChildren_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is physically rough with others</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_PhysicallyRoughOthers_1" VALUE="1" <<ClientDevl_PhysicallyRoughOthers_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_PhysicallyRoughOthers_1" VALUE="0" <<ClientDevl_PhysicallyRoughOthers_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_PhysicallyRoughOthers_1" VALUE="S" <<ClientDevl_PhysicallyRoughOthers_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is excessively bossy with peers</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ExcessivelyBossy_1" VALUE="1" <<ClientDevl_ExcessivelyBossy_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ExcessivelyBossy_1" VALUE="0" <<ClientDevl_ExcessivelyBossy_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ExcessivelyBossy_1" VALUE="S" <<ClientDevl_ExcessivelyBossy_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Gets into fights because of frustration</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_GetsIntoFights_1" VALUE="1" <<ClientDevl_GetsIntoFights_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_GetsIntoFights_1" VALUE="0" <<ClientDevl_GetsIntoFights_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_GetsIntoFights_1" VALUE="S" <<ClientDevl_GetsIntoFights_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Is overly submissive, easily led</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_OverlySubmissive_1" VALUE="1" <<ClientDevl_OverlySubmissive_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_OverlySubmissive_1" VALUE="0" <<ClientDevl_OverlySubmissive_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_OverlySubmissive_1" VALUE="S" <<ClientDevl_OverlySubmissive_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has to be the leader</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_HasBeLeader_1" VALUE="1" <<ClientDevl_HasBeLeader_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_HasBeLeader_1" VALUE="0" <<ClientDevl_HasBeLeader_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_HasBeLeader_1" VALUE="S" <<ClientDevl_HasBeLeader_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Resists sharing</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsSharing_1" VALUE="1" <<ClientDevl_ResistsSharing_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsSharing_1" VALUE="0" <<ClientDevl_ResistsSharing_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_ResistsSharing_1" VALUE="S" <<ClientDevl_ResistsSharing_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Assumes the role of the clown</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AssumesRoleClown_1" VALUE="1" <<ClientDevl_AssumesRoleClown_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AssumesRoleClown_1" VALUE="0" <<ClientDevl_AssumesRoleClown_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AssumesRoleClown_1" VALUE="S" <<ClientDevl_AssumesRoleClown_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Appears depressed, sad, gloomy</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_AppearsDepressed_1" VALUE="1" <<ClientDevl_AppearsDepressed_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_AppearsDepressed_1" VALUE="0" <<ClientDevl_AppearsDepressed_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_AppearsDepressed_1" VALUE="S" <<ClientDevl_AppearsDepressed_1=S>> > Sometimes
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Academic Area</TD></TR>
  <TR>
    <TD CLASS="strcol" >Difficulty with scissors</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_Scissors_1" VALUE="1" <<ClientDevl_Scissors_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_Scissors_1" VALUE="0" <<ClientDevl_Scissors_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_Scissors_1" VALUE="S" <<ClientDevl_Scissors_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty with fine hand work (puzzles, models, etc.)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_FineHandWork_1" VALUE="1" <<ClientDevl_FineHandWork_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_FineHandWork_1" VALUE="0" <<ClientDevl_FineHandWork_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_FineHandWork_1" VALUE="S" <<ClientDevl_FineHandWork_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty recognizing letters</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_RecognizingLetters_1" VALUE="1" <<ClientDevl_RecognizingLetters_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_RecognizingLetters_1" VALUE="0" <<ClientDevl_RecognizingLetters_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_RecognizingLetters_1" VALUE="S" <<ClientDevl_RecognizingLetters_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty recognizing numbers</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_RecognizingNumbers_1" VALUE="1" <<ClientDevl_RecognizingNumbers_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_RecognizingNumbers_1" VALUE="0" <<ClientDevl_RecognizingNumbers_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_RecognizingNumbers_1" VALUE="S" <<ClientDevl_RecognizingNumbers_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty with drawing or coloring tasks</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_DrawingColoringTasks_1" VALUE="1" <<ClientDevl_DrawingColoringTasks_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_DrawingColoringTasks_1" VALUE="0" <<ClientDevl_DrawingColoringTasks_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_DrawingColoringTasks_1" VALUE="S" <<ClientDevl_DrawingColoringTasks_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty with writing letters / numbers / words neatly</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_WritingNeatly_1" VALUE="1" <<ClientDevl_WritingNeatly_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_WritingNeatly_1" VALUE="0" <<ClientDevl_WritingNeatly_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_WritingNeatly_1" VALUE="S" <<ClientDevl_WritingNeatly_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty learning to count money</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_LearningMoney_1" VALUE="1" <<ClientDevl_LearningMoney_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_LearningMoney_1" VALUE="0" <<ClientDevl_LearningMoney_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_LearningMoney_1" VALUE="S" <<ClientDevl_LearningMoney_1=S>> > Sometimes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Difficulty telling time of a regular clock</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDevl_TellingTime_1" VALUE="1" <<ClientDevl_TellingTime_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientDevl_TellingTime_1" VALUE="0" <<ClientDevl_TellingTime_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientDevl_TellingTime_1" VALUE="S" <<ClientDevl_TellingTime_1=S>> > Sometimes
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" ><A NAME="AdjDis">Handicaps/Disabilities/Limitations/Challenges</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Are you experiencing any chronic medical, ambulatory, speech, hearing or visual functioning problems?</TD></TR>
  <TR>
    <TD CLASS="strcol" >Handicap 1</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap1_1" ONCHANGE="callAjax('FunctionalStatus','','selFS1','&name=ClientDevl_FuncStatus1_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap1_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 1</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS1">
      <SELECT NAME="ClientDevl_FuncStatus1_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus1_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap1_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 2</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap2_1" ONCHANGE="callAjax('FunctionalStatus','','selFS2','&name=ClientDevl_FuncStatus2_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap2_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 2</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS2">
      <SELECT NAME="ClientDevl_FuncStatus2_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus2_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap2_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 3</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap3_1" ONCHANGE="callAjax('FunctionalStatus','','selFS3','&name=ClientDevl_FuncStatus3_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap3_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 3</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS3">
      <SELECT NAME="ClientDevl_FuncStatus3_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus3_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap3_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 4</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap4_1" ONCHANGE="callAjax('FunctionalStatus','','selFS4','&name=ClientDevl_FuncStatus4_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap4_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 4</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS4">
      <SELECT NAME="ClientDevl_FuncStatus4_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus4_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap4_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Client's adjustment to disabilities or disorders?</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="MedHx_AdjDis_1" COLS="90" ROWS="2" WRAP=virtual ><<MedHx_AdjDis_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientMH.cgi)]]" VALUE="Add/Update -> Mental Health">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Devl.elements[0].focus();
callAjax('FunctionalStatus','<<ClientDevl_FuncStatus1_1>>','selFS1','&name=ClientDevl_FuncStatus1_1&Handicap=<<ClientDevl_Handicap1_1>>','popup.pl');
callAjax('FunctionalStatus','<<ClientDevl_FuncStatus2_1>>','selFS2','&name=ClientDevl_FuncStatus2_1&Handicap=<<ClientDevl_Handicap2_1>>','popup.pl');
callAjax('FunctionalStatus','<<ClientDevl_FuncStatus3_1>>','selFS3','&name=ClientDevl_FuncStatus3_1&Handicap=<<ClientDevl_Handicap3_1>>','popup.pl');
callAjax('FunctionalStatus','<<ClientDevl_FuncStatus4_1>>','selFS4','&name=ClientDevl_FuncStatus4_1&Handicap=<<ClientDevl_Handicap4_1>>','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
