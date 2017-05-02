Feature: The Tuning tab is selected

    These tests are to check if the "Tuning" tab is fully functional and works correctly.
    
    Background: 
        Given the application has been started
        
     Scenario: Entering non-digit values
         Given the user wants to change a "Tuning" tab parameter and the user enters the non-digit value
         Then the "Tuning" tab parameter cannot accept non-digit values
        
     Scenario: Emptying the normal text field
         Given the user wants to change the tuning parameter and the user deletes the value in the text field
         Then the tuning text field stays at value = 0
         
     Scenario: Emptying the hexadecimal text field
         Given the user wants to change the tuning parameter when hex number is expected and the user deletes the value in the text field
         Then the tuning hex text field stays at value = 0x0000
         
     Scenario Outline: Entering real world value to Linear Converter L11
         Given the user selects "Tuning" tab
         When the user enters the '<real_world_value>' to Linear Converter L11
         Then the calculated encoded '<hex_value>' displays in position
         Examples:
	        | real_world_value | hex_value |
	        | 16.1             | 0xda03    |
	        | 20               | 0xda80    |
	        | 9.43             | 0xd25b    |
	        | 0.00             | 0x8000    |
         
     Scenario Outline: Entering encoded hex value to Linear Converter L16
         Given the user selects "Tuning" tab
         When the user enters the encoded '<hex_value>' to Linear Converter L16
         Then the calculated '<real_world_value>' displays in position
         Examples:
	        | real_world_value | hex_value |
	        | 1.39             | 0x2c7a    |
	        | 1.50             | 0x3000    |
	        | 1.10             | 0x2333    |
	        | 0.00             | 0x0       |
         
     Scenario Outline: Selecting PMBus command from Direct Access Functions box
         When the user selects an '<option>' from Direct Access Function combo-box
         Then the '<code>' in hex of this command displays in position
         And the '<size>' in bytes displays in position
         And the rest of the text fields stays with values 0 or 0x
         When the user presses the Read button
         Then the values in '<decimal>', '<hex>', '<L11>' and '<L16>' are displayed in positions
         Examples:
         	| option                     |  code     | size   |  decimal  |  hex     |  L11       |  L16   |
         	| VOUT\\_COMMAND             |  0x21     | 2      |  10650    |  0x299a  |  13120.00  |  1.30  |
         	#| VIN\\_OV\\_FAULT\\_LIMIT   |  0x55     | 2      |  55822    |  0xda0e  |  16.44     |  6.81  |
         	#| POWER\\_GOOD\\_ON          |  0x5e     | 2      |  10040    |  0x2738  |  -3200.00  |  1.23  |
         	#| READ\\_FREQUENCY           |  0x95     | 2      |  800      |  0x0320  |  800.00    |  0.10  |
         	
         
     Scenario: Writing in Direct Access
         Given the user wants to write a value to particular PMBus command and the user enters a value to write in hex
         When the user presses the Write button
         Then the write command is send to the device and the new value is stored in the device
         

        
