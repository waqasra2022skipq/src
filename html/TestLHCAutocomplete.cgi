[[myHTML->newPage(%form+Test AutoCompletes+++++lhcautocomplete)]]

<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-1.12.4.js" ></SCRIPT>
<SCRIPT TYPE="text/javascript" src="/cgi/lhc/autocomplete-lhc-17.0.3/autocomplete-lhc.min.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  /* ICD-10-CM */
  new Def.Autocompleter.Search(
    'icd10',
    'https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?sf=code,name',
    {tableFormat: true, valueCols: [0], colHeaders: ['Code', 'Name']});

  /* NPI - individuals */
  new Def.Autocompleter.Search(
    'npi_idv',
    'https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search',
    {tableFormat: true, valueCols: [0, 1],
      colHeaders: ['Name', 'NPI', 'Type', 'Practice Address']});

  /* NPI - organizations */
  new Def.Autocompleter.Search(
    'npi_org',
    'https://clinicaltables.nlm.nih.gov/api/npi_org/v3/search',
    {tableFormat: true, valueCols: [0, 1],
      colHeaders: ['Name', 'NPI', 'Type', 'Practice Address']
    });

  /* RxTerms drug names & strength lists */
  new Def.Autocompleter.Prefetch('drug_strengths', []);
  new Def.Autocompleter.Search('rxterms',
    'https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?ef=STRENGTHS_AND_FORMS');
  Def.Autocompleter.Event.observeListSelections('rxterms', function() {
    var drugField = $('#rxterms')[0];
    var autocomp = drugField.autocomp;
    var strengths =
      autocomp.getSelectedItemData()[0].data['STRENGTHS_AND_FORMS'];
    if (strengths)
      $('#drug_strengths')[0].autocomp.setListAndField(strengths, '');
  })

  /* Major surgeries and implants */
  new Def.Autocompleter.Search('procedure', 'https://clinicaltables.nlm.nih.gov/api/procedures/v3/search');
});

function onSubmit(form) {
  const icd10 = $(form).find('#icd10').val();
  const npi_idv = $(form).find('#npi_idv').val();
  const npi_org = $(form).find('#npi_org').val();
  const rxterms = $(form).find('#rxterms').val();
  const drug_strengths = $(form).find('#drug_strengths').val();
  const procedure = $(form).find('#procedure').val();

  const alertStr = `ICD-10-CM: ${icd10}\nNPI - individuals: ${npi_idv}\nNPI - organizations: ${npi_org}\nRxTerms drug names & strength lists: ${rxterms} ${drug_strengths}\nMajor surgeries and implants: ${procedure}`;
  alert(alertStr);
  return false;
}
</SCRIPT>

<FORM NAME="AutoComplete" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Test Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Test</TD></TR>
  <TR>
    <TD CLASS="port hdrtxt">
      <TABLE CLASS="home fullsize" >
        <TR >
          <TD CLASS="strcol " >
            ICD-10-CM
          </TD>
          <TD CLASS="strcol " >
            <input type="text" id="icd10" placeholder="Code or name">
          </TD>
        </TR>
        <TR >
          <TD CLASS="strcol " >
            NPI - Individuals
          </TD>
          <TD CLASS="strcol " >
            <input type="text" id="npi_idv" placeholder="Provider name or NPI">
          </TD>
        </TR>
        <TR >
          <TD CLASS="strcol " >
            NPI - Organizations
          </TD>
          <TD CLASS="strcol " >
            <input type="text" id="npi_org" placeholder="Provider name or NPI">
          </TD>
        </TR>
        <TR >
          <TD CLASS="strcol " >
            RxTerms drug names & strength lists
          </TD>
          <TD CLASS="strcol " >
            <input type="text" id="rxterms" placeholder="Drug name">
            <input type="text" id="drug_strengths" placeholder="Strength list">
          </TD>
        </TR>
        <TR >
          <TD CLASS="strcol " >
            Major surgeries and implants
          </TD>
          <TD CLASS="strcol " >
            <input type="text" id="procedure" placeholder="Procedure">
          </TD>
        </TR>
      </TABLE>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return onSubmit(this.form);" VALUE="Submit">
    </TD>
  </TR>
</TABLE>
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
