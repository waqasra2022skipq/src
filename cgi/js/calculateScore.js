/**
 * Dynamic Assessment Score Calculator
 * This script automatically calculates scores for different assessment forms
 * including BIMS, MMSE, and other similar forms with select inputs.
 */

// Main function to set up score calculators for all assessment forms
function setupAssessmentCalculators() {
	// Define form configurations (can be extended for other forms)
	const formConfigs = [
		// BIMS Assessment
		{
			scoreField: "ClientBIMS_Score_1",
			selectPrefix: "ClientBIMS_q",
			specialRules: [
				// If q1 is "no" (value 1), set score to 99
				{
					field: "ClientBIMS_q1_1",
					value: "1",
					action: "setScore",
					scoreValue: "99",
				},
			],
		},

		// MMSE Assessment
		{
			scoreField: "ClientMMSE_Score_1",
			selectPrefix: "ClientMMSE_q",
			// No special rules for MMSE, just sum all question values
		},

		// Add more form configurations here as needed

		{
			scoreField: "ClientDAS_Score_1",
			selectPrefix: "ClientDAS_q",
			// No special rules for MMSE, just sum all question values
		},
		{
			scoreField: "ClientSDS_Score_1",
			selectPrefix: "ClientSDS_q",
			// No special rules for MMSE, just sum all question values
		},
	];

	// Set up calculators for each form configuration
	formConfigs.forEach(setupCalculator);
}

// Function to set up a calculator for a specific form
function setupCalculator(config) {
	// Find the score field for this form
	const scoreField = document.getElementsByName(config.scoreField)[0];
	if (!scoreField) return; // Skip if this form is not present on the page

	// Find all select elements that match this form's prefix
	const selectPrefix = config.selectPrefix;
	const selectElements = Array.from(
		document.querySelectorAll('select[id^="' + selectPrefix + '"]')
	);

	if (selectElements.length === 0) {
		// If no select elements found, check for radio buttons
		const radioElements = Array.from(
			document.querySelectorAll(
				'input[type="radio"][name^="' + selectPrefix + '"]'
			)
		);

		// If radio buttons are found, use them instead
		if (radioElements.length > 0) {
			selectElements.push(...radioElements);
		}
	}

	if (selectElements.length === 0) return; // Skip if no matching select or radio elements

	// Add event listeners to all select elements for this form
	selectElements.forEach((select) => {
		select.addEventListener("change", () =>
			calculateScore(config, selectElements, scoreField)
		);
	});

	// Do an initial calculation
	calculateScore(config, selectElements, scoreField);
}

// Function to calculate the score for a specific form
function calculateScore(config, selectElements, scoreField) {
	// Check if any special rules apply first
	if (config.specialRules) {
		for (const rule of config.specialRules) {
			const ruleElement = document.getElementById(rule.field);
			if (ruleElement && ruleElement.value === rule.value) {
				if (rule.action === "setScore") {
					scoreField.value = rule.scoreValue;
					return; // Exit early, no need to calculate
				}
			}
		}
	}

	// Calculate sum of all selected values
	let totalScore = 0;

	for (const select of selectElements) {
		// Skip fields that shouldn't contribute to the score (like q3b in MMSE)
		if (select.id.includes("q3b")) continue;

		const value = select.value;
		const type = select.type;
		// Handle radio buttons differently
		if (type === "radio") {
			// Check if the radio button is checked
			if (select.checked) {
				totalScore += parseInt(value);
			}
		} else {
			if (value !== null && value !== "") {
				totalScore += parseInt(value);
			}
		}
	}

	// Update the score field
	scoreField.value = totalScore;
}

// Initialize when the DOM is loaded
document.addEventListener("DOMContentLoaded", setupAssessmentCalculators);

// Also try to initialize immediately in case DOM is already loaded
// or the script is added after the page loads
setupAssessmentCalculators();
