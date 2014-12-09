
// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(loadHashtagData);

// reload chart every 5 seconds
setInterval(loadHashtagData, 5000);

var MAX_WORDS = 50;
var numWords = 20;

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart(hashtags) {

  // Create the data table.
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Hashtag');
  data.addColumn('number', 'Number of Tweets');

  if (hashtags.length === 0) {
    hashtags = [
      {tag: '#mtvstars', count: 100},
      {tag: '#AMAs', count: 80},
      {tag: '#RT', count: 75},
      {tag: '#android', count: 60},
      {tag: '#love', count: 60}
    ];
  }

  hashtags = hashtags.sort(function (a, b) {
    return b.count - a.count;
  });

  var wordCloud = [];
  for (var i = 0; i < Math.min(numWords, MAX_WORDS); i++) {
    if (i > hashtags.length) {
      break;
    }
    if (i < 10) { data.addRow(['#' + hashtags[i].tag, hashtags[i].count]); }
    wordCloud.push({text: hashtags[i].tag, weight: hashtags[i].count});
  }
  numWords++;

  $('#jqtagcloud').empty();
  $('#jqtagcloud').jQCloud(wordCloud);

  var options = {height: 600};
  var chart = new google.visualization.BarChart(document.getElementById('chart-div'));
  chart.draw(data, options);
}

function loadHashtagData() {
  var query = '/hashtagmap';
  $.ajax({
    url: query
  }).then(function(data) {
    $('#spinner').hide()
    data = $.parseJSON(data);
    drawChart(data);
  });
};
