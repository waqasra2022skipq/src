[[myHTML->newPage(%form+PHQ 2 LHC Form+++++lhcform)]]

<STYLE>
label {
  width: inherit;
}
</STYLE>
<script TYPE="text/javascript" src="/cgi/lhc/lforms-13.2.0/lforms.min.js"></script>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  $.get('https://clinicaltables.nlm.nih.gov/loinc_form_definitions?loinc_num=55757-9',
    function(data) {
      LForms.Util.addFormToPage(data, 'formContainer');
    }
  );
});

function onSubmit() {
  var formElement = $('#formContainer');
  var userData = LForms.Util.getUserData(formElement);
  alert(userData);

  return false;
}
</SCRIPT>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>LHC Form Test Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >LHC Form Test</TD></TR>
  <TR>
    <TD CLASS="port hdrtxt">
      <DIV id="formContainer" CLASS="home fullsize" >
      </DIV>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return onSubmit();" VALUE="Submit">
    </TD>
  </TR>
</TABLE>
</LOADHIDDEN>

[[myHTML->rightpane(%form+search)]]
