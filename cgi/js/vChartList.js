function vDenyNote(form,transid,trid,clientid,contdate,scnum,code)
{
//  alert("CALL DenyNote! transid=" + transid + ", trid=" + trid + ", clientid=" + clientid + ", contdate=" + contdate + ", scnum=" + scnum + ", code=" + code);
  if ( code == 'BI' )
  {
    if ( confirm("Are you sure you want to Deny this InProcess note transaction?") )
    { 
      var reason = prompt('Please enter the Reference/Reason...(30 chars max)','Enter 30 characters max');
      if ( reason == null || reason == 'Enter 30 characters max' || reason == '' )
      { alert('Please enter a Reference/Reason'); }
      else
      {
        var formname = form.name;
        form.DENYNOTE_TRANSID.value = transid;
        form.DENYNOTE_TRID.value = trid;
        form.DENYNOTE_CLIENTID.value = clientid;
        form.DENYNOTE_CONTDATE.value = contdate;
        form.DENYNOTE_SCNUM.value = scnum;
        form.DENYNOTE_REASON.value = reason;
        return true;
      }
    }
  }
  else
  { alert("Cannot Deny! code = " + code + " (code mismatch!)"); }
  return false;
}
function vAdjust(form,transid,trid,amt)
{
  if ( amt == 0 )
  {
    if ( confirm("Are you sure you want to reverse transaction " + transid + " for TrID " + trid + " to be $" + amt + "?") )
    {
      form.ADJUST_TRANSID.value = transid;
      form.ADJUST_TRID.value = trid;
      form.ADJUST_AMT.value = amt;
      return true;
    }
  }
  else
  {
    if ( confirm("Are you sure you want to reverse transaction " + transid + " for TrID " + trid + " in the amount of $" + amt + "?") )
    { 
      var reason = prompt('Please enter the Note/Reason...(30 chars max)','Enter 30 characters max');
      if ( reason == null || reason == 'Enter 30 characters max' || reason == '' )
      { alert('Please enter a Note/Reason'); }
      else
      {
        form.ADJUST_TRANSID.value = transid;
        form.ADJUST_TRID.value = trid;
        form.ADJUST_AMT.value = amt;
        form.ADJUST_REASON.value = reason;
        return true;
      }
    }
  }
  return false;
}
function vWriteOff(form,trid,amt)
{
  if ( confirm("Are you sure you want to WriteOff remaining balance in the amount of $" + amt + "?") )
  { 
    var reason = prompt('Please enter the Note/Reason...(30 chars max)','Enter 30 characters max');
    if ( reason == null || reason == 'Enter 30 characters max' || reason == '' )
    { alert('Please enter a Note/Reason'); }
    else
    {
      var formname = form.name;
      form.WRITEOFF_TRID.value = trid;
      form.WRITEOFF_AMT.value = amt;
      form.WRITEOFF_REASON.value = reason;
      return true;
    }
  }
  return false;
}
function vUnReview(form,trid,revstatus)
{
//  alert("CALL UnReview! RevStatus = " + revstatus + " (RevStatus mismatch!)");
  if ( revstatus == 3 )
  {
    if ( confirm("Are you sure you want to UnReview and REMOVE the Manager Approval?") )
    { 
      var reason = prompt('Please enter the Note/Reason why...(30 chars max)','Enter 30 characters max');
      if ( reason == null || reason == 'Enter 30 characters max' || reason == '' )
      { alert('Please enter a Note/Reason'); }
      else
      {
        var formname = form.name;
        form.UNREVIEW_TRID.value = trid;
        form.UNREVIEW_REASON.value = reason;
        return true;
      }
    }
  }
  else
  { alert("Cannot UnReview! RevStatus = " + revstatus + " (RevStatus mismatch!)"); }
  return false;
}

function getConsent(message) {
  const consent = confirm(message)

  if(consent) {
    setTimeout(()=>{
      location.reload()
    }, 5000)
    return true
  }
  return false
}