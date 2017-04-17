
$(function() {
    $('#error').hide();
    $('#success').hide();
    $( "#btn_login" ).click(function() {
        console.log('ok2');
	var fsignin = $('#signinform');
	fsignin.parsley().validate();
	if (fsignin.parsley().isValid()) {
		console.log('data input is valid. proceed to submit login form');
		login();
	} else {
		console.log('data validation failed');
	}
    });
});


var view_data;
var destination = 'https://eubrabigsea.dei.uc.pt/web/manage_info_user'
//use condition to determine wether user is admin or normal user to define the destination endpoint

var newpage;

function SendInfoManUserPage(data) {
	//console.log(data);
        console.log('Ready to send answer and close!!!!!!!!!');
	try {
		//window.location = destination;
		newpage = window.open(destination);
		setTimeout(function()
		{
			newpage.postMessage(data,destination);
		}, 500);
		//newpage.postMessage(data, destination);

		//window.opener.HandlePopupResult(data);
		//window.opener.HandlePopupResult(sender.getAttribute(data));
		console.log(data);
		console.log('Sent the answer!');
            }
            catch (err) {}
            //window.close();
	    // not necessary for now
            return false;
	}

function login(){
    $.ajax({
        url: '/engine/api/checkin_data',
        type: 'post',
        data: {'user': $('#user').val(), 'pwd': $('#pwd').val()},
        success: function (result) {
		view_data = result;
                console.log(result);
		console.log(view_data);
                console.log(result['error']);
		//SendInfoManUserPage(view_data);
		error = result['error'];
		if (error) {
			//alert(error);
			$('#success').text('');
			$('#success').hide();
			$('#error').text(error);
			$('#error').show();
                } else {
                   	msg = "Authenticated with success!";
			$('#error').text('');
			$('#error').hide();
			$('#success').text(msg);
			$('#success').show();
			setTimeout(function()
                        {
                                SendInfoManUserPage(view_data); 
                        }, 1000);
                }
        }
    });
}
