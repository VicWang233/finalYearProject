import re
from collections import OrderedDict
from operator import itemgetter

###############################################################################################################
#                                                VERIFY                                                       #
#                                                                                                             #
#  Description: verifies object's state (enabled, checked, etc)                                               #
#  Arguments: object, 'enabled'/'checked' etc, 'True'/'False'                                                 #
#  Returns: none                                                                                              #
###############################################################################################################

def verify(object, propName, expected):
    
    actual = getattr(object, propName)
    
    if actual == expected:
        test.passes("Property {} has expected value".format(propName),
                    "Property value is '{}' as expected".format(expected))
    else:
        test.fail("Property {} does not have expected value!".format(propName),
                  "Expected '{}' but got '{}'".format(expected, actual))

###############################################################################################################
#                                            START THE AUT                                                    #
#                                                                                                             #
#  Description: start the AUT                                                                                 #
#  Arguments: none                                                                                            #
#  Returns: none                                                                                              #
###############################################################################################################
        
@Given("the application has been started")
def step(context):
    
    startApplication("main")

###############################################################################################################
#                                            STARTUP TESTS                                                    #
#                                                                                                             #
#  Description: startup steps to test                                                                         #
###############################################################################################################

@Given("the PMBus device is not available")
def step(context):
    
    mouseClick(waitForObject(":PMBus Power GUI.PMBus™ device\nnot connected!_QLabel"), 36, 120, 0, Qt.LeftButton)
    label = waitForObject(":PMBus Power GUI.PMBus™ device\nnot connected!_QLabel")
    label_text = label.text
    expected_text = "PMBus™ device\nnot connected!"
    test.compare(expected_text, label_text)                    
    pass

@Then("the parameters are filled with 0.00")
def step(context):
    
    main_widgets = {":Voltage.VOUT_QLineEdit": (40, 13),
                    ":Voltage.Margin High_QLineEdit": (25, 12),
                    ":Voltage.Margin Low_QLineEdit": (44, 12)
                    }
    
    configuration_widgets = {":Parameters.TON_DELAY:_QLineEdit": (34, 6),
                             ":Parameters.TOFF_DELAY:_QLineEdit": (30, 9),
                             ":Parameters.TON_RISE:_QLineEdit": (26, 15),
                             ":Parameters.TOFF_FALL:_QLineEdit": (38, 9),
                             ":Parameters.TON_MAX:_QLineEdit": (28, 11),
                             ":Parameters.TOFF_MAX:_QLineEdit": (25, 1),
                             ":Parameters.ON:_QLineEdit": (20, 12),
                             ":Parameters.OFF:_QLineEdit": (27, 6)
                             }
    
    protection_widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (85, 12),
                          ":PMBus Protection Parameters.V_QLineEdit": (67, 8),
                          ":PMBus Protection Parameters_QLineEdit": (82, 8),
                          ":PMBus Protection Parameters.V_QLineEdit_2": (52, 14),
                          ":PMBus Protection Parameters_QLineEdit_2": (72, 13),
                          ":PMBus Protection Parameters.V_QLineEdit_3": (42, 11),
                          ":PMBus Protection Parameters_QLineEdit_3": (77, 15),
                          ":PMBus Protection Parameters.V_QLineEdit_4": (55, 12),
                          ":PMBus Protection Parameters_QLineEdit_4": (84, 13),
                          ":PMBus Protection Parameters.A_QLineEdit": (57, 4),
                          ":PMBus Protection Parameters_QLineEdit_5": (85, 7),
                          ":PMBus Protection Parameters.°C_QLineEdit": (54, 8),
                          ":ON/OFF Levels.POWER OK_QLineEdit": (194, 10),
                          ":ON/OFF Levels.  _QLineEdit": (113, 11),
                          ":ON/OFF Levels.VIN_QLineEdit": (186, 7),
                          ":ON/OFF Levels.  _QLineEdit_2": (109, 13)
                          }
    
    for key, value in sorted(main_widgets.items()):
        mouseClick(waitForObject(key), value[0], value[1], 0, Qt.LeftButton)
        if value[0] == 40:
            expected_text = "0.00"
            test.compare(waitForObject(key).text, expected_text)
        else:
            expected_text = "0.0"
            test.compare(waitForObject(key).text, expected_text)
            
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))
    
    for key, value in sorted(configuration_widgets.items()):
        mouseClick(waitForObject(key), value[0], value[1], 0, Qt.LeftButton)
        expected_text = "0.00"
        test.compare(waitForObject(key).text, expected_text)
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    
    for key, value in sorted(protection_widgets.items()):
        mouseClick(waitForObject(key), value[0], value[1], 0, Qt.LeftButton)
        expected_text = "0.00"
        test.compare(waitForObject(key).text, expected_text)
    
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))
    mouseClick(waitForObject(":Real Time Readings.VIN:  0.00 V_QLabel"), 33, 9, 0, Qt.LeftButton)
    vin_real_time = waitForObject(":Real Time Readings.VIN:  0.00 V_QLabel").text
    expected_text = "VIN:  0.00 V"
    test.compare(vin_real_time, expected_text)
    
    mouseClick(waitForObject(":Real Time Readings.VOUT:  0.00 V_QLabel"), 41, 12, 0, Qt.LeftButton)
    vout_real_time = waitForObject(":Real Time Readings.VOUT:  0.00 V_QLabel").text
    expected_text = "VOUT:  0.00 V"
    test.compare(vout_real_time, expected_text)
    
    mouseClick(waitForObject(":Real Time Readings.IOUT:  0.00 A_QLabel"), 46, 13, 0, Qt.LeftButton)
    iout_real_time = waitForObject(":Real Time Readings.IOUT:  0.00 A_QLabel").text
    expected_text = "IOUT:  0.00 A"
    test.compare(iout_real_time, expected_text)
    
    mouseClick(waitForObject(":Real Time Readings.TEMP:  0.00 °C_QLabel"), 50, 15, 0, Qt.LeftButton)
    temp_real_time = waitForObject(":Real Time Readings.TEMP:  0.00 °C_QLabel").text
    expected_text = "TEMP:  0.00 °C"
    test.compare(temp_real_time, expected_text)
    pass

@Then("all buttons are disabled")
def step(context):
    
    verify(findObject(":Real Time Readings.Control Pin_QPushButton"), 'enabled', False)
    verify(findObject(":Real Time Readings.OPERATION_CMD_QPushButton"), 'enabled', False)
    verify(findObject(":Real Time Readings.Monitoring_QPushButton"), 'enabled', False)
    verify(findObject(":Real Time Readings.Write volatile_QPushButton"), 'enabled', False)
    verify(findObject(":Real Time Readings.Clear Faults_QPushButton"), 'enabled', False)
    clickButton(waitForObject(":PMBus Power GUI.Tuning_QToolButton"))
    verify(findObject(":Direct Access Functions.Read_QPushButton"), 'enabled', False)
    verify(findObject(":Direct Access Functions.Write_QPushButton"), 'enabled', False)
    
@Given("the PMBus device is available")
def step(context):
    
    mouseClick(waitForObject(":PMBus Power GUI.EM2130L\nStep-Down DC-DC\nSwitching Converter\nwith\nIntegrated Inductor,\nFeaturing\nDigital Control\nwith PMBus™ v1.2\ncompliant Interface\n_QLabel"), 39, 74, 0, Qt.LeftButton)
    label = waitForObject(":PMBus Power GUI.EM2130L\nStep-Down DC-DC\nSwitching Converter\nwith\nIntegrated Inductor,\nFeaturing\nDigital Control\nwith PMBus™ v1.2\ncompliant Interface\n_QLabel")
    label_text = label.text
    expected_text = "EM2130L\nStep-Down DC-DC\nSwitching Converter\nwith\nIntegrated Inductor,\nFeaturing\nDigital Control\nwith PMBus™ v1.2\ncompliant Interface\n"
    test.compare(expected_text, label_text)                    
    pass

