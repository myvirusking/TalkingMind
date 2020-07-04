$(document).ready(function(){
    $("#other-profile-action .threeDot .blocking").click(function(e) {
        if ($(this).hasClass("block")) {
            e.preventDefault();

            user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/block/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    location.reload()

                },
                error: function (xhr, status, error) {
                    console.log(error);
                    console.log(xhr);
                }

            });

        } else if ($("#other-profile-action .threeDot .blocking").hasClass("unblock")) {
            e.preventDefault();

            var user_id = $("#other-profile-action .threeDot .blocking").attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/unblock/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    location.reload()

                },
                error: function (xhr, status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });
        }
    });
});


