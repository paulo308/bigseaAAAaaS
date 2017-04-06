var source = 'https://eubrabigsea.dei.uc.pt/web/manage_info_auth'

$(function() {
    $('#error').hide();
    $('#success').hide();
    window.addEventListener("message", postMessageHandler, false);
    //window.addEventListener('message', function(event) {
    //  alert(`Received ${event.data} from ${event.origin}`);
    //});
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


var source = 'https://eubrabigsea.dei.uc.pt/web/manage_info_auth'

function postMessageHandler( event ) {
	console.log("Received info from user to update data.");
  	console.log("* Message:", event.data);
  	console.log("* Origin:", event.origin);
  	console.log("* Source:", event.source);

//	for (element in event.data.user_info.user){
		//document.write('<input type="text" name="'+ element + '" value="' + event.data.user_info.user[element] + '">')
	$('#user').val(event.data.user_info.user.username)
	$('#email').val(event.data.user_info.user.email)
	$('#fname').val(event.data.user_info.user.fname)
	$('#lname').val(event.data.user_info.user.lname)
//	}
//	user
//	email
//	fname
//	lname

	// check request is from legitimate source and message is expected or not
  	if ( event.origin !== source ) { return; }
    	// give response
    	//in case I want to send a reply to auth page, do it here
	// but handle the response there
	//event.source.postMessage( 'response', 'http://eubrabigsea.dei.uc.pt/web/manage_info_auth' );
    	}




function signup(){
    $.ajax({
        url: '/engine/api/signup_data',
        type: 'post',
        data: {'user': $('#user').val(), 'pwd': $('#password1').val(), 'fname': $('#fname').val(), 'lname': $('#lname').val(), 'email': $('#email').val()},
        success: function (result) {
	    view_data = result;
	    console.log(result);
            console.log(result['error']);
	    CloseMySelf(view_data);
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
	    }
        }
    });
}