@Then("the parameters are filled with information stored in the PMBus device")
def step(context):
    
    main_widgets = {":Voltage.VOUT_QLineEdit": (40, 13, "1.30"),
                    ":Voltage.Margin High_QLineEdit": (25, 12, "5.0"),
                    ":Voltage.Margin Low_QLineEdit": (44, 12, "5.0")
                    }
    
    configuration_widgets = {":Parameters.TON_DELAY:_QLineEdit": (34, 6, 0.00),
                             ":Parameters.TOFF_DELAY:_QLineEdit": (30, 9, 0.00),
                             ":Parameters.TON_RISE:_QLineEdit": (26, 15, 4.81),
                             ":Parameters.TOFF_FALL:_QLineEdit": (38, 9, 4.81),
                             ":Parameters.TON_MAX:_QLineEdit": (28, 11, 19.81),
                             ":Parameters.TOFF_MAX:_QLineEdit": (25, 1, 49.81),
                             ":Parameters.ON:_QLineEdit": (20, 12, 1.30),
                             ":Parameters.OFF:_QLineEdit": (27, 6, 0.00)
                             }
    
    protection_widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (85, 12, 1.39),
                          ":PMBus Protection Parameters.V_QLineEdit": (67, 8, 1.50),
                          ":PMBus Protection Parameters_QLineEdit": (82, 8, 1.21),
                          ":PMBus Protection Parameters.V_QLineEdit_2": (52, 14, 1.11),
                          ":PMBus Protection Parameters_QLineEdit_2": (72, 13, 15.98),
                          ":PMBus Protection Parameters.V_QLineEdit_3": (42, 11, 16.44),
                          ":PMBus Protection Parameters_QLineEdit_3": (77, 15, 4.32),
                          ":PMBus Protection Parameters.V_QLineEdit_4": (55, 12, 3.96),
                          ":PMBus Protection Parameters_QLineEdit_4": (84, 13, 45.00),
                          ":PMBus Protection Parameters.A_QLineEdit": (57, 4, 49.50),
                          ":PMBus Protection Parameters_QLineEdit_5": (85, 7, 130.00),
                          ":PMBus Protection Parameters.°C_QLineEdit": (54, 8, 135.00),
                          ":ON/OFF Levels.POWER OK_QLineEdit": (194, 10, 1.23),
                          ":ON/OFF Levels.  _QLineEdit": (113, 11, 1.17),
                          ":ON/OFF Levels.VIN_QLineEdit": (186, 7, 4.41),
                          ":ON/OFF Levels.  _QLineEdit_2": (109, 13, 4.20)
                          }
    
    for key, value in sorted(main_widgets.items()):
        mouseClick(waitForObject(key), value[0], value[1], 0, Qt.LeftButton)
        expected_text = value[2]
        test.compare(waitForObject(key).text, expected_text)
            
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))
    
    for key, value in sorted(configuration_widgets.items()):
        mouseClick(waitForObject(key), value[0], value[1], 0, Qt.LeftButton)
        expected_text = str(value[2])
        test.compare(waitForObject(key).text, expected_text)
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    
    for key, value in sorted(protection_widgets.items()):
        mouseClick(waitForObject(key), value[0], value[1], 0, Qt.LeftButton)
        expected_text = str(value[2])
        test.compare(waitForObject(key).text, expected_text)


###############################################################################################################
#                                            MAIN TAB TESTS                                                   #
#                                                                                                             #
#  Description: "Main" tab steps to test                                                                      #
###############################################################################################################

@Given("the user wants to change a \"Main\" tab parameter and the user enters the non-digit value")
def step(context):
    
    # When the user enters non-digit values followed by a digit,
    # the text field will only accept digit value and ignore non-digit ones.
    # The text field also does not accept negative numbers.
    
    mouseClick(waitForObject(":Voltage.VOUT_QLineEdit"), 47, 11, 0, Qt.LeftButton)
    mouseDrag(waitForObject(":Voltage.VOUT_QLineEdit"), 42, 13, 43, -8, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.VOUT_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-1")
    mouseClick(waitForObject(":Voltage.Margin High_QLineEdit"), 46, 13, 0, Qt.LeftButton)
    mouseDrag(waitForObject(":Voltage.Margin High_QLineEdit"), 48, 13, 36, -6, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.Margin High_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-3")
    mouseClick(waitForObject(":Voltage.Margin Low_QLineEdit"), 46, 13, 0, Qt.LeftButton)
    mouseDrag(waitForObject(":Voltage.Margin Low_QLineEdit"), 48, 13, 36, -6, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.Margin Low_QLineEdit"), "dhdh-d^&$#@^*+==_bbfhdhdrh5")
    
    
@Then("the \"Main\" tab parameter cannot accept non-digit values")
def step(context):
    
    test.compare(waitForObject(":Voltage.VOUT_QLineEdit").text, "1")
    test.compare(waitForObject(":Voltage.Margin High_QLineEdit").text, "3")
    test.compare(waitForObject(":Voltage.Margin Low_QLineEdit").text, "5")
    
    
@Given("the user wants to change a main tab parameter and the user enters too big '|any|'")
def step(context, val):
    
    mouseClick(waitForObject(":Voltage.Margin High_QLineEdit"), 46, 13, 0, Qt.LeftButton)
    mouseDrag(waitForObject(":Voltage.Margin High_QLineEdit"), 48, 13, 36, -6, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.Margin High_QLineEdit"), val)
    mouseClick(waitForObject(":Voltage.Margin Low_QLineEdit"), 46, 13, 0, Qt.LeftButton)
    mouseDrag(waitForObject(":Voltage.Margin Low_QLineEdit"), 48, 13, 36, -6, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.Margin Low_QLineEdit"), val)
    
    
@Then("the tooltip displays that the value entered is too big")
def step(context):
    
    lineedit_marg_high = waitForObject(":Voltage.Margin High_QLineEdit")
    test.compare(lineedit_marg_high.toolTip, "Value out of range (valid range 0 - 50.0 )")
    lineedit_marg_low = waitForObject(":Voltage.Margin Low_QLineEdit")
    test.compare(lineedit_marg_low.toolTip, "Value out of range (valid range 0 - 50.0 )")


@Then("the font colour becomes red")
def step(context):
    
    lineedit = waitForObject(":Voltage.Margin High_QLineEdit")
    test.compare(lineedit.palette.color(QPalette.Text), lineedit.palette.text())
    
    
@Given("the user wants to change a main tab parameter and the user deletes the value in the text field")
def step(context):
    
    mouseDrag(waitForObject(":Voltage.VOUT_QLineEdit"), 42, 9, 42, 4, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.VOUT_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Voltage.Margin High_QLineEdit"), 52, 12, 31, 5, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.Margin High_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Voltage.Margin Low_QLineEdit"), 51, 12, 35, 1, 1, Qt.LeftButton)
    type(waitForObject(":Voltage.Margin Low_QLineEdit"), "<Backspace>")


@Then("the \"Main\" tab text field stays at value = 0")
def step(context):
    
    test.compare(waitForObject(":Voltage.VOUT_QLineEdit").text, "0")
    test.compare(waitForObject(":Voltage.Margin High_QLineEdit").text, "0")
    test.compare(waitForObject(":Voltage.Margin Low_QLineEdit").text, "0")
    

###############################################################################################################
#                                      CONFIGURATION TAB TESTS                                                #
#                                                                                                             #
#  Description: "Configuration" tab steps to test                                                             #
###############################################################################################################

@Given("the user wants to change a \"Configuration\" tab parameter and the user enters the non-digit value")
def step(context):
    
    # When the user enters non-digit values followed by a digit,
    # the text field will only accept digit value and ignore non-digit ones.
    # The text field also does not accept negative numbers.
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))
    
    mouseDrag(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), 24, 13, 53, -4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-1")
    mouseDrag(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit"), 26, 12, 62, 0, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-43")
    mouseDrag(waitForObject(":Parameters.TON_RISE:_QLineEdit"), 27, 8, 54, -1, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_RISE:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-12")
    mouseDrag(waitForObject(":Parameters.TOFF_FALL:_QLineEdit"), 26, 11, 46, -1, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_FALL:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-5.65")
    mouseDrag(waitForObject(":Parameters.TON_MAX:_QLineEdit"), 26, 9, 46, 4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_MAX:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-2.12")
    mouseDrag(waitForObject(":Parameters.TOFF_MAX:_QLineEdit"), 27, 10, 37, -4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_MAX:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-7.34")
    mouseDrag(waitForObject(":Parameters.ON:_QLineEdit"), 21, 10, 77, -6, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.ON:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-1.12")
    mouseDrag(waitForObject(":Parameters.OFF:_QLineEdit"), 26, 16, 49, -8, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.OFF:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-0.92")
    
    
@Then("the \"Configuration\" tab parameter cannot accept non-digit values")
def step(context):
    
    test.compare(waitForObject(":Parameters.TON_DELAY:_QLineEdit").text, "1")
    test.compare(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit").text, "43")
    test.compare(waitForObject(":Parameters.TON_RISE:_QLineEdit").text, "12")
    test.compare(waitForObject(":Parameters.TOFF_FALL:_QLineEdit").text, "5.65")
    test.compare(waitForObject(":Parameters.TON_MAX:_QLineEdit").text, "2.12")
    test.compare(waitForObject(":Parameters.TOFF_MAX:_QLineEdit").text, "7.34")
    test.compare(waitForObject(":Parameters.ON:_QLineEdit").text, "1.12")
    test.compare(waitForObject(":Parameters.OFF:_QLineEdit").text, "0.92")
    
    
@Given("the entered value is in range")
def step(context):
    
    mouseDrag(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), 25, 10, 29, 2, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), "1.23")


@Then("the label on Sequencing Diagram changes accordingly")
def step(context):
    
    mouseClick(waitForObject(":Sequencing Diagram.1.23_QLabel"), 12, 11, 0, Qt.LeftButton)
    test.compare(waitForObject(":Parameters.TON_DELAY:_QLineEdit").text, waitForObject(":Sequencing Diagram.1.23_QLabel").text)

@Given("the user wants to change the startup/shutdown parameter and the user deletes the value in the text field")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))
    
    mouseDrag(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), 24, 13, 53, -4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit"), 26, 12, 62, 0, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Parameters.TON_RISE:_QLineEdit"), 27, 8, 54, -1, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_RISE:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Parameters.TOFF_FALL:_QLineEdit"), 26, 11, 46, -1, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_FALL:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Parameters.TON_MAX:_QLineEdit"), 26, 9, 46, 4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_MAX:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Parameters.TOFF_MAX:_QLineEdit"), 27, 10, 37, -4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_MAX:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Parameters.ON:_QLineEdit"), 21, 10, 77, -6, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.ON:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Parameters.OFF:_QLineEdit"), 26, 16, 49, -8, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.OFF:_QLineEdit"), "<Backspace>")

