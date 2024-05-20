function createOpioidRegistryDownloadLink(getLinkBtnId, Client_ClientID, mlt) {
  $(`#${getLinkBtnId}`).click(function() {
    $(`#${getLinkBtnId}`).prop('disabled', true);
    $.post("/cgi/bin/pmp_api.pl", {
      "method": "GetOpioidRegistry",
      "Client_ClientID": Client_ClientID,
      "mlt": mlt
    }, function(data, status) {
      $(`#${getLinkBtnId}`).prop('disabled', false);
      const { patient_link, report_link } = data;
      if (report_link == "") {
        alert("Invalid request");
        return;
      }

      $(`#${getLinkBtnId}`).nextAll().remove();

      $.get(report_link, function(data) {
        const html = new Blob([data], { type: 'text/html' });
        const downloadLink = downloadBlob(html, "opioid_registry.html");
        downloadLink.title = "Download opioid registry";
        $(downloadLink).css("margin-left", "4px");
        $(downloadLink).html("<INPUT TYPE='button' VALUE='Download'>");
        $(`#${getLinkBtnId}`).parent().append(downloadLink);
      });
    });
  });
}

function downloadBlob(blob, filename) {
  // Create an object URL for the blob object
  const url = URL.createObjectURL(blob);

  // Create a new anchor element
  const a = document.createElement('a');

  // Set the href and download attributes for the anchor element
  // You can optionally set other attributes like `title`, etc
  // Especially, if the anchor element will be attached to the DOM
  a.href = url;
  a.download = filename || 'download';

  return a;
}