$(document).ready(function() {
  var kudos=0; // do not like this image

  $(".single-painting").on("click", "i", function(event){
    if(kudos===0){
        $(this).attr("class", "fa fa-heart");
        kudos=1;
    }else{
        $(this).attr("class","fa fa-heart-o");
        kudos=0;
    }
  });

  $("a[id^='aModal']").each(function(){
      $(this).unbind('click').on('click', function(){
          var aid = this.id.substr(6);
          $("#audioModal"+aid).attr("src","/getaudio/"+aid);
      });
    });

});