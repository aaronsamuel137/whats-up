$(document).ready(function() {
  var endpoint = '/data';
  var query = '?number=10';

  $.ajax({
    url: endpoint + query
  }).then(function(data) {
    data = jQuery.parseJSON(data)
    for (var i = 0; i < data.length; i++) {
      $('#tweet-listing').append($('<li/>').append(data[i]));
    }
  });
});