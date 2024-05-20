$(document).ready(function () {
    $("#file").change(function() {
        $("#form1").submit();
    });
});

function callback(msg) {
    $("#msg").html(msg);
}
