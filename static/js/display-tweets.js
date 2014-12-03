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
  $('#neg-count').empty();
  $('#pos-count').empty();


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

    counterPos = 0;
    counterNeg = 0;

    for (var i = 0; i < data.length; i++) {
      if(data[i].sentiment=="negative"){
        $('#tweet-listing-neg').append($('<li/>').append(data[i].text + '<br>Retweet count: ' + data[i].rt_count));
        counterNeg++;
      }
      else{
        $('#tweet-listing-pos').append($('<li/>').append(data[i].text + '<br>Retweet count: ' + data[i].rt_count));

        counterPos++;
      }
    }
    $('#neg-count').append($('<h3>').append(counterNeg).append('</h3>'));
    $('#pos-count').append($('<h3>').append(counterPos).append('</h3>'));

    $('#chart-div').empty();
    drawChart(counterPos, counterNeg);

  });
};

google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);
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

function getTweets(){
  $('#search-btn').blur();
  var topic = $('#search-box').val();
  loadTweets(10, topic);
  return false;
}