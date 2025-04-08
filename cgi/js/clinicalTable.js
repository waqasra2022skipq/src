// Define static field mappings for fields that always use NPI-1 or NPI-2
const referralFields = [
	["LHCAutocompleteReferringPhysician", "ClientReferrals_RefPhysNPI_1"],
	["LHCAutocompleteReferredto", "ClientReferrals_ReferredToNPI_1"],
	["SearchPhysNPI", "ClientEmergency_PhysNPI_1"],
	["SearchHosp", "ClientEmergency_DesigHospNPI_1", "NPI-2"],
	["SearchPharmacy", "ClientEmergency_PharmacyNPI_1", "NPI-2"],
	["SearchDentist", "ClientEmergency_DentistNPI_1"],
	["SearchVision", "ClientEmergency_VisionNPI_1", "NPI-2"],
	["SearchHearing", "ClientEmergency_HearingNPI_1", "NPI-2"],
];

// These two are dynamic based on select field
const dynamicReferralFields = [
	{
		inputId: "LHCAutocompletePrimaryReferral",
		hiddenId: "ClientReferrals_ReferredBy1NPI_1",
		selectId: "ClientReferrals_ReferredBy1Type_1", // example id of select
	},
	{
		inputId: "LHCAutocompleteSecondaryReferral",
		hiddenId: "ClientReferrals_ReferredBy2NPI_1",
		selectId: "ClientReferrals_ReferredBy2Type_1",
	},
];

function getNpiTypeFromValue(selectValue) {
	const npi2Values = [
		"3",
		"8",
		"9",
		"10",
		"11",
		"12",
		"14",
		"18",
		"21",
		"22",
		"23",
		"25",
		"26",
		"28",
		"30",
		"31",
		"32",
		"34",
		"35",
		"36",
		"37",
		"38",
		"39",
		"40",
		"41",
		"42",
		"43",
		"44",
		"45",
		"46",
		"47",
		"48",
		"49",
		"50",
		"51",
		"52",
		"65",
		"66",
		"67",
		"68",
		"91",
		"92",
		"93",
		"94",
		"95",
		"96",
	];
	return npi2Values.includes(selectValue) ? "NPI-2" : "NPI-1";
}

function initAutocomplete(inputId, hiddenId, type) {
	const hiddenEl = document.getElementById(hiddenId);
	if (!hiddenEl) return;

	apiUrl =
		type === "NPI-2"
			? "https://clinicaltables.nlm.nih.gov/api/npi_org/v3/search"
			: "https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search";

	new Def.Autocompleter.Search(inputId, apiUrl, {
		tableFormat: true,
		valueCols: [0, 1],
		colHeaders: ["Name", "NPI", "Type", "Practice Address"],
	});

	Def.Autocompleter.Event.observeListSelections(inputId, function (data) {
		document.getElementById(hiddenId).value = data.item_code ?? "";
	});
}

function fillSavedProvider(inputId, hiddenId, type) {
	const hiddenEl = document.getElementById(hiddenId);
	if (!hiddenEl) return;

	const savedNPI = hiddenEl.value;
	if (!savedNPI) return;

	apiUrl =
		type === "NPI-2"
			? "https://clinicaltables.nlm.nih.gov/api/npi_org/v3/search"
			: "https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search";

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

document.addEventListener("DOMContentLoaded", function () {
	// Initialize static mappings
	referralFields.forEach(([inputId, hiddenId, type]) => {
		initAutocomplete(inputId, hiddenId, type);
		fillSavedProvider(inputId, hiddenId, type);
	});

	// Initialize dynamic fields based on select box
	dynamicReferralFields.forEach(({ inputId, hiddenId, selectId }) => {
		const selectEl = document.getElementById(selectId);
		if (!selectEl) return;

		function updateField() {
			const type = getNpiTypeFromValue(selectEl.value);
			initAutocomplete(inputId, hiddenId, type);
			fillSavedProvider(inputId, hiddenId, type);
		}

		selectEl.addEventListener("change", updateField);
		updateField(); // run once on load
	});
});
