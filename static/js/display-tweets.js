$(document).ready(function() {
  var secondsBetweenReloads = 10;
  var endpoint = '/data';
  var query = '?number=10';

  /*
   * load tweets from our rest endpoint and list the in the tweet-listing <ul>
   */
  var loadTweets = function() {
    $.ajax({
      url: endpoint + query
    }).then(function(data) {
      console.log('reload');
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