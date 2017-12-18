#!/bin/bash

domain=$1

function call() {
	res=`curl -s --data "$1" $domain/engine/api/$2 | jq -r '.success'`
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
	token=`curl -s --data "$1" $domain/engine/api/checkin_data | jq -r '.user_info.user_token'`
	echo $token

	if [ ${#token} -gt 0 ]
	then 
		echo "passed!"
	else
		echo "failed!"
	fi
}

function checkout() {
	# Get token from checkin API
	token=`curl -s --data "token=$token" $domain/engine/api/checkout_data | jq -r '.user_info.user_token'`
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
	email_token=`curl -s --data "$1" $domain/engine/api/send_email_token | jq -r '.success'`
	echo $email_token
	if [ "$email_token" == "Email sent with success." ]
	then
		echo 'passed!'
	else
		echo 'failed!'
	fi
}

function test_manage_user() {
	get_token "user=teste&pwd=@bC12345"
	call "user=teste&fname=teste_new&lname=teste_new&email=eduardo.morais@gmail.com&stayin=true&token=$token" "update_user" "User information updated successfully."
	call "user=teste&token=$token" "delete_user" "User deleted with success."

}

function test_signup() {
	call "user=teste&pwd=@bC12345&fname=teste&lname=teste&email=eduardo.morais@gmail.com" "signup_data" "User signed up with success."
	get_token "user=teste&pwd=@bC12345"
	if [ "$token" == "null" ]
	then
		echo 'null token!'
	else
		call "token=$token" "read_user_info" "User info read successfully."
		checkout "token=$token"
	fi
}

function test_favorite() {
	get_token "user=teste&pwd=@bC12345"
	call "username=teste&resource_category=Software&resource_name=Favorites&max=10&token=$token" "create_authorisation" "Rule successfully created."
	call "username=teste&item_id=l&item_type=a&city_id=1&country_id=2&favorite_id=b&data=aaa&token=$token" "create_favorite" "Favorite association successfully created."
	call "username=teste&city_id=1&country_id=2&token=$token" "read_favorite" "Favorite association successfully read." 
	call "username=teste&token=$token" "read_favorites" "Favorite association successfully read." 
	call "username=teste&token=errado" "read_favorites" "Invalid token." 
	call "username=errado&token=$token" "read_favorites" "Invalid username." 
	call "username=teste&item_id=b&token=$token" "delete_favorite" "Favorite association successfully deleted."
	#call "username=teste&item_id=b&token=$token" "delete_favorite" "Favorite association successfully deleted."
}

function test_email() {
	send_email_token "username=teste2&email=eduardo.morais@gmail.com"
	call "username=teste2&email=eduardo.morais@gmail.com&token=$email_token" "email_confirmation" "User email confirmed with success."
}

function test_email_association() {
	get_token "user=teste2&pwd=@bC12345"
	call "username=teste2&email=teste@teste.com&token=$token" "create_email" "Email association successfully created."	
	# test now if system detects repetition
	call "username=teste2&email=teste@teste.com&token=$token" "create_email" "Invalid email."	
	call "username=teste2&token=$token" "read_emails" "Email association successfully read."
	call "username=teste2&email=teste@teste.com&token=$token" "delete_email" "Email association successfully deleted."
}

function test_email_checkin() {
	get_token "user=teste2&pwd=@bC12345"
	call "username=teste2&email=eduardo.morais@gmail.com&token=$token" "create_email" "Email association successfully created."	
	# next call returns user info and corresponding token
	call "email=eduardo.morais@gmail.com" "email_checkin" "Email checkin with success."
	
}

function test_authorisation() {
	get_token "user=teste2&pwd=@bC12345"
	call "username=teste2&resource_category=teste&resource_name=teste&max=10&token=$token" "create_authorisation" "Rule successfully created."
	call "username=teste2&token=$token" "read_authorisations" "Rules read successfully."
	call "username=teste2&resource_category=teste&resource_name=teste&token=$token" "read_authorisation" "Rule information read successfully."
	call "username=teste2&resource_category=teste&resource_name=teste&max=20&token=$token" "update_authorisation" "Rule successfully updated."
	call "username=teste2&resource_category=teste&resource_name=teste&token=$token" "delete_authorisation" "Rule successfully deleted."
}

function test_use_resource() {
	get_token "user=teste2&pwd=@bC12345"
	call "username=teste2&resource_name=teste&resource_category=teste&max=10&token=$token" "create_authorisation" "Rule successfully created."
	call "username=teste2&resource_name=teste&resource_category=teste&token=$token" "use_resource" "User is authorised."
	call "username=teste2&token=$token" "read_accounting" "User accounting information read successfully."
}

function test_forgot_password() {
	call "username=teste2&email=eduardo.morais@gmail.com" "forgot_password" "Email sent with success." 
}

function test_infra() {
	call "username=teste2&principal=teste&secret=teste" "insert_data_infra" "Infra data successfully created." 
	call "username=teste2&pwd=@bC12345" "checkin_data_infra" "Infra data successfully read." 
}

#test_signup
test_favorite
#test_email_association
#test_email
#test_use_resource
#test_manage_user
#test_forgot_password
#test_infra




