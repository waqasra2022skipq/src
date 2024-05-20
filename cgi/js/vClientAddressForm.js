function initClientAddressForm(dlgID, linkID, prefix, addrsize) {
  var dialog, form;
  dialog = $( `#${dlgID}` ).dialog({
    autoOpen: false,
    height: 350,
    width: 450,
    modal: true,
    buttons: {
      Update: updateAddress,
      Cancel: function() {
        dialog.dialog( "close" );
      }
    },
    close: function() {}
  });
  
  form = dialog.find( "form" ).on( "submit", function( event ) {
    event.preventDefault();
    updateAddress();
  });
  
  $( `#${linkID}` ).button().on( "click", function() {
    dialog.dialog( "open" );
  });

  function updateAddress() {
    if (addrsize === 1) {
      document.getElementsByName(`${prefix}Addr_1`)[0].value = $(`#${prefix}ClientAddrForm_address`).val();
    }
    if (addrsize === 2) {
      document.getElementsByName(`${prefix}Addr1_1`)[0].value = $(`#${prefix}ClientAddrForm_address1`).val();
      document.getElementsByName(`${prefix}Addr2_1`)[0].value = $(`#${prefix}ClientAddrForm_address2`).val();
    }
    document.getElementsByName(`${prefix}City_1`)[0].value = $(`#${prefix}ClientAddrForm_city`).val();
    if (document.getElementsByName(`${prefix}County_1`).length > 0) {
      document.getElementsByName(`${prefix}County_1`)[0].value = $(`#${prefix}ClientAddrForm_county`).val();
    }
    document.getElementsByName(`${prefix}ST_1`)[0].value = $(`#${prefix}ClientAddrForm_state`).val();
    document.getElementsByName(`${prefix}Zip_1`)[0].value = $(`#${prefix}ClientAddrForm_zip`).val();

    document.getElementsByName(`${prefix}addressVerified_1`)[0].value = 0;
    if (addrsize === 1) {
      document.getElementById(`${prefix}Check_Address_1`).innerHTML = `<A HREF="javascript:callAjax('checkAddress','','','&Tag=Address&Prefix=${prefix}&AddrSize=1&Addr1=${document.getElementsByName(`${prefix}Addr_1`)[0].value}&Addr2=&City=${document.getElementsByName(`${prefix}City_1`)[0].value}&State=${document.getElementsByName(`${prefix}ST_1`)[0].value}&Zip=${document.getElementsByName(`${prefix}Zip_1`)[0].value}','usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>`;
    }
    if (addrsize === 2) {
      document.getElementById(`${prefix}Check_Address_1`).innerHTML = `<A HREF="javascript:callAjax('checkAddress','','','&Tag=Address&Prefix=${prefix}&AddrSize=2&Addr1=${document.getElementsByName(`${prefix}Addr1_1`)[0].value}&Addr2=${document.getElementsByName(`${prefix}Addr2_1`)}&City=${document.getElementsByName(`${prefix}City_1`)[0].value}&State=${document.getElementsByName(`${prefix}ST_1`)[0].value}&Zip=${document.getElementsByName(`${prefix}Zip_1`)[0].value}','usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>`;
    }

    dialog.dialog( "close" );
    return true;
  }
}
