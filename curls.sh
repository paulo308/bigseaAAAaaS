#!/bin/bash

# Call sign up API
signup_res=`curl -s --data "user=teste&pwd=@bC12345&fname=teste&lname=teste&email=teste@teste.com" http://localhost:9000/engine/api/signup_data | jq -r '.success'`
echo $signup_res

if [ "$signup_res" == "User signed up with success." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi

# Get token from checkin API
token=`curl -s --data "user=teste&pwd=@bC12345" http://localhost:9000/engine/api/checkin_data | jq -r '.user_info.user_token'`
echo $token

if [ ${#token} -gt 0 ]
then 
	echo "passed!"
else
	echo "failed!"
fi

#test favorite creation
create_favorite_res=`curl -s --data "username=teste&item_id=b&item_type=a&city_id=1&country_id=2&favorite_id=b&data=aaa&token=$token" http://localhost:9000/engine/api/create_favorite | jq -r '.success'`
echo $create_favorite_res
if [ "$create_favorite_res" == "Favorite association successfully created." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi

#test read favorite
read_favorite_res=`curl -s --data "username=teste&city_id=1&country_id=2&token=$token" http://localhost:9000/engine/api/read_favorite | jq -r '.success'`
echo $read_favorite_res
if [ "$read_favorite_res" == "Favorite association successfully read." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi

#test favorite deletion
delete_favorite_res=`curl -s --data "username=teste&item_id=b&token=$token" http://localhost:9000/engine/api/delete_favorite | jq -r '.success'`
echo $delete_favorite_res
if [ "$delete_favorite_res" == "Favorite association successfully deleted." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi
delete_favorite_res=`curl -s --data "username=teste&item_id=b&token=$token" http://localhost:9000/engine/api/delete_favorite | jq -r '.success'`
echo $delete_favorite_res
if [ "$delete_favorite_res" == "Favorite association successfully deleted." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi

#test send_email token
email_token=`curl -s --data "username=teste&email=eduardo.morais@gmail.com" http://localhost:9000/engine/api/send_email_token | jq -r '.success'`
echo $email_token
if [ "$email_token" == "Email successfully sent." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi

#test email confirmation
email_confirmation_res=`curl -s --data "username=teste&email=eduardo.morais@gmail.com&token=$email_token" http://localhost:9000/engine/api/email_confirmation | jq -r '.success'`
echo $email_confirmation_res
if [ "$email_confirmation_res" == "User email confirmed with success." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi

#test use resource
use_resource_res=`curl -s --data "username=teste&resource_name=teste&token=$token" http://localhost:9000/engine/api/use_resource | jq -r '.success'`
echo $use_resource_res
if [ "$use_resource_res" == "User is authorised." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi

#test read accounting
read_accounting_res=`curl -s --data "username=teste&token=$token" http://localhost:9000/engine/api/read_accounting | jq -r '.success'`
echo $read_accounting_res
if [ "$read_accounting_res" == "User accounting information read successfully." ]
then
	echo 'passed!'
else
	echo 'failed!'
fi


