
$(function() {
    $( "#btn_login" ).click(function() {
        console.log('ok2');
        login();
    });
});

function get_apps(){

}

function get_users(app_id){

}

function login(){
    $.ajax({
        url: '/engine/api/checkin_data',
        type: 'post',
        data: {'user': $('#usr').val(), 'pwd': $('#pwd').val()},
        success: function (result) {
            console.log(result)
        }
    });
}