@Then("the \"Configuration\" tab text field stays at value = 0")
def step(context):
    
    test.compare(waitForObject(":Parameters.TON_DELAY:_QLineEdit").text, "0")
    test.compare(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit").text, "0")
    test.compare(waitForObject(":Parameters.TON_RISE:_QLineEdit").text, "0")
    test.compare(waitForObject(":Parameters.TOFF_FALL:_QLineEdit").text, "0")
    test.compare(waitForObject(":Parameters.TON_MAX:_QLineEdit").text, "0")
    test.compare(waitForObject(":Parameters.TOFF_MAX:_QLineEdit").text, "0")
    test.compare(waitForObject(":Parameters.ON:_QLineEdit").text, "0")
    test.compare(waitForObject(":Parameters.OFF:_QLineEdit").text, "0")
    
    
@Given("the user wants to change the startup/shutdown parameter and the user enters too big '|any|'")
def step(context, value):
    
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))
    mouseDrag(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), 25, 7, 57, -4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), value)
    mouseDrag(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit"), 26, 12, 62, 0, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_DELAY:_QLineEdit"), value)
    mouseDrag(waitForObject(":Parameters.TON_RISE:_QLineEdit"), 27, 8, 54, -1, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_RISE:_QLineEdit"), value)
    mouseDrag(waitForObject(":Parameters.TOFF_FALL:_QLineEdit"), 26, 11, 46, -1, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_FALL:_QLineEdit"), value)
    mouseDrag(waitForObject(":Parameters.TON_MAX:_QLineEdit"), 26, 9, 46, 4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_MAX:_QLineEdit"), value)
    mouseDrag(waitForObject(":Parameters.TOFF_MAX:_QLineEdit"), 27, 10, 37, -4, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TOFF_MAX:_QLineEdit"), value)
    
@Given("the user wants to change the vout on/off parameter and the user enters too big '|any|'")
def step(context, value):
    
    mouseDrag(waitForObject(":Parameters.ON:_QLineEdit"), 21, 10, 77, -6, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.ON:_QLineEdit"), value)
    mouseDrag(waitForObject(":Parameters.OFF:_QLineEdit"), 26, 16, 49, -8, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.OFF:_QLineEdit"), value)
    
@Then("the tooltip displays that the startup/shutdown value entered is too big")
def step(context):
    
    lineedit_ton_delay = waitForObject(":Parameters.TON_DELAY:_QLineEdit")
    test.compare(lineedit_ton_delay.toolTip, "Value out of range (valid range 0 - 5000.0 )")
    
    lineedit_toff_delay = waitForObject(":Parameters.TOFF_DELAY:_QLineEdit")
    test.compare(lineedit_toff_delay.toolTip, "Value out of range (valid range 0 - 5000.0 )")
    
    lineedit_ton_max = waitForObject(":Parameters.TON_MAX:_QLineEdit")
    test.compare(lineedit_ton_max.toolTip, "Value out of range (valid range 0 - 5000.0 )")
    
    lineedit_toff_max = waitForObject(":Parameters.TOFF_MAX:_QLineEdit")
    test.compare(lineedit_toff_max.toolTip, "Value out of range (valid range 0 - 5000.0 )")
    
    lineedit_ton_rise = waitForObject(":Parameters.TON_RISE:_QLineEdit")
    test.compare(lineedit_ton_rise.toolTip, "Value out of range (valid range 0 - 5000.0 )")
    
    lineedit_toff_fall = waitForObject(":Parameters.TOFF_FALL:_QLineEdit")
    test.compare(lineedit_toff_fall.toolTip, "Value out of range (valid range 0 - 5000.0 )")
    
    lineedit_ton_rise = waitForObject(":Parameters.ON:_QLineEdit")
    test.compare(lineedit_ton_rise.toolTip, "Value out of range (valid range 0 - 5.25 )")
    
    lineedit_toff_fall = waitForObject(":Parameters.OFF:_QLineEdit")
    test.compare(lineedit_toff_fall.toolTip, "Value out of range (valid range 0 - 5.25 )")


@Given("the user wants to select Device Startup option from the combo-box")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))

@Given("the user selects OPERATION_CMD")
def step(context):
    
    mouseClick(waitForObject(":Parameters.Device Startup:_QComboBox"), 136, 9, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":Parameters.Device Startup:_QComboBox", "OPERATION\\_CMD"), 98, 6, 0, Qt.LeftButton)

@When("the user opens the Monitoring tab")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))

@Then("the OPERATION_CMD button is enabled")
def step(context):
    
    clickButton(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"))
    sendEvent("QWheelEvent", waitForObject(":Input Voltage (V)_GraphCanvas"), 119, 231, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":Input Voltage (V)_GraphCanvas"), 125, 230, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":Input Voltage (V)_GraphCanvas"), 125, 230, -240, 0, 2)
    scrollTo(waitForObject(":Real Time Readings_QScrollBar"), 442)
    clickButton(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"))
    scrollTo(waitForObject(":Real Time Readings_QScrollBar"), 472)
    clickButton(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"))
    clickButton(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"))
    mouseClick(waitForObject(":Real Time Readings.OPERATION_CMD_QComboBox"), 162, 15, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Real Time Readings.OPERATION_CMD_QComboBox"), 162, 15, 0, Qt.LeftButton)
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))

@Then("Control Pin button is disabled")
def step(context):
    
    verify(findObject(":Real Time Readings.Control Pin_QPushButton"), 'enabled', False)

@Then("OPERATION_CMD functions combo-box is enabled")
def step(context):
    
    sendEvent("QMouseEvent", waitForObject(":Real Time Readings.OPERATION_CMD_QComboBox"), QEvent.MouseButtonPress, 157, 14, Qt.LeftButton, 1, 0)
    sendEvent("QMouseEvent", waitForObject(":Real Time Readings.OPERATION_CMD_QComboBox"), QEvent.MouseButtonRelease, 157, -8, Qt.LeftButton, 0, 0)
    mouseClick(waitForObjectItem(":Real Time Readings.OPERATION_CMD_QComboBox", "Soft off with sequencing"), 141, 0, 0, Qt.LeftButton)
    verify(waitForObject(":Real Time Readings.OPERATION_CMD_QComboBox"), 'enabled', True)

@Given("the user selects CTRL_POS or CTRL_NEG")
def step(context):
    
    mouseClick(waitForObject(":Parameters.Device Startup:_QComboBox"), 115, 13, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":Parameters.Device Startup:_QComboBox", "CTRL\\_POS"), 108, 9, 0, Qt.LeftButton)

@Then("the Control Pin button is enabled")
def step(context):
    
    scrollTo(waitForObject(":Real Time Readings_QScrollBar"), 475)
    clickButton(waitForObject(":Real Time Readings.Control Pin_QPushButton"))
    clickButton(waitForObject(":Real Time Readings.Control Pin_QPushButton"))
    verify(waitForObject(":Real Time Readings.Control Pin_QPushButton"), 'enabled', True)

@Then("OPERATION_CMD button is disabled")
def step(context):
    
    verify(findObject(":Real Time Readings.OPERATION_CMD_QPushButton"), 'enabled', False)

@Then("OPERATION_CMD functions combo-box is disabled")
def step(context):
    
    verify(findObject(":Real Time Readings.OPERATION_CMD_QComboBox"), 'enabled', False)
    
    
###############################################################################################################
#                                            TUNING TAB TESTS                                                 #
#                                                                                                             #
#  Description: "Tuning" tab steps to test                                                                    #
###############################################################################################################

@Given("the user wants to change a \"Tuning\" tab parameter and the user enters the non-digit value")
def step(context):
    
    # When the user enters non-digit values followed by a digit,
    # the text field will only accept digit value and ignore non-digit ones.
    # The text field also does not accept negative numbers.
    # In case of hex text fields, it only accept a value followed my "0x" and then digits 0-9 and letters a-f.
    
    clickButton(waitForObject(":PMBus Power GUI.Tuning_QToolButton"))
   
    mouseDrag(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), 121, 13, 107, -13, 1, Qt.LeftButton)
    type(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-1")
    mouseDrag(waitForObject(":Linear L16 Format Converter.Real world value:_QLineEdit"), 115, 10, 121, -15, 1, Qt.LeftButton)
    type(waitForObject(":Linear L16 Format Converter.Real world value:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-1")
    mouseDrag(waitForObject(":Direct Access Functions.Write:_QLineEdit"), 66, 8, 66, 6, 1, Qt.LeftButton)
    type(waitForObject(":Direct Access Functions.Write:_QLineEdit"), "dhdhd^&$#@^*+==_bbfhdhdrh-0xda03")
    
    
@Then("the \"Tuning\" tab parameter cannot accept non-digit values")
def step(context):
    
    test.compare(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit").text, "1")
    test.compare(waitForObject(":Linear L16 Format Converter.Real world value:_QLineEdit").text, "1")
    test.compare(waitForObject(":Direct Access Functions.Write:_QLineEdit").text, "0xda03") 
    
    
@Given("the user selects \"Tuning\" tab")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Tuning_QToolButton"))


@When("the user enters the '|any|' to Linear Converter L11")
def step(context, real_world_value):
    
    mouseDrag(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), 144, 12, 28, -6, 1, Qt.LeftButton)
    type(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), real_world_value)


@Then("the calculated encoded '|any|' displays in position")
def step(context, hex_value):
    
    mouseClick(waitForObject(":Linear L11 Format Converter.Encoded hex value:_QLineEdit"), 152, 11, 0, Qt.LeftButton)


@When("the user enters the encoded '|any|' to Linear Converter L16")
def step(context, hex_value):
    
    mouseDrag(waitForObject(":Linear L16 Format Converter.Encoded hex value:_QLineEdit"), 116, 12, 99, 7, 1, Qt.LeftButton)
    type(waitForObject(":Linear L16 Format Converter.Encoded hex value:_QLineEdit"), hex_value)


@Then("the calculated '|any|' displays in position")
def step(context, real_world_value):
    
    mouseClick(waitForObject(":Linear L16 Format Converter.Real world value:_QLineEdit"), 120, 9, 0, Qt.LeftButton)

@Given("the user wants to change the tuning parameter and the user deletes the value in the text field")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Tuning_QToolButton"))
   
    mouseDrag(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), 121, 13, 107, -13, 1, Qt.LeftButton)
    type(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Linear L16 Format Converter.Real world value:_QLineEdit"), 115, 10, 121, -15, 1, Qt.LeftButton)
    type(waitForObject(":Linear L16 Format Converter.Real world value:_QLineEdit"), "<Backspace>")

@ Then("the tuning text field stays at value = 0")
def steps(context):
    
    test.compare(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit").text, "0")
    test.compare(waitForObject(":Linear L16 Format Converter.Real world value:_QLineEdit").text, "0")
    


@Given("the user wants to change the tuning parameter when hex number is expected and the user deletes the value in the text field")
def steps(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Tuning_QToolButton"))
    mouseDrag(waitForObject(":Linear L11 Format Converter.Encoded hex value:_QLineEdit"), 92, 11, 108, -8, 1, Qt.LeftButton)
    type(waitForObject(":Linear L11 Format Converter.Encoded hex value:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Linear L16 Format Converter.Encoded hex value:_QLineEdit"), 92, 15, 173, -27, 1, Qt.LeftButton)
    type(waitForObject(":Linear L16 Format Converter.Encoded hex value:_QLineEdit"), "<Backspace>")
    mouseDrag(waitForObject(":Direct Access Functions.Write:_QLineEdit"), 66, 8, 66, 6, 1, Qt.LeftButton)
    type(waitForObject(":Direct Access Functions.Write:_QLineEdit"), "<Backspace>")
    
@Then("the tuning hex text field stays at value = 0x0000")
def step(context):
    
    test.compare(waitForObject(":Linear L11 Format Converter.Encoded hex value:_QLineEdit").text, "0x0000")
    test.compare(waitForObject(":Linear L16 Format Converter.Encoded hex value:_QLineEdit").text, "0x0000")
    test.compare(waitForObject(":Direct Access Functions.Write:_QLineEdit").text, "0x0000")   

@When("the user selects an '|any|' from Direct Access Function combo-box")
def step(context, option):
    
    clickButton(waitForObject(":PMBus Power GUI.Tuning_QToolButton"))
    
    mouseClick(waitForObject(":Direct Access Functions_QComboBox"), 182, 14, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":Direct Access Functions_QComboBox", option), 103, 7, 0, Qt.LeftButton)

@Then("the '|any|' in hex of this command displays in position")
def step(context, code):
    
    mouseClick(waitForObject(":Direct Access Functions.Code:_QLineEdit"), 62, 12, 0, Qt.LeftButton)
    test.compare(waitForObject(":Direct Access Functions.Code:_QLineEdit").text, code)

@Then("the '|any|' in bytes displays in position")
def step(context, size):
    
    mouseClick(waitForObject(":Direct Access Functions.Size in Bytes:_QLineEdit"), 76, 9, 0, Qt.LeftButton)
    test.compare(waitForObject(":Direct Access Functions.Size in Bytes:_QLineEdit").text, size)

@Then("the rest of the text fields stays with values 0 or 0x")
def step(context):
    
    mouseClick(waitForObject(":Direct Access Functions.Decimal:_QLineEdit"), 47, 12, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Direct Access Functions.Hex:_QLineEdit"), 44, 11, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Direct Access Functions.L11:_QLineEdit"), 49, 10, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Direct Access Functions.L16:_QLineEdit"), 54, 11, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Direct Access Functions.Write:_QLineEdit"), 62, 7, 0, Qt.LeftButton)
    
    test.compare(waitForObject(":Direct Access Functions.Decimal:_QLineEdit").text, "0")
    test.compare(waitForObject(":Direct Access Functions.Hex:_QLineEdit").text, "0x")
    test.compare(waitForObject(":Direct Access Functions.L11:_QLineEdit").text, "0")
    test.compare(waitForObject(":Direct Access Functions.L16:_QLineEdit").text, "0")
    test.compare(waitForObject(":Direct Access Functions.Write:_QLineEdit").text, "0x0")

