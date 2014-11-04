$(document).ready(function() {
  var secondsBetweenReloads = 5;
  var endpoint = '/data';

  /*
   * load tweets from our rest endpoint and list the in the tweet-listing <ul>
   */
  var loadTweets = function(number, topic) {
    var query = '?number=' + number + '&' + 'topic=' + topic;
    $.ajax({
      url: endpoint + query
    }).then(function(data) {
      data = $.parseJSON(data)
      $('#tweet-listing').empty();
      for (var i = 0; i < data.length; i++) {
        $('#tweet-listing').append($('<li/>').append(data[i]));
      }
    });
  };

  loadTweets(10);
  window.setInterval(function() {loadTweets(10);}, secondsBetweenReloads * 1000);
});