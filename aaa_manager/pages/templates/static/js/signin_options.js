var token;
var object;

$(function() {
    $('#error').hide();
    $('#success').hide();
    $( "#btn_reset_pw" ).click(function() {
        console.log('clickResetPW');
	var f = $('#forgotpwform');
	f.parsley().validate();
	if (f.parsley().isValid()) {
		console.log('email and user are valid. proceed to submit form and reset password');
		forgot_pw();
	} else {
		console.log('username or email validation failed');
	}
    });

   $( "#btn_resend_email" ).click(function() {
        console.log('clickResendEmail');
        var f = $('#resendemailform');
        f.parsley().validate();
        if (f.parsley().isValid()) {
                console.log('email and user are valid. proceed to submit form and resend confirmation email');
                resend_email();
        } else {
                console.log('username or email validation failed');
        }
    });

});

var view_data;

function forgot_pw(){
    $.ajax({
        url: '/engine/api/forgot_password',
        type: 'post',
        data: {'username': $('#user').val(), 'email': $('#email').val()},
        success: function (result) {
            view_data = result;
            console.log(result);
            console.log(result['error']);
            error = result['error'];
            if (error) {
                //alert(error);
                $('#success').text('');
                $('#success').hide();
                $('#error').text(error);
                $('#error').show();
            } else {
                msg = "Password reset with success!";
                $('#error').text('');
                $('#error').hide();
                $('#success').text(msg);
                $('#success').show();
            }
        }
    });
}


function resend_email(){
    $.ajax({
        url: '/engine/api/send_email_token',
        type: 'post',
        data: {'username': $('#user').val(), 'email': $('#email').val()},
        success: function (result) {
            view_data = result;
            console.log(result);
            console.log(result['error']);
            error = result['error'];
            if (error) {
                //alert(error);
                $('#success').text('');
                $('#success').hide();
                $('#error').text(error);
                $('#error').show();
            } else {
                msg = "Confirmation email sent!";
                $('#error').text('');
                $('#error').hide();
                $('#success').text(msg);
                $('#success').show();
            }
        }
    });
}
