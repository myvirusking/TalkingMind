function cmt_like(el){
        console.log("------comment like----------")
        $(el).toggleClass('press');

        var cmt_id = $(el).attr('data-catid')
        var postid = $(el).attr('data-postid')
        console.log('cmt_id '+ cmt_id)
        $.ajax({
            type: 'GET',
            url: 'comment_like/',
            data: {
                cmt_id: cmt_id,
                postid: postid
            },
            success: function(data){
                console.log(data)
                var class_exists = $('.commentlikeBtn i').hasClass('press')
                console.log('class_exists '+ class_exists)
                console.log('likes_count '+ 'likes_count'+cmt_id)
                if(class_exists){
                    $('.likes_count'+cmt_id).text(data['likes_count'])
                }else{
                    $('.likes_count'+cmt_id).text(data['likes_count'])
                }

            },
            error: function(xhr, status, error){
                console.log(error)
            }
        })

}