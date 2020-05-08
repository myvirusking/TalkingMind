$(document).ready(function(){
    $(".footerBtn .save i").click(function(e){
        var thisSave = $(this);
        $(this).toggleClass("saved");

        var post_id;
        catid = $(this).attr("data-catid");
        console.log(catid);
        $.ajax({
            type: "GET",
            url: "save/",
            data: {
                post_id:catid
            },
            success:function(data)
            {

            },
            error:function (xhr,status, error) {
                console.log(error);
                cconsole.log(xhr);
            }
        });

    });
});

