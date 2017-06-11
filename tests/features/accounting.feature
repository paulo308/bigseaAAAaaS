Feature: Test accounting functionalities

	As AAA Manager, I have accounting records associated to 
	system resources and users. I must be able to manager this 
	records.

	Scenario: Create record
		Given I have correct username, message and category
		When I create accounting
		Then I create record successfully 
