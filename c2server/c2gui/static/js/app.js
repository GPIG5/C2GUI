
var timeline = {
	"timeline": {
		"headline":"My Fav Things",
		"type":"default",
		"text":"This is a collection of my favourite things over the last week",
		"date": [{
			"headline": 'Initiated search in the area',
			"text": '',
			"asset": {},
			"startDate": "2016,5,10,20,30",
			"endDate": this.startDate
		}, {
			"headline": 'Lemon Jelly',
			"text": '',
			"asset": {},
			"startDate": "2016,5,11,20,30",
			"endDate": this.startDate
		}]
	}
};

/*
var timeline = {
	"timeline": {
		"headline":"My Fave Things",
		"type":"default",
		"text":"This is a collection of my favourite things",
		"date": []
	}
};


function jsonFlickrApi(response) {
	populateTimeline.flickrCallback(response);
}

var populateTimeline = (function() {

	function twitter() {
		return $.Deferred(function() {
			var deferred = this;

			$.getJSON("https://api.twitter.com/1/statuses/user_timeline/timofetimo.json?callback=?", function(data){
				var tweets = data.length;

				for (var i = 0; i < tweets; i++) {
					var timestamp = Date.parse(data[i].created_at),
						date = new Date(timestamp),
						month = date.getMonth() + 1;
					
					var tweet = {
						headline: data[i].text.split(' ')[0],
						text: '',
						asset: {
							media: 'https://twitter.com/' + data[i].user.screen_name + '/status/' + data[i].id_str,
							credit: '',
							caption: ''
						},
						startDate: date.getFullYear() + ',' + month + ',' + date.getDate(),
						endDate: this.startDate
					};
					
					timeline.timeline.date.push(tweet);
					
				}
				deferred.resolve();
			});
		});
	}
	
	function flickr() {
		return $.Deferred(function() {
			var deferred = this;
			var script = document.createElement('script');
			script.src = 'http://api.flickr.com/services/rest/?method=flickr.favorites.getPublicList&format=json&api_key=dfe82aea164aa183a555938136493c82&user_id=10266210@N00';
			document.body.appendChild(script);

			setInterval(function() {
				if (flickrReturned) {
					deferred.resolve();
				}
			}, 200);

		});
	}

	function youtube() {
		$.get('https://gdata.youtube.com/feeds/api/users/nitesshadow/favorites?alt=json', function(data) {
			for (var i=0; i < data.feed.entry.length; i++) {

				var url = data.feed.entry[i].media$group.media$player[0].url,
					taintedId = url.substr(url.indexOf('?v='), 14),
					id = taintedId.replace('?v=', '');

				var timestamp = Date.parse(data.feed.entry[i].published.$t),
					date = new Date(timestamp),
					month = date.getMonth() + 1;

				var video = {
					headline: data.feed.entry[i].title.$t,
					text: '',
					asset: {
						media: 'http://youtu.be/' + id,
						credit: data.feed.entry[i].author[0].name.$t,
						caption: data.feed.entry[i].content.$t
					},
					startDate: date.getFullYear() + ',' + month + ',' + date.getDate(),
					endDate: this.startDate
				};

				timeline.timeline.date.push(video);
			}
		});
	}

	function vimeo() {
		$.getJSON('http://vimeo.com/api/v2/user11663077/likes.json?callback=?', function(data) {
			for (var i=0; i < data.length; i++) {
				
				var date = data[i].liked_on.split('-');
				var year = date[0];
				var month = date[1];
				var day = date[2].substr(0,2);

				var video = {
					headline: data[i].title,
					text: '',
					asset: {
						media: data[i].url.replace('http', 'https'),
						credit: data[i].user_name,
						caption: data[i].description
					},
					startDate: year + ',' + month + ',' + day,
					endDate: this.startDate
				};

				timeline.timeline.date.push(video);
			}
		});
	}

	var flickrReturned = false;

	function flickrCallback(response) {
		return $.Deferred(function() {
			var deferred = this;
			if (response.stat === "ok") {
				var photos = response.photos.photo.length;
				for (var i=0; i < photos; i++) {

					var date = new Date(response.photos.photo[i].date_faved * 1000),
						month = date.getMonth() + 1;
					
					var photo = {
						headline: response.photos.photo[i].title,
						text: '',
						asset: {
							media: 'http://www.flickr.com/photos/' + response.photos.photo[i].owner + '/' + response.photos.photo[i].id,
							credit: '',
							caption: ''
						},
						startDate: date.getFullYear() + ',' + month + ',' + date.getDate(),
						endDate: this.startDate
					};
										
					timeline.timeline.date.push(photo);
				}
				
				flickrReturned = true;
			}
		});
	}

	return {
		twitter: twitter,
		flickr: flickr,
		flickrCallback: flickrCallback,
		youtube: youtube,
		vimeo: vimeo
	};
})();
	
$.when(
	populateTimeline.twitter()
	//populateTimeline.flickr(),
	//populateTimeline.youtube(),
	//populateTimeline.vimeo()
).then(function() {
	createStoryJS({
		width: window.innerWidth,
		height: window.innerHeight,
		source: timeline,
		embed_id: 'my-timeline'
	});
});
*/

var createTimeline = function () {
    {% for event in event_list %}
        var new_event = {
            headline: {{ event.text }},
            text: '',
            asset: {},
            startDate: {{ event.timestamp|date:"Y,m,d,G,i" }}
            endDate: this.startDate
        }
        timeline.timeline.date.push(new_event);
    {% endfor %}
}

$(document).ready(function() {
    createTimeline();
    createStoryJS({
        width: '800',
        height: '600',
        source: timeline,
        embed_id: 'my-timeline'
    });
});
