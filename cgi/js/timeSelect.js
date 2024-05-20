<!--Cloak
function timeSelect(form, masterArray, selectArray)
{
  var i, j;
//alert("m=" + masterArray);
//alert("s=" + selectArray);
// empty existing items
  var currentOpt = selectArray.options[selectArray.selectedIndex].value;
  if (masterArray != null)
  {
    preSet(form, masterArray);
// delete in outgoing array
    for (i = 0; i < selectArray.length; i++) 
    { selectArray.options[i] = null; }
    selectArray.length = 0;
// add new items
    selectArray.options[0] = new Option('unselected');
    selectArray.options[0].value = '';
    j=1;
    for (i = 1; i < masterArray.length; i++) 
    {
//alert("j=" + j + ", i=" + i + ", 0=" + masterArray[i][0] + ", 1=" + masterArray[i][1]);
      if ( masterArray[i][0] == 0 )
      {
        selectArray.options[j] = new Option(masterArray[i][2]);
        if (masterArray[i][1] != null)
        { selectArray.options[j].value = masterArray[i][1]; }
        if ( currentOpt == masterArray[i][1] ) { selectArray.options[j].selected = true; }
        j++;
      }
    }
var s=selectArray.selectedIndex;
alert("s=" + s + ", " + selectArray.selectedIndex);
    if ( selectArray.selectedIndex == 0 ) { selectArray.options[0].selected = true; }
  }
}
function preSet(form, setArray)
{
var t=9;
var t1 = t/2;
var t2 = parseInt(t/2,10);
var t3 = parseFloat(t/2,10) - parseInt(t/2,10);
alert("preSet: t1=" + t1 + " t2=" + t2 + " t3=" + t3);
  var flag = false;
  var start = 0;
  var Fields = setArray[0];
  for (var f=0; f<Fields.length; f++)
  {
    var loc = isSet(form,Fields[f],setArray);
alert("f=" + f + ", Field=" + Fields[f] + ", loc=" + loc + ", flag=" + flag + ", start=" + start);
    if ( loc && flag && start < setArray.length && loc > 0 )
    {
alert("preSet: start=" + start + " loc=" + loc);
      for (i = start + 1; i <= loc - 1; i++) { setArray[i][0] = 1; }
      flag = 0;
    }
    else if ( loc ) { start = loc; flag = true; }
    else { flag = false; }
  }
}
function isSet(form, Field, checkArray)
{
  var obj = eval("form." + Field);
  var val = obj.options[obj.selectedIndex].value;
alert("isSet: Field=" + Field + ", obj=" + obj.selectedIndex + ", val=" + val);
  if ( val != "" )
  {
    for (a = 1; a < checkArray.length; a++) 
    {
alert("isSet: a=" + a + ", checkArray=" + checkArray[a][1]);
      if ( val == checkArray[a][1] ) { return a; }
    }
  }
  return false;
}
//  End -->
