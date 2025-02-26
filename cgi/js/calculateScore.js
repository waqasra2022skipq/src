// Function to calculate total score from all select elements
function calculateBIMSScore() {
	// Get all select elements that contribute to the score
	const q2Element = document.getElementById("ClientBIMS_q2_1");
	const q3Element = document.getElementById("ClientBIMS_q3_1");
	const q4Element = document.getElementById("ClientBIMS_q4_1");
	const q5Element = document.getElementById("ClientBIMS_q5_1");
	const q6Element = document.getElementById("ClientBIMS_q6_1");
	const q7Element = document.getElementById("ClientBIMS_q7_1");
	const q8Element = document.getElementById("ClientBIMS_q8_1");

	// Get the select for question 1 (whether BIMS should be conducted)
	const q1Element = document.getElementById("ClientBIMS_q1_1");

	// Get the score input field
	const scoreField = document.getElementsByName("ClientBIMS_Score_1")[0];

	// Check if BIMS should be conducted (q1 value is 0 for "yes")
	if (q1Element && q1Element.value === "1") {
		// If BIMS should not be conducted, set score to 99 (as per instructions)
		scoreField.value = "99";
		return;
	}

	// Calculate the total score by adding the numeric values from each select
	let totalScore = 0;

	if (q2Element) totalScore += parseInt(q2Element.value || 0);
	if (q3Element) totalScore += parseInt(q3Element.value || 0);
	if (q4Element) totalScore += parseInt(q4Element.value || 0);
	if (q5Element) totalScore += parseInt(q5Element.value || 0);
	if (q6Element) totalScore += parseInt(q6Element.value || 0);
	if (q7Element) totalScore += parseInt(q7Element.value || 0);
	if (q8Element) totalScore += parseInt(q8Element.value || 0);

	// Update the score field
	scoreField.value = totalScore;
}

// Function to add event listeners to all select elements
function setupBIMSCalculator() {
	// Get all select elements
	const selectElements = document.querySelectorAll(
		'select[id^="ClientBIMS_q"]'
	);

	// Add change event listener to each select element
	selectElements.forEach((select) => {
		select.addEventListener("change", calculateBIMSScore);
	});

	// Initial calculation in case some values are already set
	calculateBIMSScore();
}

// Run the setup when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", setupBIMSCalculator);

// If the page might be loaded dynamically, also try to set up the calculator immediately
setupBIMSCalculator();
