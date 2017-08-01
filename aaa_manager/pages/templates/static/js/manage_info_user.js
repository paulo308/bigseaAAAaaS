var source = 'https://eubrabigsea.dei.uc.pt/web/manage_info_auth'
var token;
var object;

$(function() {
    $('#error').hide();
    $('#success').hide();
    window.addEventListener("message", postMessageHandler, false);
    //window.addEventListener('message', function(event) {
    //  alert(`Received ${event.data} from ${event.origin}`);
    //});

    $( "#btn_save" ).click(function() {
        console.log('clickSave');
	var f = $('#updateform');
	f.parsley().validate();
	if (f.parsley().isValid()) {
		console.log('data input is valid. proceed to submit form and update records');
		updateInfo();
	} else {
		console.log('user info validation failed');
	}
    });

    $( "#btn_delete" ).click(function() {
        console.log('clickDelete');
	var f = $('#updateform');
        f.parsley().validate();
        if (f.parsley().isValid()) {
                console.log('data input is valid. proceed to submit form and delete account');
                var r = confirm('Are you sure you want to delete your account? This action is irreversible.');
		if (r == true) {
			deleteAccount();
		}
        } else {
                console.log('delete failed');
        }
    });

    $( "#btn_changepassword" ).click(function() {
        console.log('clickChangePW');
	var f = $('#passwordform');
	f.parsley().validate();
        if (f.parsley().isValid()) {
                console.log('passwords are valid. proceed to submit form and change password');
                changePW();
		//console.log('old pwd:',$('#password'));
		//console.log('new pwd:',$('#password1'));
        } else {
                console.log('password validation failed');
        }
    });


    $( "#btn_addemail" ).click(function() {
        console.log('clickAddEmail');
        var f = $('#addemailform');
        f.parsley().validate();
        if (f.parsley().isValid()) {
                console.log('email is valid. proceed to submit form and add secondary email');
		console.log('sec email:',$('#secemail'));
                addEmail();
        } else {
                console.log('email validation failed');
        }
    });
});



function postMessageHandler( event ) {
	console.log("Received info from user to update data.");
  	console.log("* Message:", event.data);
  	console.log("* Origin:", event.origin);
  	console.log("* Source:", event.source);

	token = event.data.user_info.user_token;
	console.log("* Token", event.data.user_info.user_token);
	object = event.data;

	$('#user').val(event.data.user_info.user.username)
	$('#email').val(event.data.user_info.user.email)
	$('#fname').val(event.data.user_info.user.fname)
	$('#lname').val(event.data.user_info.user.lname)
	$('#token').val(event.data.user_info.user_token)

	// check request is from legitimate source and message is expected or not
  	if ( event.origin !== source ) { return; }
    	// give response
    	//in case I want to send a reply to auth page, do it here
	// but handle the response there
	//event.source.postMessage( 'response', 'http://eubrabigsea.dei.uc.pt/web/manage_info_auth' );

    	}




function updateInfo(){
    var newtoken0;
    newtoken0 = String(token);
    $.ajax({
        url: '/engine/api/update_user',
        type: 'post',
        data: {'user': $('#user').val(), 'fname': $('#fname').val(), 'lname': $('#lname').val(), 'email': $('#email').val(), 'token': newtoken0},
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
		msg = "Updated with success!";
		$('#error').text('');
		$('#error').hide();
		$('#success').text(msg);
		$('#success').show();
	    }
        }
    });
}

function deleteAccount(){
    var newtoken;
    newtoken = String(token);

    $.ajax({
        url: '/engine/api/delete_user',
        type: 'post',
        data: {'user': $('#user').val(), 'token': newtoken},
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
                msg = "Account permanently deleted!";
                $('#error').text('');
                $('#error').hide();
                $('#success').text(msg);
                $('#success').show();
            }
        }
    });
}

function changePW(){
    var newtoken2;
    newtoken2 = String(token);
    $.ajax({
        url: '/engine/api/change_password',
        type: 'post',
        data: {'user': $('#user').val(), 'oldpwd': $('#pwd').val(), 'newpwd': $('#password1').val(), 'token': newtoken2},
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
                msg = "Password changed with success!";
                $('#error').text('');
                $('#error').hide();
                $('#success').text(msg);
                $('#success').show();
            }
        }
    });
}


function addEmail(){
    var newtoken3;
    newtoken3 = String(token);
    $.ajax({
        url: '/engine/api/create_email',
        type: 'post',
        data: {'username': $('#user').val(), 'email': $('#secemail').val(), 'token': newtoken3},
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
                msg = "Email added with success!";
                $('#error').text('');
                $('#error').hide();
                $('#success').text(msg);
                $('#success').show();
            }
        }
    });
}
