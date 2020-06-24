function newNotification(){
 $.ajax({
  url: '/new-notification/',
  type: 'post',
  success: function(response){
      if(response['newNotification']>0){
          $(".total-notification").text(response['newNotification'])
      }
  }
 });
}

$(document).ready(function(){
 setInterval(newNotification,8000);
});