// test function using .search method and .add method
function searchSel(val,arr)
{
  var searchvalue = val.value;
  var searcharray = document.getElementById(arr);
alert('val='+val.value+' arr='+arr);
alert('searchvalue='+searchvalue);
  for (var i=0;i<searcharray.options.length-1;i++)
  {
    var st=searcharray.options[i].text;
    if ( st.search(searchvalue)>-1 )
    {
      var temp = searcharray.options[i];
      searcharray.add(temp, searcharray.options[0]);
    }
  }
}
