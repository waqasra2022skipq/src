<!-- Cloak

// Checks if time is in HH:MM:SS AM/PM format.
// The seconds and AM/PM are optional.
function vTime(timeStr) 
{
  var args = vTime.arguments;
  var emptyok = args[1];
  var milTime = args[2];
  var Min = args[3];
  var Max = args[4];

  if ( timeStr.value == "" )
  { if ( emptyok ) { return true; }
    else { return vOK(timeStr,"Time Required!"); }
  }

//alert('timeStr=' + timeStr.value + ' Min=' + Min + ' Max=' + Max);
  var timePat = /^(\d{1,2})(\:)?(\d{2})?(\:)?(\d{2})?(\s?(A|a|AM|am|P|p|PM|pm|))?$/;
  var matchArray = timeStr.value.match(timePat);
  if (matchArray == null) 
  { return vOK(timeStr,"Time is not in a valid format.\n(hh:mm[:ss] [am|pm])"); }
  var hour = matchArray[1];
  var minute = matchArray[3];
  var second = matchArray[5];
  var ampm = matchArray[7];
//alert('h=' + hour + ', m=' + minute + ', s=' + second + ', ampm=' + ampm);

  if (minute==undefined) { minute = '0'; }
  if (second==undefined) { second = '0'; }
  if (minute=="") { minute = '0'; }
  if (second=="") { second = '0'; }
  if (ampm == "a" || ampm == "am" || ampm == "A" || ampm == "AM")
  { ampm = "AM"; }
  else if (ampm == "p" || ampm == "pm" || ampm == "P" || ampm == "PM")
  { ampm = "PM"; }
  else { ampm = ""; }

//alert('h=' + hour + ', m=' + minute + ', s=' + second + ', ampm=' + ampm);
  if (hour < 0  || hour > 23)
  { return vOK(timeStr,"Hour must be between 1 and 12.\n(or 0 and 23 for military time)"); }
  if (hour <= 12 && ampm == "")
  { return vOK(timeStr,"You must specify AM or PM."); }
  if  (hour > 12 && ampm != "" ) 
  { return vOK(timeStr,"You can't specify AM or PM for military time."); }
  if (minute<0 || minute > 59) 
  { return vOK (timeStr,"Minute must be between 0 and 59."); }
  if (second && (second < 0 || second > 59)) 
  { return vOK (timeStr,"Second must be between 0 and 59."); }
  if ( hour.length < 2 ) { hour = '0' + hour; }
  if ( minute.length < 2 ) { minute = '0' + minute; }
  if ( second > 0 )
  { if ( second.length < 2 ) { second = '0' + second; }
    timeStr.value = hour + ":" + minute + ":" + second + ampm; 
  }
  else
  { timeStr.value = hour + ":" + minute + ampm; }

// set Military time field if requested.
//alert('milTime=' + milTime);
//alert('h=' + hour + ', m=' + minute + ', s=' + second + ', ampm=' + ampm);
  var MilitaryTime;
  if ( second.length < 2 ) { second = '0' + second; }
  if ( ampm == "AM" )
  { if ( hour == 12 ) { hour = '00'; }
    MilitaryTime = hour + ":" + minute + ":" + second; 
  }
  else if ( ampm == "PM" && hour < 12 )
  { var mhour = "" + (parseInt(hour,10) + 12);
//alert('test: h=' + hour + ', mh=' + mhour + ', m=' + minute + ', s=' + second + ', ampm=' + ampm);
    MilitaryTime = mhour + ":" + minute + ":" + second;
  }
  else
  { MilitaryTime = hour + ":" + minute + ":" + second; }

  if ( milTime )
  { milTime.value = MilitaryTime; }
//alert('MilitaryTime=' + MilitaryTime + ', milTime=' + milTime.value);

//alert('timeStr=' + timeStr.value + ' Min=' + Min + ' Max=' + Max);
  if ( Min )
  { 
//alert('Min, MilitaryTime=' + MilitaryTime + ' Min=' + Min + ' Max=' + Max);
    if ( Min > MilitaryTime )
    { if ( !vOK(timeStr,"Time is BEFORE normal business hours (" + Min + ").\nPlease confirm using " + timeStr.value + "?",1) )
      { return false; }
    }
  }
  if ( Max )
  {
//alert('Max, MilitaryTime=' + MilitaryTime + ' Min=' + Min + ' Max=' + Max);
    if ( MilitaryTime > Max)
    { if ( !vOK(timeStr,"Time is AFTER normal business hours (" + Max + ").\nPlease confirm using " + timeStr.value + "?",1) )
      { return false; }
    }
  }
  return true;
}

// DeCloak -->
