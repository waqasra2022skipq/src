function mcAutocompleteAsyncTest(autocomplete, target, mlt) {
  // Sets up the multicolumn autocomplete widget.
  $(`#${autocomplete}`).mcautocomplete({
    // These next two options are what this plugin adds to the autocomplete widget.
    showHeader: true,

    columns: [
      {name: 'ProvLastName', width: '8em'},
      {name: 'ProvFirstName', width: '8em'},
      {name: 'Addr1', width: '10em'},
      {name: 'City', minWidth: '8em'},
      {name: 'ST', width: '8em'},
      {name: 'Zip', width: '8em'},
      {name: 'NPI', width: '10em'},
    ],
    source: function (request, response) {
      $.ajax({
        type: 'GET',
        dataType: 'json',
        url: `/cgi/bin/popup_api.pl?method=Physicians&terms=${request.term}&mlt=${mlt}`,
        success: function(data){
          response(data);
      	}
      });
    },

    // Event handler for when a list item is selected.
    select: 
      function (event, ui) {
        this.value = (ui.item ? Object.values(ui.item).join(' | ') : '');
        document.getElementsByName(target)[0].value = Object.values(ui.item)[6];
        return false;
      },

    change:
      function (event, ui) {
        if (ui.item === null) {
          document.getElementsByName(target)[0].value = this.value;
        }
      },

    minLength: 1
  });
}
