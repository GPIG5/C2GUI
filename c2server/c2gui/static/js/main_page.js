$( document ).ready(function() {
    var min_lat = 53.929472;
    var max_lat = 54.007111;
    var min_lon = -1.165084;
    var max_lon = -1.004663;
    var lat_range = max_lat - min_lat;
    var lon_range = max_lon - min_lon;
    var map_left_x = $("#map").offset().left;
    var map_right_x = map_left_x + $("#map").width();
    var map_top_y = $("#map").offset().top;
    var map_bottom_y = map_top_y + $("#map").height();
    var map_left_offset = $("#map").offset().left;
    var map_width = $("#map").width();
    var map_height = $("#map").height();

    $('#map').on('dragstart', function(event) {event.preventDefault(); });
    $('#map').on('mousedown', function(event) {event.preventDefault(); });

    $(document).on('submit', '#coordForm', function(e)
    {
        e.preventDefault();
        $(".ghost-select").removeClass("ghost-active");
        $(".ghost-select").width(0).height(0);
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
             };
             timeline.add(new_event);
             timeline.goToEnd();
          }
        });
        
        var form = document.getElementById("coordForm");
        form.reset();
      });

    $("#mapContainer").mousedown(function (e) {
        //$(".ghost-select").removeClass("ghost-active");
        $(".ghost-select").width(0).height(0);
        $(".ghost-select").addClass("ghost-active");
        $(".ghost-select").css({
            'left': e.pageX - $("#map").offset().left,
            'top': e.pageY - $("#map").offset().top
        });

        initialW = e.pageX;
        initialH = e.pageY;

        $(document).bind("mouseup", selectElements);
        $(document).bind("mousemove", openSelector);
    });

    function selectElements(e) {
        $(document).unbind("mousemove", openSelector);
        $(document).unbind("mouseup", selectElements);
        var $selection = $(".ghost-select");
        var height = $selection.height();
        var width = $selection.width();
        var left_x = $selection.offset().left;
        var right_x = left_x + $selection.width();
        var top_y = $selection.offset().top;
        var bottom_y = top_y + $selection.height();
        var bottomleftlat = max_lat - lat_range*((bottom_y - map_top_y)/map_height);
        var bottomleftlon = min_lon + lon_range*((left_x - map_left_x)/map_width);
        var toprightlat = max_lat - lat_range*((top_y - map_top_y)/map_height);
        var toprightlon = min_lon + lon_range*((right_x - map_left_x)/map_width);
        
        document.getElementById("bottomleftlat").value = bottomleftlat;
        document.getElementById("bottomleftlon").value = bottomleftlon;
        document.getElementById("toprightlat").value = toprightlat;
        document.getElementById("toprightlon").value = toprightlon;

        /*var maxX = 0;
        var minX = 5000;
        var maxY = 0;
        var minY = 5000;
        var elementArr = new Array();
        $(".tile").each(function () {
            var aElem = $(".ghost-select");
            var bElem = $(this);
            var result = doObjectsCollide(aElem, bElem);

            if (result == true) {
                var aElemPos = bElem.offset();
                var bElemPos = bElem.offset();
                var aW = bElem.width();
                var aH = bElem.height();
                var bW = bElem.width();
                var bH = bElem.height();

                var coords = checkMaxMinPos(aElemPos, bElemPos, aW, aH, bW, bH, maxX, minX, maxY, minY);
                maxX = coords.maxX;
                minX = coords.minX;
                maxY = coords.maxY;
                minY = coords.minY;
                var parent = bElem.parent();

               if (bElem.css("left") === "auto" && bElem.css("top") === "auto") {
                   bElem.css({
                       'left': parent.css('left'),
                       'top': parent.css('top')
                   });
               }


            }
        });*/
        //$(".ghost-select").removeClass("ghost-active");
        //$(".ghost-select").width(0).height(0);
    }

    function doObjectsCollide(a, b) {
        var aTop = a.offset().top;
        var aLeft = a.offset().left;
        var bTop = b.offset().top;
        var bLeft = b.offset().left;

        return !(
            ((aTop + a.height()) < (bTop)) ||
            (aTop > (bTop + b.height())) ||
            ((aLeft + a.width()) < bLeft) ||
            (aLeft > (bLeft + b.width()))
        );
    }

    function checkMaxMinPos(a, b, aW, aH, bW, bH, maxX, minX, maxY, minY) {
        'use strict';

        if (a.left < b.left) {
            if (a.left < minX) {
                minX = a.left;
            }
        } else {
            if (b.left < minX) {
                minX = b.left;
            }
        }

        if (a.left + aW > b.left + bW) {
            if (a.left > maxX) {
                maxX = a.left + aW;
            }
        } else {
            if (b.left + bW > maxX) {
                maxX = b.left + bW;
            }
        }

        if (a.top < b.top) {
            if (a.top < minY) {
                minY = a.top;
            }
        } else {
            if (b.top < minY) {
                minY = b.top;
            }
        }

        if (a.top + aH > b.top + bH) {
            if (a.top > maxY) {
                maxY = a.top + aH;
            }
        } else {
            if (b.top + bH > maxY) {
                maxY = b.top + bH;
            }
        }

        return {
            'maxX': maxX,
            'minX': minX,
            'maxY': maxY,
            'minY': minY
        };
    }

    function openSelector(e) {
        var w = Math.abs(initialW - e.pageX);
        var h = Math.abs(initialH - e.pageY);

        $(".ghost-select").css({
            'width': w,
            'height': h
        });
        if (e.pageX <= initialW && e.pageY >= initialH) {
            $(".ghost-select").css({
                'left': e.pageX - $("#map").offset().left
            });
        } else if (e.pageY <= initialH && e.pageX >= initialW) {
            $(".ghost-select").css({
                'top': e.pageY - $("#map").offset().top
            });
        } else if (e.pageY < initialH && e.pageX < initialW) {
            $(".ghost-select").css({
                "left": e.pageX - $("#map").offset().left,
                "top": e.pageY - $("#map").offset().top
            });
        }
    }

});

var colourAllTiles = function() {
    
}
