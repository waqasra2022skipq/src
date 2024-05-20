<!--Cloak
function vEntry(type)
{
  var args = vEntry.arguments;
  for (var i=1; i<args.length; i++)
  {
    var CheckField = args[i];
//alert("type=" + type + " CheckField=" + CheckField + " name=" + CheckField.name + " type=" + CheckField.type);
    if ( type == "notnull" && isEmpty( CheckField ) )
    { 
      var FieldName = CheckField.name;
      if ( !FieldName ) { FieldName = CheckField[0].name; }
      var field = FieldName;
      var NamePat = /^(.+)_(.+)_(\d+)/;
//alert("field = " + field + ", NamePat=" + NamePat + ", FieldName=" + FieldName);
      var matchArray = FieldName.match(NamePat); 
      if ( matchArray ) { var field = matchArray[2]; }
      return vOK(CheckField,"Input is required in " + field + " field."); 
    }
    else if ( type == "setnull" )
    { CheckField.value = ""; }
  }
  return true;
}
// Check for field empty.
function isEmpty( Str )
{
//alert("value=" + Str.value + ", length=" + Str.length + ", type=" + Str.type + ", index=" + Str.selectedIndex + ", idx=" + Str.index);
  if ( Str.type == "text" || Str.type == "textarea" || Str.type == "hidden" || Str.type == "password" )
  { CheckStr = Str; }
  else if ( Str.type == "select-one" || Str.type == "select-multiple" )
  { CheckStr = Str.options[Str.selectedIndex]; }
  else if ( Str.length > 0 )
  { 
//alert("length=" + Str.length);
    for (var i=0; i<Str.length; i++)
    { if ( Str[i].checked ) { return false; } }
    return true;
  }
  else if ( Str.type == "checkbox" || Str.type == "radio" )
  { 
//alert("type=" + Str.type);
    if ( Str.checked ) { return false; }
    return true;
  }
  else
  { return false; }
//alert("Name=" + CheckStr.name + ", value=" + CheckStr.value );
  if( CheckStr.value == "" ) { return true; }
  return false;
}
// Allows for clean return on error.
function vOK(Field,errmsg)
{
  var args = vOK.arguments;
  var confirmError = args[2];

// It is an ERROR if not ok, so return true.
//alert("value=" + Field.value + ", type=" + Field.type + ", index=" + Field.selectedIndex + ", def=" +  + Field.defaultValue);
  if ( confirmError && confirm(errmsg) ) { return true; }
  alert(errmsg);

  if( Field.type == "text" || Field.type == "textarea" || Field.type == "hidden" || Field.type == "password" )
  {
    Field.value = Field.defaultValue;
    Field.focus(); 
    Field.select();
  }
  else if ( Field.type == "select-one" || Field.type == "select-multiple" )
  {
    Field.focus(); 
  }
  else if ( Field.type == "checkbox" || Field.type == "radio" )    
  { 
    Field.checked = Field.defaultChecked;
    Field.focus(); 
  }
  else                                   // ??
  {
    Field[0].focus(); 
  }
  return false;
}
// Keeps a Field from changing.
function vUNDO(Field,errmsg)
{
//alert("value=" + Field.value + ", type=" + Field.type + ", index=" + Field.selectedIndex + ", def=" +  + Field.defaultValue);
  alert(errmsg + "\nField cannot be changed.");
  if( Field.type == "text" || Field.type == "textarea" )
  { Field.value = Field.defaultValue; Field.focus(); Field.select(); }
  else if ( Field.type == "select-one" || Field.type == "select-multiple" )
  { Field.focus(); }
  else if ( Field.type == "checkbox" || Field.type == "radio" )    
  { Field.checked = Field.defaultChecked; Field.focus(); }
  else                                   // ??
  { Field[0].focus(); }
  return false;
}
function vDELETE(delmsg)
{ 
  if ( confirm(delmsg) ) { return true; }
  return false; 
} 
// DeCloak -->
