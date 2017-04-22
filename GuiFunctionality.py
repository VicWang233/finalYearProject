#####################################################################
#                                                                   #
#                         GuiFunctionality.py                       #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#             Description: GUI Application implementation           #
#                                                                   #
#####################################################################

from PyQt4 import QtCore, QtGui
import LinearConversions
import Monitoring
from PMBusCall import pmbus
import ftd2xx
import Gui
import functools
import string


class GuiFunctionality(Gui.GuiMainWindow):

    ###############################################################################################################
    #                                            CLASS INIT DEFINITION                                            #
    #                                                                                                             #
    #  Description: set GuiFunctionality class as subclass of GuiMainWindow class                                 #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def __init__(self):

        Gui.GuiMainWindow.__init__(self)

        # paint panel for device's sequencing diagram
        self.paint_panel = 0

        # flag used for monitoring turn on/off option
        self.index = 1

        # check if device is turned on
        self.device_on = 0

        # flags to check if WRITE TO DEVICE button can be enabled
        self.write_ok = 0
        self.write_ok_ov = 0
        self.write_ok_uv = 0
        self.write_ok_temp = 0

        # timer for real time values displaying on monitoring tab (1s interval)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_monitoring_labels)
        self.timer.start(1000)

        # reference for LinearConversions class
        self.linear_conv = LinearConversions.LinearConversions()

        # by default protection parameters are enabled
        self.is_vout_ov_enabled = 1
        self.is_vout_uv_enabled = 1
        self.is_vin_ov_enabled = 1
        self.is_vin_uv_enabled = 1
        self.is_iout_enabled = 1
        self.is_temp_enabled = 1

        # variables to calculate values for protection RESPONSE commands
        # delay
        self.num_delay_a = 0
        self.num_delay_b = 0
        self.num_delay_c = 0
        self.num_delay_d = 0
        self.num_delay_e = 0
        self.num_delay_f = 0

        # number of retries
        self.num_retries_a = 0
        self.num_retries_b = 0
        self.num_retries_c = 0
        self.num_retries_d = 0
        self.num_retries_e = 0
        self.num_retries_f = 0

        # type of response
        self.num_resp_a = 0
        self.num_resp_b = 0
        self.num_resp_c = 0
        self.num_resp_d = 0
        self.num_resp_e = 0
        self.num_resp_f = 0

    ###############################################################################################################
    #                                               TEXT VALIDATION                                               #
    #                                                                                                             #
    #  Description: validates user input                                                                          #
    #  Arguments: text_field                                                                                      #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def text_validation(self, text_field):

        reg_ex = QtCore.QRegExp("^\d+(\.\d{1,2})?$")
        text_validator = QtGui.QRegExpValidator(reg_ex, text_field)
        text_field.setValidator(text_validator)

    ###############################################################################################################
    #                                    TEXT VALIDATION FOR HEX TEXT FIELDS                                      #
    #                                                                                                             #
    #  Description: validates user input in hex text fields                                                       #
    #  Arguments: text_field                                                                                      #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def text_validation_hex(self, text_field):

        reg_ex = QtCore.QRegExp("^0x[0-9A-Fa-f]+$")
        text_validator = QtGui.QRegExpValidator(reg_ex, text_field)
        text_field.setValidator(text_validator)

    ###############################################################################################################
    #                                            CREATE LABEL                                                     #
    #                                                                                                             #
    #  Description: create label with defined size and text                                                       #
    #  Arguments: group (group-box or frame), x-dimension, y-dimension, width, height, text of the label          #
    #  Returns: generated label                                                                                   #
    ###############################################################################################################

    def create_label(self, group, x, y, w, h, text):

        label = QtGui.QLabel(group)
        label.setGeometry(QtCore.QRect(x, y, w, h))
        label.setText(text)
        return label

    ###############################################################################################################
    #                                          CREATE BUTTON FOR MENU                                             #
    #                                                                                                             #
    #  Description: create button foe each tab of the GUI menu                                                    #
    #  Arguments: x-dimension, y-dimension, width, height, text on the button, page to connect to, icon image     #
    #  Returns: generated tool button                                                                             #
    ###############################################################################################################

    def create_button_tab(self, x, y, w, h, text, page, icon):

        button_tab = QtGui.QToolButton(self.buttons_frame)
        button_tab.setGeometry(QtCore.QRect(x, y, w, h))
        button_tab.setCheckable(True)
        button_tab.setAutoExclusive(True)
        button_tab.clicked.connect(page)
        button_tab.setText(text)
        button_tab.setIcon(QtGui.QIcon(icon))
        button_tab.setIconSize(QtCore.QSize(32, 32))
        button_tab.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon | QtCore.Qt.AlignLeading)
        return button_tab

    ###############################################################################################################
    #                                            SIZE AND NAME                                                    #
    #                                                                                                             #
    #  Description: set size and name of the widget                                                               #
    #  Arguments: component (widget), x-dimension, y-dimension, width, height, widget's title                     #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def size_and_name(self, component, x, y, w, h, name):

        component.setGeometry(QtCore.QRect(x, y, w, h))
        component.setTitle(name)

    ###############################################################################################################
    #                                            CREATE LINE EDIT                                                 #
    #                                                                                                             #
    #  Description: create line-edit with defined size and text                                                   #
    #  Arguments: default text of the line-edit                                                                   #
    #  Returns: generated line-edit                                                                               #
    ###############################################################################################################

    def create_line_edit(self, text):

        line_edit = QtGui.QLineEdit()
        line_edit.setAlignment(QtCore.Qt.AlignRight)
        line_edit.setText(text)
        self.text_validation(line_edit)  # validate user input
        arg = functools.partial(self.handle_editing_finished, line_edit)
        line_edit.textChanged.connect(arg)
        return line_edit

    ###############################################################################################################
    #                                         CREATE LINE EDIT FOR HEX DIGITS                                     #
    #                                                                                                             #
    #  Description: create line-edit with defined size and text for hex digits only                               #
    #  Arguments: default text of the line-edit                                                                   #
    #  Returns: generated line-edit                                                                               #
    ###############################################################################################################

    def create_hex_line_edit(self, text):

        line_edit = QtGui.QLineEdit()
        line_edit.setAlignment(QtCore.Qt.AlignRight)
        line_edit.setText(text)
        self.text_validation_hex(line_edit)  # validate user input
        arg = functools.partial(self.handle_hex_lineedit, line_edit)
        line_edit.textChanged.connect(arg)
        return line_edit

    ###############################################################################################################
    #                                            CREATE CHECK-BOX                                                 #
    #                                                                                                             #
    #  Description: create check-box with defined state and function                                              #
    #  Arguments: none                                                                                            #
    #  Returns: generated check-box                                                                               #
    ###############################################################################################################

    def create_checkbox(self):

        checkbox = QtGui.QCheckBox()
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.state_changed)
        return checkbox

    ###############################################################################################################
    #                                     HANDLE LINE-EDIT CHANGES (HEX ONLY)                                     #
    #                                                                                                             #
    #  Description: handle all user changes of the line-edit (hex only)                                           #
    #  Arguments: line-edit                                                                                       #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_hex_lineedit(self, line_edit):

        # when widget is empty, fill it with "0x0000"
        widget = line_edit
        if widget.text().isEmpty():
            widget.setText("0x0000")

        # when widget is empty, fill with "0x0000" and corresponding real world value fill wih "0"
        if self.encoded_hex_l11.text().isEmpty():
            self.encoded_hex_l11.setText("0x0000")
            self.rwv_l11.setText("0")

        # when widget is empty, fill with "0x0000" and corresponding real world value fill wih "0"
        if self.encoded_hex_l16.text().isEmpty():
            self.encoded_hex_l16.setText("0x0000")
            self.rwv_l16.setText("0")

        # when line-edit is modified, change corresponding real world value accordingly
        if self.encoded_hex_l11.isModified() and not self.encoded_hex_l11.text().isEmpty():
            value = self.encoded_hex_l11.text()
            if value == "0x":
                self.rwv_l11.setText("0")
            else:
                self.rwv_l11.setText(str(self.linear_conv.l11_to_float(int(str(value), 16))))

        # when line-edit is modified, change corresponding real world value accordingly
        if self.encoded_hex_l16.isModified() and not self.encoded_hex_l16.text().isEmpty():
            value = self.encoded_hex_l16.text()
            if value == "0x":
                self.rwv_l16.setText("0")
            else:
                self.rwv_l16.setText(str(self.linear_conv.l16_to_float(int(str(value), 16))))

    ###############################################################################################################
    #                                             CHECK RANGE                                                     #
    #                                                                                                             #
    #  Description: this method takes care of out of range situations in line-edits                               #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def check_range(self):

        warnings_ov = [self.vout_ov_warning, self.vin_ov_warning,
                    self.iout_oc_warning, self.temp_ot_warning]

        warnings_uv = [self.vout_uv_warning, self.vin_uv_warning]

        faults_ov = [self.vout_ov_fault, self.vin_ov_fault,
                  self.iout_oc_fault, self.temp_ot_fault]

        faults_uv = [self.vout_uv_fault, self.vin_uv_fault]

        prot_parameters_ov = ["VOUT OV", "VIN OV", "IOUT OC", "TEMP OT"]
        prot_parameters_uv = ["VOUT UV", "VIN UV"]

        widgets = [self.ton_delay, self.toff_delay, self.ton_rise, self.toff_fall,
                   self.ton_max, self.toff_max, self.vout_on, self.vout_off,
                   self.power_on, self.power_off, self.vin_on, self.vin_off,
                   self.marg_high, self.marg_low]

        ranges = [5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5.250, 5.250, 5.25, 5.25, 20.0, 20.0, 50.0, 50.0]
        params = ["TON_DELAY", "TOFF_DELAY", "TON_RISE", "TOFF_FALL", "TON_MAX", "TOFF_MAX", "VOUT ON", "VOUT OFF",
                  "POWER ON", "POWER OFF", "VIN ON", "VIN OFF", "margin high", "margin low"]

        # check if parameters are out of range
        for widget, r, param in zip(widgets, ranges, params):
            if float(widget.text()) > r:
                self.write_ok = 0
                widget.setStyleSheet("color: rgb(255, 51, 51);")
                widget.setToolTip("Value out of range (valid range 0 - " + str(r) + " )")
            elif float(widget.text()) <= r:
                self.write_ok = 1
                widget.setStyleSheet("color: rgb(0, 0, 0);")
                widget.setToolTip("Enter here " + param)

        # check ov protection parameters if warning threshold is less than fault threshold
        for fault, warning, param in zip(faults_ov, warnings_ov, prot_parameters_ov):
            if float(warning.text()) >= float(fault.text()):
                # disable writing to the device
                self.write_ok_ov = 0
                warning.setStyleSheet("color: rgb(255, 153, 51);")
                warning.setToolTip(param + " Warning threshold should be "
                                   "less than " + param + " Fault threshold")
                fault.setStyleSheet("color: rgb(255, 153, 51);")
                fault.setToolTip(param + " Warning threshold should be "
                                 "less than " + param + " Fault threshold")
            elif float(warning.text()) < float(fault.text()):
                if param == "TEMP OT":
                    if float(warning.text()) > 175:
                        self.write_ok_temp = 0
                        warning.setStyleSheet("color: rgb(255, 51, 51);")
                        warning.setToolTip("Value out of range (valid range 0 - 175)")
                    if float(fault.text()) > 175:
                        self.write_ok_temp = 0
                        fault.setStyleSheet("color: rgb(255, 51, 51);")
                        fault.setToolTip("Value out of range (valid range 0 - 175)")
                    else:
                        self.write_ok_temp = 1
                        warning.setStyleSheet("color: rgb(0, 0, 0);")
                        warning.setToolTip("Enter here " + param + " warning threshold")
                        fault.setStyleSheet("color: rgb(0, 0, 0);")
                        fault.setToolTip("Enter here " + param + " fault threshold")
                else:
                    self.write_ok_ov = 1
                    warning.setStyleSheet("color: rgb(0, 0, 0);")
                    warning.setToolTip("Enter here " + param + " warning threshold")
                    fault.setStyleSheet("color: rgb(0, 0, 0);")
                    fault.setToolTip("Enter here " + param + " fault threshold")

        # check uv protection parameters if warning threshold is more than fault threshold
        for fault, warning, param in zip(faults_uv, warnings_uv, prot_parameters_uv):
            if float(warning.text()) <= float(fault.text()):
                self.write_ok_uv = 0
                warning.setStyleSheet("color: rgb(255, 153, 51);")
                warning.setToolTip(param + " Warning threshold should be "
                                   "more than " + param + " Fault threshold")
                fault.setStyleSheet("color: rgb(255, 153, 51);")
                fault.setToolTip(param + " Warning threshold should be "
                                 "more than " + param + " Fault threshold")
            else:
                self.write_ok_uv = 1
                warning.setStyleSheet("color: rgb(0, 0, 0);")
                warning.setToolTip("Enter here " + param + " warning threshold")
                fault.setStyleSheet("color: rgb(0, 0, 0);")
                fault.setToolTip("Enter here " + param + " fault threshold")

    ###############################################################################################################
    #                                         HANDLE LINE-EDIT CHANGES                                            #
    #                                                                                                             #
    #  Description: handle all user changes of the line-edit                                                      #
    #  Arguments: line-edit                                                                                       #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_editing_finished(self, line_edit):

        # when line-edit is changed in "Configuration tab" then change the label on Sequencing Diagram accordingly
        if self.toff_max.isModified():
            self.toffmax_label.setText("TOFF_MAX = " + self.toff_max.text())
        elif self.ton_max.isModified():
            self.tonmax_label.setText("TON_MAX = " + self.ton_max.text())
        elif self.ton_delay.isModified():
            self.tondelay_label.setText(self.ton_delay.text())
        elif self.toff_delay.isModified():
            self.toffdelay_label.setText(self.toff_delay.text())
        elif self.ton_rise.isModified():
            self.tonrise_label.setText(self.ton_rise.text())
        elif self.toff_fall.isModified():
            self.tofffall_label.setText(self.toff_fall.text())
        elif self.vout_on.isModified():
            self.vouton_label.setText("VOUT ON \n " + self.vout_on.text() + " V")
        elif self.vout_off.isModified():
            self.voutoff_label.setText("VOUT OFF \n " + self.vout_off.text() + " V")

        self.toff_max.setModified(False)
        self.ton_max.setModified(False)
        self.ton_delay.setModified(False)
        self.toff_delay.setModified(False)
        self.ton_rise.setModified(False)
        self.toff_fall.setModified(False)
        self.vout_off.setModified(False)
        self.vout_on.setModified(False)

        # when line-edit is modified, change corresponding hex value accordingly
        if self.rwv_l11.isModified() and not self.rwv_l11.text().isEmpty():
            value = self.rwv_l11.text()
            self.encoded_hex_l11.setText(self.linear_conv.float_to_l11(float(value)))

        # when line-edit is modified, change corresponding hex value accordingly
        if self.rwv_l16.isModified() and not self.rwv_l16.text().isEmpty():
            value = self.rwv_l16.text()
            self.encoded_hex_l16.setText(self.linear_conv.float_to_l16(float(value)))

        # when widget is empty set it to "0" and corresponding hex value to "0x0000"
        if self.rwv_l11.text().isEmpty():
            self.rwv_l11.setText("0")
            self.encoded_hex_l11.setText("0x0000")

        # when widget is empty set it to "0" and corresponding hex value to "0x0000"
        if self.rwv_l16.text().isEmpty():
            self.encoded_hex_l16.setText("0x0000")
            self.rwv_l16.setText("0")

        # when any line-edit is empty set it to "0"
        widget = line_edit
        if widget.text().isEmpty():
            widget.setText("0")

    ###############################################################################################################
    #                                   HANDLE STATE CHANGES OF PROTECTION CHECK-BOXES                            #
    #                                                                                                             #
    #  Description: when check-box is enabled, enable corresponding settings;                                     #
    #  Othwerwise disable corresponding settings                                                                  #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def state_changed(self):

        widgets = [self.vout_ov_warning, self.vout_ov_fault, self.vout_ov_delay,
                   self.vout_ov_retry, self.vout_ov_resp, self.vout_uv_warning,
                   self.vout_uv_fault, self.vout_uv_delay, self.vout_uv_retry,
                   self.vout_uv_resp, self.vin_ov_warning, self.vin_ov_fault,
                   self.vin_ov_delay, self.vin_ov_retry, self.vin_ov_resp,
                   self.vin_uv_warning, self.vin_uv_fault, self.vin_uv_delay,
                   self.vin_uv_retry, self.vin_uv_resp, self.iout_oc_warning,
                   self.iout_oc_fault, self.iout_oc_delay, self.iout_oc_retry,
                   self.iout_oc_resp, self.temp_ot_warning, self.temp_ot_fault,
                   self.temp_ot_delay, self.temp_ot_retry, self.temp_ot_resp]

        # check if any of the check-boxes is selected and enable/disable corresponding settings accordingly
        # only if check-box is enabled, the corresponding settings can be written to the device
        if self.vout_ov_enable.isChecked():
            self.is_vout_ov_enabled = 1
            for i in range(5):
                widgets[i].setEnabled(True)
        else:
            self.is_vout_ov_enabled = 0
            for i in range(5):
                widgets[i].setEnabled(False)

        if self.vout_uv_enable.isChecked():
            self.is_vout_uv_enabled = 1
            for i in range(5, 10):
                widgets[i].setEnabled(True)
        else:
            self.is_vout_uv_enabled = 0
            for i in range(5, 10):
                widgets[i].setEnabled(False)

        if self.vin_ov_enable.isChecked():
            self.is_vin_ov_enabled = 1
            for i in range(10, 15):
                widgets[i].setEnabled(True)
        else:
            for i in range(10, 15):
                self.is_vin_ov_enabled = 0
                widgets[i].setEnabled(False)

        if self.vin_uv_enable.isChecked():
            self.is_vin_uv_enabled = 1
            for i in range(15, 20):
                widgets[i].setEnabled(True)
        else:
            self.is_vin_uv_enabled = 0
            for i in range(15, 20):
                widgets[i].setEnabled(False)

        if self.iout_oc_enable.isChecked():
            self.is_iout_enabled = 1
            for i in range(20, 25):
                widgets[i].setEnabled(True)
        else:
            self.is_iout_enabled = 0
            for i in range(20, 25):
                widgets[i].setEnabled(False)

        if self.temp_ot_enable.isChecked():
            self.is_temp_enabled = 1
            for i in range(25, 30):
                widgets[i].setEnabled(True)
        else:
            self.is_temp_enabled = 0
            for i in range(25, 30):
                widgets[i].setEnabled(False)

    ###############################################################################################################
    #                                      SELECTION CHANGE FOR DEVICE STARTUP                                    #
    #                                                                                                             #
    #  Description: handle selection change for device startup combo-box on "Configuration" tab                   #
    #  Arguments: i - index of the selection                                                                      #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def startup_selection_change(self, i):

        if self.cb.currentText() == "OPERATION_CMD":
            self.control_pin.setEnabled(False)
            self.operation_cmd.setEnabled(True)
            self.cb_mon.setEnabled(True)
            pmbus.configure_command(pmbus.device, "iw_3f0020218")  # write operation cmd 0x18
        elif self.cb.currentText() == "CTRL_POS":
            self.control_pin.setEnabled(True)
            self.operation_cmd.setEnabled(False)
            self.cb_mon.setEnabled(False)
            pmbus.configure_command(pmbus.device, "iw_3f0020216")  # write ctrl_pos 0x16
        else:
            self.control_pin.setEnabled(True)
            self.operation_cmd.setEnabled(False)
            self.cb_mon.setEnabled(False)
            pmbus.configure_command(pmbus.device, "iw_3f0020214")  # write ctrl_neg 0x14

    ###############################################################################################################
    #                                   SELECTION CHANGE FOR PMBUS COMMANDS                                       #
    #                                                                                                             #
    #  Description: handle selection change for PMBus commands in combo-box on "Tuning" tab                       #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def selection_pmbus_commands(self):

        # set code
        key = str(self.pmbus_cb.currentText())  # make sure it's a string
        value = self.dict.get(key)
        code_val = '0x' + hex(value[0])[2:].zfill(2)
        self.code.setText(code_val)

        # set size
        size_val = value[1]
        self.size.setText(str(size_val))

        # set read button
        cmd_hex = code_val[2:]
        arg1 = functools.partial(self.handle_rd_direct, cmd_hex, size_val)
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.read_direct.setEnabled(False)
        elif code_val is not self.write_only:
            self.read_direct.setEnabled(True)
            self.read_direct.clicked.connect(arg1)
        else:
            self.read_direct.setEnabled(False)

        # set write button
        arg2 = functools.partial(self.handle_wr_direct, cmd_hex)
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.write_direct.setEnabled(False)
        elif code_val is not self.read_only:
            self.write_direct.setEnabled(True)
            self.write_direct.clicked.connect(arg2)
        else:
            self.write_direct.setEnabled(False)

    ###############################################################################################################
    #                                      HANDLE READ BUTTON ON TUNING TAB                                       #
    #                                                                                                             #
    #  Description: handle "Read" button on "Tuning" tab - read data from the device                              #
    #  Arguments: arg (command in hex), size (size of the command in bytes)                                       #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_rd_direct(self, arg, size):

        # send query to the device for the PMBus command selected from the combo-box
        if size > 2:
            size += 1
        response = pmbus.configure_command(pmbus.device, "iq_3f010" + str(size) + str(arg))
        a = response[-4:]
        b = response[1:3]
        a = a.rstrip()
        b = b.rstrip()
        hex_value = "0x" + a + b
        # convert to decimal and display
        decimal_value = int(hex_value, 16)
        self.read_dec.setText(str(decimal_value))
        # display hex
        self.read_hex.setText(hex_value)
        # convert to L11 and L16 and display
        response_l11 = pmbus.l11_query_command(pmbus.device, "iq_3f010" + str(size) + str(arg))
        response_l16 = pmbus.l16_query_command(pmbus.device, "iq_3f010" + str(size) + str(arg))
        self.read_l11.setText(response_l11)
        self.read_l16.setText(response_l16)

    ###############################################################################################################
    #                                      HANDLE READ BUTTON ON TUNING TAB                                       #
    #                                                                                                             #
    #  Description: handle "Read" button on "Tuning" tab - read data from the device                              #
    #  Arguments: arg (command in hex)                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_wr_direct(self, arg):

        # write specified command and value to the device
        pmbus.write_direct(pmbus.device, "iw_3f003" + arg, self.write_hex.text())

    ###############################################################################################################
    #                                      HANDLE MONITORING BUTTON                                               #
    #                                                                                                             #
    #  Description: turn real-time plots on/off and set led to green/red                                          #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def mon_on_off(self):

        if self.index:
            self.pix_map = QtGui.QPixmap('icons/red.jpg')
            self.led.setPixmap(self.pix_map)
            self.timer.stop()
        else:
            self.pix_map = QtGui.QPixmap('icons/green.jpg')
            self.led.setPixmap(self.pix_map)
            self.timer.start(1000)
        self.index = not self.index

    ###############################################################################################################
    #                                     WRITE NEW CONFIGURATIONS TO THE DEVICE                                  #
    #                                                                                                             #
    #  Description: get information from all line-edits and combo-boxes and save new configurations               #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def write_to_device(self):

        # convert margin high and margin low values from percentages back to floats
        marg_low_val = float(self.vout_nom.text()) - (float(self.vout_nom.text()) * (float(self.marg_low.text()) / 100))
        marg_high_val = float(self.vout_nom.text()) + (float(self.vout_nom.text()) * (float(self.marg_high.text()) / 100))

        values_l11 = [self.ton_delay.text(), self.ton_rise.text(), self.ton_max.text(),
                      self.toff_delay.text(), self.toff_fall.text(), self.toff_max.text(),
                      self.vin_on.text(), self.vin_off.text()]

        values_l16 = [self.vout_nom.text(), self.power_on.text(), self.power_off.text(),
                      str(marg_high_val), str(marg_low_val)]

        pmbus_l11_hex_codes = ["60", "61", "62", "64", "65", "66", "35", "36"]
        pmbus_l16_hex_codes = ["21", "5E", "5F", "25", "26"]

        # determine values to send to the device from "Delay" combo-box + "Number of retries" combo-box
        # and "Response type" combo-box from the "Protection" tab
        vout_ov_fault_response = bin(self.num_resp_a)[2:].zfill(2)
        vout_ov_fault_retries = bin(self.num_retries_a)[2:].zfill(3)
        vout_ov_fault_delay = bin(self.num_delay_a)[2:].zfill(3)
        vout_ov_to_send = self.bin_to_hex(vout_ov_fault_response + vout_ov_fault_retries + vout_ov_fault_delay)

        vout_uv_fault_response = bin(self.num_resp_b)[2:].zfill(2)
        vout_uv_fault_retries = bin(self.num_retries_b)[2:].zfill(3)
        vout_uv_fault_delay = bin(self.num_delay_b)[2:].zfill(3)
        vout_uv_to_send = self.bin_to_hex(vout_uv_fault_response + vout_uv_fault_retries + vout_uv_fault_delay)

        vin_ov_fault_response = bin(self.num_resp_c)[2:].zfill(2)
        vin_ov_fault_retries = bin(self.num_retries_c)[2:].zfill(3)
        vin_ov_fault_delay = bin(self.num_delay_c)[2:].zfill(3)
        vin_ov_to_send = self.bin_to_hex(vin_ov_fault_response + vin_ov_fault_retries + vin_ov_fault_delay)

        vin_uv_fault_response = bin(self.num_resp_d)[2:].zfill(2)
        vin_uv_fault_retries = bin(self.num_retries_d)[2:].zfill(3)
        vin_uv_fault_delay = bin(self.num_delay_d)[2:].zfill(3)
        vin_uv_to_send = self.bin_to_hex(vin_uv_fault_response + vin_uv_fault_retries + vin_uv_fault_delay)

        iout_oc_fault_response = bin(self.num_resp_e)[2:].zfill(2)
        iout_oc_fault_retries = bin(self.num_retries_e)[2:].zfill(3)
        iout_oc_fault_delay = bin(self.num_delay_e)[2:].zfill(3)
        iout_oc_to_send = self.bin_to_hex(iout_oc_fault_response + iout_oc_fault_retries + iout_oc_fault_delay)

        temp_ot_fault_response = bin(self.num_resp_f)[2:].zfill(2)
        temp_ot_fault_retries = bin(self.num_retries_f)[2:].zfill(3)
        temp_ot_fault_delay = bin(self.num_delay_f)[2:].zfill(3)
        temp_ot_to_send = self.bin_to_hex(temp_ot_fault_response + temp_ot_fault_retries + temp_ot_fault_delay)

        vout_ov_protection = [self.vout_ov_fault.text(), self.vout_ov_warning.text(), vout_ov_to_send]
        vout_uv_protection = [self.vout_uv_fault.text(), self.vout_uv_warning.text(), vout_uv_to_send]
        vin_ov_protection = [self.vin_ov_fault.text(), self.vin_ov_warning.text(), vin_ov_to_send]
        vin_uv_protection = [self.vin_uv_fault.text(), self.vin_uv_warning.text(), vin_uv_to_send]
        iout_oc_protection = [self.iout_oc_fault.text(), self.iout_oc_warning.text(), iout_oc_to_send]
        temp_ot_protection = [self.temp_ot_fault.text(), self.temp_ot_warning.text(), temp_ot_to_send]

        vout_ov_code = ["40", "42", "41"]
        vout_uv_code = ["44", "46", "45"]
        vin_ov_code = ["55", "57", "56"]
        vin_uv_code = ["59", "58", "5A"]
        iout_oc_code = ["46", "4A", "47"]
        temp_ot_code = ["4F", "51", "50"]

        # write to the device only if all parameters are entered correctly
        if self.write_ok and self.write_ok_ov and self.write_ok_uv and self.write_ok_temp:
            # write particular parameter only when "enable" checkbox is checked
            if self.vout_ov_enable:
                for value, code in zip(vout_ov_protection, vout_ov_code):
                    pmbus.configure_command(pmbus.device, "iw_3f001" + code + value)
            if self.vout_uv_enable:
                for value, code in zip(vout_uv_protection, vout_uv_code):
                    pmbus.configure_command(pmbus.device, "iw_3f001" + code + value)
            if self.vin_ov_enable:
                for value, code in zip(vin_ov_protection, vin_ov_code):
                    pmbus.configure_command(pmbus.device, "iw_3f001" + code + value)
            if self.vin_uv_enable:
                for value, code in zip(vin_uv_protection, vin_uv_code):
                    pmbus.configure_command(pmbus.device, "iw_3f001" + code + value)
            if self.iout_oc_enable:
                for value, code in zip(iout_oc_protection, iout_oc_code):
                    pmbus.configure_command(pmbus.device, "iw_3f001" + code + value)
            if self.temp_ot_enable:
                for value, code in zip(temp_ot_protection, temp_ot_code):
                    pmbus.configure_command(pmbus.device, "iw_3f001" + code + value)

            # write other L11 commands
            for value, code in zip(values_l11, pmbus_l11_hex_codes):
                pmbus.l11_write_command(pmbus.device, "iw_3f003" + code, float(value))

            # write other L16 commands
            for value, code in zip(values_l16, pmbus_l16_hex_codes):
                pmbus.l16_write_command(pmbus.device, "iw_3f003" + code, float(value))

    ###############################################################################################################
    #                                            BIN TO HEX CONVERTER                                             #
    #                                                                                                             #
    #  Description: convert binary to hex                                                                         #
    #  Arguments: s - binary string                                                                               #
    #  Returns: hex number                                                                                        #
    ###############################################################################################################

    def bin_to_hex(self, s):

        return ''.join(["%x" % string.atoi(b, 2) for b in s.split()])

    ###############################################################################################################
    #                                            CREATE POPUP WINDOW                                              #
    #                                                                                                             #
    #  Description: create popup windows when warning or fault occurs                                             #
    #  Arguments: message ("warning"/"fault"), val ("VIN"/"VOUT"/"TEMP"/"IOUT"), sign ("+"/"-"/None)              #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def popup(self, message, val, sign):

        values = ["VIN", "VOUT", "TEMP", "IOUT"]

        msg_box = QtGui.QMessageBox()

        # determine if "warning" or "fault", what sign and what value to display correct popup
        for value in values:
            if val == value:
                if message == "warning":
                    if sign == "+":
                        msg_box.setIconPixmap(QtGui.QPixmap('icons/warning.png'))
                        msg_box.setWindowTitle("Warning")
                        msg_box.setText("Warning! " + val + " value is over " + val + "_OV_WARNING threshold!")
                    elif sign == "-":
                        msg_box.setIconPixmap(QtGui.QPixmap('icons/warning.png'))
                        msg_box.setWindowTitle("Warning")
                        msg_box.setText("Warning! " + val + " value is under " + val + "_UV_WARNING threshold!")
                    else:
                        msg_box.setIconPixmap(QtGui.QPixmap('icons/warning.png'))
                        msg_box.setWindowTitle("Warning")
                        if value == "IOUT":
                            msg_box.setText("Warning! " + val + " value is over " + val + "_OC_WARNING threshold!")
                        elif value == "TEMP":
                            msg_box.setText("Warning! " + val + " value is over " + val + "_OT_WARNING threshold!")
                elif message == "fault":
                    if sign == "+":
                        msg_box.setIconPixmap(QtGui.QPixmap('icons/fault.png'))
                        msg_box.setWindowTitle("Fault")
                        msg_box.setText("Fault! " + val + " value is over " + val + "_OV_FAULT threshold!")
                    elif sign == "-":
                        msg_box.setIconPixmap(QtGui.QPixmap('icons/fault.png'))
                        msg_box.setWindowTitle("Fault")
                        msg_box.setText("Fault! " + val + " value is under " + val + "_UV_FAULT threshold!")
                    else:
                        msg_box.setIconPixmap(QtGui.QPixmap('icons/fault.png'))
                        msg_box.setWindowTitle("Fault")
                        if value == "IOUT":
                            msg_box.setText("Fault! " + val + " value is over " + val + "_OC_FAULT threshold!")
                        elif value == "TEMP":
                            msg_box.setText("Fault! " + val + " value is over " + val + "_OT_FAULT threshold!")
        msg_box.exec_()

    ###############################################################################################################
    #                                      UPDATE REAL-TIME READINGS                                              #
    #                                                                                                             #
    #  Description: update real-time readings on "Monitoring" tab and display popup if fault or warning occurs    #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def update_monitoring_labels(self):

        vin_average = pmbus.l11_query_command(pmbus.device, "iq_3f010288")
        self.vin_average_label.setText("VIN:  " + vin_average + " V")
        if self.is_vin_ov_enabled:
            if self.device_on:
                if float(vin_average) > float(self.vin_ov_warning.text()):
                    self.popup("warning", "VIN", "+")
                if float(vin_average) > float(self.vin_ov_fault.text()):
                    self.popup("fault", "VIN", "+")
        if self.is_vin_uv_enabled:
            if self.device_on:
                if float(vin_average) < float(self.vin_uv_warning.text()):
                    self.popup("warning", "VIN", "-")
                if float(vin_average) < float(self.vin_uv_fault.text()):
                    self.popup("fault", "VIN", "-")

        vout_average = pmbus.l16_query_command(pmbus.device, "iq_3f01028B")
        self.vout_average_label.setText("VOUT:  " + vout_average + " V")
        if self.is_vout_ov_enabled:
            if self.device_on:
                if float(vout_average) > float(self.vout_ov_warning.text()):
                    self.popup("warning", "VOUT", "+")
                if float(vout_average) > float(self.vout_ov_fault.text()):
                    self.popup("fault", "VOUT", "+")
        if self.is_vout_uv_enabled:
            if self.device_on:
                if float(vout_average) < float(self.vout_uv_warning.text()):
                    self.popup("warning", "VOUT", "-")
                if float(vout_average) < float(self.vout_uv_fault.text()):
                    self.popup("fault", "VOUT", "-")

        iout_average = pmbus.l11_query_command(pmbus.device, "iq_3f01028C")
        self.iout_average_label.setText("IOUT:  " + iout_average + " A")
        if self.is_iout_enabled:
            if self.device_on:
                if float(iout_average) > float(self.iout_oc_warning.text()):
                    self.popup("warning", "IOUT", "")
                if float(iout_average) > float(self.iout_oc_fault.text()):
                    self.popup("fault", "IOUT", "")

        temp_average = pmbus.l11_query_command(pmbus.device, "iq_3f01028E")
        self.temp_average_label.setText("TEMP:  " + temp_average + " " + u"\u00b0" + "C")
        if self.is_temp_enabled:
            if self.device_on:
                if float(temp_average) > float(self.temp_ot_warning.text()):
                    self.popup("warning", "TEMP", "")
                if float(temp_average) > float(self.temp_ot_fault.text()):
                    self.popup("fault", "TEMP", "")

    ###############################################################################################################
    #                                         PAUSE REAL-TIME PLOTS                                               #
    #                                                                                                             #
    #  Description: signal created for "Monitoring" button to pause real-time plots                               #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def do_pause(self):

        self.monitoring_but.clicked.connect(self.graph.stop_timer)

    ###############################################################################################################
    #                                      HANDLE CONTROL PIN BUTTON                                              #
    #                                                                                                             #
    #  Description: handle "Control Pin" button which turns on/off the device                                     #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_control_pin(self):

        pmbus.configure_command(pmbus.device, "iw_3f0020216")  # set ON_OFF_CONFIG to 0x16 for Control Pin
        if self.index_pin:
            self.device_on = 1
            pmbus.configure_command(pmbus.device, "ip_1")
        else:
            self.device_on = 0
            pmbus.configure_command(pmbus.device, "ip_0")
        self.index_pin = not self.index_pin

    ###############################################################################################################
    #                                      HANDLE CLEAR FAULTS BUTTON                                             #
    #                                                                                                             #
    #  Description: handle "Clear Faults" button on "Monitoring tab to clear register bits                        #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_clear_faults(self):

        pmbus.configure_command(pmbus.device, "iw_3f00103")  # set CLEAR FAULTS command

    ###############################################################################################################
    #                                      HANDLE OPERATION CMD BUTTON                                            #
    #                                                                                                             #
    #  Description: handle "OPERATION_CMD" button on "Monitoring" tab which turns on/off the device               #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_operation_cmd(self):

        if self.index_oper_cmd:
            pmbus.configure_command(pmbus.device, "iw_3f0020180")  # turn device on
        else:
            if self.cb_mon.currentText() == "Immediate off w/o sequencing":
                pmbus.configure_command(pmbus.device, "iw_3f0020100")  # 0x00 immediate off w/o sequencing
            elif self.cb_mon.currentText() == "Soft off with sequencing":
                pmbus.configure_command(pmbus.device, "iw_3f0020140")  # 0x40 soft off with sequencing
            elif self.cb_mon.currentText() == "On":
                pmbus.configure_command(pmbus.device, "iw_3f0020180")  # 0x80 on
            elif self.cb_mon.currentText() == "Margin Low w/o fault":
                pmbus.configure_command(pmbus.device, "iw_3f0020194")  # 0x94 margin low w/o fault
            elif self.cb_mon.currentText() == "Margin Low with fault":
                pmbus.configure_command(pmbus.device, "iw_3f0020198")  # 0x98 margin low with fault
            elif self.cb_mon.currentText() == "Margin High w/o fault":
                pmbus.configure_command(pmbus.device, "iw_3f00201A4")  # 0xA4 margin high w/o fault
            elif self.cb_mon.currentText() == "Margin High with fault":
                pmbus.configure_command(pmbus.device, "iw_3f00201A8")  # 0xA8 margin high with fault
        self.index_oper_cmd = not self.index_oper_cmd

    ###############################################################################################################
    #                                      HANDLE NUMBER OF RETRIES                                               #
    #                                                                                                             #
    #  Description: handle "Number of retries" combo-box on "Protection" tab                                      #
    #  Arguments: widget (vout ov / vout uv / vin ov / vin uv / iout oc / temp ot, i (index of the selection)     #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_retries(self, widget, i):

        if widget == self.vout_ov_retry:
            self.num_retries_a = i
        if widget == self.vout_uv_retry:
            self.num_retries_b = i
        if widget == self.vin_ov_retry:
            self.num_retries_c = i
        if widget == self.vin_uv_retry:
            self.num_retries_d = i
        if widget == self.iout_oc_retry:
            self.num_retries_e = i
        if widget == self.temp_ot_retry:
            self.num_retries_f = i

    ###############################################################################################################
    #                                      HANDLE NUMBER OF TYPES OF RESPONSES                                    #
    #                                                                                                             #
    #  Description: handle "Type of response" combo-box on "Protection" tab                                       #
    #  Arguments: widget (vout ov / vout uv / vin ov / vin uv / iout oc / temp ot, i (index of the selection)     #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_responses(self, widget, i):

        if widget == self.vout_ov_resp:
            self.num_resp_a = i
            # PMBus device continues; delay = 0, retry = 0
            if i == 0:
                self.vout_ov_delay.setEnabled(False)
                self.vout_ov_delay.setCurrentIndex(0)
                self.vout_ov_retry.setEnabled(False)
                self.vout_ov_retry.setCurrentIndex(0)
                self.num_retries_a = 0
                self.num_delay_a = 0
            # Delay + retries
            if i == 1:
                self.vout_ov_delay.setEnabled(True)
                self.vout_ov_retry.setEnabled(True)
            # Retries only; delay = 0
            if i == 2:
                self.vout_ov_delay.setEnabled(False)
                self.vout_ov_delay.setCurrentIndex(0)
                self.vout_ov_retry.setEnabled(True)
                self.num_delay_a = 0
            # Device shuts down immediately; retry = 0, delay = 0
            if i == 3:
                self.vout_ov_delay.setEnabled(False)
                self.vout_ov_delay.setCurrentIndex(0)
                self.vout_ov_retry.setEnabled(False)
                self.vout_ov_retry.setCurrentIndex(0)
                self.num_retries_a = 0
                self.num_delay_a = 0

        if widget == self.vout_uv_resp:
            self.num_resp_b = i
            if i == 0:
                self.vout_uv_delay.setEnabled(False)
                self.vout_uv_delay.setCurrentIndex(0)
                self.vout_uv_retry.setEnabled(False)
                self.vout_uv_retry.setCurrentIndex(0)
                self.num_retries_b = 0
                self.num_delay_b = 0
            # Delay + retries
            if i == 1:
                self.vout_uv_delay.setEnabled(True)
                self.vout_uv_retry.setEnabled(True)
            # Retries only; delay = 0
            if i == 2:
                self.vout_uv_delay.setEnabled(False)
                self.vout_uv_delay.setCurrentIndex(0)
                self.vout_uv_retry.setEnabled(True)
                self.num_delay_b = 0
            # Device shuts down immediately; retry = 0, delay = 0
            if i == 3:
                self.vout_uv_delay.setEnabled(False)
                self.vout_uv_delay.setCurrentIndex(0)
                self.vout_uv_retry.setEnabled(False)
                self.vout_uv_retry.setCurrentIndex(0)
                self.num_retries_b = 0
                self.num_delay_b = 0

        if widget == self.vin_ov_resp:
            self.num_resp_c = i
            if i == 0:
                self.vin_ov_delay.setEnabled(False)
                self.vin_ov_delay.setCurrentIndex(0)
                self.vin_ov_retry.setEnabled(False)
                self.vin_ov_retry.setCurrentIndex(0)
                self.num_retries_c = 0
                self.num_delay_c = 0
            # Delay + retries
            if i == 1:
                self.vin_ov_delay.setEnabled(True)
                self.vin_ov_retry.setEnabled(True)
            # Retries only; delay = 0
            if i == 2:
                self.vin_ov_delay.setEnabled(False)
                self.vin_ov_delay.setCurrentIndex(0)
                self.vin_ov_retry.setEnabled(True)
                self.num_delay_c = 0
            # Device shuts down immediately; retry = 0, delay = 0
            if i == 3:
                self.vin_ov_delay.setEnabled(False)
                self.vin_ov_delay.setCurrentIndex(0)
                self.vin_ov_retry.setEnabled(False)
                self.vin_ov_retry.setCurrentIndex(0)
                self.num_retries_c = 0
                self.num_delay_c = 0

        if widget == self.vin_uv_resp:
            self.num_resp_d = i
            if i == 0:
                self.vin_uv_delay.setEnabled(False)
                self.vin_uv_delay.setCurrentIndex(0)
                self.vin_uv_retry.setEnabled(False)
                self.vin_uv_retry.setCurrentIndex(0)
                self.num_retries_d = 0
                self.num_delay_d = 0
            # Delay + retries
            if i == 1:
                self.vin_uv_delay.setEnabled(True)
                self.vin_uv_retry.setEnabled(True)
            # Retries only; delay = 0
            if i == 2:
                self.vin_uv_delay.setEnabled(False)
                self.vin_uv_delay.setCurrentIndex(0)
                self.vin_uv_retry.setEnabled(True)
                self.num_delay_d = 0
            # Device shuts down immediately; retry = 0, delay = 0
            if i == 3:
                self.vin_uv_delay.setEnabled(False)
                self.vin_uv_delay.setCurrentIndex(0)
                self.vin_uv_retry.setEnabled(False)
                self.vin_uv_retry.setCurrentIndex(0)
                self.num_retries_d = 0
                self.num_delay_d = 0

        if widget == self.iout_oc_resp:
            self.num_resp_e = i
            if i == 0:
                self.iout_oc_delay.setEnabled(False)
                self.iout_oc_delay.setCurrentIndex(0)
                self.iout_oc_retry.setEnabled(False)
                self.iout_oc_retry.setCurrentIndex(0)
                self.num_retries_e = 0
                self.num_delay_e = 0
            # Delay + retries
            if i == 1:
                self.iout_oc_delay.setEnabled(True)
                self.iout_oc_retry.setEnabled(True)
            # Retries only; delay = 0
            if i == 2:
                self.iout_oc_delay.setEnabled(False)
                self.iout_oc_delay.setCurrentIndex(0)
                self.iout_oc_retry.setEnabled(True)
                self.num_delay_e = 0
            # Device shuts down immediately; retry = 0, delay = 0
            if i == 3:
                self.iout_oc_delay.setEnabled(False)
                self.iout_oc_delay.setCurrentIndex(0)
                self.iout_oc_retry.setEnabled(False)
                self.iout_oc_retry.setCurrentIndex(0)
                self.num_retries_e = 0
                self.num_delay_e = 0

        if widget == self.temp_ot_resp:
            self.num_resp_f = i
            if i == 0:
                self.temp_ot_delay.setEnabled(False)
                self.temp_ot_delay.setCurrentIndex(0)
                self.temp_ot_retry.setEnabled(False)
                self.temp_ot_retry.setCurrentIndex(0)
                self.num_retries_f = 0
                self.num_delay_f = 0
            # Delay + retries
            if i == 1:
                self.temp_ot_delay.setEnabled(True)
                self.temp_ot_retry.setEnabled(True)
            # Retries only; delay = 0
            if i == 2:
                self.temp_ot_delay.setEnabled(False)
                self.temp_ot_delay.setCurrentIndex(0)
                self.temp_ot_retry.setEnabled(True)
                self.num_delay_f = 0
            # Device shuts down immediately; retry = 0, delay = 0
            if i == 3:
                self.temp_ot_delay.setEnabled(False)
                self.temp_ot_delay.setCurrentIndex(0)
                self.temp_ot_retry.setEnabled(False)
                self.temp_ot_retry.setCurrentIndex(0)
                self.num_retries_f = 0
                self.num_delay_f = 0

    ###############################################################################################################
    #                                             HANDLE DELAYS                                                   #
    #                                                                                                             #
    #  Description: handle "Delay" combo-box on "Protection" tab                                                  #
    #  Arguments: widget (vout ov / vout uv / vin ov / vin uv / iout oc / temp ot, i (index of the selection)     #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def handle_delays(self, widget, i):

        if widget == self.vout_ov_delay:
            self.num_delay_a = i
        if widget == self.vout_uv_delay:
            self.num_delay_b = i
        if widget == self.vin_ov_delay:
            self.num_delay_c = i
        if widget == self.vin_uv_delay:
            self.num_delay_d = i
        if widget == self.iout_oc_delay:
            self.num_delay_e = i
        if widget == self.temp_ot_delay:
            self.num_delay_f = i

    ###############################################################################################################
    #                                       DISPLAY REAL-TIME PLOTS                                               #
    #                                                                                                             #
    #  Description: create group box, set minimum size and fill with the real-time plot for VIN, VOUT and TEMP    #
    #  Arguments: name ("Input Voltage (V)" / "Output Voltage (V)" / "Temperature C"),                            #
    #  value ("vin" / "vout" / "temp")                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def display_plot(self, name, value):

        group_box = QtGui.QGroupBox(name)
        group_layout = QtGui.QHBoxLayout()
        # add plot diagram to graph_frame
        self.graph = Monitoring.GraphCanvas(value)
        self.graph.setMinimumSize(200, 400)
        group_layout.addWidget(self.graph)
        group_box.setLayout(group_layout)
        self.scroll_layout.addWidget(group_box)
