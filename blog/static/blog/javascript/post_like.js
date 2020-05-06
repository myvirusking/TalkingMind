$(document).ready(function(){
    $("#like").click(function(e){
        var postid;
        catid = $(this).attr("data-catid");
        $.ajax({
            type: "GET",
            url: "like/",
            data: {
                post_id:catid
            },
            success:function(data)
            {
                $("#total-likes").text(data['likes']);
            },
            error:function (xhr,status, error) {
                console.log("Error");
            }
        })
    })
});