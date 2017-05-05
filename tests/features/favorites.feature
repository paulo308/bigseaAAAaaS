Feature: Test secondary favorite functionalities

	As AAA Manager, I have favorite information associated to username. 
	I must be able to manager this information.

	Scenario: Create favorite
		Given I have correct username and favorite
		When I create favorite
		Then I create favorite successfully 
	
	Scenario: Read favorite
		Given I have correct username and city id and country_id
		When I read favorite
		Then I read favorite successfully 
	
	Scenario: Delete favorite
		Given I have correct username and favorite id
		When I delete favorite
		Then I delete favorite successfully 
