Feature: Test authentication functionalities

        As AAA Manager, I have authentication features that allows to
        manipulate user information.

        Scenario: Create user
                Given I have user information and application identification
                When I user is not repeated
                Then User is successfully created
