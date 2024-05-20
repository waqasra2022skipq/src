var FLDsData = ['SubjectMatterDomain','Role','Setting','TypeOfService','Kind','Descr'];

function eDocsAutocompletes(mlt) {
  FLDsData.forEach(FLD => {
    new Def.Autocompleter.Search(
      `DocumentOntology_${FLD}`,
      `/cgi/bin/popup_api.pl?method=xLDO&FLD=${FLD}&mlt=${mlt}`
    );
  });

  Def.Autocompleter.Event.observeListSelections('DocumentOntology_Descr', data => {
    var code = data.item_code;
    if (data.item_code === null) code = '';
    $('input[name="ClientEDocs_Loinc_1"]').val(code);
    setDocumentOntology(code, mlt);
  });
}

function setDocumentOntology(code, mlt) {
  var flds = ['SubjectMatterDomain','Role','Setting','TypeOfService','Kind'];
  var autocomp;
  if (code === '') {
    flds.forEach(fld => $(`#DocumentOntology_${fld}`).val(''));
  } else {
    $.ajax({
      type: 'POST',
      dataType: 'json',
      url: '/cgi/bin/popup_api.pl',
      data: {
        method: 'getxLDODetail',
        terms: code,
        mlt
      },
      success: function(data){
        flds.forEach(fld => $(`#DocumentOntology_${fld}`).val((data[`${fld}Descr`] === undefined || data[`${fld}Descr`] === null) ? '' : data[`${fld}Descr`]));
      }
    });
  }
}
