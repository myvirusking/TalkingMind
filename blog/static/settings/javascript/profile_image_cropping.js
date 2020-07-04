$(document).ready(function(){
    var base64Img;

    function readFile(input) {
        var reader = new FileReader();
        reader.readAsDataURL(input.files[0]);
        reader.onload = function(e) {
            base64Img = e.target.result;
        };
    }

    $("#image").change(function() {
        readFile(this);
        $("#cropImagePopModal").modal("show");
    });

    var croppieDivObj = $("#croppieDiv").croppie({
        enableExif: true,
        viewport: {
            width: 300,
            height: 300,
            type: 'circle'
        },
        boundary: {
            width: 360,
            height: 360
        }
    });

    $("#cropImagePopModal").on('shown.bs.modal', function() {
        croppieDivObj.croppie("bind", {
            url: base64Img
        });
    });

    $("#cropImageBtn").click(function(){
        croppieDivObj.croppie('result',{
            type:"blob",
            circle: false
        }).then(function(blob){
            var fileName = $("#image")[0].files[0].name;
            const croppedImageFIle = new File([blob], fileName, { type: blob.type });
            var formData =  new FormData();
            formData.append("image",croppedImageFIle);
            formData.append("csrfmiddlewaretoken",csrf_token);
            fetch(profileUpdateUrl,{
                method:"post",
                body:formData
            }).then(function(response){
                $("#cropImagePopModal").modal("hide");
                window.location.href = response.url;
                $("#croppieDiv").croppie.destroy();
            });
        });
    });

});