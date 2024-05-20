[[myHTML->newPage(%form+Resources)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientResources.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="Resources" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Resources Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="heading" COLSPAN="2" >RESOURCES</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Income</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientIncome" >
[[myHTML->ListSel(%form+ListClientIncome+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Number of people who contribute to or must live on the total annual income: (1-15)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientResources_IncomeDeps_1" VALUE="<<ClientResources_IncomeDeps_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,15);" SIZE="5" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Are you able to pay your monthly bills and meet your budgeting and money needs?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_AbleToPay_1" VALUE=0 <<ClientResources_AbleToPay_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_AbleToPay_1" VALUE=1 <<ClientResources_AbleToPay_1=1>> > Yes
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Caregiver/Client Resources,Issues, or Concerns About Meeting Basic Needs (food,shelter,health,transportation,etc.)</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Do you have a valid driver's license? (ASI E4)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_ValidDL_1" VALUE=0 <<ClientResources_ValidDL_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_ValidDL_1" VALUE=1 <<ClientResources_ValidDL_1=1>> > Yes � Valid license; not suspended/revoked. 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Do you have an automobile available for use?
      <BR> � Does not require ownership, only requires availability on a regular basis. (ASI E5)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_AutoForUse_1" VALUE=0 <<ClientResources_AutoForUse_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_AutoForUse_1" VALUE=1 <<ClientResources_AutoForUse_1=1>> > Yes � If above is "No", then "No". 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Are you able to care for your basic needs such as food preparation and meal planning, obtaining clothing, completing chores,
personal care and life skills?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_AbleToCare_1" VALUE=0 <<ClientResources_AbleToCare_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_AbleToCare_1" VALUE=1 <<ClientResources_AbleToCare_1=1>> > Yes
    </TD>
  <TR>
    <TD CLASS="strcol" >
      Are you able to meet your needs for medical, dental, mental health including abuse/neglect, violence or domestic violence
and/or substance abuse concerns?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_AbleToMeetNeeds_1" VALUE=0 <<ClientResources_AbleToMeetNeeds_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_AbleToMeetNeeds_1" VALUE=1 <<ClientResources_AbleToMeetNeeds_1=1>> > Yes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Are you able to meet your legal demands?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_AbleToMeetLegal_1" VALUE=0 <<ClientResources_AbleToMeetLegal_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_AbleToMeetLegal_1" VALUE=1 <<ClientResources_AbleToMeetLegal_1=1>> > Yes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Do you have the resources to meet your recovery needs and/or recovery environment?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_RecoveryNeeds_1" VALUE=0 <<ClientResources_RecoveryNeeds_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_RecoveryNeeds_1" VALUE=1 <<ClientResources_RecoveryNeeds_1=1>> > Yes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Are the resources available to your family adequate in meeting the family's basic needs?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientResources_BasicNeeds_1" VALUE=0 <<ClientResources_BasicNeeds_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_BasicNeeds_1" VALUE=1 <<ClientResources_BasicNeeds_1=1>> > Yes
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >If no on any of the above, describe the limitations:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientResources_FinDesc_1" COLS="90" ROWS="12" WRAP="virtual" ><<ClientResources_FinDesc_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Current Support System</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >
      Does someone contribute to your support in any way?<BR>
      Is patient receiving any regular support (i.e., cash, food, housing) from family/friend. Include spouse's contribution; exclude support by an institution. (ASI E8)
    </TD>
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >
      <INPUT TYPE="radio" NAME="ClientResources_RegSupport_1" VALUE=0 <<ClientResources_RegSupport_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_RegSupport_1" VALUE=1 <<ClientResources_RegSupport_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >
      Does this constitute the majority of your support? (ASI E9)
    </TD>
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >
      <INPUT TYPE="radio" NAME="ClientResources_MajSupport_1" VALUE=0 <<ClientResources_MajSupport_1=0>> > No � If above is "No", then "No".
      <INPUT TYPE="radio" NAME="ClientResources_MajSupport_1" VALUE=1 <<ClientResources_MajSupport_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >
      Will they be active with treatment?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >
      <INPUT TYPE="radio" NAME="ClientResources_ActiveSupport_1" VALUE=0 <<ClientResources_ActiveSupport_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientResources_ActiveSupport_1" VALUE=1 <<ClientResources_ActiveSupport_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="25%" >
      Family Supportive?
    </TD>
    <TD CLASS="strcol" WIDTH="25%" >
      <INPUT TYPE="radio" NAME="ClientResources_FamilySupport_1" VALUE=1 <<ClientResources_FamilySupport_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientResources_FamilySupport_1" VALUE=0 <<ClientResources_FamilySupport_1=0>> > No
    </TD>
    <TD CLASS="strcol" WIDTH="25%" >
      Employer Supportive?
    </TD>
    <TD CLASS="strcol" WIDTH="25%" >
      <INPUT TYPE="radio" NAME="ClientResources_EmplSupport_1" VALUE=1 <<ClientResources_EmplSupport_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientResources_EmplSupport_1" VALUE=0 <<ClientResources_EmplSupport_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="25%" >
      Self help involvement?
    </TD>
    <TD CLASS="strcol" WIDTH="25%" >
      <INPUT TYPE="radio" NAME="ClientResources_SelfHelp_1" VALUE=1 <<ClientResources_SelfHelp_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientResources_SelfHelp_1" VALUE=0 <<ClientResources_SelfHelp_1=0>> > No
    </TD>
    <TD CLASS="strcol" WIDTH="25%" >
      Church Supportive?
    </TD>
    <TD CLASS="strcol" WIDTH="25%" >
      <INPUT TYPE="radio" NAME="ClientResources_ChurchSupport_1" VALUE=1 <<ClientResources_ChurchSupport_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientResources_ChurchSupport_1" VALUE=0 <<ClientResources_ChurchSupport_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >In the past 30 days, how many times have you attended self-help/support groups, or since admission if less than 30 days.</TD>
    <TD CLASS="strcol" COLSPAN="2" WIDTH="50%" >
      <INPUT TYPE=text NAME="ClientResources_SelfHelp30_1" VALUE="<<ClientResources_SelfHelp30_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="5" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="4" >Comments:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
       <TEXTAREA NAME="ClientResources_SupportDesc_1" COLS="80" ROWS="2" WRAP="virtual" ><<ClientResources_SupportDesc_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientLegal.cgi)]]" VALUE="Add/Update -> Legal">
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Resources.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
