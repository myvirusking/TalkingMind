function newNotification(){
 $.ajax({
  url: '/new-notification/',
  type: 'post',
  success: function(response){
      if(response['newNotification']>0){
          console.log("new noti")
          $(".total-notification").text(response['newNotification']).addClass("d-block")
      }
  }
 });
}


$(document).ready(function(){
    newNotification();
 setInterval(newNotification,3000);
});