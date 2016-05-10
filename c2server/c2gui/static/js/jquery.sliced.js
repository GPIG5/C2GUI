;(function( $, window ) {
    var _defaults = {
        x      : 10, // number of tiles in x axis
        y      : 10, // number of tiles in y axis
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
              backgroundImage: 'url('+ $img.attr('src') + ')'
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

            $tiles.each(function() {
              $(this).css('position', 'absolute');
            });
            
        });

    };
}( jQuery, window ));
