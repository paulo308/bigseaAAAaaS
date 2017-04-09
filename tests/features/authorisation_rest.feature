@rest
Feature: Authorisation REST API unit tests

	Scenario: Create rule
		Given I have correct query string parameters username, resource name and rule
		When I call create rule RESP API service
		Then I receive expected success response

		
