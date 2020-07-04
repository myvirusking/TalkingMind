$(document).ready(function () {

  $("#2FAForm input[type=checkbox]").click(function(){
      $("input[name=method]").val(this.value);
      if(this.checked){
        $("#2FAForm").submit();
      }
      else{
          this.checked = true;
          $("#verifyPasswordModal").modal("show");
      }
  });

  $("#cant_scan_qr_code").click(function(){
      $(this).hide();
      $("#secret_key_div").show();
      var formatSecretKey = $("#secret_key").html().replace(/[^\dA-Z]/gi, '')
            .replace(/(.{4})/g, '$1 ')
            .trim();
      $("#secret_key").html(formatSecretKey);
  });

  $("#btnNextToken").click(function(){
      $("#p_token_verification").html("Token Verification");
      $("#set_up_authentication").hide();
      $("#verify_token").show();
  });

  $("#verifyPasswordForm").submit(function(e){
    e.preventDefault();
      $.ajax({
          type : "POST",
          url : window.location,
          data : {
            "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val(),
            "password" : $("input[name=password]").val(),
            "method" : $("input[name=method]").val()
          },
          success : function(data){
            if(data.is_verify){
              window.location = window.location.href;
            }else{
              $("#invalid_password_error").show();
            }
          }
      });
  });

});

function printTokens(){
  var orgContents = document.body.innerHTML;
  $("form").hide();
  $("span").hide();
  $("#header").hide();
  $(".font-weight-bold.pl-5").html("TalkingMind 2FA Backup Tokens");
  $(".font-weight-bold.pl-5").css({'text-align':'center','margin-top':'20px','padding-top':'20px','border-top': '1px solid darkgray'});
  var printContents = $("#tokens_div").html();
  document.body.innerHTML = printContents;
  window.print();
  document.body.innerHTML = orgContents;
}
