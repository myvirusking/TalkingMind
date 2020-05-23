/* This is the function for sending follow request when the user is on other user profile. The functions
* changes the class value depending on the state of the button, if the user follows another user the
* class changes and it becomes cancelRequestBtn and if the user cancels the request then the class again
* becomes followBtn. If the other user accepted the request of the current logged in user then the
* class values changes to unfollowBtn and if the user unfollows the other user then it becomes
* followBtn. Different views of django will be called depending on the state of the button(see the
* code for more info)*/


$(document).ready(function(){
    console.log("reached");
    $("#follow-user").click(function(e){
        if ($(".profileEditBtn p a").hasClass("followBtn"))
        {
             e.preventDefault();
            var thisSave = $(this);

            var post_id;
            user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/send/",
                data: {
                    userid:user_id
                },
                success:function(data)
                {
                    $(".profileEditBtn p a").removeClass("followBtn").
                    addClass("cancelRequestBtn").
                    text("Cancel request");

                },
                error:function (xhr,status, error) {
                    console.log(error);
                    cconsole.log(xhr);
                }

            });

        }
        else if($(".profileEditBtn p a").hasClass("cancelRequestBtn"))
        {
            e.preventDefault();

            var user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/cancel/",
                data: {
                    userid:user_id
                },
                success:function(data)
                {
                    $(".profileEditBtn p a").removeClass("cancelRequestBtn").
                    addClass("followBtn").
                    text("Follow");

                },
                error:function (xhr,status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });
        }
        else if($(".profileEditBtn p a").hasClass("unfollowBtn"))
        {
            e.preventDefault();

            var user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/other-profile/unfollow/",
                data: {
                    userid:user_id
                },
                success:function(data)
                {
                    console.log("success");
                    $(".profileEditBtn p a").removeClass("unfollowBtn").
                    addClass("followBtn").
                    text("Follow");

                },
                error:function (xhr,status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });

        }

    });
});


/*This functions gets called when the user opens his follower modal. If the user follows the other user
* in his followers list then only the remove button will be shown and if the user doesn't follow the other
* user then the follow link will be shown beside the username of the other user. If the user clicks
* on the follow link the class of the link will be changed(for more look at the below code) and the
* text will be changed to 'Requested' and if the user again clicks on requested link then the class
* will again change and the text will be changed to 'Follow'. Different views of django will be called
* depending on the state of the button(see the code for more info)*/

$(document).ready(function() {
    $(".modal-follow-request-button a").click(function (e) {
        var class_f = $(this).attr("data-id")+"follow";
        console.log(class_f);
        if ($(this).hasClass(class_f))
        {
            e.preventDefault();
            var thisSave = $(this);

            var post_id;
            user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/send/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    $(".modal-follow-request-button a").removeClass(class_f).addClass(user_id+"requested").text("Requested");

                },
                error: function (xhr, status, error) {
                    console.log(error);
                    cconsole.log(xhr);
                }

            });

        }
        else if ($(this).hasClass($(this).attr("data-id")+"requested")) {
            e.preventDefault();

            user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/cancel/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    $(".modal-follow-request-button a").removeClass(user_id+"requested").addClass(class_f).text("Follow");

                },
                error: function (xhr, status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });
        }
         else if ($(this).hasClass($(this).attr("data-id")+"unfollow")) {
            e.preventDefault();

            user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/unfollow/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    $(".modal-follow-request-button a").removeClass(user_id+"unfollow").addClass(class_f).text("Follow");
                    $(".total-following-count").text(data['following_count']);

                },
                error: function (xhr, status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });
        }
    });
});




/*This function gets called when a user removes someone from his followers list. If the user removes
* the other user from the followers list then the django view will be called through this function
* (see the code for more info). The followers count of the current user will be decremented and also
* the current user will be removed from the following list of the user being removed. The django view
* will return the followers count of the current user and it will be changed each time a user removes
* someone from the list*/

$(document).ready(function() {
    $(".remove-button-of-followers p a").click(function (e) {
        e.preventDefault();
        var thisSave = $(this);

        var user_id = $(this).attr("data-id");
        console.log(user_id);
        $.ajax({

            type: "GET",
            url: "/remove-from-followers/",
            data: {
                userid: user_id
            },
            success: function (data) {
                $("."+user_id).remove();
                $(".total-followers-count").text(data['followers_count']);
            },
            error: function (xhr, status, error) {
                console.log(error);
                console.log(xhr);
            }

        });

    });
});



/*This function gets called when the current logged user unfollows some other user from his following
* list. The django views gets called from this method. The view removes the current user from the unfollowed
* users's followers list and also unfollowed user gets removed from the current user's following list
* (See the code below for more info)*/

$(document).ready(function() {
    $(".unfollow-button-of-followings p a").click(function (e) {
        e.preventDefault();
        var thisSave = $(this);

        var user_id = $(this).attr("data-id");
        console.log(user_id);
        $.ajax({

            type: "GET",
            url: "/user/other-profile/unfollow/",
            data: {
                userid: user_id
            },
            success: function (data) {
                $("."+user_id+"followed-user").remove();
                $(".total-following-count").text(data['following_count']);
            },
            error: function (xhr, status, error) {
                console.log(error);
                console.log(xhr);
            }

        });

    });
});















