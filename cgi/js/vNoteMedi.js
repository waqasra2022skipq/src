<!-- Cloak
function validate(form)
{
//alert('in validate: form='+form);
  if ( !vEntry("notnull",form.Treatment_ClinicID_1
                        ,form.Treatment_SCID_1
                        ,form.Treatment_POS_1
                        ,form.Treatment_ContLogDate_1
                        ,form.Treatment_ContLogBegTime_1
                        ,form.Treatment_ContLogEndTime_1
                        ,form.NoteProblems
                        ,form.NoteTrPlanPG
                        ,form.ProgNotes_Methods_1
                        ,form.ProgNotes_Progress_1
                        ,form.ProgNotes_ProgEvidence_1
              )
     ) { return false; }
  var CurType = form.CurType.value;
//alert('in validate: CurType='+CurType);
  if ( CurType == "GC" || CurType == "GR" )
  { if ( !vEntry("notnull",form.ProgNotes_GrpSize_1) ) { return false; } }
  else if ( CurType == "CI" )
  { 
    if ( !vEntry("notnull",form.ProgNotes_CrisisText_1
                          ,form.ProgNotes_GAFCurrent_1
                          ,form.ProgNotes_GAFRecent_1
                )
       ) { return false; }
  }
  return true;
}
//  DeCloak -->

jQuery(document).ready(() => {
	// function addIntervention() {
	// 	const $wrapper = $("#interventions_wrapper");
	// 	const $lastEntry = $wrapper.find(".intervention-entry").last();
	// 	const $newEntry = $lastEntry.clone();
	// 	$wrapper.append($newEntry);
	// }
	// $("#addIntervention").on("click", function (e) {
	// 	e.preventDefault();
	// 	addIntervention();
	// 	$("#interventions_wrapper")
	// 		.find(".intervention-entry")
	// 		.last()
	// 		.find("input")
	// 		.first()
	// 		.focus();
	// });
});


document.addEventListener("DOMContentLoaded", function () {
    function applySkipLogic(entry) {
        const performedSelect = entry.querySelector(".performedSelect");
        const findingSelect = entry.querySelector(".findingSelect");
        const followUpPlan = entry.querySelector(".FollowUpPlan");
        const notPerformed = entry.querySelector(".NotPerformed");
        const reasonForExclusion = entry.querySelector(".ReasonForExclusion");
        const reasonForException = entry.querySelector(".ReasonForException");

        setSelectValue(performedSelect);
        setSelectValue(findingSelect);
        setSelectValue(followUpPlan);
        setSelectValue(notPerformed);
        setSelectValue(reasonForExclusion);
        setSelectValue(reasonForException);

        // Attach listeners
        if (performedSelect) {
            performedSelect.addEventListener("change", () => {
                toggleVisibility(entry, performedSelect, "SNOMEDCT_171207006", [
                    ".Reason_TR",
                    ".Finding_TR",
                ]);
            });
        }

        if (findingSelect) {
            findingSelect.addEventListener("change", () => {
                toggleVisibility(entry, findingSelect, "428181000124104", [
                    ".FollowUpPlan_TR",
                ]);
            });
        }

        console.log(notPerformed)


        if (notPerformed) {
                console.log("here")

            notPerformed.addEventListener("change", () => {
                console.log("change")

                toggleVisibility(entry, notPerformed, "454841000124105", [
                    ".ReasonForExclusion_TR",
                    ".ReasonForException_TR",
                ]);
                toggleVisibility(entry, notPerformed, "", [
                    ".ReasonForRejected_TR",
                ]);
            });
        }

        // Initial display update
        toggleVisibility(entry, performedSelect, "SNOMEDCT_171207006", [
            ".Reason_TR",
            ".Finding_TR",
        ]);
        toggleVisibility(entry, findingSelect, "428181000124104", [
            ".FollowUpPlan_TR",
        ]);
        toggleVisibility(entry, notPerformed, "454841000124105", [
            ".ReasonForExclusion_TR",
            ".ReasonForException_TR",
        ]);
        toggleVisibility(entry, notPerformed, "", [".ReasonForRejected_TR"]);
    }

    function setSelectValue(selectBox) {
        if (!selectBox) return;
        const dataValue = selectBox.getAttribute("data-value");
        if (dataValue) {
            selectBox.value = dataValue;
        }
    }

    function toggleVisibility(entry, selectBox, expectedValue, selectors) {
        if (!selectBox) return;
        console.log(selectBox, expectedValue, selectors)
        const isMatch = selectBox.value === expectedValue;
        selectors.forEach((selector) => {
            const el = entry.querySelector(selector);
            if (el) {
                el.style.display = isMatch ? "" : "none";
            }
        });
    }

    // Initial logic apply
    const allEntries = document.querySelectorAll(".intervention-entry");
    allEntries.forEach(applySkipLogic);

    // When adding a new entry dynamically
    $("#addIntervention").on("click", function (e) {
        e.preventDefault();
        const $wrapper = $("#interventions_wrapper");
        const $lastEntry = $wrapper.find(".intervention-entry").last();
        const $newEntry = $lastEntry.clone();

        // Clear the values in the clone
        $newEntry.find("input, select").each(function () {
            const el = $(this);
            el.val("");
            el.attr("data-value", "");
        });

        $wrapper.append($newEntry);
        applySkipLogic($newEntry[0]); // Apply skip logic on the new section
        $newEntry.find("input").first().focus();
    });
});