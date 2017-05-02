Feature: The Protection tab is selected

    These tests are to check if the "Protection" tab is fully functional and works correctly.
    
    Background: 
        Given the application has been started
        
      Scenario: Entering non-digit values
         Given the user wants to change a "Protection" tab parameter and the user enters the non-digit value
         Then the "Protection" tab parameter cannot accept non-digit values
        
     Scenario: Emptying the "Protection" tab text field
         Given the user wants to change the protection parameter and the user deletes the value in the text field
         Then the protection text field stays at value = 0
         
     Scenario: Enabling protection settings
         Given the enable checkbox is checked 
         Then the warning limit, fault limit, delay, no. of retries and type of response are enabled
         
     Scenario: Disabling protection settings
         Given the enable checkbox is not checked 
         Then the warning limit, fault limit, delay, no. of retries and type of response are disabled
         
	 Scenario: Selecting "Continue" type of response
	     Given the "Continue" type of response is selected
	     Then the delay and number of retries are disabled
	     
	 Scenario: Selecting "Delay and retry" type of response
	     Given the "Delay and retry" type of response is selected
	     Then the delay and number of retries are enabled
	     
	 Scenario: Selecting "Retry only" type of response
	     Given the "Retry only" type of response is selected
	     Then the delay is disabled and number of retries is enabled
	     
	 Scenario: Selecting "Device shutdown" type of response
	     Given the "Device shutdown" type of response is selected
	     Then the delay and number of retries are disabled
	     
	 Scenario Outline: Entering to high protection value
         Given the user wants to change the protection parameter and the user enters too big '<value>'
         Given the user wants to change the power-ok parameter and the user enters too big '<value2>'
         Given the user wants to change the vin on/off parameter and the user enters too big '<value3>'
         Then the tooltip displays that the protection value entered is too big
         Examples:
         	| value      | value2     | value3  |
	        | 176        | 5.26       | 34      |
	        | 175.01     | 5.30       | 21.0    |
	        | 240        | 16         | 20.01   |
         	
     Scenario Outline: Entering warning value bigger or equal to fault value for OV
         Given the user wants to change the protection parameter of OV and the user enters warning '<w_value>' bigger or equal to fault '<f_value>'
         Then the tooltip displays that the warning value has to be less than fault value
         Examples:
         	| w_value      | f_value     |
	        | 5.27         | 5.26        |
	        | 2            | 1           |
	        | 1.30         | 1.30        |
	     
	 Scenario Outline: Entering warning value smaller or equal to fault value for UV
         Given the user wants to change the protection parameter of UV and the user enters warning '<w_value>' smaller or equal to fault '<f_value>'
         Then the tooltip displays that the warning value has to be bigger than fault value
         Examples:
         	| w_value      | f_value     |
	        | 45           | 46          |
	        | 23.01        | 23.02       |
	        | 15.68        | 15.68       |
