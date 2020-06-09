    function post_save(e,post_id){
            $.ajax({
                type: "GET",
                url: "/save/",
                data: {
                    post_id:post_id
                },
                success:function(data)
                {
                    if(e.className === "fa fa-bookmark"){
                        e.className = "fa fa-bookmark saved";
                    }else{
                        e.className = "fa fa-bookmark";
                    }

                },
                error:function (xhr,status, error) {
                    console.log(error);
                }
            });
    }
