document.addEventListener("DOMContentLoaded", async function () {
	const performedSelect = document.getElementById("performedSelect");
	const findingSelect = document.getElementById("finding");
	const followUpPlan = document.getElementById("FollowUpPlan");
	const notPerformed = document.getElementById("NotPerformed");
	const reasonForExclusion = document.getElementById("ReasonForExclusion");
	const ReasonForException = document.getElementById("ReasonForException");

	// Set initial values
	await setSelectValue(performedSelect);
	await setSelectValue(findingSelect);
	await setSelectValue(followUpPlan);
	await setSelectValue(notPerformed);
	await setSelectValue(reasonForExclusion);
	await setSelectValue(ReasonForException);

	// Attach event listeners
	performedSelect.addEventListener("change", () => {
		toggleVisibility(performedSelect, "SNOMEDCT_171207006", [
			"Reason_TR",
			"finding_TR",
		]);
	});

	findingSelect.addEventListener("change", () => {
		toggleVisibility(findingSelect, "428181000124104", ["FollowUpPlan_TR"]);
	});

	notPerformed.addEventListener("change", () => {
		toggleVisibility(notPerformed, "454841000124105", [
			"ReasonForExclusion_TR",
			"ReasonForException_TR",
		]);
		toggleVisibility(notPerformed, "", ["ReasonForRejected_TR"]);
	});

	// Initial visibility check
	toggleVisibility(performedSelect, "SNOMEDCT_171207006", [
		"Reason_TR",
		"finding_TR",
	]);
	toggleVisibility(findingSelect, "428181000124104", ["FollowUpPlan_TR"]);
	toggleVisibility(notPerformed, "454841000124105", [
		"ReasonForExclusion_TR",
		"ReasonForException_TR",
	]);
	toggleVisibility(notPerformed, "", ["ReasonForRejected_TR"]);
});

/**
 * Set the <select> value based on its data-value attribute
 * @param {HTMLSelectElement} selectBox
 * @returns {Promise<void>}
 */
async function setSelectValue(selectBox) {
	if (!selectBox) return;
	const dataValue = selectBox.getAttribute("data-value");
	if (dataValue) {
		selectBox.value = dataValue;
	}
}

/**
 * Show or hide elements based on a selected value
 * @param {HTMLSelectElement} selectBox
 * @param {String} expectedValue
 * @param {Array<String>} targetElementIds
 */
function toggleVisibility(selectBox, expectedValue, targetElementIds) {
	if (!selectBox) return;
	const isMatch = selectBox.value === expectedValue;
	targetElementIds.forEach((id) => {
		const element = document.getElementById(id);
		if (element) {
			element.style.display = isMatch ? "" : "none";
		}
	});
}
