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
  $('#tweet-listing-pos').empty();
  $('#tweet-listing-neg').empty();
  $('#neg-header').empty();
  $('#pos-header').empty();


  $('#spinner').append('<img src="/static/img/ajax-loader.gif">')
  $.ajax({
    url: query
  }).then(function(data) {
    $('#spinner').empty();
    data = $.parseJSON(data);
    console.log(data[0]);

    $('#tweet-listing').empty();
    $('#neg-header').append($('<h3>Negative</h3>'));
    $('#pos-header').append($('<h3>Positive</h3>'));

    for (var i = 0; i < data.length; i++) {
      if(data[i].sentiment=="negative")
        $('#tweet-listing-neg').append($('<li/>').append(data[i].text + '<br></span>'));
      else
        $('#tweet-listing-pos').append($('<li/>').append(data[i].text + '<br></span>'));
    }
  });
};

function getTweets(){
  $('#search-btn').blur();
  var topic = $('#search-box').val();
  loadTweets(10, topic);
  return false;
}