@When("the user presses the Read button")
def step(context):
    
    clickButton(waitForObject(":Direct Access Functions.Read_QPushButton"))

@Then("the values in '|any|', '|any|', '|any|' and '|any|' are displayed in positions")
def step(context, decimal, hex, l11, l16):
    
    mouseClick(waitForObject(":Direct Access Functions.Decimal:_QLineEdit"), 43, 9, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Direct Access Functions.Hex:_QLineEdit"), 43, 14, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Direct Access Functions.L11:_QLineEdit"), 45, 10, 0, Qt.LeftButton)
    mouseClick(waitForObject(":Direct Access Functions.L16:_QLineEdit"), 54, 14, 0, Qt.LeftButton)
    
    test.compare(waitForObject(":Direct Access Functions.Decimal:_QLineEdit").text, decimal)
    test.compare(waitForObject(":Direct Access Functions.Hex:_QLineEdit").text, hex)
    test.compare(waitForObject(":Direct Access Functions.L11:_QLineEdit").text, l11)
    test.compare(waitForObject(":Direct Access Functions.L16:_QLineEdit").text, l16)


@Given("the user wants to write a value to particular PMBus command and the user enters a value to write in hex")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Tuning_QToolButton"))
    mouseClick(waitForObject(":Direct Access Functions_QComboBox"), 270, 15, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":Direct Access Functions_QComboBox", "VIN\\_OV\\_FAULT\\_LIMIT"), 106, 7, 0, Qt.LeftButton)
    clickButton(waitForObject(":Direct Access Functions.Read_QPushButton"))
    
    mouseDrag(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), 115, 7, 62, -6, 1, Qt.LeftButton)
    type(waitForObject(":Linear L11 Format Converter.Real world value:_QLineEdit"), "16.1")
    
    mouseDrag(waitForObject(":Direct Access Functions.Write:_QLineEdit"), 76, 11, 31, 1, 1, Qt.LeftButton)
    type(waitForObject(":Direct Access Functions.Write:_QLineEdit"), "0xda03")
    

