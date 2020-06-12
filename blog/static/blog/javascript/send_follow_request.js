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
                    if(data['profile_privacy']==='private')
                    {
                        console.log("Private");
                        $(".profileEditBtn p a").removeClass("followBtn").
                        addClass("cancelRequestBtn").
                        text("Cancel request");
                    }
                    else if(data['profile_privacy']==='public')
                    {
                        console.log("Public");
                        $(".profileEditBtn p a").removeClass("followBtn").
                        addClass("unfollowBtn").
                        text("Unfollow");
                    }


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
    $(".modal-follow-request-button .follow-btn").click(function (e) {
        var class_f = $(this).attr("data-id")+"follow";
        console.log(class_f)
        if ($(".modal-follow-request-button .follow-btn").hasClass(class_f))
        {
            console.log("inside class")
            e.preventDefault();
            var thisSave = $(this);
            console.log(thisSave)

            var post_id;
            let user_id = $(this).attr("data-id");
            console.log("user-id "+user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/send/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    $("#follow-btn"+user_id).removeClass(class_f).addClass(user_id+"requested").text("Requested");

                },
                error: function (xhr, status, error) {
                    console.log(error);
                    cconsole.log(xhr);
                }

            });

        }
        else if ($(this).hasClass($(this).attr("data-id")+"requested")) {
            // console.log("requested "+$(this).attr("data-id")+"requested")
            e.preventDefault();

            let user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/cancel/",
                data: {
                    userid: user_id
                },
                success: function (data) {

                    $("#follow-btn"+user_id).removeClass(user_id+"requested").addClass(class_f).text("Follow");

                },
                error: function (xhr, status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });
        }
         else if ($(this).hasClass($(this).attr("data-id")+"unfollow")) {
            e.preventDefault();

            let user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/other-profile/unfollow/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    $("#follow-btn"+user_id).removeClass(user_id+"unfollow").addClass(user_id+"follow").text("Follow");
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




function accept_request(event) {
        if($(".follow-request .accpet-delete-btn a").hasClass("accept")){
            console.log("accept");

            var user_id = $(".follow-request .accpet-delete-btn a").attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/accept/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    console.log("success");
                    $("."+user_id+"follow-request").remove();
                },
                error: function (xhr, status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });
        }
        else if(this.hasClass('delete')){
            e.preventDefault();

            var user_id = $(this).attr("data-id");
            console.log(user_id);
            $.ajax({

                type: "GET",
                url: "/user/follow-request/delete/",
                data: {
                    userid: user_id
                },
                success: function (data) {
                    $("."+user_id+"follow-request").remove();
                },
                error: function (xhr, status, error) {
                    console.log(error);
                    console.log(xhr);
                }
            });
        }
}


















