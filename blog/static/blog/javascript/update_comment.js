var updateForm = "";


function editComment(event){
    console.log("--------editcomment---------");
    console.log(event);

    var commentId = event.target.dataset["catid"];
    console.log(commentId);
    var cmtText = $(".comment-main-content"+commentId+" p").text();
    console.log(cmtText);


    updateForm = ('<div class="edit-comment-div'+commentId+' mb-2">\
                        <form class="edit-comment-form" method="post" data-catid="'+commentId+'" onsubmit="editCommentSubmit(event)">\
                            <div class="form-group mb-0">\
                                <input type="text" class="form-control form-control-sm edit-comment-input" value="'+cmtText+'" placeholder="Write a comment..." data-catid="'+commentId+'" required>\
                            </div>\
                            <div>\
                                <button type="submit" class="btn save-editBtn">save changes</button>\
                                <button type="button" class="btn btn-danger cancel-editBtn" onclick="canceleditform(event, '+commentId+')">cancel</button>\
                            </div>\
                        </form>\
                    </div>\
                    ');

    $(".comment-main-content"+commentId).hide();
    $(".replace-maincontent"+commentId).replaceWith(updateForm);
}

function canceleditform(e, commentId){
    console.log(e);
    console.log(commentId);    
    $(".comment-main-content"+commentId).show();
    $(".edit-comment-div"+commentId).replaceWith('<div class="replace-maincontent'+commentId+'"></div>')
}


function editCommentSubmit(event){
    console.log(event);
    console.log(event.target);
    event.preventDefault();
    var commentId = $("input.edit-comment-input", event.target).attr("data-catid");
    var text = $("input.edit-comment-input", event.target).val();
    
    console.log(commentId)
    console.log(text)

    $.ajax({
        type: "POST",
        url: "/edit-comment/",
        data: {
            commentId: commentId,
            new_commented_text: text,
            csrfmiddlewaretoken: $("input[type=hidden]").val()
        },
        success: function(data){
            console.log(data)

            $(".comment-main-content"+data.commentId+ " p.commentText").text(data.new_commented_text);
            $(".comment-main-content"+data.commentId+" .text-edited").show();
            $(".comment-main-content"+data.commentId).show();
            
            $(".edit-comment-div"+commentId).replaceWith('<div class="replace-maincontent'+data.commentId+'"></div>')
            
        },
        error: function(xhr, status, error){
            console.log(error)
        }
        
    })

}

