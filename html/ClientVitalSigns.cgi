[[myHTML->newHTML(%form+Client Vital Signs+clock mail managertree collapseipad mismenu)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientVitalSigns.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="VitalSigns" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Vital Signs Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="hdrcol" COLSPAN="2" >VITAL SIGNS</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Observation Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_VDate_1" VALUE="<<ClientVitalSigns_VDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Rejected</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientVitalSigns_Rejected_1">
        [[DBA->selxTable(%form+xPhysicalExamRejected+<<ClientVitalSigns_Rejected_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Height
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" ID="HeightFeet" NAME="ClientVitalSigns_HeightFeet_1" VALUE="<<ClientVitalSigns_HeightFeet_1>>" ONFOCUS="select()" ONCHANGE="callAjax('calcBMI',this.value,this.id,'&hi='+document.VitalSigns.ClientVitalSigns_HeightInches_1.value+'&w='+document.VitalSigns.ClientVitalSigns_Weight_1.value);" SIZE="10" >
      Feet
      <INPUT TYPE="text" ID="HeightInches" NAME="ClientVitalSigns_HeightInches_1" VALUE="<<ClientVitalSigns_HeightInches_1>>" ONFOCUS="select()" ONCHANGE="callAjax('calcBMI',this.value,this.id,'&hf='+document.VitalSigns.ClientVitalSigns_HeightFeet_1.value+'&w='+document.VitalSigns.ClientVitalSigns_Weight_1.value);" SIZE="10" >
      Inches
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Weight
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" ID="Weight" NAME="ClientVitalSigns_Weight_1" VALUE="<<ClientVitalSigns_Weight_1>>" ONFOCUS="select()" ONCHANGE="callAjax('calcBMI',this.value,this.id,'&hf='+document.VitalSigns.ClientVitalSigns_HeightFeet_1.value+'&hi='+document.VitalSigns.ClientVitalSigns_HeightInches_1.value);" SIZE="10" >
      Pounds
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      BMI
    </TD>
    <TD CLASS="strcol hotmsg" >
      <SPAN ID="Client_BMI" ></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      BSA
    </TD>
    <TD CLASS="strcol hotmsg" >
      <SPAN ID="Client_BSA" ></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Waist
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_Waist_1" VALUE="<<ClientVitalSigns_Waist_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,100)" SIZE="10" >
      Inches
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Temperature
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_Temperature_1" VALUE="<<ClientVitalSigns_Temperature_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,80,120)" SIZE="10" >
      Fahrenheit
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Blood Pressure
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_BPSystolic_1" VALUE="<<ClientVitalSigns_BPSystolic_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,30,200)" SIZE="10" >
      Systolic /
      <INPUT TYPE="text" NAME="ClientVitalSigns_BPDiastolic_1" VALUE="<<ClientVitalSigns_BPDiastolic_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,30,200)" SIZE="10" >
      Diastolic mmHg
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Body Site
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientVitalSigns_BodySite_1">
        [[DBA->selxTable(%form+xBodySite+<<ClientVitalSigns_BodySite_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Pulse
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_Pulse_1" VALUE="<<ClientVitalSigns_Pulse_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,30,250)" SIZE="10" >
      Beats per Minute
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="rptmsg" > A normal resting heart rate for adults ranges from 60 to 100 beats a minute.  </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Pulse Oximetry
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_Oximetry_1" VALUE="<<ClientVitalSigns_Oximetry_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,50,100)" SIZE="10" >
      SpO2
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="rptmsg" > Normal pulse oximeter readings range from 95 to 100 percent, under most circumstances. Values under 90 percent are considered low.  </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      FS Blood Sugar (finger stick)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_BloodSugar_1" VALUE="<<ClientVitalSigns_BloodSugar_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1000)" SIZE="10" >
      mg/dl
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="rptmsg" > A normal fasting (no food for eight hours) blood sugar level is between 70 and 99 mg/dL A normal blood sugar level two hours after eating is less than 140 mg/dL </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Hemoglobin A1c Blood Test
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_HbA1c_1" VALUE="<<ClientVitalSigns_HbA1c_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30)" SIZE="10" >
      (HbA1c)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="rptmsg" >
Normal - less than 5.7% (39 mmol/mol).<BR>
Diabetes - 6.5% (48 mmol/mol) or higher.<BR>
Increased risk/pre-diabetes - 5.7% to 6.4% (39-46 mmol/mol)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Respiration
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_Respiration_1" VALUE="<<ClientVitalSigns_Respiration_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,100)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="rptmsg" > The typical respiratory rate for a healthy adult at rest is 12-20 breaths per minute. Average resting respiratory rates by age are: birth to 6 weeks: 30-60 breaths per minute. 6 months: 25-40 breaths per minute.  </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >
      Pain
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientVitalSigns_Pain_1" VALUE="<<ClientVitalSigns_Pain_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10)" SIZE="4" > Scale 0 - 10
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Comparative Pain Scale</TD>
    <TD CLASS="rptmsg" > 
