#!/bin/bash

# Get token from checkin API
token=`curl -s --data "user=teste&pwd=@bC12345" http://localhost:9000/engine/api/checkin_data | jq -r '.user_info.user_token'`
echo $token

if [ ${#token} -gt 0 ]
then 
	echo "passed!"
else
	echo "failed!"
fi

#test create authorisation
create_authorisation_res=`curl -s --data "username=teste&resource_type=teste&resource_name=teste&max=10&token=$token" http://localhost:9000/engine/api/create_authorisation | jq -r '.success'`
echo $create_authorisation_res
if [ "$create_authorisation_res" == "Rule successfully created." ]
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


