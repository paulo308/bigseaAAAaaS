Feature: Test secondary favorite functionalities

	As AAA Manager, I have favorite information associated to username. 
	I must be able to manager this information.

	Scenario: Create favorite
		Given I have correct username and favorite
		When I create favorite
		Then I create favorite successfully 
