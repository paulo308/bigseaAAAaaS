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

function test_use_resource() {
	get_token "user=teste&pwd=@bC12345"
	call "username=teste&resource_type=teste&resource_name=teste&max=10&token=$token" "create_authorisation" "Rule successfully created."
	call "username=teste&resource_name=teste&token=$token" "use_resource" "User is authorised."
	call "username=teste&token=$token" "read_accounting" "User accounting information read successfully."
}

test_use_resource

