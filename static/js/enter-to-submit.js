$(document).ready(function(){
    $('#search-box').keypress(function(e){
      if(e.keyCode==13)
      $('#search-btn').click();
    });
});