<A HREF="javascript:void()" TITLE="Feeling perfectly normal.  Minor Does not interfere with most activities.  Able to adapt to pain psychologically and with medication or devices such as cushions.">0 No pain.</A>
<A HREF="javascript:void()" TITLE="Very light barely noticeable pain, like a mosquito bite or a poison ivy itch. Most of the time you never think about the pain.">1 Very Mild</A>
<A HREF="javascript:void()" TITLE="Minor pain, like lightly pinching the fold of skin between the thumb and first finger with the other hand, using the fingernails. Note that people react differently to this selftest.">2 Discomforting</A>
<A HREF="javascript:void()" TITLE="Very noticeable pain, like an accidental cut, a blow to the nose causing a bloody nose, or a doctor giving you an injection. The pain is not so strong that you cannot get used to it. Eventually, most of the time you don't notice the pain.  You have adapted to it.  Moderate Interferes with many activities.  Requires lifestyle changes but patient remains independent.  Unable to adapt to pain.">3 Tolerable</A>
<A HREF="javascript:void()" TITLE="Strong, deep pain, like an average toothache, the initial pain from a bee sting, or minor trauma to part of the body, such as stubbing your toe real hard. So strong you notice the pain all the time and cannot completely adapt. This pain level can be simulated by pinching the fold of skin between the thumb and first finger with the other hand, using the fingernails, and squeezing real hard. Note how the simulated pain is initially piercing but becomes dull after that.">4 Distressing</A>
<A HREF="javascript:void()" TITLE="Strong, deep, piercing pain, such as a sprained ankle when you stand on it wrong or mild back pain. Not only do you notice the pain all the time, you are now so preoccupied with managing it that you normal lifestyle is curtailed. Temporary personality disorders are frequent.">5 Very Distressing</A>
<A HREF="javascript:void()" TITLE="Strong, deep, piercing pain so strong it seems to partially dominate your senses, causing you to think somewhat unclearly. At this point you begin to have trouble holding a job or maintaining normal social relationships. Comparable to a bad non-migraine headache combined with several bee stings, or a bad back pain.  Severe Unable to engage in normal activities.  Patient is disabled and unable to function independently.">6 Intense</A>
<A HREF="javascript:void()" TITLE="Same as 6 except the pain completely dominates your senses, causing you to think unclearly about half the time.  At this point you are effectively disabled and frequently cannot live alone. Comparable to an average migraine headache.">7 Very Intense</A>
<A HREF="javascript:void()" TITLE="Pain so intense you can no longer think clearly at all, and have often undergone severe personality change if the pain has been present for a long time. Suicide is frequently contemplated and sometimes tried. Comparable to childbirth or a real bad migraine headache.">8 Utterly Horrible</A>
<A HREF="javascript:void()" TITLE="Unbearable Pain so intense you cannot tolerate it and demand pain killers or surgery, no matter what the side effects or risk. If this doesn't work, suicide is frequent since there is no more joy in life whatsoever. Comparable to throat cancer.">9 Excruciating Unbearable</A>
<A HREF="javascript:void()" TITLE="Pain so intense you will go unconscious shortly. Most people have never experienced this level of pain. Those who have suffered a severe accident, such as a crushed hand, and lost consciousness as a result of the pain and not blood loss, have experienced level 10.">10 Unimaginable Unspeakable</A>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<SCRIPT LANGUAGE="javascript">
//Pain Scale (painscale)
//Lucile Packard Children’s Hospital Heart Center/CVICU
//http://www.pudendal.info/info/documents/ComparativePainScale.htm - Author
//Alice Rich, RN – Recommender and Maintainer 12/08 Last Update
</SCRIPT>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=Agent) <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Vital Signs record?')" NAME="ClientVitalSigns_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" > ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updClientVitalSigns(%form+<<<ClientVitalSigns_ID>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.VitalSigns.elements[0].focus();
callAjax('calcBMI','','','&hf=<<<ClientVitalSigns_HeightFeet_1>>>&hi=<<<ClientVitalSigns_HeightInches_1>>>&w=<<<ClientVitalSigns_Weight_1>>>');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
