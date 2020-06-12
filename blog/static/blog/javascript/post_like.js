
function post_like(e,post_id){
    $.ajax({
        type: "GET",
        url: "/like/",
        data: {
            post_id:post_id
        },
        success:function(data)
        {
            if(e.className === "fa fa-heart"){
                e.className = "fa fa-heart press";
            }else{
                e.className = "fa fa-heart";
        
            }
            
            e.innerHTML = "<span class='total-likes'>"+data.likes+"</span>";
        },
        error:function (xhr,status, error) {
            console.log(error);
        }
    });

}