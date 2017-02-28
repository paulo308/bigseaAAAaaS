
$(function() {
  // Handler for .ready() called.
  console.log('ok1');
  insert_user();
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
