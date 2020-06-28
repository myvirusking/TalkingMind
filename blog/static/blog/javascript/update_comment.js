var updateForm = "";

function editComment(event){
    console.log("--------editcomment---------");
    console.log(event);
    // console.log(event.path[5]);
    // console.log(event.path[5].children[1].children[0]);

    var commentId = event.target.dataset["catid"];
    var mainContentDiv = event.path[5].children[1];
    console.log(commentId);
    var commentText = $(event.path[5].children[1].children[0]).text();
    // debugger;
    console.log(commentText);


    updateForm = ('<div class="edit-comment-div mb-2">\
                        <form class="edit-comment-form" method="post" data-catid="'+commentId+'" onsubmit="editCommentSubmit(event)">\
                            <div class="form-group mb-0">\
                                <input type="text" class="form-control form-control-sm edit-comment-input" value="'+commentText+'" placeholder="Write a comment..." data-catid="'+commentId+'" required>\
                            </div>\
                            <div>\
                                <button type="submit" class="btn save-editBtn">save changes</button>\
                                <button type="button" class="btn btn-danger cancel-editBtn" onclick="canceleditform(event)">cancel</button>\
                            </div>\
                        </form>\
                    </div>\
                    ');

    $(event.path[5].children[1]).hide();
    $(event.path[5].children[2]).replaceWith(updateForm);
}

function canceleditform(e){
    console.log(e);
    console.log(e.path[3]);    
    var commentId = $(e.path[2]).attr("data-catid");
    $(".comment-main-content"+commentId).show();
    $(e.path[3]).hide();
}

// $(document).ready(function(){
//     $(".edit-comment-form").submit(function(e){
//         console.log(e);
//         debugger;
//         e.preventDefault();
//     })
// })

function editCommentSubmit(event){
    console.log(event);
    console.log(event.target);
    event.preventDefault();
    var commentId = $("input.edit-comment-input", event.target).attr("data-catid");
    var text = $("input.edit-comment-input", event.target).val();
    // debugger;
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
            // console.log(updateForm)
            // console.log(event.path[1])

            $(".comment-main-content"+data.commentId+ " p.commentText").text(data.new_commented_text);
            $(".comment-main-content"+data.commentId+" .text-edited").show();
            $(".comment-main-content"+data.commentId).show();
            

            $(event.path[1]).remove();
            // $(event.path[1]).replaceWith(".comment-main-content");
        },
        error: function(xhr, status, error){
            console.log(error)
        }
        
    })

}

