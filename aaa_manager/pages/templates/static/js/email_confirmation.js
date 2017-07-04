function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}


$(function() {
	values = getUrlVars(); 
	console.log('username: ' + values['username'].toString()); 
	console.log('token: ' + values['token'].toString()); 
	console.log('email: ' + values['email'].toString()); 
	$.ajax({
            url: '/engine/api/email_confirmation',
            type: 'post',
            dataType: 'json',
            data: {'username': values['username'], 'email': values['email'], 'token': values['token']},
            success: function (result) {
		if (result['success'] != ''){
                	console.log(result['success']);
			$('#divResult').text(result['success']);
		}
		else if (result['error'] != '') {
                	console.log(result['error']);
			$('#divResult').text(result['success']);
		}
            },

        });
});
