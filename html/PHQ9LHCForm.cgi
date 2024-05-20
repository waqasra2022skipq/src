[[myHTML->newPage(%form+PHQ 9 LHC Form+++++lhcform)]]

<STYLE>
label {
  width: inherit;
}
</STYLE>

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
<script src="https://clinicaltables.nlm.nih.gov/lforms-versions/24.1.4/lforms.min.js"></script>
<script src="https://clinicaltables.nlm.nih.gov/lforms-versions/24.1.4/fhir/R4/lformsFHIR.min.js"></script>
<script src="https://clinicaltables.nlm.nih.gov/lforms-versions/24.1.4/fhir/STU3/lformsFHIR.min.js"></script>
<SCRIPT LANGUAGE="JavaScript" >
var FHIRURL = 'https://okmis.info/hapi-fhir-jpaserver/baseStu3';
var patientID = 1;
var qID = 1166;
var qrID = 1164;

$(document).ready(function() {

  $.getJSON(`${FHIRURL}/Questionnaire/${qID}`, function(fhirQ) {
    // Convert FHIR Questionnaire to LForms format
    var lformsQ = LForms.FHIR.STU3.SDC.convertQuestionnaireToLForms(fhirQ, 'STU3');

    $.get(`${FHIRURL}/QuestionnaireResponse/${qrID}`, function (qr) {
      // Merge QuestoinnaireResponse
      var formWithUserData = LForms.Util.mergeFHIRDataIntoLForms("QuestionnaireResponse", qr, lformsQ, "STU3")
      
      // Add the form to the page
      LForms.Util.addFormToPage(formWithUserData, formContainer);
    });
  });

});

function onSubmit() {
  var qr = LForms.Util.getFormFHIRData('QuestionnaireResponse', 'STU3');
  qr = {
    ...qr,
    subject: {
      reference: `Patient/${patientID}`
    },
    questionnaire: {
      reference: `Questionnaire/${qID}`
    },
    id: qrID
  };
  
  $.ajax({
    url: `${FHIRURL}/QuestionnaireResponse/${qrID}`,
    method: 'PUT',
    contentType: 'application/json',
    data: JSON.stringify(qr),
    success: function (result) {
      alert('Successfully updated');
    }
  });

  return false;
}
</SCRIPT>
