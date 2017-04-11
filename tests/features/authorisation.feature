Feature: Test authorisation functionalities

	As AAA Manager, I have authorisation rules that must be applied to 
	system resources. I must be able to manager this rules and resources.

	Scenario: Create rule
		Given I have correct username, resource name and rule
		When I create authorisation
		Then I create rule successfully 