@When("the user presses the Write button")
def step(context):
    
    clickButton(waitForObject(":Direct Access Functions.Write_QPushButton"))

@Then("the write command is send to the device and the new value is stored in the device")
def step(context):
        
    clickButton(waitForObject(":Direct Access Functions.Read_QPushButton"))
    
    mouseClick(waitForObject(":Direct Access Functions.L11:_QLineEdit"), 58, 11, 0, Qt.LeftButton)
    test.compare(waitForObject(":Direct Access Functions.L11:_QLineEdit").text, "16.1")
    
    
###############################################################################################################
#                                          PROTECTION TAB TESTS                                               #
#                                                                                                             #
#  Description: "Protection" tab steps to test                                                                #
###############################################################################################################   

@Given("the user wants to change a \"Protection\" tab parameter and the user enters the non-digit value")
def step(context):
    
    # When the user enters non-digit values followed by a digit,
    # the text field will only accept digit value and ignore non-digit ones.
    # The text field also does not accept negative numbers.
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
   
    widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (83, 11, 75, 4),
               ":PMBus Protection Parameters.V_QLineEdit": (71, 10, 127, -14),
               ":PMBus Protection Parameters_QLineEdit": (84, 5, 80, 4),
               ":PMBus Protection Parameters.V_QLineEdit_2": (73, 16, 78, 3),
               ":PMBus Protection Parameters_QLineEdit_2": (91, 13, 46, 6),
               ":PMBus Protection Parameters.V_QLineEdit_3": (86, 13, 88, 1),
               ":PMBus Protection Parameters_QLineEdit_3": (93, 9, 46, 0),
               ":PMBus Protection Parameters.V_QLineEdit_4": (77, 10, 90, -3),
               ":PMBus Protection Parameters_QLineEdit_4": (89, 14, 78, -1),
               ":PMBus Protection Parameters.A_QLineEdit": (81, 3, 88, 8),
               ":PMBus Protection Parameters_QLineEdit_5": (85, 13, 103, -10),
               ":PMBus Protection Parameters.°C_QLineEdit": (92, 10, 77, -4),
               ":ON/OFF Levels.POWER OK_QLineEdit": (205, 7, 51, 3),
               ":ON/OFF Levels.  _QLineEdit": (193, 6, 103, 10),
               ":ON/OFF Levels.VIN_QLineEdit": (210, 12, 79, 0),
               ":ON/OFF Levels.  _QLineEdit_2": (195, 16, 85, -3)}

    for key, value in sorted(widgets.items()):
        mouseDrag(waitForObject(key), value[0], value[1], value[2], value[3], 1, Qt.LeftButton)
        type(waitForObject(key), "dhdhd^&$#@^*+==_bbfhdhdrh-1.24")  
    
    
@Then("the \"Protection\" tab parameter cannot accept non-digit values")
def step(context):
    
    widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (83, 11, 75, 4),
               ":PMBus Protection Parameters.V_QLineEdit": (71, 10, 127, -14),
               ":PMBus Protection Parameters_QLineEdit": (84, 5, 80, 4),
               ":PMBus Protection Parameters.V_QLineEdit_2": (73, 16, 78, 3),
               ":PMBus Protection Parameters_QLineEdit_2": (91, 13, 46, 6),
               ":PMBus Protection Parameters.V_QLineEdit_3": (86, 13, 88, 1),
               ":PMBus Protection Parameters_QLineEdit_3": (93, 9, 46, 0),
               ":PMBus Protection Parameters.V_QLineEdit_4": (77, 10, 90, -3),
               ":PMBus Protection Parameters_QLineEdit_4": (89, 14, 78, -1),
               ":PMBus Protection Parameters.A_QLineEdit": (81, 3, 88, 8),
               ":PMBus Protection Parameters_QLineEdit_5": (85, 13, 103, -10),
               ":PMBus Protection Parameters.°C_QLineEdit": (92, 10, 77, -4),
               ":ON/OFF Levels.POWER OK_QLineEdit": (205, 7, 51, 3),
               ":ON/OFF Levels.  _QLineEdit": (193, 6, 103, 10),
               ":ON/OFF Levels.VIN_QLineEdit": (210, 12, 79, 0),
               ":ON/OFF Levels.  _QLineEdit_2": (195, 16, 85, -3)}
    
    for key, value in sorted(widgets.items()):
        test.compare(waitForObject(key).text, "1.24")
    
    
@Given("the enable checkbox is checked")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    verify(waitForObject(":PMBus Protection Parameters.VOUT OV_QCheckBox"), 'checked', True)
    verify(waitForObject(":PMBus Protection Parameters.VOUT UV_QCheckBox"), 'checked', True)
    verify(waitForObject(":PMBus Protection Parameters.VIN OV_QCheckBox"), 'checked', True)
    verify(waitForObject(":PMBus Protection Parameters.VIN UV_QCheckBox"), 'checked', True)
    verify(waitForObject(":PMBus Protection Parameters.IOUT_QCheckBox"), 'checked', True)
    verify(waitForObject(":PMBus Protection Parameters.TEMP_QCheckBox"), 'checked', True)

@Then("the warning limit, fault limit, delay, no. of retries and type of response are enabled")
def step(context):
    
    widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (77, 13),
               ":PMBus Protection Parameters.V_QLineEdit": (86, 6),
               ":PMBus Protection Parameters.V_QComboBox": (37, 8),
               ":PMBus Protection Parameters.us_QComboBox": (61, 6),
               ":PMBus Protection Parameters.Type of Response_QComboBox": (28, 11),
               ":PMBus Protection Parameters_QLineEdit": (80, 10),
               ":PMBus Protection Parameters.V_QLineEdit_2": (104, 9),
               ":PMBus Protection Parameters.V_QComboBox_2": (22, 4),
               ":PMBus Protection Parameters.us_QComboBox_2": (44, 3),
               ":PMBus Protection Parameters_QComboBox": (26, 4),
               ":PMBus Protection Parameters_QLineEdit_2": (93, 17),
               ":PMBus Protection Parameters.V_QLineEdit_3": (62, 16),
               ":PMBus Protection Parameters.V_QComboBox_3": (25, 12),
               ":PMBus Protection Parameters.us_QComboBox_3": (9, 6),
               ":PMBus Protection Parameters_QComboBox_2": (48, 8),
               ":PMBus Protection Parameters_QLineEdit_3": (87, 14),
               ":PMBus Protection Parameters.V_QLineEdit_4": (54, 18),
               ":PMBus Protection Parameters.V_QComboBox_4": (43, 9),
               ":PMBus Protection Parameters.us_QComboBox_4": (38, 3),
               ":PMBus Protection Parameters_QComboBox_3": (44, 11),
               ":PMBus Protection Parameters_QLineEdit_4": (89, 12),
               ":PMBus Protection Parameters.A_QLineEdit": (98, 9),
               ":PMBus Protection Parameters.A_QComboBox": (25, 7),
               ":PMBus Protection Parameters.us_QComboBox_5": (19, 7),
               ":PMBus Protection Parameters_QComboBox_4": (61, 5),
               ":PMBus Protection Parameters_QLineEdit_5": (104, 9),
               ":PMBus Protection Parameters.°C_QLineEdit": (86, 5),
               ":PMBus Protection Parameters.°C_QComboBox": (39, 12),
               ":PMBus Protection Parameters.us_QComboBox_6": (35, 2),
               ":PMBus Protection Parameters_QComboBox_5": (23, 16)}

    for key, value in sorted(widgets.items()):
        mouseClick(waitForObject(key), value[0], value[1], 0, Qt.LeftButton)
        verify(waitForObject(key), 'enabled', True)
        
