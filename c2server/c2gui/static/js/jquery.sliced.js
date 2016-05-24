;(function( $, window ) {
    var _defaults = {
        x      : 20, // number of tiles in x axis
        y      : 16, // number of tiles in y axis
    };
    
    $.fn.sliced = function ( options ) {
    
        var o = $.extend( {}, _defaults, options );

        return this.each(function() {
            var $container = $(this); // cache selector for best performance
            var width = $container.width(),
                height = $container.height(),
                $img = $container.find('img'),
                n_tiles = o.x * o.y, // total number of tiles
                tiles = [], $tiles;

            for (var i=0; i<n_tiles; i++) {
                tiles.push('<div class="tile"/>');
            }

            $tiles = $( tiles.join('') );

            // Hide original image and insert tiles in DOM
            $img.hide().after( $tiles );

            // Set background
            $tiles.css({
              width: width / o.x,
              height: height / o.y,
              //backgroundImage: 'url('+ $img.attr('src') + ')'
            });

            // Adjust position and add id to each tile
            var counter = 0;
            $tiles.each(function() {
              counter++;
              $(this).attr('id', 'region' + counter);
              var pos = $(this).position();
              $(this).css('backgroundPosition', -pos.left + 'px ' + -pos.top + 'px');
              //$(this).css('position', 'absolute');
              $(this).css('top', pos.top);
              $(this).css('left', pos.left);
            });

            // Receive the current status of each region
            $.ajax({
                url : 'get_all_regions_status',
                data : {},
                success: function(data) {
                    let regionStatuses = data.statuses;
                    for (let region of regionStatuses) {
                        if (region.status === 'DD') {
                            $('#region' + region.id).css({'background-color': 'yellow', 'opacity': 0.4});
                        } else if (region.status == 'RE') {
                            $('#region' + region.id).css({'background-color': 'red', 'opacity': 0.4});
                        } else if (region.status == 'NRE'){
                            $("#region" + region.id).css({'background-color': 'green', 'opacity': 0.4});
                        } else {
                            $('#region' + region.id).css({'opacity':0});
                        }
                    }
                }
            });

            $tiles.each(function() {
              $(this).css({'position' : 'absolute'});
            });
            $('#map').css({'display' : 'block'});
            
        });

    };
}( jQuery, window ));

$(document).ready(function() {
    $('#mapContainer').sliced({x: 20, y: 16});
});
