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

function initAutocompleteNPI(inputId, hiddenId, type, selectedBoxValue) {
	const hiddenEl = document.getElementById(hiddenId);
	if (!hiddenEl) return;

	let condition = "";

	if ("3" === selectedBoxValue) {
		condition =
			"q=addr_practice.state:OK AND (licenses.taxonomy.code:251300000X OR licenses.taxonomy.code:251K00000X)";
	} else if ("41" === selectedBoxValue) {
		condition =
			"q=addr_practice.state:OK AND licenses.taxonomy.code:283Q00000X";
	} else if ("11" === selectedBoxValue || "14" === selectedBoxValue) {
		condition =
			"q=addr_practice.state:OK AND licenses.taxonomy.code:251K00000X";
	} else if ("9" === selectedBoxValue) {
		condition =
			"q=addr_practice.state:OK AND (licenses.taxonomy.code:261QV0200X OR licenses.taxonomy.code:261QM1100X OR licenses.taxonomy.code:261QM1101X OR licenses.taxonomy.code:2865M2000X OR licenses.taxonomy.code:282N00000X)";
	} else if ("10" === selectedBoxValue) {
		condition =
			"q=addr_practice.state:OK AND (licenses.taxonomy.code:282N00000X OR licenses.taxonomy.code:261Q00000X OR licenses.taxonomy.code:261QA1903X OR licenses.taxonomy.code:261QF0400X OR licenses.taxonomy.code:261QP0904X OR licenses.taxonomy.code:251K00000X)";
	} else if (
		"18" === selectedBoxValue ||
		"21" === selectedBoxValue ||
		"37" === selectedBoxValue ||
		"40" === selectedBoxValue ||
		"42" === selectedBoxValue ||
		"43" === selectedBoxValue ||
		"44" === selectedBoxValue ||
		"45" === selectedBoxValue ||
		"46" === selectedBoxValue ||
		"47" === selectedBoxValue
	) {
		condition = "q=addr_practice.state:OK";
	}
	apiUrl =
		type === "NPI-2"
			? `https://clinicaltables.nlm.nih.gov/api/npi_org/v3/search?df=name.full,NPI,provider_type,addr_practice.full,licenses.taxonomy.classification&${condition}`
			: "https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search";

	let colHeaders = ["Name", "NPI", "Type", "Practice Address"];
	if (type === "NPI-2") {
		colHeaders.push("Taxonomy Classification");
	}

	new Def.Autocompleter.Search(inputId, apiUrl, {
		tableFormat: true,
		valueCols: [0, 1],
		colHeaders: colHeaders,
	});

	Def.Autocompleter.Event.observeListSelections(inputId, function (data) {
		document.getElementById(hiddenId).value = data.item_code ?? "";
	});
}

function fillSavedProvider(inputId, hiddenId, type) {
	const hiddenEl = document.getElementById(hiddenId);
	const inputEl = document.getElementById(inputId);
	if (!hiddenEl || !inputEl) return;

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
		initAutocompleteNPI(inputId, hiddenId, type);
		fillSavedProvider(inputId, hiddenId, type);
	});

	// Initialize dynamic fields based on select box
	dynamicReferralFields.forEach(({ inputId, hiddenId, selectId }) => {
		const selectEl = document.getElementById(selectId);
		if (!selectEl) return;

		function updateField() {
			// Auto-fill for specific Referral Types
			const referralTypeMap = {
				1: "Self",
				2: "Significant other",
			};

			const referralText = referralTypeMap[selectEl.value];
			if (referralText) {
				document.getElementById(inputId).value = referralText;
				return;
			} else {
				document.getElementById(inputId).value = "";
			}

			const selectedBoxValue = selectEl.value;

			const type = getNpiTypeFromValue(selectEl.value);
			initAutocompleteNPI(inputId, hiddenId, type, selectedBoxValue);
			fillSavedProvider(inputId, hiddenId, type);
		}

		selectEl.addEventListener("change", updateField);
		updateField(); // run once on load
	});
});

function fillGooglePlaceFromPlaceId($inputEl, placeId) {
	if (!placeId || !window.google || !google.maps || !google.maps.places) {
		console.error("Google Maps API is not loaded or placeId missing");
		return;
	}

	const service = new google.maps.places.PlacesService(
		document.createElement("div")
	);

	service.getDetails({ placeId: placeId }, (place, status) => {
		if (status === google.maps.places.PlacesServiceStatus.OK) {
			const display = place.name
				? `${place.name}, ${place.formatted_address}`
				: place.formatted_address;

			console.log("Google Place Found:", display);
			$inputEl.val(display);
		} else {
			console.error("Failed to retrieve place details:", status);
		}
	});
}

$(document).ready(function () {
	const $select = $("#ClientReferrals_ReferredBy1Type_1");
	const $npiField = $("#LHCAutocompletePrimaryReferral");
	const $googleField = $("#PrimaryReferralMaps");

	const $select2 = $("#ClientReferrals_ReferredBy2Type_1");
	const $npiField2 = $("#LHCAutocompleteSecondaryReferral");
	const $googleField2 = $("#SecondaryReferralMaps");

	function toggleReferralFields() {
		const selectedValue = $select.val();
		let isNonNPI = getNonNPIStatus(selectedValue);

		if (isNonNPI) {
			$googleField.show();
			$npiField.hide();

			// Autofill address from place ID if available
			const placeId = $("#ClientReferrals_ReferredBy1NPI_1").val();
			if (placeId) {
				fillGooglePlaceFromPlaceId($googleField, placeId);
			}
		} else {
			$googleField.hide();
			$npiField.show();
		}

		const selectedValue2 = $select2.val();
		isNonNPI = getNonNPIStatus(selectedValue2);

		if (isNonNPI) {
			$googleField2.show();
			$npiField2.hide();

			const placeId2 = $("#ClientReferrals_ReferredBy2NPI_1").val();
			if (placeId2) {
				fillGooglePlaceFromPlaceId($googleField2, placeId2);
			}
		} else {
			$googleField2.hide();
			$npiField2.show();
		}
	}

	// Run on page load
	toggleReferralFields();

	// Re-run on change
	$select.on("change", toggleReferralFields);
	$select2.on("change", toggleReferralFields);
});

// Utility from you
const getNonNPIStatus = (selectValue) => {
	const nonNPIValues = [
		"4",
		"5",
		"6",
		"12",
		"22",
		"23",
		"25",
		"26",
		"28",
		"31",
		"32",
		"33",
		"34",
		"35",
		"36",
		"38",
		"39",
		"48",
		"49",
		"50",
		"51",
		"52",
		"65",
		"66",
		"67",
		"68",
	];
	return nonNPIValues.includes(selectValue) ? 1 : 0;
};
