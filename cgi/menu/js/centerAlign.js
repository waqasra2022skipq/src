function centerAlignMenu() {
    var menuWrapper = document.getElementById("menuWrapper");
    if (menuWrapper === null) return;
    var menu = getChild(menuWrapper);
    var wrapper2 = document.createElement("div");
    wrapper2.style.margin = "0 auto";
    wrapper2.style.width = menu.offsetWidth + 2 + "px";
    menuWrapper.appendChild(wrapper2);
    wrapper2.appendChild(menu);
}

function getChild(n)
{
    var o = n.firstChild;
    while (o && o.nodeType != 1) {
        o = o.nextSibling;
    }
    return o;
}

var addToPageLoadEvent = function (el, eventName, eventHandler) {
    if (el.addEventListener)
        el.addEventListener(eventName, eventHandler, false);
    else if (el.attachEvent) //IE
        el.attachEvent('on' + eventName, eventHandler);
};

addToPageLoadEvent(window, "load", centerAlignMenu);
