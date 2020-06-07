$(document).ready(function(){
    $(".footerBtn .like i").click(function(e){
        var thisLike = $(this);
        $(this).toggleClass("press");

        var post_id;
        catid = $(this).attr("data-catid");
        $.ajax({
            type: "GET",
            url: "/like/",
            data: {
                post_id:catid
            },
            success:function(data)
            {

                var exists =$( ".footerBtn .like i" ).hasClass( "press" );
                if(exists) {
                    $(thisLike[0]).find(".total-likes").text(data['likes']);
                }
                else {
                    $(thisLike[0]).find(".total-likes").text(data['likes']);

                }

            },
            error:function (xhr,status, error) {
                console.log(error);
            }
        });

    });
});


