function deleteFile(filepath, dbname, rowId) {
    console.log(filepath)
      fetch(`/cgi/bin/deleteFile.pl?filepath=${filepath}&dbname=${dbname}`, {
          method: 'GET',
      })
      .then((response)=>{
          return response.json()
      })
      .then(data => {
          if (data.success) {
              removeTableRow(rowId)
              alert(data.success);
          } else if (data.error) {
              removeTableRow(rowId)
              alert(data.error);
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
}
const removeTableRow = (rowId)=>{
    const rowToRemove = document.getElementById(rowId);
    const tableBody = rowToRemove.parentNode;
    tableBody.removeChild(rowToRemove);
}

jQuery(document).ready(()=>{
    jQuery("#Rollup_Button").on("click", (e)=>{
        var result = window.confirm("Warning !!!! Hit okay and wait for screen to refersh");
        if(!result) {
            e.preventDefault()
            return false
        }

        Swal.fire({
            title: "Rollup Started",
            html: "Please Wait for the Roll up to complete",
            allowOutsideClick: () => false,
            didOpen: () => {
                Swal.showLoading();
            }
        })
    })
})
