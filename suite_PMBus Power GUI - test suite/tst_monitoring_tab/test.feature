Feature: The Monitoring Tab is selected

    These tests are to check if the "Monitoring" tab is fully functional and works correctly.
    
    Background: 
        Given the application has been started
        
     Scenario: Pressing "Clear Faults" button
         When the user presses the "Clear Faults" button
         Then the command is written to the device and all bits setted for warning or fault becomes cleared
         
     Scenario: Pressing "Control Pin"
         Given the "Control Pin" is enabled
         When the user presses the Control Pin button
         Then the device turns on/off and the plot displays rise/fall of the device in real time
         
     Scenario: Pressing "OPERATION_CMD"
         Given the "OPERATION_CMD" is enabled
         When the user presses the OPERATION_CMD button
         Then the device turns on/off and the plot displays rise/fall of the device in real time
	     
	 Scenario: Selecting "OPERATION_CMD" setting
	     Given the "OPERATION_CMD" is enabled
	     When the user selects the OPERATION_CMD option
	     Then the correct value is written to the device and the device turns off with different setting
	     
     Scenario: Pressing "Monitoring" button
         When the user presses the "Monitoring" button  
         Then the real time plots start/stop
         And the led turns red when turned off and turns green when turned on
         
     Scenario: Pressing "Write volatile" button
         When the user presses the "Write volatile" button
         Then all parameters from the GUI are saved in to the devices volatile memory

        
