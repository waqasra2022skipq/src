<!-- Cloak
function validate(form)
{
    return vEntry("notnull", form.ClientGDSS_TestDate_1,form.ClientGDSS_Score_1);
}
//  DeCloak -->

// Function to calculate the GDS Short Form score
function calculateGDSSScore() {
    let totalScore = 0;
    
    // Define which answers indicate depression symptoms
    // For some questions, "Yes" (value 1) indicates depression
    // For others, "No" (value 0) indicates depression
    const depressiveAnswers = {
        // For questions 1, 5, 7, 11, 13: "No" indicates depression
        "ClientGDSS_q1_1": "0",
        "ClientGDSS_q5_1": "0",
        "ClientGDSS_q7_1": "0",
        "ClientGDSS_q11_1": "0",
        "ClientGDSS_q13_1": "0",
        
        // For questions 2, 3, 4, 6, 8, 9, 10, 12, 14, 15: "Yes" indicates depression
        "ClientGDSS_q2_1": "1",
        "ClientGDSS_q3_1": "1",
        "ClientGDSS_q4_1": "1",
        "ClientGDSS_q6_1": "1",
        "ClientGDSS_q8_1": "1",
        "ClientGDSS_q9_1": "1",
        "ClientGDSS_q10_1": "1",
        "ClientGDSS_q12_1": "1",
        "ClientGDSS_q14_1": "1",
        "ClientGDSS_q15_1": "1"
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
    document.getElementsByName("ClientGDSS_Score_1")[0].value = totalScore;
    
    // Optional: Interpretation of score
    return totalScore;
}


// Attach event listeners to all radio buttons in both forms
function attachRadioListeners() {
    // For Short Form
    for (let i = 1; i <= 15; i++) {
        const shortFormRadios = document.getElementsByName(`ClientGDSS_q${i}_1`);
        for (let j = 0; j < shortFormRadios.length; j++) {
            shortFormRadios[j].addEventListener('change', calculateGDSSScore);
        }
    }
}

// Initialize when the page loads
window.addEventListener('load', function() {
    attachRadioListeners();
    
    // Calculate initial scores (if any options are pre-selected)
    calculateGDSSScore();
});
