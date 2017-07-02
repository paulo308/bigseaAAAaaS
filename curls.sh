#!/bin/bash

function call() {
	res=`curl -s --data "$1" http://localhost:9000/engine/api/$2 | jq -r '.success'`
	echo $res

	if [ "$res" == "$3" ]
	then
		echo 'passed!'
	else
		echo 'failed!'
	fi
}

function get_token() {
	# Get token from checkin API
	token=`curl -s --data "$1" http://localhost:9000/engine/api/checkin_data | jq -r '.user_info.user_token'`
	echo $token

	if [ ${#token} -gt 0 ]
	then 
		echo "passed!"
	else
		echo "failed!"
	fi
}

function send_email_token() {
	#test send_email token
	email_token=`curl -s --data "$1" http://localhost:9000/engine/api/send_email_token | jq -r '.success'`
	echo $email_token
	if [ "$email_token" == "Email sent with success." ]
	then
		echo 'passed!'
	else
		echo 'failed!'
	fi
}


function test_signup() {
	call "user=teste&pwd=@bC12345&fname=teste&lname=teste&email=teste@teste.com" "signup_data" "User signed up with success."
	get_token "user=teste&pwd=@bC12345"
}

function test_favorite() {
	call "username=teste&item_id=b&item_type=a&city_id=1&country_id=2&favorite_id=b&data=aaa&token=$token" "create_favorite" "Favorite association successfully created."
	call "username=teste&city_id=1&country_id=2&token=$token" "read_favorite" "Favorite association successfully read." 
	call "username=teste&item_id=b&token=$token" "delete_favorite" "Favorite association successfully deleted."
	#call "username=teste&item_id=b&token=$token" "delete_favorite" "Favorite association successfully deleted."
}

function test_email() {
	send_email_token "username=teste&email=eduardo.morais@gmail.com"
	call "username=teste&email=eduardo.morais@gmail.com&token=$email_token" "email_confirmation" "User email confirmed with success."
}

function test_use_resource() {
	get_token "user=teste&pwd=@bC12345"
	call "username=teste&resource_type=teste&resource_name=teste&max=10&token=$token" "create_authorisation" "Rule successfully created."
	call "username=teste&resource_name=teste&token=$token" "use_resource" "User is authorised."
	call "username=teste&token=$token" "read_accounting" "User accounting information read successfully."
}


test_signup
test_favorite
test_email
test_use_resource





