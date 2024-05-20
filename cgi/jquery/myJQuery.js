  $(document).ready(function() {

    $("#dialog").dialog({
      autoOpen: false,
      modal: true
    });

    $('<div id="dialog-confirm" title="Confirmation Required">Please confirm.</div>').dialog({
      autoOpen: false,
      modal: true,
      width: 400
    });

// we use CLASS because ID needs to be unique
    $(".confirmLINK").click(function(e) {
      e.preventDefault();
      var thisbutton = $(this);
      var thispopup = $("#dialog-confirm");
      var targetUrl = thisbutton.attr("href");
      var mytitle = thisbutton.attr("mytitle");
      if ( mytitle ) thispopup.dialog("option","title",mytitle); 
      var mytext = thisbutton.attr("mytext");
      if ( mytext ) thispopup.html(mytext); 
      var mybusy = thisbutton.attr("mybusy");

      thispopup.dialog({
        buttons : {
          "OK" : function() {
            $(thisbutton).prop('disabled', true);
            if ( mybusy ) { thisbutton.html(mybusy); }
            else { thisbutton.html('Processing...'); }
            $(this).dialog("close");
            window.location.href = targetUrl;
          },
          "Cancel" : function() {
            $(this).dialog("close");
          }
        }
      });
      thispopup.dialog("open");
    });

    $( document ).tooltip({
      content: function () {
          return $(this).prop('title');
      },
      position: {
        /* my: "left center", at: "right+10 center", */    /* this one is for right */
        /* my: "center bottom-20", at: "center top", */    /* this one is for top */
        my: "left center", at: "right+10 center",
          using: function( position, feedback ) {
            $( this ).css( position );
            /* $( this ).addClass( feedback.horizontal ); */ /* this goes with right */
            /* $( this ).addClass( feedback.vertical );   */ /* this goes with top */
            $( this ).addClass( feedback.horizontal );
          }
      }
    });

    // for all elements that have this class watch for clicks
    myCheckBoxToggle();
//    $(".js-checkbox-group-toggle").on("click", function(){
//      // create jquery object of what was clicked 
//      var thisbox = $(this);
//      // find the selector target for what was clicked; 
//      var target = $(thisbox).data("group-target");
//      // find all the selector targets */
//      var targets = $(target);
//      // assign all the targets the value of what was clicked 
//      $(targets).prop("checked", $(thisbox).prop("checked"));
//    });

    $( ".dialog-onload" ).hide();

    $( ".accordion" ).accordion({
      collapsible: true,
      active: false,
      heightStyle: "content",
      icons: { "header": "ui-icon-plus", "activeHeader": "ui-icon-minus" }
    });

  }); // end of $(document).ready
//      $(this).prop('disabled', true);
//      $(this).val('Sending...');
//      $('.ui-dialog-titlebar-close').tooltip('disable')  /* get rid of 'x'??

  $.extend({
    alert: function (message, title, h, w) {
      var myh = typeof(h) == 'undefined' ? 250 : h;
      var myw = typeof(w) == 'undefined' ? 500 : w;
      $("<div></div>").dialog( {
        buttons: { "OK": function () { $(this).dialog("close"); } },
        close: function (event, ui) { $(this).remove(); },
        resizable: false,
        title: title,
        height: myh,
        width: myw,
        modal: true
      }).html(message);       // was .text()
    }
  }); // end of extend JQuery

//  $(document).ajaxComplete(function() {
//    myCheckBoxToggle();
//  });

function myCheckBoxToggle()
{
    // for all elements that have this class watch for clicks
    $(".js-checkbox-group-toggle").on("click", function(){
      // create jquery object of what was clicked
      var thisbox = $(this);
      // find the selector target for what was clicked;
      var target = $(thisbox).data("group-target");
      // find all the selector targets */
      var targets = $(target);
      // assign all the targets the value of what was clicked
      $(targets).prop("checked", $(thisbox).prop("checked"));
    });
}
function myAlert(alertmsg,title,h,w)
{
  if ( alertmsg == '' ) { return false; }
  var msg = alertmsg.split("\n").join("<br />");
  $.alert(alertmsg,title,h,w);
}
function myMedAlerts(h,w,title)
{
  /* must reverse the order because the .alert stacks them in reverse order */
  $($(".dialog-onload").get().reverse()).each(function(i,e) {
    var mytitle = typeof(title) == 'undefined' ? $(this).attr("alerttitle") : title;
    var htmlString = $(this).html();
    $.alert(htmlString,mytitle,h,w);
  });
}
