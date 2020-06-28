function deleteCommentbtn(el){
        console.log("delete-------------btn")
        console.log(el)
        let commentId = $(el).attr('data-catid');
        console.log("delete commentId "+ commentId);
        // var url =  "/blog/post/"+postId+"/delete/";
        $('.modal-deleteCommentBtn').attr("data-catid", commentId);
    }

$(document).ready(function () {
    $(".modal-deleteCommentBtn").click(function (e) {
        console.log("-----Modal delete btn clicked------")
        e.preventDefault();
        
        var commentId = $(".modal-deleteCommentBtn").attr("data-catid");
        // debugger;
        console.log("modal delete commentId "+ commentId);
        

        $.ajax({
            type: "POST",
            url: "/delete-comment/",
            data: {
                commentId: commentId,
                csrfmiddlewaretoken: $("input[type=hidden]").val()
            },
            success: function (data) {
                console.log(data)
                $(".allCommentDiv ul li#"+commentId).css("display","none");
                $("#deleteCommentModal .close").click()
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        })

    })

})





