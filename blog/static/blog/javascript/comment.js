$(document).ready(function(){
    $(".comment-form").submit(function(e){
        e.preventDefault();
        var thisLike = $(this);

        var input = $('input.commentInpt', this).val();
        console.log('input '+input)

        var postId = $(".commentBtn", this).attr("data-catid");
        var commentText = $("input.commentInpt", this).val();

        // var postId = $(".commentBtn").attr("data-catid");
        // var commentText = $(".commentInpt").val();

        $.ajax({
            type: "POST",
            url: "/comment/",
            data: {
                commentText: commentText,
                postId: postId
            },
            success:function(data){
                $("#allCommentDiv ul.single-post-cmt-div"+postId+" li:nth-child(1)").remove();
                
                $('.single-post-cmt-div'+postId).
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
        $("input.commentInpt", this).val('');
        
    })
    
})