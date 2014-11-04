$(document).ready(function() {
  var secondsBetweenReloads = 60;
  var endpoint = '/data';
  var query = '?number=10';

  /*
   * load tweets from our rest endpoint and list the in the tweet-listing <ul>
   */
  var loadTweets = function() {
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

  loadTweets();
  window.setInterval(loadTweets, secondsBetweenReloads * 1000);
});