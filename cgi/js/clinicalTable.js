// Define field mappings: [autocompleteFieldId, hiddenFieldId]
const referralFields = [
	["LHCAutocompletePrimaryReferral", "ClientReferrals_ReferredBy1NPI_1"],
	["LHCAutocompleteSecondaryReferral", "ClientReferrals_ReferredBy2NPI_1"],
	["LHCAutocompleteReferringPhysician", "ClientReferrals_RefPhysNPI_1"],

	// Client Emergency Page
	["SearchPhysNPI", "ClientEmergency_PhysNPI_1"],
	["SearchHosp", "ClientEmergency_DesigHospNPI_1", "NPI-2"],
	["SearchPharmacy", "ClientEmergency_PharmacyNPI_1", "NPI-2"],
	["SearchDentist", "ClientEmergency_DentistNPI_1"],
	["SearchVision", "ClientEmergency_VisionNPI_1", "NPI-2"],
	["SearchHearing", "ClientEmergency_HearingNPI_1", "NPI-2"],
	// Add more pairs here if needed
];

let apiUrl;

// Initialize autocomplete and set up selection observer
function initAutocomplete(inputId, hiddenId, type) {
	const hiddenEl = document.getElementById(hiddenId);
	if (!hiddenEl) return;

	if ("NPI-2" === type) {
		apiUrl =
			"https://clinicaltables.nlm.nih.gov/api/npi_org/v3/search?q=state=OK";
	} else {
		apiUrl =
			"https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search?q=state=OK";
	}

	new Def.Autocompleter.Search(inputId, apiUrl, {
		tableFormat: true,
		valueCols: [0, 1],
		colHeaders: ["Name", "NPI", "Type", "Practice Address"],
	});

	Def.Autocompleter.Event.observeListSelections(inputId, function (data) {
		let code = data.item_code ?? "";
		document.getElementById(hiddenId).value = code;
	});
}

// Fetch saved NPI and fill display input
function fillSavedProvider(inputId, hiddenId, type) {
	const hiddenEl = document.getElementById(hiddenId);
	if (!hiddenEl) return;

	const savedNPI = document.getElementById(hiddenId)?.value;
	if (!savedNPI) return;

	if ("NPI-2" === type) {
		apiUrl = "https://clinicaltables.nlm.nih.gov/api/npi_org/v3/search";
	} else {
		apiUrl = "https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search";
	}
	console.log(`Filling saved provider for ${savedNPI} and ${apiUrl}`);

	fetch(
		`${apiUrl}?terms=${encodeURIComponent(
			savedNPI
		)}&ef=Name,NPI,Type,Practice%20Address`
	)
		.then((res) => res.json())
		.then((data) => {
			const results = data[3];
			const match = results.find((item) => item[1] === savedNPI);
			if (match) {
				document.getElementById(
					inputId
				).value = `${match[0]} (${match[1]}), ${match[2]}, ${match[3]}`;
			}
		})
		.catch((err) => console.error(`NPI Lookup failed for ${savedNPI}:`, err));
}

// Run everything on DOM ready
document.addEventListener("DOMContentLoaded", function () {
	referralFields.forEach(([inputId, hiddenId, type]) => {
		initAutocomplete(inputId, hiddenId, type);
		fillSavedProvider(inputId, hiddenId, type);
	});
});
