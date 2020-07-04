$(document).ready(function(){
		if (verify_mobile == "True"){
			$("#verifyMobileModal").modal("show");
		}

		$("#resend_otp").click(function(){
			if(enableResend === true){
				resendCounter++;
				if(resendCounter >= 2){
					enableResend = false;
					$(this).css({'color':'grey'});
					clearInterval(getTimer);
					getTimer = setInterval(startTimer,1000);
				}
				$.ajax({
					type:"POST",
					url:url,
					data:{
						'csrfmiddlewaretoken' : csrf_token,
						'resend_otp' : true
					}
				});
				$("#display_msg").html("New OTP has been sent successfully on "+$(this).attr('data-mask_mobile_no'));
			}
		});

		$("#verifyOTPForm").submit(function(e){
			e.preventDefault();
			$.ajax({
				type:"POST",
				url:url,
				data:{
					'csrfmiddlewaretoken' : csrf_token,
					'otp' : $("input[name=otp]").val(),
					'new_number' : new_mobile_no
				},
				success:function(data){
					if(data.is_verify){
						location.reload();
					}else{
						$("#invalid_otp_error").show();
					}
				}
			});
		});
});

	function startTimer() {
		minutes = parseInt(timer / 60, 10);
		seconds = parseInt(timer % 60, 10);
		minutes = minutes < 10 ? "0" + minutes : minutes;
		seconds = seconds < 10 ? "0" + seconds : seconds;

		$("#resend_otp").html("Resend OTP  "+minutes + ":" + seconds);

		if (--timer < 0) {
			enableResend = true;
			timer = 19;
			$("#resend_otp").html("Resend OTP");
			$("#resend_otp").css({'color':'green'});
			clearInterval(getTimer);
		}
	}

