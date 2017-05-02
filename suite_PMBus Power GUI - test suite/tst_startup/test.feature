Feature: Starting application

    These tests are to determine what happens when the application starts.
    
    Background: 
        Given the application has been started

    Scenario: PMBus device is not available
        Given the PMBus device is not available
        Then the parameters are filled with 0.00
        Then all buttons are disabled

    Scenario: PMBus device is available
        Given the PMBus device is available
        Then the parameters are filled with information stored in the PMBus device