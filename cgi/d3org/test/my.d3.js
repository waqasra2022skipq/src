    function getStyle(el, cssprop)
    {
      if (el.currentStyle) //IE
        return el.currentStyle[cssprop]
      else if (document.defaultView && document.defaultView.getComputedStyle) //Firefox
        return document.defaultView.getComputedStyle(el, "")[cssprop]
      else //try and get inline style
        return el.style[cssprop]
    }

    var theEl=document.getElementById("chart1");
    var ml = getStyle(theEl,'margin-left');
    var mr = getStyle(theEl,'margin-right');
    var mt = getStyle(theEl,'margin-top');
    var mb = getStyle(theEl,'margin-bottom');
    var h = getStyle(theEl,'height');
    var w = getStyle(theEl,'width');
    w = w.substr(0, w.length - 2);
    ml = ml.substr(0, ml.length - 2);
    mr = mr.substr(0, mr.length - 2);
    var cw = w - ml - mr;
    h = h.substr(0, h.length - 2);
    mt = mt.substr(0, mt.length - 2);
    mb = mb.substr(0, mb.length - 2);
    var ch = h - mt - mb;
//alert("1: h="+h+", ch="+ch+", w="+w);
