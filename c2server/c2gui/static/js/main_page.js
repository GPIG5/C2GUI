$( document ).ready(function() {
    $(document).on('submit', '#coordForm', function()
    {
        var str = $(this).serialize();

        $.ajax({

        type: 'POST',
        url : 'send_search_coord',
        data : str,
        success : function(data)
            {
             let regions = data.ids;
             for (let region of regions) {
                 $('#region' + region.id).css({'background-color': 'yellow', 'opacity': 0.4});
             }
            }
         });
        return false;
      });

    // Add events to the timeline
});

var colourAllTiles = function() {
    
}
