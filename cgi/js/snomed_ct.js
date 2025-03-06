async function fetchSNOMED(term, tag = "finding") {
	const url = `https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN%2FSNOMEDCT-US/descriptions?term=${encodeURIComponent(
		term
	)}&active=true&conceptActive=true&lang=english&semanticTags=${tag}&groupByConcept=true`;
	const response = await fetch(url);
	const data = await response.json();
	return data.items;
}

async function updateDropdown(e, tag, targetElementId) {
	console.log(e.currentTarget);
	let searchTerm = e.currentTarget.value;

	let results = await fetchSNOMED(searchTerm, tag);
	let dropdown = document.getElementById(targetElementId);

	dropdown.innerHTML = "";
	results.forEach((item) => {
		console.log(item);

		let option = document.createElement("option");
		option.value = item.concept.conceptId;
		option.textContent = `${item.term} | ${item.concept.conceptId}`;
		dropdown.appendChild(option);
	});
}

async function fetchSNOMEDByConceptId(conceptId) {
	if (!conceptId || conceptId.trim() === "") return null;

	const url = `https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN%2FSNOMEDCT-US/concepts/${conceptId}`;

	try {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error(`HTTP error! Status: ${response.status}`);
		}
		return await response.json();
	} catch (error) {
		console.error(`Error fetching SNOMED concept for ID ${conceptId}:`, error);
		return null;
	}
}

async function loadAllSavedSNOMED() {
	let selectElements = document.querySelectorAll(".ConceptCodeSearch");

	for (let select of selectElements) {
		let conceptId = select.value.trim(); // Get saved conceptId

		if (conceptId) {
			console.log("conceptId", conceptId);

			let conceptData = await fetchSNOMEDByConceptId(conceptId);

			if (conceptData) {
				select.innerHTML = ""; // Clear existing options

				let option = document.createElement("option");
				option.value = conceptData.conceptId;
				option.textContent = `${conceptData.fsn.term} | ${conceptData.conceptId}`;
				select.appendChild(option);
			} else {
				select.innerHTML = "<option value=''>Invalid SNOMED Code</option>";
			}
		}
	}
}

// Run this function on page load
document.addEventListener("DOMContentLoaded", loadAllSavedSNOMED);
