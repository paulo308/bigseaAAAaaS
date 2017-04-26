Feature: Test secondary email functionalities

	As AAA Manager, I have email information associated to username. 
	I must be able to manager this information.

	Scenario: Create email
		Given I have correct username and email
		When I create email
		Then I create email successfully 
