<!-- Cloak
function vAddNew(form,ok,no)
{ 
  if ( no )
  {
    alert(ok + no + ". Another cannot be done at this time. Click the View/Edit button to complete.");
    return false;
  }
  if ( ok )
  {
    if ( confirm("Are you sure you want to " + ok + "? If so, then click the OK button below. If NOT, and you wish to modify the current information, click the Cancel button below and then click the View/Edit button next to the section you want to View or Edit.") ) 
    { 
      form.submit(); 
    } 
    else { return false; }
    return true;
  }
} 
//  DeCloak -->
