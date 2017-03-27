Feature: Test authentication functionalities

        As AAA Manager, I have authentication features that allows to
        manipulate user information.

        Scenario: Create user
                Given I have user information and application identification
                When I user is not repeated
                Then User is successfully created
        
        Scenario: Create user
                Given I have user information and application identification
                When I user is repeated
                Then User is not created and user string is returned
        
        Scenario: Create user
                Given I have user information and application identification
                When I user is admin
                Then User is not created and admin string is returned

        Scenario: Access application
                Given I have username and password
                When I access application
                Then I get user information 

        Scenario: Get token
                Given I have valid application ID and user information
                When I consult token
                Then I get valid token

