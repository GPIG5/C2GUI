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

    (function periodic_worker() {
      $.ajax({
        url: 'retrieve_new_data',
        success: function(data) {
          let new_events = data.new_events;
          console.log(new_events);
          let drones = data.drones;
          for (let drone of drones) {
              calculateDroneImageCoordinates(drone);
          }

          for (let new_event of new_events) {
              event_date = new Date(new_event.timestamp);
              var ev = {
                  "start_date": {
                      "year": event_date.getUTCFullYear(),
                      "month": event_date.getUTCMonth() + 1,
                      "day": event_date.getUTCDate(),
                      "hour": event_date.getUTCHours(),
                      "minute": event_date.getUTCMinutes(),
                      "second": event_date.getUTCSeconds(),
                      "millisecond": "",
                      "format": ""
                  },
                  "text": {
                      "headline": new_event.headline,
                      "text": new_event.text
                  }
              };
              timeline.add(ev);
              console.log(new_event);
              if (new_event.pinor) {
                  if (new_event.pinor.region.status === "RE"){
                      $("#region" + new_event.pinor.region.id).css({"background-color": "red", "opacity": 0.4});
                  } else if (new_event.pinor.region.status === "DD"){
                      $("#region" + new_event.pinor.region.id).css({"background-color": "yellow", "opacity": 0.4});
                  } else if (new_event.pinor.region.status === "NRE"){
                      $("#region" + new_event.pinor.region.id).css({"background-color": "green", "opacity": 0.4});
                  }
              }
              if (new_event.regions.length > 0) {
                  if (new_event.event_type === "CS"){
                      for (let region of new_event.regions) {
                          $("#region" + region.id).css({"background-color": "green", "opacity": 0.4});
                      }
                  }
              }
          }
          if (new_events.length > 0){
              timeline.goToEnd();
          }
        },
        complete: function() {
          // Schedule the next request when the current one is complete
          setTimeout(periodic_worker, 15000);    
        }
      });
    })();

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
                    "second": data.timestamp.second,
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

    function calculateDroneImageCoordinates(drone) {
        left_offset = (drone.lon - min_lon)/(max_lon - min_lon)*map_width;
        top_offset = (max_lat - drone.lat)/(max_lat - min_lat)*map_height;
        if ($("#drone" + drone.uid).length == 0) {
            $("#drone-container").append("<img class='drone' id='drone" + drone.uid + "' src='/static/img/drone.png'>");
        }
        $("#drone" + drone.uid).css({"left": left_offset, "top": top_offset});
    }

});

var colourAllTiles = function() {
    
}
