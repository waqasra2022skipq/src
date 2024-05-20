function fillSelect(Field, masterArray, selectArray)
{
  var i, j;
  itemArray = masterArray[Field.value];
//alert("s=" + selectArray + ", i=" + itemArray + ", Field=" + Field.value);
// empty existing items
  for (i = selectArray.options.length; i >= 0; i--)
  for (i = 0; i < selectArray.length; i++) 
  { selectArray.options[i] = null; }
  selectArray.length = 0;
  if (itemArray != null)
  {
// add new items
    j=0;
    for (i = 0; i < itemArray.length; i++) 
    {
//alert("j=" + j + ", i=" + i + ", 0=" + itemArray[i][2] + ", 1=" + itemArray[i][1]);
      selectArray.options[j] = new Option(itemArray[i][2]);
      if (itemArray[i][1] != null)
      { selectArray.options[j].value = itemArray[i][1]; }
      j++;
    }
// select first item (prompt) for sub list
    selectArray.options[0].selected = true;
  }
}
function setSelect(Field, masterArray, selectArray)
{
  var i, j;
  var idx = selectArray.selectedIndex;
  var val = selectArray.options[idx].value;
  var txt = selectArray.options[idx].text;
  itemArray = masterArray[Field.selectedIndex];
  found = 'no';
//alert("s=" + selectArray + ", i=" + itemArray + ", Field=" + Field.selectedIndex);
//alert("selectedIndex=" + selectArray.selectedIndex + ", length=" + selectArray.length + ", value=" + selectArray.options[selectArray.selectedIndex].selected);
// empty existing items
  for (i = selectArray.options.length; i >= 0; i--)
  for (i = 0; i < selectArray.length; i++) 
  { selectArray.options[i] = null; }
//alert("Field=" + Field.selectedIndex + ", idx= " + idx + ", val=" + val + ", txt=" + txt);
  selectArray.length = 0;
  if (itemArray != null)
  {
// add new items
    j=0;
    for (i = 0; i < itemArray.length; i++) 
    {
//alert("j=" + j + ", i=" + i + ", 0=" + itemArray[i][2] + ", 1=" + itemArray[i][1]);
      selectArray.options[j] = new Option(itemArray[i][2]);
      if (itemArray[i][1] != null)
      { selectArray.options[j].value = itemArray[i][1]; }
      // selected item found, make selected in new array.
      if ( itemArray[i][1] == val )
      { selectArray.options[j].selected = true; found = 'yes'; }
      j++;
    }
// selected item found ??
    if ( found == 'no' )
    {
      selectArray.options[j] = new Option(txt);
      selectArray.options[j].value = val;
      selectArray.options[j].selected = true;
    }
  }
}
//  End -->