@Given("the enable checkbox is not checked")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))

    clickButton(waitForObject(":PMBus Protection Parameters.VOUT OV_QCheckBox"))
    clickButton(waitForObject(":PMBus Protection Parameters.VOUT UV_QCheckBox"))
    clickButton(waitForObject(":PMBus Protection Parameters.VIN OV_QCheckBox"))
    clickButton(waitForObject(":PMBus Protection Parameters.VIN UV_QCheckBox"))
    clickButton(waitForObject(":PMBus Protection Parameters.IOUT_QCheckBox"))
    clickButton(waitForObject(":PMBus Protection Parameters.TEMP_QCheckBox"))

    verify(waitForObject(":PMBus Protection Parameters.VOUT OV_QCheckBox"), 'checked', False)
    verify(waitForObject(":PMBus Protection Parameters.VOUT UV_QCheckBox"), 'checked', False)
    verify(waitForObject(":PMBus Protection Parameters.VIN OV_QCheckBox"), 'checked', False)
    verify(waitForObject(":PMBus Protection Parameters.VIN UV_QCheckBox"), 'checked', False)
    verify(waitForObject(":PMBus Protection Parameters.IOUT_QCheckBox"), 'checked', False)
    verify(waitForObject(":PMBus Protection Parameters.TEMP_QCheckBox"), 'checked', False)

@Then("the warning limit, fault limit, delay, no. of retries and type of response are disabled")
def step(context):
    
    widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (77, 13),
               ":PMBus Protection Parameters.V_QLineEdit": (86, 6),
               ":PMBus Protection Parameters.V_QComboBox": (37, 8),
               ":PMBus Protection Parameters.us_QComboBox": (61, 6),
               ":PMBus Protection Parameters.Type of Response_QComboBox": (28, 11),
               ":PMBus Protection Parameters_QLineEdit": (80, 10),
               ":PMBus Protection Parameters.V_QLineEdit_2": (104, 9),
               ":PMBus Protection Parameters.V_QComboBox_2": (22, 4),
               ":PMBus Protection Parameters.us_QComboBox_2": (44, 3),
               ":PMBus Protection Parameters_QComboBox": (26, 4),
               ":PMBus Protection Parameters_QLineEdit_2": (93, 17),
               ":PMBus Protection Parameters.V_QLineEdit_3": (62, 16),
               ":PMBus Protection Parameters.V_QComboBox_3": (25, 12),
               ":PMBus Protection Parameters.us_QComboBox_3": (9, 6),
               ":PMBus Protection Parameters_QComboBox_2": (48, 8),
               ":PMBus Protection Parameters_QLineEdit_3": (87, 14),
               ":PMBus Protection Parameters.V_QLineEdit_4": (54, 18),
               ":PMBus Protection Parameters.V_QComboBox_4": (43, 9),
               ":PMBus Protection Parameters.us_QComboBox_4": (38, 3),
               ":PMBus Protection Parameters_QComboBox_3": (44, 11),
               ":PMBus Protection Parameters_QLineEdit_4": (89, 12),
               ":PMBus Protection Parameters.A_QLineEdit": (98, 9),
               ":PMBus Protection Parameters.A_QComboBox": (25, 7),
               ":PMBus Protection Parameters.us_QComboBox_5": (19, 7),
               ":PMBus Protection Parameters_QComboBox_4": (61, 5),
               ":PMBus Protection Parameters_QLineEdit_5": (104, 9),
               ":PMBus Protection Parameters.°C_QLineEdit": (86, 5),
               ":PMBus Protection Parameters.°C_QComboBox": (39, 12),
               ":PMBus Protection Parameters.us_QComboBox_6": (35, 2),
               ":PMBus Protection Parameters_QComboBox_5": (23, 16)}

    for key, value in sorted(widgets.items()):
        verify(findObject(key), 'enabled', False)


@Given("the \"Continue\" type of response is selected")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    
    mouseClick(waitForObject(":PMBus Protection Parameters.Type of Response_QComboBox"), 28, 6, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters.Type of Response_QComboBox", "Continue"), 40, 6, 0, Qt.LeftButton)

    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox"), 30, 10, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox", "Continue"), 41, 10, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_2"), 42, 7, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_2", "Continue"), 42, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_3"), 33, 15, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_3", "Continue"), 35, 8, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_4"), 32, 12, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_4", "Continue"), 32, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_5"), 33, 9, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_5", "Continue"), 35, 8, 0, Qt.LeftButton)

     
@Given("the \"Delay and retry\" type of response is selected")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    mouseClick(waitForObject(":PMBus Protection Parameters.Type of Response_QComboBox"), 42, 11, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters.Type of Response_QComboBox", "Delay and retry"), 44, 5, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox"), 30, 10, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox", "Delay and retry"), 41, 10, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_2"), 42, 7, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_2", "Delay and retry"), 42, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_3"), 33, 15, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_3", "Delay and retry"), 35, 8, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_4"), 32, 12, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_4", "Delay and retry"), 32, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_5"), 33, 9, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_5", "Delay and retry"), 35, 8, 0, Qt.LeftButton)
    
@Given("the \"Retry only\" type of response is selected")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    mouseClick(waitForObject(":PMBus Protection Parameters.Type of Response_QComboBox"), 42, 14, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters.Type of Response_QComboBox", "Retry only"), 44, 6, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox"), 30, 10, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox", "Retry only"), 41, 10, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_2"), 42, 7, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_2", "Retry only"), 42, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_3"), 33, 15, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_3", "Retry only"), 35, 8, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_4"), 32, 12, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_4", "Retry only"), 32, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_5"), 33, 9, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_5", "Retry only"), 35, 8, 0, Qt.LeftButton)
    
@Given("the \"Device shutdown\" type of response is selected")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    mouseClick(waitForObject(":PMBus Protection Parameters.Type of Response_QComboBox"), 38, 10, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters.Type of Response_QComboBox", "Device shutdown"), 45, 4, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox"), 30, 10, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox", "Device shutdown"), 41, 10, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_2"), 42, 7, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_2", "Device shutdown"), 42, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_3"), 33, 15, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_3", "Device shutdown"), 35, 8, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_4"), 32, 12, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_4", "Device shutdown"), 32, 7, 0, Qt.LeftButton)
    
    mouseClick(waitForObject(":PMBus Protection Parameters_QComboBox_5"), 33, 9, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":PMBus Protection Parameters_QComboBox_5", "Device shutdown"), 35, 8, 0, Qt.LeftButton)

@Then("the delay and number of retries are disabled")
def step(context):
    
    widgets = {":PMBus Protection Parameters.V_QComboBox": (37, 8),
               ":PMBus Protection Parameters.us_QComboBox": (61, 6),
               ":PMBus Protection Parameters.V_QComboBox_2": (22, 4),
               ":PMBus Protection Parameters.us_QComboBox_2": (44, 3),
               ":PMBus Protection Parameters.V_QComboBox_3": (25, 12),
               ":PMBus Protection Parameters.us_QComboBox_3": (9, 6),
               ":PMBus Protection Parameters.V_QComboBox_4": (43, 9),
               ":PMBus Protection Parameters.us_QComboBox_4": (38, 3),
               ":PMBus Protection Parameters.A_QComboBox": (25, 7),
               ":PMBus Protection Parameters.us_QComboBox_5": (19, 7),
               ":PMBus Protection Parameters.°C_QComboBox": (39, 12),
               ":PMBus Protection Parameters.us_QComboBox_6": (35, 2)}

    for key, value in sorted(widgets.items()):
        verify(findObject(key), 'enabled', False)
    
