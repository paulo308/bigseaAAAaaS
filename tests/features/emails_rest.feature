@rest
Feature: Email information REST API unit tests

	Scenario: Create email
		Given I have correct query string parameters username and email
		When I call create email RESP API service
		Then I receive expected success response from email association

		
