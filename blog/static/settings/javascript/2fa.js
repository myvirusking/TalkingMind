$(document).ready(function () {

  $("form input[type=checkbox]").click(function(){
      if(this.checked){
        $("input[name=method]").val(this.value);
        $("form").submit();
      }
      else{
          var input = confirm("You are about to disable two-factor authentication. This weakens your account security, are you sure?");     
          if(input){
            $("input[name=method]").val(this.value);
            $("form").submit();
          }
          else{
            this.checked = true;
          }

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
      $(".font-weight-bold.pl-5").html("Verification Process");
      $("#set_up_authentication").hide();
      $("#verify_token").show();
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
