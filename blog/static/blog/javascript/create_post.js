var imgFile = Array(3);
var imgAvailableIndex = Array();
imgAvailableIndex = [0,1,2];

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

    if($("#imagePreview")[0].childElementCount==3){
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

$("#postCreateForm").submit(function(e) {
    e.preventDefault();
    const url = "/blog/post/create/";
    const formData = new FormData();

    formData.append("csrfmiddlewaretoken",this.elements[0].value);
    formData.append("title",this.elements[1].value);
    formData.append("category",this.elements[2].value);
    formData.append("content",this.elements[3].value);
    imgFile.forEach(function(item, index){
        formData.append('images', item);
    });

    this.reset();
  
    fetch(url, {
      method: 'POST',
      body: formData,
    }).then(response => {
      window.location.href = response.url;
    });

});