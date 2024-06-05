// Original JavaScript code by Chirp Internet: www.chirp.com.au
// Please acknowledge use of this code by including this header.

function callAjax(method,value,target,link,pgm)
{
  var req = new AjaxRequest();
  var params = "method=" + method + "&value=" + encodeURIComponent(value) + "&target=" + target + link;
  var script = "validate.pl";
  if (pgm) { script = pgm; }
//alert("url="+params);
  req.loadXMLDoc("/cgi/bin/"+script, params);
//  return true; causes a white screen in IE and FireFox
}
function AjaxRequest()
{
  var req;
  var method = "POST";
  var nocache = false;

  this.loadXMLDoc = function(url, params)
  {
    if(window.XMLHttpRequest) {
      try {
        req = new XMLHttpRequest();
      } catch(e) {
        req = false;
      }
    } else if(window.ActiveXObject) {
      try {
        req = new ActiveXObject("Msxml2.XMLHTTP");
      } catch(e) {
        try {
          req = new ActiveXObject("Microsoft.XMLHTTP");
        } catch(e) {
          req = false;
        }
      }
    }
    if(req) {
      req.onreadystatechange = processReqChange;
      if(nocache) {
        params += (params != '') ? '&' + (new Date()).getTime() : (new Date()).getTime();
      }
      if(method == "POST") {
        req.open("POST", url, true);
        req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        req.send(params);
      } else {
        req.open(method, url + '?' + params, true);
        req.send(null);
      }
      return true;
    }
    return false;
  }

  this.setMethod = function(newmethod) { method = newmethod.toUpperCase(); }
  this.nocache = function() { nocache = true; }

  // define private methods

  var getNodeValue = function(parent, tagName)
  {
    var node = parent.getElementsByTagName(tagName)[0];
    return (node && node.firstChild) ? node.firstChild.nodeValue : '';
  }

  var processReqChange = function() 
  {
    if(req.readyState == 4 && req.status == 200) {
//alert("req ok:"+req.responseText);
      var response  = req.responseXML.documentElement;
      var commands = response.getElementsByTagName('command');
      for(var i=0; i < commands.length; i++) {
        method = commands[i].getAttribute('method');
        switch(method) {

          case 'alert':
            var message = getNodeValue(commands[i], 'message');
            window.alert(message);
            break;

          case 'setvalue':
            var target = getNodeValue(commands[i], 'target');
            var value = getNodeValue(commands[i], 'value');
//alert("req setvalue: target="+target+" and "+value);
            if(target && value != null) {
              document.getElementById(target).value = value;
            }
            break;

          case 'setdefault':
            var target = getNodeValue(commands[i], 'target');
            if(target) {
              document.getElementById(target).value = document.getElementById(target).defaultValue;
            }
            break;

          case 'focus':
            var target = getNodeValue(commands[i], 'target');
            if(target) {
              document.getElementById(target).focus();
            }
            break;

          case 'setcontent':
            var target = getNodeValue(commands[i], 'target');
            var content = getNodeValue(commands[i], 'content');
//alert("req setcontent: target="+target+" and "+content);
            if(target && content != null) {
              document.getElementById(target).innerHTML = content;
            }
            break;

          case 'setscript':
            var target = getNodeValue(commands[i], 'target');
            var content = getNodeValue(commands[i], 'content');
//alert("req setscript: target="+target+" and "+content);
            if(target && content != null) {
              eval(content);
            }
            break;

          case 'setstyle':
            var target = getNodeValue(commands[i], 'target');
            var property = getNodeValue(commands[i], 'property');
            var value = getNodeValue(commands[i], 'value');
            if(target && property && value) {
              document.getElementById(target).style[property] = value;
            }
            break;

          case 'setproperty':
            var target = getNodeValue(commands[i], 'target');
            var property = getNodeValue(commands[i], 'property');
            var value = getNodeValue(commands[i], 'value');
            if(value == "true") value = true;
            if(value == "false") value = false;
            if(target) {
              document.getElementById(target)[property] = value;
            }
            break;

          default:
            window.console.log("Error: unrecognised method '" + method + "' in processReqChange()");
        }
      }
    }
  }
}


document.addEventListener('DOMContentLoaded', ()=>{
  //When The Document is fully Loaded
  
  // Check on the first Load/referesh
  toggleSelectBox();

  const checkboxes = document.querySelectorAll('.IC_CHECKBOX')
  checkboxes.forEach(checkbox =>{
    checkbox.addEventListener('change', toggleSelectBox)
  })
  const selectBox = document.getElementById('Treatment_SCID2_1')
  selectBox.addEventListener('change', ()=>{
    toggleSelectBox('selectChange')
  })

})

const toggleSelectBox = (selectChange) =>{

  const checkboxes = document.querySelectorAll('.IC_CHECKBOX')
  const selectBox = document.getElementById('Treatment_SCID2_1')

  // Check if any checkbox is checked
  const anyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

  if(anyChecked) {
    // If any of the checkbox is checked reset the value of the Secodary service code selectBox
    selectBox.value = ""

    if(selectChange == 'selectChange') {
      // If the call is from the change of Secondary Service Code Select Box
      alert("Cannot Select This Service Code as Interactive Therapy is already checked")
    }
  }
}