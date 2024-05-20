var onet_ws = null;
var username = 'okmis';
var columns = null;

onet_ws = new OnetWebService(username);
columns = [
  {name: 'Title', width: '30em'},
];

function onetAutocomplete(autocomplete, target, targetLink) {
  $(`#${autocomplete}`).mcautocomplete({
    showHeader: false,
    columns: columns,
    source: function (request, response) {
      onet_ws.call('online/search', { keyword: request.term }, function(kwresults) {
        if (check_for_error(kwresults)) { return; }
        if (!kwresults.hasOwnProperty('occupation') || !kwresults.occupation.length) {
          console.log('No Result');
        } else {
          var res = kwresults.occupation.map(item => ([item.title, item.code]));
          response(res);
        }
      });
    },
    select:
      function (event, ui) {
        this.value = (ui.item ? ui.item[0]: '');
        document.getElementsByName(target)[0].value = (ui.item ? ui.item[1]: '');
        var link = document.getElementById(targetLink);
        link.setAttribute('href', `https://www.onetonline.org/link/summary/${(ui.item ? ui.item[1]: '')}`);
        return false;
      },
    change:
      function (event, ui) {
        if (this.value === "") {
          document.getElementsByName(target)[0].value = '';
        }
      },
    minLength: 1,
  });
}

function check_for_error(resp) {
  if (resp.hasOwnProperty('error')) {
    return true;
  }
  return false;
}
