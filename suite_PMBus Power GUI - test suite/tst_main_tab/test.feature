Feature: The Main Tab is selected

    These tests are to check if the "Main" tab is fully functional and works correctly.
    
    Background: 
        Given the application has been started
        
     Scenario: Entering non-digit values
         Given the user wants to change a "Main" tab parameter and the user enters the non-digit value
         Then the "Main" tab parameter cannot accept non-digit values
        
     Scenario: Emptying the text field
         Given the user wants to change a main tab parameter and the user deletes the value in the text field
         Then the "Main" tab text field stays at value = 0
         
     Scenario Outline: Entering to high value
         Given the user wants to change a main tab parameter and the user enters too big '<value>'
         Then the font colour becomes red
         Then the tooltip displays that the value entered is too big
         Examples:
         	| value | 
	        | 50.1  |
	        | 51    | 
	        | 60    |
	        | 145   | 

        
