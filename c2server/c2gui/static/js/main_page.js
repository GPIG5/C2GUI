var dateTimeOptions = {
  weekday: "long", year: "numeric", month: "short",
  day: "numeric", hour: "2-digit", minute: "2-digit"
};
var drawingManager;
var all_overlays = new Object;
var selectedShape;
var map;
var infowindow = null;
var markers = [];
var lastMarker = 0;
var regHeight = 0;
var regWidth = 0;
var SHAPE_Z_INDEX = 100;

function deleteSelectedShape() {
  if (selectedShape) {
    selectedShape.setMap(null);
    selectedShape = null;
  }
}

function initialize() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 53.960667, lng: -1.083338},
    mapTypeId: google.maps.MapTypeId.SATELLITE,
    zoomControl: true,
    streetViewControl: false
  });

  infowindow = new google.maps.InfoWindow({
    content: "holding..."
  });

  drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.RECTANGLE,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.RECTANGLE
      ]
    }
  });
  drawingManager.setMap(map);

  $.ajax({
      url: 'get_all_regions_status',
      data: {},
      success: function(data) {
        let regionStatuses = data.statuses;
        regHeight = parseFloat(data.height);
        regWidth = parseFloat(data.width);
        let pinors = data.pinors;
        for (let region of regionStatuses) {
          var regionOptions = {"strokeWeight": 0, "fillOpacity": 0};
          if (region.status === 'DD') {
            regionOptions = {"fillColor": "yellow", "strokeWeight": 0};
          } else if (region.status === 'NRE') {
            regionOptions = {"fillColor": "#ff00ff", "strokeWeight": 0};
          } else if (region.status === 'RE') {
            regionOptions = {"fillColor": "blue", "strokeWeight": 0};
          }
          if (region.status !== 'NE') {
            var rectangle = new google.maps.Rectangle({
              map: map,
              bounds: {
               north: region.lat + regHeight,
               south: region.lat,
               east: region.lon + regWidth,
               west: region.lon
              },
              clickable: false,
              zIndex: SHAPE_Z_INDEX,
              fillOpacity: 0.3
            });
            rectangle.setOptions(regionOptions);
            all_overlays[region.id] = rectangle;
          }
        }
        for (let pinor of pinors) {
          var imageStr = "";
          if (pinor.images.length > 0) {
            imageStr = '<br><img src="/c2gui' + pinor.images[0].photo + '">';
          }
          var timeString = new Date(pinor.timestamp).toLocaleTimeString("en-uk", dateTimeOptions);
          var contentString = '<div class="content">' +
            'Detected on ' + timeString +
            ' at the location (' + pinor.lat + ' N, ' +
            (-pinor.lon) + ' W)' +
            imageStr +
            '</div>';

          var marker = new google.maps.Marker({
            position: {lat: parseFloat(pinor.lat), lng: parseFloat(pinor.lon)},
            map: map,
            title: 'Person in Need',
            clickable: true,
            html: contentString
          });
          if (pinor.origin === 'O') {
            marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
          }
          markers.push(marker);        
        }
        lastMarker = markers.length;

        for (var i = 0; i < markers.length; i++) {
          var marker = markers[i];
          google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(this.html);
            infowindow.open(map, this);
          });
        }
      }
    });

  google.maps.event.addListener(drawingManager, 'rectanglecomplete', function(rectangle) {
                document.getElementById("bottomleftlat").value = rectangle.bounds.H.H;
                document.getElementById("bottomleftlon").value = rectangle.bounds.j.j;
                document.getElementById("toprightlat").value = rectangle.bounds.H.j;
                document.getElementById("toprightlon").value = rectangle.bounds.j.H;
                drawingManager.setDrawingMode(null);
                selectedShape = rectangle;
              });

  google.maps.event.addListener(map, 'click', deleteSelectedShape);
  google.maps.event.addListener(drawingManager, "drawingmode_changed", function() {
    if (drawingManager.getDrawingMode() != null) {
      deleteSelectedShape();
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

$( document ).ready(function() {
    (function periodic_worker() {
      $.ajax({
        url: 'retrieve_new_data',
        success: function(data) {
          let new_events = data.new_events;
          let regHeight = data.height;
          let regWidth = data.width;

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
              if (new_event.pinor) {
                  var pinor = new_event.pinor;
                  var imageStr = "";
                  if (pinor.hasOwnProperty('images') && pinor.images.length > 0) {
                    imageStr = '<br><img src="/c2gui' + pinor.images[0].photo + '">';
                  }
                  var timeString = new Date(pinor.timestamp).toLocaleTimeString("en-uk", dateTimeOptions);
                  var contentString = '<div class="content">' +
                    'Detected on ' + timeString +
                    ' at the location (' + pinor.lat + ' N, ' +
                    (-pinor.lon) + ' W).' +
                    imageStr +
                    '</div>';
                  var marker = new google.maps.Marker({
                      position: {lat: parseFloat(new_event.pinor.lat), lng: parseFloat(new_event.pinor.lon)},
                      title: 'Person in Need',
                      clickable: true,
                      animation: google.maps.Animation.DROP,
                      html: contentString
                  });
                  if (pinor.origin === "O") {
                    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
                  }
                  marker.setMap(map);
                  markers.push(marker);
              }
              if (new_event.regions.length > 0) {
                  for (let region of new_event.regions) {
                      var rectangle;
                      if (!all_overlays.hasOwnProperty(region.id)) {
                        rectangle = new google.maps.Rectangle({
                          map: map,
                          bounds: {
                            north: parseFloat(region.lat) + regHeight,
                            south: parseFloat(region.lat),
                            east: parseFloat(region.lon) + regWidth,
                            west: parseFloat(region.lon)
                          },
                          clickable: false,
                          zIndex: SHAPE_Z_INDEX
                        });
                        all_overlays[region.id] = rectangle;
                      } else {
                        rectangle = all_overlays[region.id];
                      }
                      if (region.status === 'NRE') {
                        rectangle.setOptions({"fillColor": "#ff00ff", "strokeWeight": 0});
                      } else if (region.status === 'RE') {
                        rectangle.setOptions({"fillColor": "blue", "strokeWeight": 0, "fillOpacity": 0.3});
                      }
                    
                  }
              }
          }
          for (var i = lastMarker; i < markers.length; i++) {
            var marker = markers[i];
            google.maps.event.addListener(marker, 'click', function() {
              infowindow.setContent(this.html);
              infowindow.open(map, this);
            });
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
        var str = $(this).serialize();
        $.ajax({

          type: 'POST',
          url : 'send_search_coord',
          data : str,
          success : function(data) {
             let regions = data.regions;
             deleteSelectedShape();
             for (let region of regions) {
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
               var rectangle;
               if (!all_overlays.hasOwnProperty(region.id)) {
                 rectangle = new google.maps.Rectangle({
                   map: map,
                   bounds: {
                     north: parseFloat(region.lat + regHeight),
                     south: parseFloat(region.lat),
                     east: parseFloat(region.lon + regWidth),
                     west: parseFloat(region.lon)
                   },
                   clickable: false,
                   zIndex: SHAPE_Z_INDEX
                 });
                 all_overlays[region.id] = rectangle;
               } else {
                 rectangle = all_overlays[region.id];
               }
               rectangle.setOptions({"fillColor": "yellow", "strokeWeight": 0});
             }
          }
        });
        
        var form = document.getElementById("coordForm");
        form.reset();
      });
});
