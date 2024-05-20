function initForm(prefix, addrSize) {
 //alert(prefix + ' ' + addrSize);
  if (addrSize === 2) {
    document.getElementsByName(`${prefix}Addr1_1`)[0].value = '';
    document.getElementsByName(`${prefix}Addr2_1`)[0].value = '';
  }
  if (addrSize === 1) {
    document.getElementsByName(`${prefix}Addr_1`)[0].value = '';
  }
  document.getElementsByName(`${prefix}City_1`)[0].value = '';
  if (document.getElementsByName(`${prefix}County_1`).length > 0) {
    document.getElementsByName(`${prefix}County_1`)[0].value = '';
  }
  document.getElementsByName(`${prefix}ST_1`)[0].value = '';
  document.getElementsByName(`${prefix}Zip_1`)[0].value = '';
  document.getElementsByName(`${prefix}addressVerified_1`)[0].value = 0;
}

function isAlphanumeric(inputtxt) { 
  var letters = /^[0-9a-zA-Z\-_\s]+$/;
 ///[^a-z\d\-_\s]+$/i
 ///^[0-9a-zA-Z\-_\s]+$/;
 //alert(letters.test(inputtxt));
  if (letters.test(inputtxt)) {
    //alert('accepted');
    return true;
  } else {
    alert('Please input alphanumeric characters only');
    return false;
  }
}

function fillInAddress(autocomplete, prefix, addrSize=2) {
  var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_2: 'short_name',
    administrative_area_level_1: 'short_name',
    country: 'long_name',
    postal_code: 'short_name'
  };

  initForm(prefix, addrSize);
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();
  var addressData = {};
  for (var attr in componentForm) {
    addressData[attr] = '';
  }

  // Get each component of the address from the place details,
  // and then fill-in the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
      var val = place.address_components[i][componentForm[addressType]];
      addressData[addressType] = val;
    }
  }

  if (addrSize === 2) {
    document.getElementsByName(`${prefix}Addr1_1`)[0].value = `${addressData['street_number']} ${addressData['route']}`;
    document.getElementsByName(`${prefix}Addr2_1`)[0].value = '';
  }
  if (addrSize === 1) {
    document.getElementsByName(`${prefix}Addr_1`)[0].value = `${addressData['street_number']} ${addressData['route']}`;
  }
  
  document.getElementsByName(`${prefix}City_1`)[0].value = addressData['locality'];
  if (document.getElementsByName(`${prefix}County_1`).length > 0) {
    if (RegExp(/\w+\s(County)/).test(addressData['administrative_area_level_2'])) {
      document.getElementsByName(`${prefix}County_1`)[0].value = addressData['administrative_area_level_2'].split(' ')[0];
    }
  }
  document.getElementsByName(`${prefix}ST_1`)[0].value = addressData['administrative_area_level_1'];
  document.getElementsByName(`${prefix}Zip_1`)[0].value = addressData['postal_code'];

  document.getElementById(`${prefix}Check_Address_1`).innerHTML
    = `<A HREF="javascript:callAjax('checkAddress','','','&Tag=Address&Prefix=${prefix}&AddrSize=${addrSize}&Addr1=${addressData['street_number']} ${addressData['route']}&Addr2=&City=${addressData['locality']}&State=${addressData['administrative_area_level_1']}&Zip=${addressData['postal_code']}','usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>`;
}

function onChangeAddr2(prefix, addr2) {
  
if (!isAlphanumeric(addr2)){
	return false;
}
  document.getElementById(`${prefix}Check_Address_1`).innerHTML
    = `<A HREF="javascript:callAjax('checkAddress','','','&Tag=Address&Prefix=${prefix}&AddrSize=2&Addr1=${document.getElementsByName(`${prefix}Addr1_1`)[0].value}&Addr2=${addr2}&City=${document.getElementsByName(`${prefix}City_1`)[0].value}&State=${document.getElementsByName(`${prefix}ST_1`)[0].value}&Zip=${document.getElementsByName(`${prefix}Zip_1`)[0].value}','usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>`;
}
