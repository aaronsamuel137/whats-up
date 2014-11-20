
// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(loadHashtagData);

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

  for (var i = 0; i < 10; i++) {
    if (i > hashtags.length) {
      break;
    }
    data.addRow("#"+[hashtags[i].tag, hashtags[i].count]);
  }

  var options = {height: 600};
  var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
  chart.draw(data, options);
}

function loadHashtagData() {
  var query = '/hashtagmap';
  $('#chart-div').empty();
  $('#spinner').empty()
  $('#spinner').append('<img src="/static/img/ajax-loader.gif">')
  $.ajax({
    url: query
  }).then(function(data) {
    $('#spinner').empty()
    data = $.parseJSON(data);
    drawChart(data);
  });
};
