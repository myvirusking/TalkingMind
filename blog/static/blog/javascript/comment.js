$(document).ready(function () {
    $(".comment-form").submit(function (e) {
        console.log(" comment ")
        e.preventDefault();
        var thisLike = $(this);

        var input = $('input.commentInpt', this).val();
        console.log('input ' + input)

        var postId = $(".commentBtn", this).attr("data-catid");
        var commentText = $("input.commentInpt", this).val();

        var hiddenVal = $("#hiddenInput").val();
        console.log("hiddenVal " + hiddenVal);



        $.ajax({
            type: "POST",
            url: "/comment/",
            data: {
                commentText: commentText,
                postId: postId,
                commentId: hiddenVal
            },
            success: function (data) {
                console.log(data)
                $("#allCommentDiv ul.single-post-cmt-div" + postId + " li:nth-child(1)").remove();

                $('.single-post-cmt-div' + postId).
                    prepend('<li class="media">\
                    <a href="#"><img class="mr-3 profilePic" src="/media/default.jpeg" alt="img"></a>\
                    <div class="media-body">\
                        <h6 class="mt-0 mb-1 profileName"><a href="#">'+ data.author_fname+' '+ data.author_lname + '</a><span class="ml-3 commentlikeBtn"><i class="fa fa-heart"></i></span></h6>\
                        <p class="commentText">'+ data.commented_text + '</p>\
                        <div class="commentTextBottomBtn">\
                            <span class="textBtn">0 minutes</span>\
                            <span class="textBtn"><span>0</span> likes</span>\
                            <span id="repltBtn'+ data.commentId + '" class="textBtn replyBtn" onclick="reply(this);" data-catid="' + data.commentId + '" >reply</span>\
                        </div>\
                        <div class="commentRplyDiv">\
                            <ul class="list-unstyled">\
                                {{comment.id | get_nested_comment:comment.id}}\
                            </ul>\
                        </div>\
                        <div class="collapse-div" id="replyInput'+ data.commentId + '" style="display: none;">\
                            <form class="reply-comment-form d-flex" id="'+data.commentId+'">\
                                {% csrf_token %}\
                                {{comment_form.commented_text}}\
                                <button id="commentBtn" type="submit" class="btn btn-outline-info commentBtn"><i class="fas fa-paper-plane"></i></button>\
                            </form>\
                        </div>\
                    </div>\
                </li>\
                ');
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        })
        $("input.commentInpt", this).val('');

    })

})

function reply(elm){
    console.log("clicked")

        var commentId = $(elm).attr("data-catid");
        console.log(commentId)
        $('.reply-comment-form input.commentInpt').val("");

        $(".collapse-div").slideUp().removeClass("d-block");
        $("#replyInput" + commentId).slideDown().addClass("d-block");

        $("#hiddenInput").val(commentId);

        $('#replyInput' + commentId + ' form input.commentInpt').attr('data-root', commentId);

        $('form.comment-form input.commentInpt').click(function () {
            $('#hiddenInput').val(0);
        });


        // $('.reply-comment-form input.commentInpt').click(function () {
        //     $("#hiddenInput").val(commentId);
        // });
}

$('.comment-form input.commentInpt').click(function () {
    $(".collapse-div").slideUp().removeClass("d-block");
});


// $(document).ready(function () {
//     $(".commentTextBottomBtn .replyBtn").on("click",function (e) {
//         console.log("clicked")
//         e.preventDefault();
//         var commentId = $(this).attr("data-catid");
//         console.log(commentId)
//         $('.reply-comment-form input.commentInpt').val("");

//         $("#replyInput" + commentId).slideDown().addClass("d-block");

//         $("#hiddenInput").val(commentId);

//         $('form.comment-form input.commentInpt').click(function () {
//             $('#hiddenInput').val(0);
//         });


//         $('.reply-comment-form input.commentInpt').click(function () {
//             $("#hiddenInput").val(commentId);
//         });

//     })

// });


function nestedReply(elm){

        console.log('nested clicked')

        var rootId = $(elm).attr("data-root");
        console.log(rootId)

        $(".collapse-div").slideUp().removeClass("d-block");
        $("#replyInput" + rootId).slideDown().addClass("d-block");

        var uname = $(elm).attr("data-uname");
        console.log(uname)
        var commentId = $(elm).attr("data-catid");
        console.log(commentId)

        $('#replyInput' + rootId + ' form input').attr('data-catid', commentId);
        $('#replyInput' + rootId + ' form input').attr('data-root', rootId);
        $('#replyInput' + rootId + ' .reply-comment-form input.commentInpt').val(uname+' ');



        $("#hiddenInput").val(commentId);

        $('form.comment-form input.commentInpt').click(function () {
            $('#hiddenInput').val(0);
        });


        $('replyInput' + rootId + ' .reply-comment-form input.commentInpt').click(function () {
            $("#hiddenInput").val($('#replyInput' + rootId + ' form input').attr('data-catid'));
            console.log('hidden value '+ commentId)
        });
}

// $(document).ready(function () {
//     $(".nested-replyBtn").click(function (e) {
//         var par = $(this).parent();

//         e.preventDefault();
//         var rootId = $(this).attr("data-root");
//         console.log(rootId)
//         $("#replyInput" + rootId).slideDown().addClass("d-block");

//         var uname = $(this).attr("data-uname");
//         console.log(uname)
//         $('#replyInput' + rootId + ' .reply-comment-form input.commentInpt').val(uname);

//         var commentId = $(this).attr("data-catid");
//         console.log(commentId)

//         $("#hiddenInput").val(commentId);

//         $('form.comment-form input.commentInpt').click(function () {
//             $('#hiddenInput').val(0);
//         });



//         $('replyInput' + rootId + ' .reply-comment-form input.commentInpt').click(function () {
//             $("#hiddenInput").val(commentId);
//         });

//     })

// });


$(document).ready(function () {
    $(".reply-comment-form").submit(function (e) {
        console.log(" nest-comment ")
        e.preventDefault();
        var thisLike = $(this);

        var input = $('input.commentInpt', this).val();
        console.log('input ' + input)

        var postId = $(".commentBtn", this).attr("data-catid");
        var commentText = $("input.commentInpt", this).val();

        var hiddenVal = $("#hiddenInput").val();
        console.log("hiddenVal " + hiddenVal)

        var rootId = $("input.commentInpt", this).attr("data-root");
        console.log('form id', rootId)


        // var postId = $(".commentBtn").attr("data-catid");
        // var commentText = $(".commentInpt").val();

        $.ajax({
            type: "POST",
            url: "/comment/",
            data: {
                commentText: commentText,
                postId: postId,
                commentId: hiddenVal
            },
            success: function (data) {
                console.log(data)
                $('#commentRplyDiv' + rootId).append(
                    '<li class="media">\
                        <a href="#"><img class="mr-3 profilePic" src="/media/default.jpeg" alt="img"></a>\
                        <div class="media-body">\
                            <h6 class="mt-0 mb-1 profileName"><a href="#">'+ data.author_fname+' '+ data.author_lname + '</a><span class="ml-3 commentlikeBtn"><i class="fa fa-heart"></i></span></h6>\
                            <p class="commentText">'+ data.commented_text + '</p>\
                            <div class="commentTextBottomBtn">\
                                <span class="textBtn">0 minutes</span>\
                                <span class="textBtn"><span>0</span> likes</span>\
                                <span id="repltBtn'+data.commentId+'" class="textBtn nested-replyBtn" data-catid="'+data.commentId+'" data-parent_id="'+data.parent_comment_id+'" data-root="'+rootId+'" data-uname="'+ data.author_fname+' '+ data.author_lname + '" onclick="nestedReply(this);">reply</span>\
                            </div>\
                        </div>\
                    </li>');
            },
            error: function (xhr, status, error) {
                console.log(error);
                console.log(xhr);
            }
        })
        $("input.commentInpt", this).val('');

    })

})
