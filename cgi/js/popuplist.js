// both these functions use document.FORM...
// keep the FORM name the same because it is hardcoded.
function allergylist(selectobj) {
	// values at load of page
	this.idx = selectobj.selectedIndex;
	this.value = selectobj.options[this.idx].value;
	this.text = selectobj.options[this.idx].text;
	//alert("idx="+this.idx+" value="+this.value+" text="+this.text);
	this.set = function (pattern) {
		var req = new AjaxRequest();
		var script = "/cgi/bin/popup.pl";
		var params =
			"method=pAllergy&pattern=" +
			encodeURIComponent(pattern) +
			"&value=" +
			document.ClientAllergies.ClientAllergies_AID_1.value;
		//alert("url="+script+" params="+params+" value="+this.value);
		req.loadXMLDoc(script, params);
	};
}
function problemlist(selectobj) {
	// values at load of page
	this.idx = selectobj.selectedIndex;
	this.value = selectobj.options[this.idx].value;
	this.text = selectobj.options[this.idx].text;
	//alert("idx="+this.idx+" value="+this.value+" text="+this.text);
	this.set = function (pattern) {
		var req = new AjaxRequest();
		var script = "/cgi/bin/popup.pl";
		var params =
			"method=sProblem&pattern=" +
			encodeURIComponent(pattern) +
			"&value=" +
			document.ClientProblems.ICD10Search.value +
			"&FINDING=" +
			document.ClientProblems.LIMSEL[0].checked +
			"&CORE=" +
			document.ClientProblems.LIMSEL[1].checked +
			"&DISORDER=" +
			document.ClientProblems.LIMSEL[2].checked;
		//alert("url="+script+" params="+params+" value="+this.value);
		req.loadXMLDoc(script, params);
	};
}
