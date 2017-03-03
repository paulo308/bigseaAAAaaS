
$(function() {
    $( "#btn_login" ).click(function() {
        login();
    });
    $( "#btn_verify_token" ).click(function() {
        verify_token();
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

function verify_token(){
    $.ajax({
        url: '/engine/api/verify_token',
        type: 'post',
        data: {'user': $('#usr').val(), 'pwd': $('#pwd').val(), 'token': $('#token').val()},
        success: function (result) {
            console.log(result)
        }
    });
}
