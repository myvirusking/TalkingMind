$(document).ready(function(){
    $("#commentForm").submit(function(e){
        e.preventDefault();

        var postId = $("#commentBtn").attr("data-catid");
        var commentText = $("#commentInpt").val();

        $.ajax({
            type: "POST",
            url: "/comment/",
            data: {
                commentText: commentText,
                postId: postId
            },
            success:function(data){
                console.log(data);
                $('.allCommentDiv .single-post-cmt-div').
                prepend('<li class="media">\
                    <a href="#"><img class="mr-3 profilePic" src="/media/default.jpeg" alt="img"></a>\
                    <div class="media-body">\
                        <h6 class="mt-0 mb-1 profileName"><a href="#">'+ data.author +'</a><span class="ml-3 commentlikeBtn"><i class="far fa-heart"></i></span></h6>\
                        <p class="commentText">'+ data.text +'</p>\
                        <div class="commentTextBottomBtn">\
                            <span class="textBtn">9h</span>\
                            <span class="textBtn"><span>5</span> likes</span>\
                            <span class="textBtn">reply</span>\
                        </div>\
                    </div>\
                </li>');
            },
            error:function(xhr,status, error){
                console.log(error);
            }
        })
        $("#commentInpt").val('');
    })
})