new Def.Autocompleter.Search(
	"LHCAutocompletePrimaryReferral",
	"https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search",
	{
		tableFormat: true,
		valueCols: [0, 1],
		colHeaders: ["Name", "NPI", "Type", "Practice Address"],
	}
);

Def.Autocompleter.Event.observeListSelections(
	"LHCAutocompletePrimaryReferral",
	function (data) {
		var code = data.item_code;
		if (data.item_code === null) code = "";
		$("#ClientReferrals_ReferredBy1NPI_1").val(code);
	}
);

new Def.Autocompleter.Search(
	"LHCAutocompleteSecondaryReferral",
	"https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search",
	{
		tableFormat: true,
		valueCols: [0, 1],
		colHeaders: ["Name", "NPI", "Type", "Practice Address"],
	}
);

Def.Autocompleter.Event.observeListSelections(
	"LHCAutocompleteSecondaryReferral",
	function (data) {
		var code = data.item_code;
		if (data.item_code === null) code = "";
		$("#ClientReferrals_ReferredBy2NPI_1").val(code);
	}
);

new Def.Autocompleter.Search(
	"LHCAutocompleteReferringPhysician",
	"https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search",
	{
		tableFormat: true,
		valueCols: [0, 1],
		colHeaders: ["Name", "NPI", "Type", "Practice Address"],
	}
);

Def.Autocompleter.Event.observeListSelections(
	"LHCAutocompleteReferringPhysician",
	function (data) {
		var code = data.item_code;
		if (data.item_code === null) code = "";
		$("#ClientReferrals_RefPhysNPI_1").val(code);
	}
);

document.addEventListener("DOMContentLoaded", function () {
	var savedNPI = document.getElementById(
		"ClientReferrals_ReferredBy1NPI_1"
	).value;

	if (savedNPI) {
		var apiUrl = "https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search";

		// Make GET request with saved NPI as the query
		fetch(
			apiUrl +
				"?terms=" +
				encodeURIComponent(savedNPI) +
				"&ef=Name,NPI,Type,Practice%20Address"
		)
			.then((response) => response.json())
			.then((data) => {
				const results = data[3]; // actual results array

				// Find the result that matches our saved NPI
				const match = results.find((item) => item[1] === savedNPI);

				if (match) {
					const displayText = `${match[0]} (${match[1]})`; // Name (NPI)
					document.getElementById("LHCAutocompletePrimaryReferral").value =
						displayText;
				}
			})
			.catch((error) => {
				console.error("NPI Lookup failed:", error);
			});
	}

	var savedNPI2 = document.getElementById(
		"ClientReferrals_ReferredBy2NPI_1"
	).value;

	if (savedNPI2) {
		var apiUrl = "https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search";

		// Make GET request with saved NPI as the query
		fetch(
			apiUrl +
				"?terms=" +
				encodeURIComponent(savedNPI2) +
				"&ef=Name,NPI,Type,Practice%20Address"
		)
			.then((response) => response.json())
			.then((data) => {
				const results = data[3]; // actual results array

				// Find the result that matches our saved NPI
				const match = results.find((item) => item[1] === savedNPI2);

				if (match) {
					const displayText = `${match[0]} (${match[1]})`; // Name (NPI)
					document.getElementById("LHCAutocompleteSecondaryReferral").value =
						displayText;
				}
			})
			.catch((error) => {
				console.error("NPI Lookup failed:", error);
			});
	}

	var RefPhysNPI = document.getElementById(
		"ClientReferrals_RefPhysNPI_1"
	).value;

	if (RefPhysNPI) {
		var apiUrl = "https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search";

		// Make GET request with saved NPI as the query
		fetch(
			apiUrl +
				"?terms=" +
				encodeURIComponent(RefPhysNPI) +
				"&ef=Name,NPI,Type,Practice%20Address"
		)
			.then((response) => response.json())
			.then((data) => {
				const results = data[3]; // actual results array

				// Find the result that matches our saved NPI
				const match = results.find((item) => item[1] === RefPhysNPI);

				if (match) {
					const displayText = `${match[0]} (${match[1]})`; // Name (NPI)
					document.getElementById("LHCAutocompleteReferringPhysician").value =
						displayText;
				}
			})
			.catch((error) => {
				console.error("NPI Lookup failed:", error);
			});
	}
});
