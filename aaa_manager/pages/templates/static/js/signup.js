$(function() {
    $('#error').hide();
    $('#success').hide();
    $( "#btn_signup" ).click(function() {
        console.log('ok2');
        var f = $('#registerform');
	f.parsley().validate();
	if (f.parsley().isValid()) {
		console.log('data input is valid. proceed to submit form');
		signup();
	} else {
		console.log('data validation failed');
	}
    });
});

function CloseMySelf(data) {
        //console.log(data);
        console.log('Ready to send answer and close!');
        try {
		window.opener.postMessage(data, '*');
                window.opener.HandlePopupResult(data);
                //window.opener.HandlePopupResult(sender.getAttribute(data));
                console.log(data);
                console.log('Sent the answer!');
            }
            catch (err) {}
            window.close();
            return false;
}

var view_data;

function signup(){
    $.ajax({
        url: '/engine/api/signup_data',
        type: 'post',
        data: {'user': $('#user').val(), 'pwd': $('#password1').val(), 'fname': $('#fname').val(), 'lname': $('#lname').val(), 'email': $('#email').val()},
        success: function (result) {
	    view_data = result;
	    console.log(result);
            console.log(result['error']);
	    //CloseMySelf(view_data);
	    error = result['error'];
            if (error) {
		//alert(error);
		$('#success').text('');
		$('#success').hide();
		$('#error').text(error);
		$('#error').show();
            } else {
		msg = "Signed up with success!";
		$('#error').text('');
		$('#error').hide();
		$('#success').text(msg);
		$('#success').show();
		setTimeout(function()
                {
                	CloseMySelf(view_data); 
                }, 1000);
	    }
        }
    });
}

