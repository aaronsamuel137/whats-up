$(document).ready(function() {
  var secondsBetweenReloads = 5;

  // loadTweets(10);
  // window.setInterval(function() {loadTweets(10);}, secondsBetweenReloads * 1000);
});

/*
 * load tweets from our rest endpoint and list the in the tweet-listing <ul>
 */
function loadTweets(number, topic) {
  var query = '/data?number=' + number + '&' + 'topic=' + topic;
  $('#tweet-listing').empty();
  $('#spinner').append('<img src="/static/img/ajax-loader.gif">')
  $.ajax({
    url: query
  }).then(function(data) {
    $('#spinner').empty();
    data = $.parseJSON(data);
    console.log(data[0]);

    $('#tweet-listing').empty();
    for (var i = 0; i < data.length; i++) {
      $('#tweet-listing').append($('<li/>').append(data[i]));
    }
  });
};

function getTweets(){
  $('#search-btn').blur();
  var topic = $('#search-box').val();
  loadTweets(10, topic);
  return false;
}