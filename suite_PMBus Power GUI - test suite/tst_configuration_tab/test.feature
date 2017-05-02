Feature: The Configuration tab is selected

    These tests are to check if the "Configuration" tab is fully functional and works correctly.
    
    Background: 
        Given the application has been started
        
     Scenario: Entering non-digit values
         Given the user wants to change a "Configuration" tab parameter and the user enters the non-digit value
         Then the "Configuration" tab parameter cannot accept non-digit values
        
     Scenario: Emptying the "Configuration" tab text field
         Given the user wants to change the startup/shutdown parameter and the user deletes the value in the text field
         Then the "Configuration" tab text field stays at value = 0
         
     Scenario Outline: Entering to high value in "Configuration" tab
     	 Given the user wants to change the startup/shutdown parameter and the user enters too big '<value>'
         Given the user wants to change the vout on/off parameter and the user enters too big '<vout_value>'
         Then the tooltip displays that the startup/shutdown value entered is too big
         Examples:
         	| value           | vout_value |
	        | 5001            | 5.26       |
	        | 5000.1          | 5.30       |
	        | 7000            | 7          |
     
     Scenario: Selecting Device Startup - Control Pin
         Given the user wants to select Device Startup option from the combo-box 
         And the user selects CTRL_POS or CTRL_NEG
         When the user opens the Monitoring tab
         Then the Control Pin button is enabled
         And OPERATION_CMD button is disabled
         And OPERATION_CMD functions combo-box is disabled
         
    Scenario: Selecting Device Startup - OPERATION_CMD
         Given the user wants to select Device Startup option from the combo-box 
         And the user selects OPERATION_CMD
         When the user opens the Monitoring tab
         Then the OPERATION_CMD button is enabled
         And Control Pin button is disabled  
         And OPERATION_CMD functions combo-box is enabled
         
         

        
