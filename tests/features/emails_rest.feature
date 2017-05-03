@rest
Feature: Favorite information REST API unit tests

	Scenario: Create favorite
		Given I have correct query string parameters username and favorite
		When I call create favorite RESP API service
		Then I receive expected success response from favorite association

		
