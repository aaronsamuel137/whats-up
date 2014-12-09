$(document).ready(function() {
  $('#spinner').hide();
})

google.load("visualization", "1", {packages:["corechart"]});
var refreshInterval;

/*
 * load tweets from our rest endpoint and list the in the tweet-listing <ul>
 */
 function loadTweets(number, topic) {
  var query = '/data?number=' + number + '&' + 'topic=' + topic;

  // on the first time only, append these headers for positive and negative columns
  if (!refreshInterval) {
    $('#neg-header').append($('<h3>Negative</h3>'));
    $('#pos-header').append($('<h3>Positive</h3>'));
  }

  $.ajax({
    url: query
  }).then(function(data) {

    $('#neg-tweets').empty();
    $('#pos-tweets').empty();
    $('#neg-header').empty();
    $('#pos-header').empty();

    $('#spinner').hide();
    data = $.parseJSON(data);

    counterPos = 0;
    counterNeg = 0;

    data = data.sort(function (a, b) {
      return b.rt_count - a.rt_count;
    });

    var posTweetHTML = '', negTweetHTML = '';
    for (var i = 0; i < data.length; i++) {
      //print negative tweets
      if(data[i].sentiment=="negative"){
        // $('#tweet-listing-neg').append($('<li/>').append(data[i].text + '<br><span class="retweet">Retweet count: </span>' + data[i].rt_count));
        twttr.widgets.createTweet(data[i].tweet_id, document.getElementById('neg-tweets'));

        counterNeg++;
      }
      //print positive tweets
      else{
        // $('#tweet-listing-pos').append($('<li/>').append(data[i].text + '<br><span class="retweet">Retweet count: </span>' + data[i].rt_count));
        twttr.widgets.createTweet(data[i].tweet_id, document.getElementById('pos-tweets'));

        counterPos++;
      }
    }

    // $('.tweet-listing').empty();
    // $('#tweet-listing-neg').append(negTweetHTML);
    // $('#tweet-listing-pos').append(posTweetHTML);

    $('#chart-div').empty();
    drawChart(counterPos, counterNeg);

  });
};

// google.setOnLoadCallback(drawChart);
function drawChart(counterPos, counterNeg) {

  var data = google.visualization.arrayToDataTable([
    ['Sentiment', 'Number of tweets'],
    ['Negative', counterNeg],
    ['Positive', counterPos]
    ]);

  var options = {
    title: 'Sentiment Analysis',
    width: 500,
    slices: {
      1: { color: '#01A9DB' },
      0: { color: '#0431B4' }
    },
    titleTextStyle: {
      fontSize: 20
    }

  };

  var chart = new google.visualization.PieChart(document.getElementById('chart-div'));

  chart.draw(data, options);
}

function getTweets() {
  $('#spinner').show();
  clearInterval(refreshInterval);
  $('#search-btn').blur();
  var topic = $('#search-box').val();
  loadTweets(10, topic);
  // refreshInterval = setInterval(function() { loadTweets(10, topic); }, 5000);
  return false;
}