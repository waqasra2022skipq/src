[[myHTML->newPage(%form+MCAutocompleteAsync Test+++++lhcautocomplete)]]

<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-1.12.4.js" ></SCRIPT>
<SCRIPT TYPE="text/javascript" src="/cgi/lhc/autocomplete-lhc-17.0.3/autocomplete-lhc.min.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.12.1/jquery-ui.min.js" ></SCRIPT>
<LINK HREF="/src/cgi/css/autocomplete.css?v=202008071708" REL="stylesheet">
<FORM NAME="Intake" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      MCAutocompleteAsync Test
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >JQuery MC Autocomplete</TD>
    <TD CLASS="strcol" >
      <input id="autocomplete"
             type="text"
             size="50"/>
      <input type="hidden" name="test" />
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >LHC Autocomplete</TD>
    <TD CLASS="strcol" >
      <input type="text" id="npi_idv" placeholder="Provider name or NPI">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>

[[myHTML->rightpane(%form+search)]]
<SCRIPT type="text/javascript" src="/src/cgi/js/vMCAutocomplete.js?v=202008241747"></SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/vMCAutocompleteAsyncTest.js?v=202009101505"></SCRIPT>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  mcAutocompleteAsyncTest('autocomplete', 'test', '<<mlt>>');

  new Def.Autocompleter.Search(
  'npi_idv',
  `/cgi/bin/popup_api.pl?method=Physicians&mlt=<<mlt>>`,
  {tableFormat: true, valueCols: [0, 1, 6],
    colHeaders: ['Last Name', 'First Name', 'Address', 'City', 'State', 'Zip', 'NPI']
  });

  Def.Autocompleter.Event.observeListSelections('npi_idv', function(data) {
    var field = $('#npi_idv')[0];
    var autocomp = field.autocomp;
    var itemData = autocomp.getSelectedItemData();
    console.log(field, itemData);
    console.log(data.item_code);
  });
});
</script>