@Then("the delay and number of retries are enabled")
def step(context):
    
    widgets = {":PMBus Protection Parameters.V_QComboBox": (37, 8),
               ":PMBus Protection Parameters.us_QComboBox": (61, 6),
               ":PMBus Protection Parameters.V_QComboBox_2": (22, 4),
               ":PMBus Protection Parameters.us_QComboBox_2": (44, 3),
               ":PMBus Protection Parameters.V_QComboBox_3": (25, 12),
               ":PMBus Protection Parameters.us_QComboBox_3": (9, 6),
               ":PMBus Protection Parameters.V_QComboBox_4": (43, 9),
               ":PMBus Protection Parameters.us_QComboBox_4": (38, 3),
               ":PMBus Protection Parameters.A_QComboBox": (25, 7),
               ":PMBus Protection Parameters.us_QComboBox_5": (19, 7),
               ":PMBus Protection Parameters.°C_QComboBox": (39, 12),
               ":PMBus Protection Parameters.us_QComboBox_6": (35, 2)}

    for key, value in sorted(widgets.items()):
        verify(findObject(key), 'enabled', True)
        
@Then("the delay is disabled and number of retries is enabled")
def step(context):
    
    widgets_delay = {  ":PMBus Protection Parameters.V_QComboBox": (37, 8),
                       ":PMBus Protection Parameters.V_QComboBox_2": (22, 4),
                       ":PMBus Protection Parameters.V_QComboBox_3": (25, 12),
                       ":PMBus Protection Parameters.V_QComboBox_4": (43, 9),
                       ":PMBus Protection Parameters.A_QComboBox": (25, 7),
                       ":PMBus Protection Parameters.°C_QComboBox": (39, 12)}
    
    widgets_retries = {":PMBus Protection Parameters.us_QComboBox": (61, 6),
                       ":PMBus Protection Parameters.us_QComboBox_2": (44, 3),
                       ":PMBus Protection Parameters.us_QComboBox_3": (9, 6),
                       ":PMBus Protection Parameters.us_QComboBox_4": (38, 3),
                       ":PMBus Protection Parameters.us_QComboBox_5": (19, 7),
                       ":PMBus Protection Parameters.us_QComboBox_6": (35, 2)}

    for key, value in sorted(widgets_delay.items()):
        verify(findObject(key), 'enabled', False)
        
    for key, value in sorted(widgets_retries.items()):
        verify(findObject(key), 'enabled', True)

