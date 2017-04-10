@rest
Feature: Test REST API

	As AAA MAnager, I have a REST API that is used to access services.

	Scenario: Signup
		Given I have correct user information
		When I signup
		Then I signup successfully
	
	Scenario: Signup
		Given I have wrong user information
		When I signup
		Then I receive expected signup error message
	
	Scenario: Checkin
		Given I have user credential
		When I checkin
		Then I checkin successully
	
	Scenario: Checkin
		Given I have wrong user credential
		When I checkin
		Then I receive expected checkin error message
	
	Scenario: Checkout
		Given I have correct user token
		When I checkout
		Then I checkout successfully

	Scenario: Checkout
		Given I have wrong user token
		When I checkout
		Then I receive expected checkout error message

	Scenario: Update user
		Given I have new user information and a valid token
		When I update user using REST API
		Then I update user successfully using REST API

	Scenario: Update user
		Given I have wrong new user information or an invalid token
		When I update user using REST API
		Then I receive corresponding update user error message
	
	Scenario: Delete user
		Given I have correct user information and a valid token
		When I delete user using REST API
		Then I delete user successfully using REST API

	Scenario: Delete user
		Given I have wrong user information and a valid token
		When I delete user using REST API
		Then I receive corresponding delete user error message

	Scenario: Email confirmation
		Given I have valid username and email token
		When I call the email confirmation REST API
		Then I receive expected email confirmation message
