[[myHTML->newPage(%form+SOGS)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vSOGS.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="SOGS" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      South Oaks Gambling Screen
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >SOGS</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Member ID: <<<Client_ClientID_1>>>
    </TD>
    <TD CLASS="strcol" >
      TransDate: 
      <INPUT TYPE="text" NAME="SOGS_TransDate_1" VALUE="<<SOGS_TransDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Provider ID:
      <SELECT NAME="SOGS_ProvID_1" >[[DBA->selProviders(%form+<<SOGS_ProvID_1>>)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      Type: 
      <INPUT TYPE="radio" NAME="SOGS_TransType_1" VALUE="A" <<SOGS_TransType_1=A>> > Admit
      <INPUT TYPE="radio" NAME="SOGS_TransType_1" VALUE="U" <<SOGS_TransType_1=U>> > Update
      <INPUT TYPE="radio" NAME="SOGS_TransType_1" VALUE="D" <<SOGS_TransType_1=D>> > Discharge
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      1. Please indicate which of the following types of gambling you have done. For each type, mark one answer which describes the last time you performed each listed behavior and how often you did the behavior. If you check "Not at all" simply go on to the next item as you will not need to report "how often". 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      a. did any kind of gambling
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1a1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1a1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1a2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1a2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      b. played cards for money (such as Texas Hold'em, poker, or other card games)
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1b1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1b1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1b2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1b2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      c. bet on horses, dogs, or other animals (at OTB, the track or with a bookie) for money
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1c1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1c1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1c2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1c2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      d. bet on sports for money (including basketball, football, parlay cards, Jai Alai, or other sports) with friends, a bookie, at work, etc.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1d1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1d1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1d2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1d2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      e. played dice games (including craps, over and under, or other dice games) for money
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1e1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1e1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1e2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1e2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      f. gambled in a casino or on a casino boat (legal or otherwise) for money
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1f1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1f1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1f2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1f2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      g. played the numbers or bet on lotteries, Kino, or Quick Draw
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1g1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1g1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1g2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1g2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      h. played bingo for money
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1h1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1h1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1h2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1h2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      i. played the stock, options, and /or commodities market
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1i1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1i1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1i2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1i2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      j. played slot machines, poker machines, or other gambling machines
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1j1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1j1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1j2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1j2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      k. bowled, shot pool, played golf or darts, or some other game of skill for money
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1k1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1k1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1k2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1k2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      l. pull tabs or "paper" games other than lotteries (such as Lucky 7's)
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1l1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1l1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1l2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1l2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      m. some form of gambling not listed above
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1m1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1m1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1m2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1m2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" COLSPAN="3" >
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;please specify
      <INPUT TYPE="text" NAME="SOGS_A1m_1" VALUE="<<SOGS_A1m_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      n. gambled and used alcohol or drugs at the same time
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1n1_1">[[DBA->selxTable(%form+xSOGSWhen+<<SOGS_A1n1_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SOGS_A1n2_1">[[DBA->selxTable(%form+xSOGSOften+<<SOGS_A1n2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      2. How troubled or bothered have you been, due to your gambling, in the past six months?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A2_1">[[DBA->selxTable(%form+xRateScale+<<SOGS_A2_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      3. Have you ever quit gambling for a period or time?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A3_1">[[DBA->selxTable(%form+xSOGS3+<<SOGS_A3_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      4. What is the largest amount of money you have ever gambled on any one day?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A4_1">[[DBA->selxTable(%form+xSOGS4+<<SOGS_A4_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      5a. Which of the following people in your life has (or had) a gambling problem.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A5a_1">[[DBA->selxTable(%form+xSOGS5a+<<SOGS_A5a_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      5b. Have your family members ever been criticized about their gambling? (Yes or No)
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A5b_1" VALUE="Yes" <<SOGS_A5b_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A5b_1" VALUE="No" <<SOGS_A5b_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      6. When you gamble, how often do you go back another day to win back money you lost?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A6_1">[[DBA->selxTable(%form+xSOGS6+<<SOGS_A6_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      7. Do you feel you have had a problem with betting money or gambling?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A7_1">[[DBA->selxTable(%form+xSOGS7+<<SOGS_A7_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      7a. If you answered yes to item seven, how long ago did you have a problem betting?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A7a_1">[[DBA->selxTable(%form+xSOGS7a+<<SOGS_A7a_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      8. Have you ever claimed to be winning money gambling but weren't really? In fact, you lost?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="SOGS_A8_1">[[DBA->selxTable(%form+xSOGS8+<<SOGS_A8_1>>+Descr+0+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol hdrtxt" >
      Please answer "yes" or "no" for each of the following statements as they describe you.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      9. Did you ever gamble more than you intended to?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A9_1" VALUE="Yes" <<SOGS_A9_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A9_1" VALUE="No" <<SOGS_A9_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >

      10. Have people criticized your betting or told you that you had a gambling problem, regardless of whether or not you thought it was true?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A10_1" VALUE="Yes" <<SOGS_A10_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A10_1" VALUE="No" <<SOGS_A10_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >

      11. Have you ever felt guilty about the way you gamble or what happens when you gamble?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A11_1" VALUE="Yes" <<SOGS_A11_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A11_1" VALUE="No" <<SOGS_A11_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      12. Have you ever felt like you would like to stop betting money or gambling but didn't think you could?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A12_1" VALUE="Yes" <<SOGS_A12_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A12_1" VALUE="No" <<SOGS_A12_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      13. Have you ever hidden betting slips, lottery tickets, gambling money, I.O.U.'s or other signs of betting or gambling from your spouse, parents, children, or other important people in your life?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A13_1" VALUE="Yes" <<SOGS_A13_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A13_1" VALUE="No" <<SOGS_A13_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      14. Have you ever argued with people you live with over how you handle money?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A14_1" VALUE="Yes" <<SOGS_A14_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A14_1" VALUE="No" <<SOGS_A14_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      15. (If you answered yes to question 14): Have money arguments ever centered on your gambling?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A15_1" VALUE="Yes" <<SOGS_A15_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A15_1" VALUE="No" <<SOGS_A15_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      16. Have you ever lost time from work or school due to betting money or gambling?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A16_1" VALUE="Yes" <<SOGS_A16_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A16_1" VALUE="No" <<SOGS_A16_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      17. Have you ever borrowed from someone and not paid them back as a result of your gambling?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A17_1" VALUE="Yes" <<SOGS_A17_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A17_1" VALUE="No" <<SOGS_A17_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol hdrtxt" COLSPAN="3" >
      18. If you borrowed money to gamble or to pay gambling debts., who or where did you borrow from?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      a. From household money
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18a_1" VALUE="Yes" <<SOGS_A18a_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18a_1" VALUE="No" <<SOGS_A18a_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      b. From your spouse or parents
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18b_1" VALUE="Yes" <<SOGS_A18b_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18b_1" VALUE="No" <<SOGS_A18b_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      c. From other relatives, friends, boyfriends or girlfriends, or in-laws
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18c_1" VALUE="Yes" <<SOGS_A18c_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18c_1" VALUE="No" <<SOGS_A18c_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      d. From banks, loan companies, or credit unions
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18d_1" VALUE="Yes" <<SOGS_A18d_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18d_1" VALUE="No" <<SOGS_A18d_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      e. From credit cards or debit cards
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18e_1" VALUE="Yes" <<SOGS_A18e_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18e_1" VALUE="No" <<SOGS_A18e_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      f. From loan sharks
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18f_1" VALUE="Yes" <<SOGS_A18f_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18f_1" VALUE="No" <<SOGS_A18f_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      g. You cashed in stock, bonds, or other securities
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18g_1" VALUE="Yes" <<SOGS_A18g_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18g_1" VALUE="No" <<SOGS_A18g_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      h. You sold personal or family property
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18h_1" VALUE="Yes" <<SOGS_A18h_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18h_1" VALUE="No" <<SOGS_A18h_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      i. You borrowed from your checking (you passed bad checks)
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18i_1" VALUE="Yes" <<SOGS_A18i_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18i_1" VALUE="No" <<SOGS_A18i_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      j. You have (had) a credit line with a bookie
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18j_1" VALUE="Yes" <<SOGS_A18j_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18j_1" VALUE="No" <<SOGS_A18j_1=No>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      k. You have (had) a credit line with a casino
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="SOGS_A18k_1" VALUE="Yes" <<SOGS_A18k_1=Yes>> > Yes
      <INPUT TYPE="radio" NAME="SOGS_A18k_1" VALUE="No" <<SOGS_A18k_1=No>> > No
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="2" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Total Score =
      <INPUT TYPE="TEXT" NAME="SOGS_TotalScore_1" VALUE="<<SOGS_TotalScore_1>>" ONFOCUS="this.blur()" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      0-2 = no problem<BR>
      3-4 = some problem<BR>
      5 or more = probable pathological gambler<BR>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this entire SOGS record?');" NAME="SOGS_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updSOGS(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.SOGS.elements[1].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
