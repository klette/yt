$(function(){

    var status_bar = $('div[id^=id_]').first();
    var id = status_bar.attr('id').substr(3);
    setInterval(function(){
        $.get("/report/" + id, function(data){
            if (data != "Done"){
                status_bar.show().html(data);
            } else {
                status_bar.html("<a href=\"/media/audio/" + id + ".mp3\">Download MP3 file</a>");
            }
        });
    },
    500);

});
