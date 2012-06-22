$(document).ready(function(){
    $("#onlineDocsLink").click(function(e){
        e.preventDefault();
        if($("#dialog-modal").length == 0) {
            $("body").prepend('<div id="dialog-modal" title="Online documentation"></div>');
        }

        var url = $(this).attr("href");
        $("#dialog-modal").load(url);

        $("#dialog-modal").dialog({
            height: 540,
            width: 500,
            modal: true
		});
    });
});
