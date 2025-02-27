<!-- Cloak
function validate(form)
{
  return vEntry("notnull", form.ClientGDSL_TestDate_1,form.ClientGDSL_Score_1);
}
//  DeCloak -->

// Function to calculate the GDS Long Form score
function calculateGDSLScore() {
    let totalScore = 0;
    
    // Define which answers indicate depression symptoms
    const depressiveAnswers = {
        // For these questions, "No" (value 0) indicates depression
        "ClientGDSL_q1_1": "0",
        "ClientGDSL_q5_1": "0",
        "ClientGDSL_q7_1": "0",
        "ClientGDSL_q9_1": "0",
        "ClientGDSL_q15_1": "0",
        "ClientGDSL_q19_1": "0",
        "ClientGDSL_q21_1": "0",
        "ClientGDSL_q27_1": "0",
        "ClientGDSL_q29_1": "0",
        "ClientGDSL_q30_1": "0",
        
        // For these questions, "Yes" (value 1) indicates depression
        "ClientGDSL_q2_1": "1",
        "ClientGDSL_q3_1": "1",
        "ClientGDSL_q4_1": "1",
        "ClientGDSL_q6_1": "1",
        "ClientGDSL_q8_1": "1",
        "ClientGDSL_q10_1": "1",
        "ClientGDSL_q11_1": "1",
        "ClientGDSL_q12_1": "1",
        "ClientGDSL_q13_1": "1",
        "ClientGDSL_q14_1": "1",
        "ClientGDSL_q16_1": "1",
        "ClientGDSL_q17_1": "1",
        "ClientGDSL_q18_1": "1",
        "ClientGDSL_q20_1": "1",
        "ClientGDSL_q22_1": "1",
        "ClientGDSL_q23_1": "1",
        "ClientGDSL_q24_1": "1",
        "ClientGDSL_q25_1": "1",
        "ClientGDSL_q26_1": "1",
        "ClientGDSL_q28_1": "1"
    };
    
    // Loop through all questions and add to score if depressive answer is selected
    for (let question in depressiveAnswers) {
        const radios = document.getElementsByName(question);
        for (let i = 0; i < radios.length; i++) {
            if (radios[i].checked && radios[i].value === depressiveAnswers[question]) {
                totalScore += 1;
            }
        }
    }
    
    // Update the score field
    document.getElementsByName("ClientGDSL_Score_1")[0].value = totalScore;
    
    // Optional: Interpretation of score
    return totalScore;
}

// Attach event listeners to all radio buttons in both forms
function attachRadioListeners() {
    // For Long Form
    for (let i = 1; i <= 30; i++) {
        const longFormRadios = document.getElementsByName(`ClientGDSL_q${i}_1`);
        for (let j = 0; j < longFormRadios.length; j++) {
            if (longFormRadios[j]) {
                longFormRadios[j].addEventListener('change', calculateGDSLScore);
            }
        }
    }
}

// Initialize when the page loads
window.addEventListener('load', function() {
    attachRadioListeners();
    
    // Calculate initial scores (if any options are pre-selected)
    calculateGDSLScore();
});