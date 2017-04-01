
$(function() {
  // Handler for .ready() called.
  console.log('ok1');
//  insert_user();
});

function get_apps(){

}

function get_users(app_id){

}

function insert_user(){
	$.ajax({
            url: '/engine/api/checkin_data',
            type: 'post',
            dataType: 'json',
            data: {},
            success: function (result) {
                console.log(result)
            },
        });
}


function openWin(url, w, h)
{
	console.log('openwindow');
	var left = (screen.width/2)-(w/2);
	var top = (screen.height/2)-(h/2);
	w=window.open(url, '_blank');
	w.focus();
}

var answer_data;

function HandlePopupResult(answer_data) {
	console.log('Received the answer!');
	console.log(answer_data);
	//From here, take care of answer.
}
