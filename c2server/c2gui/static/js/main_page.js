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
             // Add a new event to the timeline
             divHtml = "<div class='cd-timeline-block'>" +
                 "<div class='cd-timeline-img cd-movie'><img src='/static/img/cd-icon-picture.svg' alt='Picture'></div>" +
                 "<div class='cd-timeline-content'><h2>" + data.text + "</h2><span class='cd-date'>" + data.timestamp + "</span></div></div>";
             $("#cd-timeline").append(divHtml);
             $timelineBlock = $(".cd-timeline-block").last();
             $('#timeline-wrapper').animate({
                 scrollTop: $timelineBlock.offset().top
             });
            }
         });
        return false;
      });

});

var colourAllTiles = function() {
    
}
