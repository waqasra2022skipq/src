
function serverREQ(str,fld,path)
{ 
  var XMLHttpRequestObject = false; 

  if (window.XMLHttpRequest) 
  { XMLHttpRequestObject = new XMLHttpRequest(); }
  else if (window.ActiveXObject)
  { XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP"); }

  if(XMLHttpRequestObject)
  {
    var url=path+"&q="+str+"&sid="+Math.random();
//alert("url=" + url + ", fld=" + fld);
    XMLHttpRequestObject.open("GET",url,true); 

    XMLHttpRequestObject.onreadystatechange = function() 
    { 
      if (XMLHttpRequestObject.readyState == 4 && XMLHttpRequestObject.status == 200)
      { 
        document.getElementById(fld).innerHTML = XMLHttpRequestObject.responseText; 
        delete XMLHttpRequestObject;
        XMLHttpRequestObject = null;
      } 
    } 
    XMLHttpRequestObject.send(null); 
  }
  else
  { alert ("Your browser does not support XMLHTTP!"); return; }
}

//str=field on form we are verifing
//path  =function to run to verify field
//fid   =field id=object to display new field in
//a1id  =argument 1 id, a value on the html form, passed to function
//a2id  =argument 2 id, a value on the html form, passed to function
function createFLD(str,path,fid,a1id,a2id)
{ 
  var XMLHttpRequestObject = false; 

  if (window.XMLHttpRequest) 
  { XMLHttpRequestObject = new XMLHttpRequest(); }
  else if (window.ActiveXObject)
  { XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP"); }

  if(XMLHttpRequestObject)
  {
    var a1=''; var a2='';
    if ( a1id ) { a1=document.getElementById(a1id).value; }
    if ( a2id ) { a2=document.getElementById(a2id).value; }
//alert("a1=" + a1 + "=, a2=" + a2 + "=");
    var url=path+"&s="+str.value+"&a1="+a1+"&a2="+a2+"&sid="+Math.random();
//alert("url=" + url + ", fid=" + fid);
    XMLHttpRequestObject.open("GET",url,true); 

    XMLHttpRequestObject.onreadystatechange = function() 
    { 
      if (XMLHttpRequestObject.readyState == 4 && XMLHttpRequestObject.status == 200)
      { 
        var resp = XMLHttpRequestObject.responseText; 
//alert("resp=" + resp + "=");
        document.getElementById(fid).innerHTML = resp;
        delete XMLHttpRequestObject;
        XMLHttpRequestObject = null;
      } 
    } 
    XMLHttpRequestObject.send(null); 
  }
  else
  { alert ("Your browser does not support XMLHTTP!"); return; }
}

//str=field on form we are verifing
//path  =function to run to verify field
//eid   =error id=object to display error message in
//a1id  =argument 1 id, a value on the html form, passed to function
//a2id  =argument 2 id, a value on the html form, passed to function
//rid   =reset id=object to reset if failed test (if not str)
//defidx=index of default value IF str/rid is a SELECT 
//         otherwise '0', use unselected as '0' is good.
function verifyFLD(str,path,eid,a1id,a2id,rid,defidx)
{ 
  var XMLHttpRequestObject = false; 

  if (window.XMLHttpRequest) 
  { XMLHttpRequestObject = new XMLHttpRequest(); }
  else if (window.ActiveXObject)
  { XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP"); }

  if(XMLHttpRequestObject)
  {
    var obj = str;
    var idx = 0;
    if ( defidx ) { idx=defidx; }
//alert("idx=" + idx + ", obj.value=" + obj.value + "=, rid=" + rid);
    var a1=''; var a2=''; var m='';
    if ( a1id ) { a1=document.getElementById(a1id).value; }
    if ( a2id ) { a2=document.getElementById(a2id).value; }
    if ( rid ) { m=document.getElementById(rid); obj = m; }
//alert("a1=" + a1 + "=, a2=" + a2 + "=");
//alert("rid=" + rid + "=");
    var url=path+"&s="+str.value+"&a1="+a1+"&a2="+a2+"&sid="+Math.random();
//alert("url=" + url + ", eid=" + eid);
    XMLHttpRequestObject.open("GET",url,true); 

    XMLHttpRequestObject.onreadystatechange = function() 
    { 
      if (XMLHttpRequestObject.readyState == 4 && XMLHttpRequestObject.status == 200)
      { 
        var resp = XMLHttpRequestObject.responseText; 
//alert("resp=" + resp + "=");
        document.getElementById(eid).innerHTML = resp;
        if ( resp != '' )                            // resp contains error
        {
//alert("obj.value=" + obj.value + "=");
          if( obj.type == "text"   || obj.type == "textarea" 
           || obj.type == "hidden" || obj.type == "password" )
          { obj.value = obj.defaultValue; obj.focus(); obj.select(); }
          else if ( obj.type == "select-one" || obj.type == "select-multiple" )
          { obj.selectedIndex = idx; obj.focus(); }
          else if ( obj.type == "checkbox" )    
          { obj.checked = obj.defaultChecked; obj.focus(); }
          else { obj[0].focus(); }                  // radio button?
        }
        delete XMLHttpRequestObject;
        XMLHttpRequestObject = null;
      } 
    } 
    XMLHttpRequestObject.send(null); 
  }
  else
  { alert ("Your browser does not support XMLHTTP!"); return; }
}