@Given("the user wants to change the protection parameter and the user enters too big '|any|'")
def step(context, val):

    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    
    mouseDrag(waitForObject(":PMBus Protection Parameters.°C_QLineEdit"), 101, 7, 29, 8, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.°C_QLineEdit"), val)

@Given("the user wants to change the power-ok parameter and the user enters too big '|any|'")
def step(context, val):    
    
    mouseDrag(waitForObject(":ON/OFF Levels.  _QLineEdit"), 214, 11, 34, -5, 1, Qt.LeftButton)
    type(waitForObject(":ON/OFF Levels.  _QLineEdit"), val)
    mouseDrag(waitForObject(":ON/OFF Levels.POWER OK_QLineEdit"), 200, 11, 46, -1, 1, Qt.LeftButton)
    type(waitForObject(":ON/OFF Levels.POWER OK_QLineEdit"), val)
    
@Given("the user wants to change the vin on/off parameter and the user enters too big '|any|'")
def step(context, val):
    
    mouseDrag(waitForObject(":ON/OFF Levels.VIN_QLineEdit"), 219, 9, 25, 2, 1, Qt.LeftButton)
    type(waitForObject(":ON/OFF Levels.VIN_QLineEdit"), val)
    mouseDrag(waitForObject(":ON/OFF Levels.  _QLineEdit_2"), 193, 9, 81, -10, 1, Qt.LeftButton)
    type(waitForObject(":ON/OFF Levels.  _QLineEdit_2"), val)    
        
@Then("the tooltip displays that the protection value entered is too big")
def step(context):
    
    lineedit_temp = waitForObject(":PMBus Protection Parameters.°C_QLineEdit")
    test.compare(lineedit_temp.toolTip, "Value out of range (valid range 0 - 175)")
    
    lineedit_power_on = waitForObject(":ON/OFF Levels.POWER OK_QLineEdit")
    test.compare(lineedit_power_on.toolTip, "Value out of range (valid range 0 - 5.25 )")
    
    lineedit_power_off = waitForObject(":ON/OFF Levels.  _QLineEdit")
    test.compare(lineedit_power_off.toolTip, "Value out of range (valid range 0 - 5.25 )")
    
    lineedit_vin_on = waitForObject(":ON/OFF Levels.VIN_QLineEdit")
    test.compare(lineedit_vin_on.toolTip, "Value out of range (valid range 0 - 20.0 )")
    
    lineedit_vin_off = waitForObject(":ON/OFF Levels.  _QLineEdit_2")
    test.compare(lineedit_vin_off.toolTip, "Value out of range (valid range 0 - 20.0 )")
    

@Given("the user wants to change the protection parameter of OV and the user enters warning '|any|' bigger or equal to fault '|any|'")
def step(context, w_value, f_value):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    
    # vout ov fault
    mouseDrag(waitForObject(":PMBus Protection Parameters.V_QLineEdit"), 86, 13, 46, 3, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.V_QLineEdit"), f_value)
    # vout ov warning
    mouseDrag(waitForObject(":PMBus Protection Parameters.Warning Limit_QLineEdit"), 89, 11, 35, 3, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.Warning Limit_QLineEdit"), w_value)
    # vin ov fault
    mouseDrag(waitForObject(":PMBus Protection Parameters.V_QLineEdit_3"), 89, 7, 51, -8, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.V_QLineEdit_3"), f_value)
    # vin ov warning
    mouseDrag(waitForObject(":PMBus Protection Parameters_QLineEdit_2"), 89, 7, 53, 8, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters_QLineEdit_2"), w_value)
    # iout oc fault
    mouseDrag(waitForObject(":PMBus Protection Parameters.A_QLineEdit"), 81, 6, 85, -1, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.A_QLineEdit"), f_value)
    # iout oc warning
    mouseDrag(waitForObject(":PMBus Protection Parameters_QLineEdit_4"), 83, 8, 68, 11, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters_QLineEdit_4"), w_value)
    # temp ot fault
    mouseDrag(waitForObject(":PMBus Protection Parameters.°C_QLineEdit"), 74, 14, 74, -3, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.°C_QLineEdit"), f_value)
    # temp ot warning
    mouseDrag(waitForObject(":PMBus Protection Parameters_QLineEdit_5"), 95, 9, 42, 6, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters_QLineEdit_5"), w_value)
 
 
@Then("the tooltip displays that the warning value has to be less than fault value")   
def step(context):
    
    tooltips = { ":PMBus Protection Parameters.V_QLineEdit": 
                "VOUT OV Warning threshold should be less than VOUT OV Fault threshold",
                ":PMBus Protection Parameters.Warning Limit_QLineEdit":
                "VOUT OV Warning threshold should be less than VOUT OV Fault threshold",
                ":PMBus Protection Parameters.V_QLineEdit_3":
                "VIN OV Warning threshold should be less than VIN OV Fault threshold",
                ":PMBus Protection Parameters_QLineEdit_2":
                "VIN OV Warning threshold should be less than VIN OV Fault threshold",
                ":PMBus Protection Parameters.A_QLineEdit":
                "IOUT OC Warning threshold should be less than IOUT OC Fault threshold",
                ":PMBus Protection Parameters_QLineEdit_4":
                "IOUT OC Warning threshold should be less than IOUT OC Fault threshold",
                ":PMBus Protection Parameters.°C_QLineEdit":
                "TEMP OT Warning threshold should be less than TEMP OT Fault threshold",
                ":PMBus Protection Parameters_QLineEdit_5":
                "TEMP OT Warning threshold should be less than TEMP OT Fault threshold"
                }
    
    for key, value in sorted(tooltips.items()):
        test.compare(waitForObject(key).toolTip, value)
    
    
@Given("the user wants to change the protection parameter of UV and the user enters warning '|any|' smaller or equal to fault '|any|'")
def step(context, w_value, f_value):
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))
    
    # vout uv fault
    mouseDrag(waitForObject(":PMBus Protection Parameters.V_QLineEdit_2"), 92, 7, 63, 0, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.V_QLineEdit_2"), f_value)
    # vout uv warning
    mouseDrag(waitForObject(":PMBus Protection Parameters_QLineEdit"), 94, 8, 39, 11, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters_QLineEdit"), w_value)
    # vin uv fault
    mouseDrag(waitForObject(":PMBus Protection Parameters.V_QLineEdit_4"), 87, 9, 63, 1, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters.V_QLineEdit_4"), f_value)
    # vin uv warning
    mouseDrag(waitForObject(":PMBus Protection Parameters_QLineEdit_3"), 91, 9, 61, -1, 1, Qt.LeftButton)
    type(waitForObject(":PMBus Protection Parameters_QLineEdit_3"), w_value)
    
    
@Then("the tooltip displays that the warning value has to be bigger than fault value")
def step(context):
    
    tooltips = { ":PMBus Protection Parameters.V_QLineEdit_2": 
                "VOUT UV Warning threshold should be more than VOUT UV Fault threshold",
                ":PMBus Protection Parameters_QLineEdit":
                "VOUT UV Warning threshold should be more than VOUT UV Fault threshold",
                ":PMBus Protection Parameters.V_QLineEdit_4":
                "VIN UV Warning threshold should be more than VIN UV Fault threshold",
                ":PMBus Protection Parameters_QLineEdit_3":
                "VIN UV Warning threshold should be more than VIN UV Fault threshold",
                }
    
    for key, value in sorted(tooltips.items()):
        test.compare(waitForObject(key).toolTip, value)



    

@Given("the user wants to change the protection parameter and the user deletes the value in the text field")
def step(context):
    
    widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (83, 11, 75, 4),
               ":PMBus Protection Parameters.V_QLineEdit": (71, 10, 127, -14),
               ":PMBus Protection Parameters_QLineEdit": (84, 5, 80, 4),
               ":PMBus Protection Parameters.V_QLineEdit_2": (73, 16, 78, 3),
               ":PMBus Protection Parameters_QLineEdit_2": (91, 13, 46, 6),
               ":PMBus Protection Parameters.V_QLineEdit_3": (86, 13, 88, 1),
               ":PMBus Protection Parameters_QLineEdit_3": (93, 9, 46, 0),
               ":PMBus Protection Parameters.V_QLineEdit_4": (77, 10, 90, -3),
               ":PMBus Protection Parameters_QLineEdit_4": (89, 14, 78, -1),
               ":PMBus Protection Parameters.A_QLineEdit": (81, 3, 88, 8),
               ":PMBus Protection Parameters_QLineEdit_5": (85, 13, 103, -10),
               ":PMBus Protection Parameters.°C_QLineEdit": (92, 10, 77, -4),
               ":ON/OFF Levels.POWER OK_QLineEdit": (205, 7, 51, 3),
               ":ON/OFF Levels.  _QLineEdit": (193, 6, 103, 10),
               ":ON/OFF Levels.VIN_QLineEdit": (210, 12, 79, 0),
               ":ON/OFF Levels.  _QLineEdit_2": (195, 16, 85, -3)}
    
    clickButton(waitForObject(":PMBus Power GUI.Protection_QToolButton"))

    for key, value in sorted(widgets.items()):
        mouseDrag(waitForObject(key), value[0], value[1], value[2], value[3], 1, Qt.LeftButton)
        type(waitForObject(key), "<Backspace>")  
        
@Then("the protection text field stays at value = 0")
def step(context):
    widgets = {":PMBus Protection Parameters.Warning Limit_QLineEdit": (83, 11, 75, 4),
               ":PMBus Protection Parameters.V_QLineEdit": (71, 10, 127, -14),
               ":PMBus Protection Parameters_QLineEdit": (84, 5, 80, 4),
               ":PMBus Protection Parameters.V_QLineEdit_2": (73, 16, 78, 3),
               ":PMBus Protection Parameters_QLineEdit_2": (91, 13, 46, 6),
               ":PMBus Protection Parameters.V_QLineEdit_3": (86, 13, 88, 1),
               ":PMBus Protection Parameters_QLineEdit_3": (93, 9, 46, 0),
               ":PMBus Protection Parameters.V_QLineEdit_4": (77, 10, 90, -3),
               ":PMBus Protection Parameters_QLineEdit_4": (89, 14, 78, -1),
               ":PMBus Protection Parameters.A_QLineEdit": (81, 3, 88, 8),
               ":PMBus Protection Parameters_QLineEdit_5": (85, 13, 103, -10),
               ":PMBus Protection Parameters.°C_QLineEdit": (92, 10, 77, -4),
               ":ON/OFF Levels.POWER OK_QLineEdit": (205, 7, 51, 3),
               ":ON/OFF Levels.  _QLineEdit": (193, 6, 103, 10),
               ":ON/OFF Levels.VIN_QLineEdit": (210, 12, 79, 0),
               ":ON/OFF Levels.  _QLineEdit_2": (195, 16, 85, -3)}
    
    for key, value in sorted(widgets.items()):
        test.compare(waitForObject(key).text, "0")
        

###############################################################################################################
#                                         MONITORING TAB TESTS                                                #
#                                                                                                             #
#  Description: "Monitoring" tab steps to test                                                                #
###############################################################################################################


@When("the user presses the \"Monitoring\" button")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))
    clickButton(waitForObject(":Real Time Readings.Monitoring_QPushButton"))
        
@Then("the real time plots start/stop")
def step(context):
          
    mouseClick(waitForObject(":Input Voltage (V)_GraphCanvas"), 256, 219, 0, Qt.LeftButton)
    sendEvent("QWheelEvent", waitForObject(":Input Voltage (V)_GraphCanvas"), 254, 219, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":Input Voltage (V)_GraphCanvas"), 254, 219, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":Input Voltage (V)_GraphCanvas"), 254, 219, -120, 0, 2)
    scrollTo(waitForObject(":Real Time Readings_QScrollBar"), 451)
    
@Then("the led turns red when turned off and turns green when turned on")
def step(context):
       
    mouseClick(waitForObject(":Real Time Readings.Monitoring_QLabel"), 12, 13, 0, Qt.LeftButton)
    clickButton(waitForObject(":Real Time Readings.Monitoring_QPushButton"))
    mouseClick(waitForObject(":Real Time Readings.Monitoring_QLabel"), 15, 11, 0, Qt.LeftButton)
    
@When("the user presses the \"Clear Faults\" button")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))
    clickButton(waitForObject(":Real Time Readings.Clear Faults_QPushButton"))
    
@Then("the command is written to the device and all bits setted for warning or fault becomes cleared")
def step(context):
    
    # the fault and warning bits are cleared in the register
    pass

@Given("the \"OPERATION_CMD\" is enabled")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))
    verify(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"), 'enabled', True)
    verify(findObject(":Real Time Readings.OPERATION_CMD_QComboBox"), 'enabled', True)
    
@When("the user selects the OPERATION_CMD option")
def step(context):
    
    pass

@Then("the correct value is written to the device and the device turns off with different setting")
def step(context):
    
    # this can be checked by turning device on/off and observing the real-time plots
    clickButton(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"))
    clickButton(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"))
  
@When("the user presses the OPERATION_CMD button")
def step(context):
    
    clickButton(waitForObject(":Real Time Readings.OPERATION_CMD_QPushButton"))
    
@When("the user presses the Control Pin button")
def step(context):
    
    clickButton(waitForObject(":Real Time Readings.Control Pin_QPushButton"))
    
@Given("the \"Control Pin\" is enabled")
def step(context):
     
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))
    verify(waitForObject(":Real Time Readings.Control Pin_QPushButton"), 'enabled', True)
    
@When("the user presses the \"Write volatile\" button")
def step(context):
    
    clickButton(waitForObject(":PMBus Power GUI.Configuration_QToolButton"))
    mouseDrag(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), 23, 10, 37, -1, 1, Qt.LeftButton)
    type(waitForObject(":Parameters.TON_DELAY:_QLineEdit"), "0.01")
    clickButton(waitForObject(":PMBus Power GUI.Monitoring_QToolButton"))
    clickButton(waitForObject(":Real Time Readings.Write volatile_QPushButton"))
    
@Then("all parameters from the GUI are saved in to the devices volatile memory")
def step(context):
    
    # close application and open it again manually to check if the parameters are changed correctly
    # in "Squish" I cannot close application in middle of the test
    pass

@Then("the device turns on/off and the plot displays rise/fall of the device in real time")
def step(context):
    
    # plots and real time values are displayed correctly
    pass
       

#@Then("the correct value is written to the device and the device turns off with different setting")
#def step(context):
    
    # the value is written correctly. The tester can check this by pressing OPERATION_CMD and 
    # check the real-time plots
    #pass

