[[myHTML->newPage(%form+ICD-10-CM+++++lhcautocomplete)]]

<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-1.12.4.js" ></SCRIPT>
<SCRIPT TYPE="text/javascript" src="/cgi/lhc/autocomplete-lhc-17.0.3/autocomplete-lhc.min.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  /* ICD-10-CM */
  new Def.Autocompleter.Search(
    'icd10',
    'https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?sf=code,name',
    {tableFormat: true, valueCols: [0], colHeaders: ['Code', 'Name']});
  Def.Autocompleter.Event.observeListSelections('icd10', function(data) {
    onSearchICD10CM(data.item_code);
  });
});

function onSearchICD10CM(code) {
  $.get(`https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?df=code,name&sf=code&terms=${code}`, function(data, status) {
    var result, name;

    [,,,result] = data;
    [,name] = result[0];

    $('#code')[0].value = code;
    $('#name')[0].value = name;
  });
}

function onSubmit(form) {
  var code = $(form).find('#code').val();
  var name = $(form).find('#name').val();

  var alertStr = `Code: ${code}\nName: ${name}`;
  alert(alertStr);
  return false;
}
</SCRIPT>

<FORM NAME="ICD10CM" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>ICD-10-CM Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >ICD-10-CM</TD></TR>
  <TR>
    <TD CLASS="port hdrtxt">
      <TABLE CLASS="home fullsize" >
        <TR >
          <TD CLASS="strcol ">
            ICD-10-CM Search:
            <input type="text" id="icd10" placeholder="Code or name">
          </TD>
        </TR>
        <TR >
          <TD CLASS="strcol " >
            The ICD-10-CM unique disease code containing 3, 4, 5, 6 or 7 digits
            <input type="text" id="code" name="code" value="" placeholder="Code" size="100">
          </TD>
        </TR>
        <TR >
          <TD CLASS="strcol " >
            The long description of the diagnosis string(s)
            <input type="text" id="name" name="name" value="" placeholder="Name" size="100">
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
