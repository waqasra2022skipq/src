[[myHTML->newPage(%form+SOGSGSI)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vSOGSGSI.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vSSN.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="SOGSGSI" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      South Oaks Gambling Screen Gambling Severity Index - RH
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 1</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Member ID: <<<Client_ClientID_1>>>
    </TD>
    <TD CLASS="strcol" >
      TransDate: 
      <INPUT TYPE="text" NAME="SOGSGSI_TransDate_1" VALUE="<<SOGSGSI_TransDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Provider ID:
      <SELECT NAME="SOGSGSI_ProvID_1" > [[DBA->selProviders(%form+<<SOGSGSI_ProvID_1>>]] </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      Type: 
      <INPUT TYPE="radio" NAME="SOGSGSI_TransType_1" VALUE="A" <<SOGSGSI_TransType_1=A>> > Admit
      <INPUT TYPE="radio" NAME="SOGSGSI_TransType_1" VALUE="U" <<SOGSGSI_TransType_1=U>> > Update
      <INPUT TYPE="radio" NAME="SOGSGSI_TransType_1" VALUE="D" <<SOGSGSI_TransType_1=D>> > Discharge
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      A1. How old were you the very first time you gambled on anything (for money)?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A1_1" VALUE="<<SOGSGSI_A1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A2. How old were you when you started gambling 4 days per month or more frequently?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A2_1" VALUE="<<SOGSGSI_A2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A3. How old were you when your gambling became a real problem for you?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A3_1" VALUE="<<SOGSGSI_A3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A4. What type of gambling is the biggest problem for you NOW?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A4_1" VALUE="<<SOGSGSI_A4_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A5. Approximately how much money do you currently owe as a result of gambling? (Include credit card debt, bank loans, second mortgages, money borrowed from business, personal loans, outstanding checks, and other borrowing).
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A5_1" VALUE="<<SOGSGSI_A5_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,999999);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A6. In addition to your current debts, could you estimate the value of the assets you may have sold in the past to raise money for gambling including savings, stocks, bonds, other securities, IRAs, other retirement accounts, life insurance policies cashed in, etc.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A6_1" VALUE="<<SOGSGSI_A6_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,999999);" SIZE="10" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >&nbsp;</TD></TR>
  <TR ><TD CLASS="strcol" >Of the amount of money you have lost, please try to figure out what percentage was lost at:</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      A7. Hardrock Casino
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A7_1" VALUE="<<SOGSGSI_A7_1>>" ONFOCUS="select()" ONCHANGE="return validateLost(this.form,this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A8. Lucky Star
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A8_1" VALUE="<<SOGSGSI_A8_1>>" ONFOCUS="select()" ONCHANGE="return validateLost(this.form,this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A9. Remington Park Racino
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A9_1" VALUE="<<SOGSGSI_A9_1>>" ONFOCUS="select()" ONCHANGE="return validateLost(this.form,this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A10. Riverwind
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A10_1" VALUE="<<SOGSGSI_A10_1>>" ONFOCUS="select()" ONCHANGE="return validateLost(this.form,this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A11. Windstar
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A11_1" VALUE="<<SOGSGSI_A11_1>>" ONFOCUS="select()" ONCHANGE="return validateLost(this.form,this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A12. Oklahoma Lottery (Powerball, Mega Millions, Megaplier, Hot Lotto, Cash 5, Pick 3, scratch tickets and other �instant� games)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A12_1" VALUE="<<SOGSGSI_A12_1>>" ONFOCUS="select()" ONCHANGE="return validateLost(this.form,this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      A13. Other places
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_A13_1" VALUE="<<SOGSGSI_A13_1>>" ONFOCUS="select()" ONCHANGE="return validateLost(this.form,this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="homesublink" >
      Total should add up to 100% ==>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="SOGSGSI_TotalLost_1" VALUE="<<SOGSGSI_TotalLost_1>>" ONFOCUS="this.blur()" SIZE="10" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_ACOM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_ACOM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Types of Gambling Activity:</TD>
    <TD CLASS="strcol" > Past 30 days </TD>
    <TD CLASS="strcol" > Lifetime (years) </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      1. Gambling -card games (non-casino)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G1D_1" VALUE="<<SOGSGSI_G1D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G1Y_1" VALUE="<<SOGSGSI_G1Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      2. Gambling -Horses, dogs, etc.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G2D_1" VALUE="<<SOGSGSI_G2D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G2Y_1" VALUE="<<SOGSGSI_G2Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      3. Sports
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G3D_1" VALUE="<<SOGSGSI_G3D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G3Y_1" VALUE="<<SOGSGSI_G3Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      4. Dice games, dominoes (non-casino)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G4D_1" VALUE="<<SOGSGSI_G4D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G4Y_1" VALUE="<<SOGSGSI_G4Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      5. Casino table games (blackjack, craps, roulette, casino poker)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G5D_1" VALUE="<<SOGSGSI_G5D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G5Y_1" VALUE="<<SOGSGSI_G5Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      6. Lottery, daily numbers ( not "instant") games like Scratch-offs
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G6D_1" VALUE="<<SOGSGSI_G6D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G6Y_1" VALUE="<<SOGSGSI_G6Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      7. Bingo
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G7D_1" VALUE="<<SOGSGSI_G7D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G7Y_1" VALUE="<<SOGSGSI_G7Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_G1COM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_G1COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
  <TR ><TD CLASS="port hdrtxt" >Page 2</TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Types of Gambling Activity:</TD>
    <TD CLASS="strcol" > Past 30 days </TD>
    <TD CLASS="strcol" > Lifetime (years) </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      8. Stocks, options, commodities
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G8D_1" VALUE="<<SOGSGSI_G8D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G8Y_1" VALUE="<<SOGSGSI_G8Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      9. Slots, poker machines, video poker terminals,
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G9D_1" VALUE="<<SOGSGSI_G9D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G9Y_1" VALUE="<<SOGSGSI_G9Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      10. Bowl, pool, golf, or other games of skill for money.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G10D_1" VALUE="<<SOGSGSI_G10D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G10Y_1" VALUE="<<SOGSGSI_G10Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      11. Scratch-offs, pull tabs, or other " instant" games.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G11D_1" VALUE="<<SOGSGSI_G11D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G11Y_1" VALUE="<<SOGSGSI_G11Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      12. Some other type of gambling not listed, e.g., keno.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G12D_1" VALUE="<<SOGSGSI_G12D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G12Y_1" VALUE="<<SOGSGSI_G12Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      13. Gambling more than you could afford.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G13D_1" VALUE="<<SOGSGSI_G13D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G13Y_1" VALUE="<<SOGSGSI_G13Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      14. Any gambling at all.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G14D_1" VALUE="<<SOGSGSI_G14D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G14Y_1" VALUE="<<SOGSGSI_G14Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >TO INTERVIEWER: Take all forms of gambling into account to determine how many days client gambled.</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      15. Gambling and substance use in same day?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G15D_1" VALUE="<<SOGSGSI_G15D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G15Y_1" VALUE="<<SOGSGSI_G15Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      16. Which would you say is your primary addiction?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G16D_1" VALUE="<<SOGSGSI_G16D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G16Y_1" VALUE="<<SOGSGSI_G16Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" > (check all that apply) 
      <INPUT TYPE="checkbox" NAME="SOGSGSI_G16GT_1" VALUE="1" <<SOGSGSI_G16GT_1=checkbox>> > Gambling
      <INPUT TYPE="checkbox" NAME="SOGSGSI_G16SAT_1" VALUE="1" <<SOGSGSI_G16SAT_1=checkbox>> > Substance abuse
      <INPUT TYPE="checkbox" NAME="SOGSGSI_G16MHT_1" VALUE="1" <<SOGSGSI_G16MHT_1=checkbox>> > Mental Health
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_G8COM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_G8COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      17. How long was your last period of voluntary abstinence from gambling? (Months) * "0" = never abstinent
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G17_1" VALUE="<<SOGSGSI_G17_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      18. How many months ago did abstinence from gambling end ?  * "0" = still abstinent
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G18_1" VALUE="<<SOGSGSI_G18_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      19. How many times in your life have you been treated for gambling (including GA)?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G19_1" VALUE="<<SOGSGSI_G19_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      20. How much money have you lost in the last 30 days on gambling?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G20_1" VALUE="<<SOGSGSI_G20_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      21. How many days have you been treated in an outpatient setting in the past 30 days? (* include GA)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G21_1" VALUE="<<SOGSGSI_G21_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      22. How many days in the past 30 have you experienced gambling problems? (*include craving, withdrawal sypmtoms, disturbing effects of gambling, or wanting to stop and being unable)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G22_1" VALUE="<<SOGSGSI_G22_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_G17COM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_G17COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="homelabel" COLSPAN="2" >24. Have any of thefollowing people in your life had (or still have) a gambling problem? *0=no; 1=yes</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      1. Father
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x1_1" VALUE="1" <<SOGSGSI_G24x1_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x1_1" VALUE="0" <<SOGSGSI_G24x1_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      2. Mother
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x2_1" VALUE="1" <<SOGSGSI_G24x2_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x2_1" VALUE="0" <<SOGSGSI_G24x2_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      3. A brother or sister
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x3_1" VALUE="1" <<SOGSGSI_G24x3_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x3_1" VALUE="0" <<SOGSGSI_G24x3_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      4. A grandparent
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x4_1" VALUE="1" <<SOGSGSI_G24x4_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x4_1" VALUE="0" <<SOGSGSI_G24x4_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      5. Spouse or partner
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x5_1" VALUE="1" <<SOGSGSI_G24x5_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x5_1" VALUE="0" <<SOGSGSI_G24x5_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      6. Child(ren)
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x6_1" VALUE="1" <<SOGSGSI_G24x6_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x6_1" VALUE="0" <<SOGSGSI_G24x6_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      7. Another relative
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x7_1" VALUE="1" <<SOGSGSI_G24x7_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x7_1" VALUE="0" <<SOGSGSI_G24x7_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      8. A friend or other person important in my life
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x8_1" VALUE="1" <<SOGSGSI_G24x8_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G24x8_1" VALUE="0" <<SOGSGSI_G24x8_1=0>> > No
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_G24COM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_G24COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
  <TR ><TD CLASS="port hdrtxt" >Page 3</TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >In the past:</TD>
    <TD CLASS="strcol" > Lifetime </TD>
    <TD CLASS="strcol" > 6-Months </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      25. In the past, when you gambled how often do you go back another day to win back the money you lost?<BR>
1=never<BR>
2=some (less than half the time) of the time I lost<BR>
3=most of the time I lost<BR>
4=every time I lost<BR>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G25L_1" VALUE="<<SOGSGSI_G25L_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,4);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G25M_1" VALUE="<<SOGSGSI_G25M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,4);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      26. In the past, have you ever claimed to be winning money when you really were not?  In fact, you lost?<BR>
1=never<BR>
2=yes, less than half the time I lost<BR>
3=yes, most of the time<BR>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G26L_1" VALUE="<<SOGSGSI_G26L_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,3);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G26M_1" VALUE="<<SOGSGSI_G26M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,3);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      27. In the past, did you feel you have had a problem with betting money or gambling?<BR>
1=never<BR>
2=yes, in the past but not now<BR>
3=yes<BR>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G27L_1" VALUE="<<SOGSGSI_G27L_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,3);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G27M_1" VALUE="<<SOGSGSI_G27M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,3);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      28. In the past , did you ever gamble more than you intend to?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G28L_1" VALUE="1" <<SOGSGSI_G28L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G28L_1" VALUE="0" <<SOGSGSI_G28L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G28M_1" VALUE="1" <<SOGSGSI_G28M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G28M_1" VALUE="0" <<SOGSGSI_G28M_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      29. In the past, have people criticized your betting or told you that you had a gambling problem, regardless of whether or not you thought it was true?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G29L_1" VALUE="1" <<SOGSGSI_G29L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G29L_1" VALUE="0" <<SOGSGSI_G29L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G29M_1" VALUE="1" <<SOGSGSI_G29M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G29M_1" VALUE="0" <<SOGSGSI_G29M_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      30. In the past, have you felt guilty about the way you gamble or what happens when you gamble?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G30L_1" VALUE="1" <<SOGSGSI_G30L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G30L_1" VALUE="0" <<SOGSGSI_G30L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G30M_1" VALUE="1" <<SOGSGSI_G30M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G30M_1" VALUE="0" <<SOGSGSI_G30M_1=0>> > No
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_G25COM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_G25COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >In the past:</TD>
    <TD CLASS="strcol" > Lifetime </TD>
    <TD CLASS="strcol" > 6-Months </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      31. In the past, have you felt like you would like to stop betting money or gambling nut did not think you could?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G31L_1" VALUE="1" <<SOGSGSI_G31L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G31L_1" VALUE="0" <<SOGSGSI_G31L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G31M_1" VALUE="1" <<SOGSGSI_G31M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G31M_1" VALUE="0" <<SOGSGSI_G31M_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      32. In the past, have you hidden betting slips, lottery tickets, gambling mobey, I.O.U.s or other signs of betting or gambling from your spouse, children or other important people in your life?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G32L_1" VALUE="1" <<SOGSGSI_G32L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G32L_1" VALUE="0" <<SOGSGSI_G32L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G32M_1" VALUE="1" <<SOGSGSI_G32M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G32M_1" VALUE="0" <<SOGSGSI_G32M_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      33. In the past, have you argued with people you live with over how you handle money?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G33L_1" VALUE="1" <<SOGSGSI_G33L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G33L_1" VALUE="0" <<SOGSGSI_G33L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G33M_1" VALUE="1" <<SOGSGSI_G33M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G33M_1" VALUE="0" <<SOGSGSI_G33M_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      34. If yes, have money arguments centered on your gambling?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G34L_1" VALUE="1" <<SOGSGSI_G34L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G34L_1" VALUE="0" <<SOGSGSI_G34L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G34M_1" VALUE="1" <<SOGSGSI_G34M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G34M_1" VALUE="0" <<SOGSGSI_G34M_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      35. In the past, have you borrowed from someone and not paid them back as a result of your gambling?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G35L_1" VALUE="1" <<SOGSGSI_G35L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G35L_1" VALUE="0" <<SOGSGSI_G35L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G35M_1" VALUE="1" <<SOGSGSI_G35M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G35M_1" VALUE="0" <<SOGSGSI_G35M_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      36. In the past, have you lost time from work (or school) due to betting money or gambling?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G36L_1" VALUE="1" <<SOGSGSI_G36L_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G36L_1" VALUE="0" <<SOGSGSI_G36L_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G36M_1" VALUE="1" <<SOGSGSI_G36M_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G36M_1" VALUE="0" <<SOGSGSI_G36M_1=0>> > No
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_G31COM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_G31COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
  <TR ><TD CLASS="port hdrtxt" >Page 4</TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >37. In the past, have you utilized the following resources to gamble or pay gambling debts?</TD>
    <TD CLASS="strcol" > Lifetime </TD>
    <TD CLASS="strcol" > 6-Months </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37a. Borrowed from household money?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37aL_1" VALUE="1" <<SOGSGSI_G37aL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37aL_1" VALUE="0" <<SOGSGSI_G37aL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37aM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37aM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37aM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37aM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37b. from your spouse?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37bL_1" VALUE="1" <<SOGSGSI_G37bL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37bL_1" VALUE="0" <<SOGSGSI_G37bL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37bM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37bM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37bM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37bM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37c. from other relatives or in-laws?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37cL_1" VALUE="1" <<SOGSGSI_G37cL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37cL_1" VALUE="0" <<SOGSGSI_G37cL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37cM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37cM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37cM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37cM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37d. from banks, loan companies or credit unions?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37dL_1" VALUE="1" <<SOGSGSI_G37dL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37dL_1" VALUE="0" <<SOGSGSI_G37dL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37dM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37dM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37dM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37dM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37e. from credit cards?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37eL_1" VALUE="1" <<SOGSGSI_G37eL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37eL_1" VALUE="0" <<SOGSGSI_G37eL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37eM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37eM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37eM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37eM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37f. from loan sharks?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37fL_1" VALUE="1" <<SOGSGSI_G37fL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37fL_1" VALUE="0" <<SOGSGSI_G37fL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37fM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37fM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37fM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37fM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37g. you sold personal or family property?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37gL_1" VALUE="1" <<SOGSGSI_G37gL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37gL_1" VALUE="0" <<SOGSGSI_G37gL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37gM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37gM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37gM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37gM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37h. you cashed in stocks, bonds or other securities?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37hL_1" VALUE="1" <<SOGSGSI_G37hL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37hL_1" VALUE="0" <<SOGSGSI_G37hL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37hM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37hM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37hM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37hM_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      37i. you borrowed on your checking account (passed bad checks)?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37iL_1" VALUE="1" <<SOGSGSI_G37iL_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37iL_1" VALUE="0" <<SOGSGSI_G37iL_1=0>> > No
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G37iM_1" VALUE="1" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37iM_1=1>> > Yes<BR>
      <INPUT TYPE="radio" NAME="SOGSGSI_G37iM_1" VALUE="0" ONCLICK="return validatePast(this.form,this);" <<SOGSGSI_G37iM_1=0>> > No
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      For Questions 25 - 37
    </TD>
    <TD CLASS="homesublink" >
      6-Months Total=
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="SOGSGSI_TotalPast_1" VALUE="<<SOGSGSI_TotalPast_1>>" ONFOCUS="this.blur()" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      0-2 = no problem<BR>
3-4 = some problem<BR>
5 or more = probable pathological gambler<BR>
    </TD>
    <TD CLASS="homesublink" >
      &nbsp;
    </TD>
    <TD CLASS="strcol" >
      &nbsp;
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="SOGSGSI_G37COM_1" COLS="90" ROWS="8" WRAP="virtual" ><<SOGSGSI_G37COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="strcol" > For questions 38 and 39 use this rating scale: </TD></TR>
  <TR ><TD CLASS="strcol" ><B> 0=not at all 1=slightly 2=moderately 3=considerably 4=extremely </B></TD></TR>
  <TR >
    <TD CLASS="strcol" >
      38. How troubled or bothered have you been by gambling problems in the last 30 days?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G38_1" VALUE="<<SOGSGSI_G38_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,4);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      39. How important to you now is treatment for these gambling problems?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G39_1" VALUE="<<SOGSGSI_G39_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,4);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" > INTERVIEWER SEVERITY RATING </TD></TR>
  <TR >
    <TD CLASS="strcol" >
      41. How would you rate the patient�s need for gambling counseling?<BR>
