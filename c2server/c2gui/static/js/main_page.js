$( document ).ready(function() {
    $(document).on('submit', '#coordForm', function()
    {
        var str = $(this).serialize();

        $.ajax({

        type: 'POST',
        url : 'send_search_coord',
        data : str,
        success : function(data) {
             let regions = data.ids;
             for (let region of regions) {
                 $('#region' + region.id).css({'background-color': 'yellow', 'opacity': 0.4})
             };
             var new_event = {
                "start_date": {
                    "year": data.timestamp.year,
                    "month": data.timestamp.month,
                    "day": data.timestamp.day,
                    "hour": data.timestamp.hour,
                    "minute": data.timestamp.minute,
                    "second": "",
                    "millisecond": "",
                    "format": ""
                },
                "text": {
                    "headline": data.headline,
                    "text": data.text
                }
            }
            timeline.add(new_event);
            timeline.goToEnd();
            var form = document.getElementById("coordForm");
            form.reset();
           }
         });
        return false;
      });

    $("#mapContainer").mousedown(function (e) {
        $("#big-ghost").remove();
        $(".ghost-select").addClass("ghost-active");
        $(".ghost-select").css({
            'left': e.pageX,
            'top': e.pageY
        });

        initialW = e.pageX;
        initialH = e.pageY;

        $(document).bind("mouseup", selectElements);
        $(document).bind("mousemove", openSelector);
    });

});

var colourAllTiles = function() {
    
}
