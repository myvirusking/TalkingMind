$("document").ready(function(){
    if($("#imagePreview").find("img").length==3){
        $(".addImageBtn").addClass("disable");
        $("#id_image").prop("disabled",true);
    }
});

function removeImg(imgCurrentIndex){
    $("#img"+imgCurrentIndex).remove();
    $("#id_image").prop("disabled",false);
    $(".addImageBtn").removeClass("disable");
    imgAvailableIndex.push(imgCurrentIndex);
    imgAvailableIndex.sort();
    delete imgFile[imgCurrentIndex];
}

function filePreview(fileInput,imgCurrentIndex){
    var imgSrc = window.URL.createObjectURL(fileInput.files[0]);
    $("#imagePreview").append($('<div/>',{"id":"img"+imgCurrentIndex,"style":"padding:5px","class":"col mb-3"}).append([
            $('<img/>',{"src":imgSrc,"width":'100%',"height":'100%'}),
            $("<i/>",{"onclick":"removeImg({})".replace("{}",imgCurrentIndex),"class":"fa fa-times","style":"color:red;top: 15px;right: 15px;position: absolute;cursor: pointer;color:red;","aria-hidden":"true"})
        ])
    );

    if($("#imagePreview").find("img").length==3){
        $("#id_image").prop("disabled",true);
        $(".addImageBtn").addClass("disable");
    }
}

$("#id_image").change(function(){
    filePreview(this,imgAvailableIndex[0]);
    imgFile[imgAvailableIndex[0]] = this.files[0];
    delete imgAvailableIndex[0];
    imgAvailableIndex.shift();
}).click(function(){
    if(imgAvailableIndex.length==0){
        this.disabled = true;
        $(".addImageBtn").addClass("disable");
    }
});


$("#postUpdateForm").submit(function(e) {
    $(".btn.btn-sm.btn-outline-success").prop("disabled",true);
    e.preventDefault();
    const pk = $("#postId").attr("data-pk");
    const url = "/blog/post/"+pk+"/update/";
    const formData = new FormData();

    formData.append("csrfmiddlewaretoken",this.elements[0].value);
    formData.append("title",this.elements[2].value);
    formData.append("category",this.elements[3].value);
    formData.append("content",this.elements[4].value);
    imgFile.forEach(function(item, index){
        if(typeof(item) === "number"){
            formData.append('postImgId', item);
        }else{
            formData.append('images', item);
        }
    });
  
    this.reset();
  
    fetch(url, {
      method: 'POST',
      body: formData,
    }).then(response => {
      window.location.href = response.url;
    });

});