0=None necessary to 9-treatment needed to intervene in a life threatening situation
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SOGSGSI_G41_1" VALUE="<<SOGSGSI_G41_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,9);" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" > 42. Is the information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      42a. Patients misrepresentation?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G42a_1" VALUE="1" <<SOGSGSI_G42a_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G42a_1" VALUE="0" <<SOGSGSI_G42a_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      42b. Patients inability to understand?
    </TD>
    <TD CLASS="strcol" > 
      <INPUT TYPE="radio" NAME="SOGSGSI_G42b_1" VALUE="1" <<SOGSGSI_G42b_1=1>> > Yes
      <INPUT TYPE="radio" NAME="SOGSGSI_G42b_1" VALUE="0" <<SOGSGSI_G42b_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
Interview Severity Rating Scale:
<BR>
0-1 No real problem, treatment not indicated<BR>
2-3 Slight Problem, treatment probably not necessary<BR>
4-5 Moderate Problem, some treatment indicated<BR>
6-7 Considerable problem,treatment necessary<BR>
8-9 Extreme Problem treatment absolutely necessary
<BR>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this entire SOGSGSI record?');" NAME="SOGSGSI_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updSOGSGSI(%form)" >
<INPUT TYPE="hidden" NAME="SOGSGSI_AvgLost_1" VALUE="<<SOGSGSI_AvgLost_1>>" >
<INPUT TYPE="hidden" NAME="SOGSGSI_AvgPast_1" VALUE="<<SOGSGSI_AvgPast_1>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.SOGSGSI.elements[1].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
