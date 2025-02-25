// function toggleSelectBoxes() {
// 	var performedSelect = document.getElementsByName(
// 		"ClientInterventionsPerformed_Intervention_1"
// 	)[0];
// 	var reasonSelect = document.getElementsByName(
// 		"ClientInterventionsPerformed_Reason_1"
// 	)[0].parentElement.parentElement;
// 	var findingSelect = document.getElementsByName(
// 		"ClientInterventionsPerformed_finding_1"
// 	)[0].parentElement.parentElement;
// 	var followUpSelect = document.getElementsByName(
// 		"ClientInterventionsPerformed_FollowUpPlan_1"
// 	)[0].parentElement.parentElement;
// 	var notPerformedSelect = document.getElementsByName(
// 		"ClientInterventionsPerformed_NotPerformed_1"
// 	)[0].parentElement.parentElement;
// 	var exclusionSelect = document.getElementsByName(
// 		"ClientInterventionsPerformed_ReasonForExclusion_1"
// 	)[0].parentElement.parentElement;
// 	var rejectedSelect = document.getElementsByName(
// 		"ClientInterventionsPerformed_Rejected_1"
// 	)[0].parentElement.parentElement;

// 	// Hide all initially
// 	reasonSelect.style.display = "none";
// 	findingSelect.style.display = "none";
// 	followUpSelect.style.display = "none";
// 	exclusionSelect.style.display = "none";
// 	rejectedSelect.style.display = "none";

// 	// Get the selected value
// 	var selectedValue = performedSelect.value;

// 	// Apply logic to show/hide fields
// 	if (selectedValue === "SNOMEDCT_171207006") {
// 		reasonSelect.style.display = "";
// 		findingSelect.style.display = "";
// 	}

// 	if (selectedValue === "some_value_for_followup") {
// 		followUpSelect.style.display = "";
// 	}
// 	if (selectedValue === "some_value_for_not_performed") {
// 		notPerformedSelect.style.display = "";
// 	}
// 	if (selectedValue === "some_value_for_exclusion") {
// 		exclusionSelect.style.display = "";
// 	}
// 	if (selectedValue === "some_value_for_rejected") {
// 		rejectedSelect.style.display = "";
// 	}
// }

// // Attach event listener on page load
window.onload = function () {
	var performedSelect = document.getElementById("performedSelect");
	trackSelectBoxChange(performedSelect, "SNOMEDCT_171207006", "Reason_TR");
	trackSelectBoxChange(performedSelect, "SNOMEDCT_171207006", "finding_TR");

	performedSelect.addEventListener("change", () => {
		trackSelectBoxChange(performedSelect, "SNOMEDCT_171207006", "Reason_TR");
		trackSelectBoxChange(performedSelect, "SNOMEDCT_171207006", "finding_TR");
	});

	var findingSelect = document.getElementById("finding");

	trackSelectBoxChange(findingSelect, "428181000124104", "FollowUpPlan_TR");

	performedSelect.addEventListener("change", () => {
		trackSelectBoxChange(findingSelect, "428181000124104", "FollowUpPlan_TR");
	});
};

function trackSelectBoxChange(selectedElement, checkValue, targetElementId) {
	var selectedValue = selectedElement.value;

	if (selectedValue == null) return;

	console.log("selectedValue", selectedValue);
	console.log(selectedValue, checkValue, targetElementId);
	console.log(selectedValue, checkValue, targetElementId);

	if (selectedValue === checkValue) {
		console.log("HERE ");

		document.getElementById(targetElementId).style.display = "";
	} else {
		console.log("HERE NO");

		document.getElementById(targetElementId).style.display = "none";
	}
}
