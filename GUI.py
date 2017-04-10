# -*- coding: utf-8 -*-
#####################################################################
#                                                                   #
#                               Gui.py                              #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#             Description: GUI Application implementation           #
#                                                                   #
#####################################################################

from PyQt4 import QtCore, QtGui
import LinearConversions
import SequencingPlot
import Monitoring
from PMBusCall import pmbus
import itertools
from collections import OrderedDict
from operator import itemgetter
import functools

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class GuiMainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(GuiMainWindow, self).__init__(parent)
        self.paint_panel = 0
        self.index = 1
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_monitoring_labels)
        self.timer.start(1000)
        self.linear_conv = LinearConversions.LinearConversions()

    def set_style(self, main_window):
        main_window.resize(1200, 700)
        main_window.setStyleSheet(_fromUtf8("QFrame{\n"
                                           "background-color:rgb(255, 255, 255);\n"
                                           "border: 1px solid rgb(147, 147, 147) } \n"

                                           "QLabel{\n"
                                           "border:none;\n"
                                           "background-color:transparent;}\n"

                                           "QToolButton{\n"
                                           "background-color:transparent;\n"
                                           "border:none;}\n"

                                           "QToolButton:pressed{\n"
                                           "background-color:rgb(215, 224, 243);\n"
                                           "border: 1px solid rgb(147, 147, 147);}\n"

                                           "QToolButton:checked{\n"
                                           "background-color:rgb(101, 135, 205);\n"
                                           "border: 1px solid rgb(147, 147, 147);}\n"

                                           "QToolButton:hover {\n"
                                           "background-color:rgb(215, 224, 243);}\n"

                                           "QGroupBox { background-color:rgb(220, 228, 244); }\n"

                                           "QMainWindow { background-color:rgb(220, 228, 244); }\n"

                                           "QStackedWidget {\n"
                                           "background-color:rgb(220, 228, 244);\n"
                                           "border: 1px solid rgb(147, 147, 147)}\n" ))

    def menu(self):

        # create new buttons_frame and put menu buttons in there
        self.buttons_frame = QtGui.QFrame(self.central_widget)
        self.buttons_frame.setGeometry(QtCore.QRect(180, 10, 1010, 71))
        self.buttons_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.buttons_frame.setFrameShadow(QtGui.QFrame.Raised)

        # "main" button
        main = self.create_button_tab(10, 10, 190, 51, "Main", self.page1, "icons/main.png")
        main.setStatusTip('Power Stage')
        # "configuration" button
        conf = self.create_button_tab(210, 10, 190, 51, "Configuration", self.page2, "icons/conf.png")
        conf.setStatusTip('Startup and shutdown parameters configuration')
        # "pin" button
        pin = self.create_button_tab(410, 10, 190, 51, "Tuning", self.page3, "icons/calc.png")
        pin.setStatusTip('Direct access functions and calculators')
        # "protection" button
        prot = self.create_button_tab(610, 10, 190, 51, "Protection", self.page4, "icons/prot.png")
        prot.setStatusTip("Set device's protection parameters")
        # "monitor" button
        mon = self.create_button_tab(810, 10, 190, 51, "Monitoring", self.page5, "icons/mon.png")
        mon.setStatusTip("Device's monitoring")

    def text_validation(self, text_field):
        reg_ex = QtCore.QRegExp("^\d+(\.\d{1,2})?$")
        text_validator = QtGui.QRegExpValidator(reg_ex, text_field)
        text_field.setValidator(text_validator)

    def text_validation_hex(self, text_field):
        reg_ex = QtCore.QRegExp("^0x[0-9A-Fa-f]+$")
        text_validator = QtGui.QRegExpValidator(reg_ex, text_field)
        text_field.setValidator(text_validator)

    def create_label(self, group, x, y, w, h, text):

        label = QtGui.QLabel(group)
        label.setGeometry(QtCore.QRect(x, y, w, h))
        label.setText(text)
        return label

    def create_button_tab(self, x, y, w, h, text, page, icon):

        button_tab = QtGui.QToolButton(self.buttons_frame)
        button_tab.setGeometry(QtCore.QRect(x, y, w, h))
        button_tab.setCheckable(True)
        button_tab.setAutoExclusive(True)
        button_tab.clicked.connect(page)
        button_tab.setText(_translate("MainWindow", text, None))
        button_tab.setIcon(QtGui.QIcon(icon))
        button_tab.setIconSize(QtCore.QSize(32, 32))
        button_tab.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon | QtCore.Qt.AlignLeading)
        return button_tab

    def size_and_name(self, component, x, y, w, h, name):

        component.setGeometry(QtCore.QRect(x, y, w, h))
        component.setTitle(_translate("MainWindow", name, None))

    def create_line_edit(self, text):

        line_edit = QtGui.QLineEdit()
        line_edit.setAlignment(QtCore.Qt.AlignRight)
        line_edit.setText(text)
        self.text_validation(line_edit)  # validate user input
        arg = functools.partial(self.handle_editing_finished, line_edit)
        line_edit.textChanged.connect(arg)
        return line_edit

    def create_hex_line_edit(self, text):

        line_edit = QtGui.QLineEdit()
        line_edit.setAlignment(QtCore.Qt.AlignRight)
        line_edit.setText(text)
        self.text_validation_hex(line_edit)  # validate user input
        arg = functools.partial(self.handle_hex_lineedit, line_edit)
        line_edit.textChanged.connect(arg)
        return line_edit

    def create_checkbox(self):

        checkbox = QtGui.QCheckBox()
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.state_changed)
        return checkbox

    def handle_hex_lineedit(self, line_edit):
        widget = line_edit
        if widget.text().isEmpty():
            widget.setText("0x0000")

    def handle_editing_finished(self, line_edit):

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

        if self.rwv_l11.isModified() and not self.rwv_l11.text().isEmpty():
            value = self.rwv_l11.text()
            self.encoded_hex_l11.setText(self.linear_conv.float_to_l11(float(value)))

        if self.rwv_l16.isModified() and not self.rwv_l16.text().isEmpty():
            value = self.rwv_l16.text()
            self.encoded_hex_l16.setText(self.linear_conv.float_to_l16(float(value)))

        if self.encoded_hex_l11.isModified() and not self.encoded_hex_l11.text().isEmpty():
            value = self.encoded_hex_l11.text()
            self.rwv_l11.setText(self.linear_conv.l11_to_float(int(value)))

        if self.encoded_hex_l16.isModified() and not self.encoded_hex_l16.text().isEmpty():
            value = self.encoded_hex_l16.text()
            self.rwv_l16.setText(self.linear_conv.l16_to_float(int(value)))

        widget = line_edit
        if widget.text().isEmpty():
            widget.setText("0")

    def state_changed(self):

        is_checked = [self.vout_ov_enable.isChecked(), self.vout_uv_enable.isChecked(),
                      self.vin_uv_enable.isChecked(), self.vin_ov_enable.isChecked(),
                      self.iout_oc_enable.isChecked(), self.temp_ot_enable.isChecked()]

        widgets = [self.vout_ov_warning, self.vout_ov_fault, self.vout_ov_delay,
                   self.vout_ov_walert, self.vout_ov_falert, self.vout_uv_warning,
                   self.vout_uv_fault, self.vout_uv_delay, self.vout_uv_walert,
                   self.vout_uv_falert, self.vin_ov_warning, self.vin_ov_fault,
                   self.vin_ov_delay, self.vin_ov_walert, self.vin_ov_falert,
                   self.vin_uv_warning, self.vin_uv_fault, self.vin_uv_delay,
                   self.vin_uv_walert, self.vin_uv_falert, self.iout_oc_warning,
                   self.iout_oc_fault, self.iout_oc_delay, self.iout_oc_walert,
                   self.iout_oc_falert, self.temp_ot_warning, self.temp_ot_fault,
                   self.temp_ot_delay, self.temp_ot_walert, self.temp_ot_falert]

        if self.vout_ov_enable.isChecked():
            for i in range(5):
                widgets[i].setEnabled(True)
        else:
            for i in range(5):
                widgets[i].setEnabled(False)

        if self.vout_uv_enable.isChecked():
            for i in range(5, 10):
                widgets[i].setEnabled(True)
        else:
            for i in range(5, 10):
                widgets[i].setEnabled(False)

        if self.vin_ov_enable.isChecked():
            for i in range(10, 15):
                widgets[i].setEnabled(True)
        else:
            for i in range(10, 15):
                widgets[i].setEnabled(False)

        if self.vin_uv_enable.isChecked():
            for i in range(15, 20):
                widgets[i].setEnabled(True)
        else:
            for i in range(15, 20):
                widgets[i].setEnabled(False)

        if self.iout_oc_enable.isChecked():
            for i in range(20, 25):
                widgets[i].setEnabled(True)
        else:
            for i in range(20, 25):
                widgets[i].setEnabled(False)

        if self.temp_ot_enable.isChecked():
            for i in range(25, 30):
                widgets[i].setEnabled(True)
        else:
            for i in range(25, 30):
                widgets[i].setEnabled(False)

    def selection_change(self, i):

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

        print "Current index", i, "selection changed ", self.cb.currentText()

    def page1_main(self):

        # create page
        self.page = QtGui.QWidget()

        # create group box
        self.power_stage_box = QtGui.QGroupBox(self.page)
        self.size_and_name(self.power_stage_box, 19, 9, 970, 535, "Power Stage")

        # frame for block diagram of EM2130
        self.schematic = QtGui.QLabel(self.power_stage_box)
        self.schematic.setGeometry(QtCore.QRect(20, 20, 695, 409))
        pix_map = QtGui.QPixmap('diagrams/blockdiagram-em2130.jpg')
        self.schematic.setPixmap(pix_map)
        self.schematic.setStatusTip('EM2130 Circuit Diagram')
        self.schematic.setStyleSheet('border: 1px solid rgb(147, 147, 147)')

        # PMBus variables
        vout_val = pmbus.l16_query_command(pmbus.device, "iq_3f010221")  # vout_command L16

        # voltage group box
        self.voltage_box = QtGui.QGroupBox(self.power_stage_box)
        self.size_and_name(self.voltage_box, 750, 20, 181, 241, "Voltage")

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        self.voltage_box.setLayout(grid)

        # text fields for voltage group
        self.vin_nom = self.create_line_edit("12")
        self.vin_nom.setStatusTip('Enter here the nominal input voltage')
        self.vout_nom = self.create_line_edit(vout_val)
        self.vout_nom.setStatusTip('Enter here the nominal output voltage')
        self.marg_high = self.create_line_edit("5")
        self.marg_high.setStatusTip('Enter here the percent increase of VOUT')
        self.marg_low = self.create_line_edit("5")
        self.marg_low.setStatusTip('Enter here the percent decrease of VOUT')

        grid.addWidget(QtGui.QLabel("Nominal"), 0, 1)
        grid.addWidget(QtGui.QLabel("VIN"), 1, 0)
        grid.addWidget(self.vin_nom, 1, 1)
        grid.addWidget(QtGui.QLabel("V"), 1, 2)
        grid.addWidget(QtGui.QLabel("VOUT"), 2, 0)
        grid.addWidget(self.vout_nom, 2, 1)
        grid.addWidget(QtGui.QLabel("V"), 2, 2)
        grid.addWidget(QtGui.QLabel(" "), 3, 0)

        grid.addWidget(QtGui.QLabel("Margin High"), 4, 0)
        grid.addWidget(self.marg_high, 4, 1)
        grid.addWidget(QtGui.QLabel("%"), 4, 2)
        grid.addWidget(QtGui.QLabel("Margin Low"), 5, 0)
        grid.addWidget(self.marg_low, 5, 1)
        grid.addWidget(QtGui.QLabel("%"), 5, 2)
        grid.addWidget(QtGui.QLabel(" "), 6, 0)


        self.stacked_widget.addWidget(self.page)

    def page2_configuration(self):

        # create page 2
        self.page_2 = QtGui.QWidget()

        #  PMBus variables
        ton_delay_val = pmbus.l11_query_command(pmbus.device, "iq_3f010260")
        toff_delay_val = pmbus.l11_query_command(pmbus.device, "iq_3f010264")
        ton_rise_val = pmbus.l11_query_command(pmbus.device, "iq_3f010261")
        toff_fall_val = pmbus.l11_query_command(pmbus.device, "iq_3f010265")
        ton_max_val = pmbus.l11_query_command(pmbus.device, "iq_3f010262")  # ton max fault limit L11
        toff_max_val = pmbus.l11_query_command(pmbus.device, "iq_3f010266")  # toff_max warn limit L11
        vout_on_val = pmbus.l16_query_command(pmbus.device, "iq_3f010221")  # vout command L16
        vout_off_val = pmbus.l16_query_command(pmbus.device, "iq_3f0102E0")  # mfr_vout_off L16

        # create configuration group box
        self.configuration_box = QtGui.QGroupBox(self.page_2)
        self.size_and_name(self.configuration_box, 19, 9, 970, 350, "Sequencing Diagram")

        self.param_box = QtGui.QGroupBox(self.page_2)
        self.size_and_name(self.param_box, 19, 360, 970, 190, "Parameters")

        # set text fields
        self.ton_delay = self.create_line_edit(ton_delay_val)
        self.ton_delay.setStatusTip('Enter here turn on delay interval')
        self.toff_delay = self.create_line_edit(toff_delay_val)
        self.toff_delay.setStatusTip('Enter here turn off delay interval')
        self.ton_rise = self.create_line_edit(ton_rise_val)
        self.ton_rise.setStatusTip('Enter here turn on rise interval')
        self.toff_fall = self.create_line_edit(toff_fall_val)
        self.toff_fall.setStatusTip('Enter here turn off fall interval')
        self.ton_max = self.create_line_edit(ton_max_val)
        self.ton_max.setStatusTip('Enter here turn on max interval')
        self.toff_max = self.create_line_edit(toff_max_val)
        self.toff_max.setStatusTip('Enter here turn off max interval')
        self.vout_on = self.create_line_edit(vout_on_val)
        self.vout_on.setStatusTip('Enter here the desired output voltage')
        self.vout_off = self.create_line_edit(vout_off_val)
        self.vout_off.setStatusTip('Enter here the terminal value of the output voltage')

        # set combo box
        self.cb = QtGui.QComboBox()
        self.cb.setStatusTip('Select the starting condition for the sequencer')
        self.cb.addItem("CTRL_POS")
        self.cb.addItem("CTRL_NEG")
        self.cb.addItem("OPERATION_CMD")
        self.cb.currentIndexChanged.connect(self.selection_change)

        grid = QtGui.QGridLayout()
        grid.setSpacing(20)
        self.param_box.setLayout(grid)

        # first row
        grid.addWidget(QtGui.QLabel("Delay"), 0, 2, 0, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("\t"), 0, 3, 0, 1)
        grid.addWidget(QtGui.QLabel("\t"), 0, 4, 0, 1)
        grid.addWidget(QtGui.QLabel("Ramping"), 0, 5, 0, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("\t"), 0, 6, 0, 1)
        grid.addWidget(QtGui.QLabel("\t"), 0, 7, 0, 1)
        grid.addWidget(QtGui.QLabel("Max Timing"), 0, 8, 0, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("\t"), 0, 9, 0, 1)
        grid.addWidget(QtGui.QLabel("\t"), 0, 10, 0, 1)
        grid.addWidget(QtGui.QLabel("VOUT"), 0, 11, 0, 1, QtCore.Qt.AlignTop)
        grid.setVerticalSpacing(20)
        grid.addWidget(QtGui.QLabel(" "), 1, 0)
        grid.addWidget(QtGui.QLabel("Device Rise:"), 1, 1)
        grid.addWidget(QtGui.QLabel("TON_DELAY:"), 1, 2)
        grid.addWidget(self.ton_delay, 1, 3)
        grid.addWidget(QtGui.QLabel("ms"), 1, 4)
        grid.addWidget(QtGui.QLabel("TON_RISE:"), 1, 5)
        grid.addWidget(self.ton_rise, 1, 6)
        grid.addWidget(QtGui.QLabel("ms"), 1, 7)
        grid.addWidget(QtGui.QLabel("TON_MAX:"), 1, 8)
        grid.addWidget(self.ton_max, 1, 9)
        grid.addWidget(QtGui.QLabel("ms"), 1, 10)
        grid.addWidget(QtGui.QLabel("ON:"), 1, 11)
        grid.addWidget(self.vout_on, 1, 12)
        grid.addWidget(QtGui.QLabel("V"), 1, 13)
        grid.addWidget(QtGui.QLabel(" "), 1, 14)

        # second row
        grid.addWidget(QtGui.QLabel(" "), 2, 0)
        grid.addWidget(QtGui.QLabel("Device Fall:"), 2, 1)
        grid.addWidget(QtGui.QLabel("TOFF_DELAY:"), 2, 2)
        grid.addWidget(self.toff_delay, 2, 3)
        grid.addWidget(QtGui.QLabel("ms"), 2, 4)
        grid.addWidget(QtGui.QLabel("TOFF_FALL:"), 2, 5)
        grid.addWidget(self.toff_fall, 2, 6)
        grid.addWidget(QtGui.QLabel("ms"), 2, 7)
        grid.addWidget(QtGui.QLabel("TOFF_MAX:"), 2, 8)
        grid.addWidget(self.toff_max, 2, 9)
        grid.addWidget(QtGui.QLabel("ms"), 2, 10)
        grid.addWidget(QtGui.QLabel("OFF:"), 2, 11)
        grid.addWidget(self.vout_off, 2, 12)
        grid.addWidget(QtGui.QLabel("V"), 2, 13)
        grid.addWidget(QtGui.QLabel(" "), 2, 14)

        # third row
        grid.addWidget(QtGui.QLabel(" "), 3, 0)
        grid.addWidget(QtGui.QLabel("Device Startup:"), 3, 1)
        grid.addWidget(self.cb, 3, 2, 1, 2)
        grid.addWidget(QtGui.QLabel(" "), 4, 0)


        self.graph_frame = QtGui.QFrame(self.configuration_box)
        self.graph_frame.setGeometry(QtCore.QRect(20, 20, 930, 315))

        self.main_layout = QtGui.QGridLayout()
        self.graph_frame.setLayout(self.main_layout)

        # add plot diagram to graph_frame
        self.paint_panel = SequencingPlot.Graph()
        self.paint_panel.setStatusTip('Sequencing diagram')
        self.paint_panel.close()
        self.main_layout.addWidget(self.paint_panel, 0, 0)

        #  add labels to graph
        self.create_label(self.configuration_box, 115, 275, 65, 20, "TON_DELAY")
        self.create_label(self.configuration_box, 560, 275, 65, 20, "TOFF_DELAY")
        self.create_label(self.configuration_box, 235, 275, 65, 20, "TON_RISE")
        self.create_label(self.configuration_box, 675, 275, 65, 20, "TOFF_FALL")
        self.create_label(self.configuration_box, 840, 260, 65, 20, "Time")
        self.tonmax_label = self.create_label(self.configuration_box, 255, 295, 100, 20, "TON_MAX = " + ton_max_val)
        self.toffmax_label = self.create_label(self.configuration_box, 720, 295, 100, 20, "TOFF_MAX = " + toff_max_val)
        self.tondelay_label = self.create_label(self.configuration_box, 165, 235, 65, 20, ton_delay_val)
        self.tonrise_label = self.create_label(self.configuration_box, 277, 235, 65, 20, ton_rise_val)
        self.toffdelay_label = self.create_label(self.configuration_box, 613, 235, 65, 20, toff_delay_val)
        self.tofffall_label = self.create_label(self.configuration_box, 725, 235, 65, 20, toff_fall_val)
        self.voutoff_label = self.create_label(self.configuration_box, 30, 200, 100, 30,
                                               "VOUT OFF \n" + vout_off_val + " V")
        self.vouton_label = self.create_label(self.configuration_box, 30, 60, 100, 30,
                                              "VOUT ON \n" + vout_on_val + " V")

        self.stacked_widget.addWidget(self.page_2)

    def page3_pin(self):

        # create page 3
        self.page_3 = QtGui.QWidget()

        # Python Dictionary:
        # Command Name : (Command In Decimal, Data Size)
        self.pmbus_commands = {
            "OPERATION": (1, 1),                     "ON_OFF_CONFIG": (2, 1),                "CLEAR_FAULTS": (3, 0),
            "PHASE": (4, 1),                         "WRITE_PROTECT": (16, 1),               "STORE_DEFAULT_ALL": (17, 0),
            "RESTORE_DEFAULT_ALL": (18, 0),          "STORE_DEFAULT_CODE": (19, 1),          "RESTORE_DEFAULT_CODE": (20, 1),
            "VOUT_MODE": (32, 1),                    "VOUT_COMMAND": (33, 2),                "VOUT_TRIM": (34, 2),
            "VOUT_CAL_OFFSET": (35, 2),              "VOUT_MARGIN_HIGH": (37, 2),            "VOUT_MARGIN_LOW": (38, 2),
            "VOUT_SCALE_LOOP": (41, 2),              "VOUT_SCALE_MONITOR": (42, 2),          "VIN_ON": (53, 2),
            "VIN_OFF": (54, 2),                      "IOUT_CAL_GAIN": (56, 2),               "IOUT_CAL_OFFSET": (57, 2),
            "VOUT_OV_FAULT_LIMIT": (64, 2),          "VOUT_OV_FAULT_RESPONSE" : (65, 1),      "VOUT_OV_WARN_LIMIT": (66, 2),
            "VOUT_UV_WARN_LIMIT": (67, 2),           "VOUT_UV_FAULT_LIMIT": (68, 2),         "VOUT_UV_FAULT_RESPONSE": (69, 1),
            "IOUT_OC_FAULT_LIMIT": (70, 2),          "IOUT_OC_FAULT_RESPONSE": (71, 1),      "IOUT_OC_LV_FAULT_LIMIT": (72, 2),
            "IOUT_OC_LV_FAULT_RESPONSE": (73, 1),    "IOUT_OC_WARN_LIMIT": (74, 2),          "OT_FAULT_LIMIT": (79, 2),
            "OT_FAULT_RESPONSE": (80, 1),            "OT_WARN_LIMIT": (81, 2),               "VIN_OV_FAULT_LIMIT": (85, 2),
            "VIN_OV_FAULT_RESPONSE": (86, 1),        "VIN_OV_WARN_LIMIT": (87, 2),           "VIN_UV_WARN_LIMIT": (88, 2),
            "VIN_UV_FAULT_LIMIT": (89, 2),           "VIN_UV_FAULT_RESPONSE": (90, 1),       "POWER_GOOD_ON": (94, 2),
            "POWER_GOOD_OFF": (95, 2),               "TON_DELAY": (96, 2),                   "TON_RISE": (97, 2),
            "TON_MAX_FAULT_LIMIT": (98, 2),          "TOFF_DELAY": (100, 2),                 "TOFF_FALL": (101, 2),
            "TOFF_MAX_WARN_LIMIT": (102, 2),         "STATUS_BYTE": (120, 1),                "STATUS_WORD": (121, 2),
            "STATUS_VOUT": (122, 1),                 "STATUS_IOUT": (123, 1),                "STATUS_INPUT": (124, 1),
            "STATUS_TEMPERATURE": (125, 1),          "STATUS_CML": (126, 1),                 "STATUS_MFR_SPECIFIC": (128, 1),
            "READ_VIN": (136, 2),                    "READ_VOUT": (139, 2),                  "READ_IOUT": (140, 2),
            "READ_TEMPERATURE_1": (141, 2),          "READ_TEMPERATURE_2": (142, 2),         "READ_TEMPERATURE_3": (143, 2),
            "READ_DUTY_CYCLE": (148, 2),             "READ_FREQUENCY": (149, 2),             "READ_POUT": (150, 2),
            "PMBUS_REVISION": (152, 1),              "MFR_ID": (153, 4),                     "MFR_MODEL": (154, 4),
            "MFR_REVISION": (155, 4),                "MFR_SERIAL": (158, 12),                "MFR_VIN_MIN": (160, 2),
            "MFR_VOUT_MIN": (164, 2),                "MFR_SPECIFIC_00": (208, 2),            "MFR_SPECIFIC_01": (209, 1),
            "MFR_READ_VCC": (210, 2),                "MFR_RESYNC": (211, 0),                 "MFR_LOCK": (212, 0),
            "MFR_UNLOCK": (213, 4),                  "MFR_FAULT_RESPONSE_CONFIG": (217, 2),  "MFR_RTUNE_CONFIG": (218, 2),
            "MFR_VOUT_MARGIN_HIGH": (219, 2),        "MFR_VOUT_MARGIN_LOW": (220, 2),         "MFR_RTUNE_INDEX": (221, 1),
            "MFR_RVSET_INDEX": (222, 1),             "MFR_VOUT_OFF": (224, 2),               "MFR_EXT_TEMP_CAL_OFFSET": (225, 2),
            "MFR_IOT_FAULT_LIMIT": (226, 2),         "MFR_IOT_WARN_LIMIT": (227, 2),         "MFR_OVL_FAULT_RESPONSE": (228, 1),
            "MFR_IOT_FAULT_RESPONSE": (229, 1),      "MFR_TEMP_ON": (230, 2),                "MFR_PIN_CONFIG": (231, 2),
            "MFR_PHASE_CONTROL": (232, 1),           "MFR_STORE_CONFIG_ADDR_READ": (233, 2), "MFR_STORE_PARAMS_REMAINING": (234, 2),
            "MFR_STORE_CONFIGS_REMAINING": (235, 2), "MFR_STORE_CONFIG_BEGIN": (236, 0),      "MFR_STORE_CONFIG_ADDR_WRITE": (237, 4),
            "MFR_STORE_CONFIG_END": (238, 0)
        }

        # sort dictionary items by value
        self.dict = OrderedDict(sorted(self.pmbus_commands.items(), key=itemgetter(1)))

        # commands numbers in decimal that are READ ONLY
        self.read_only = [32, 136, 139, 140, 141, 142, 143, 148,
                          149, 150, 152, 153, 154, 155, 158, 160,
                          164, 210, 220, 221, 222, 234, 235]
        # command numbers in decimal that are WRITE ONLY
        self.write_only = [3, 17, 18, 19, 20, 211, 212, 236, 237, 238]

        # create group boxes
        calculation_box = QtGui.QGroupBox(self.page_3)
        self.size_and_name(calculation_box, 19, 9, 970, 535, "PMBus Commands & Calculations")

        direct_access_box = QtGui.QGroupBox(calculation_box)
        self.size_and_name(direct_access_box, 20, 30, 300, 470, "Direct Access Functions")

        l11_calc_box = QtGui.QGroupBox(calculation_box)
        self.size_and_name(l11_calc_box, 335, 100, 300, 300, "Linear L11 Format Converter")

        l16_calc_box = QtGui.QGroupBox(calculation_box)
        self.size_and_name(l16_calc_box, 650, 100, 300, 300, "Linear L16 Format Converter")

        # set layout for direct_access_box
        grid = QtGui.QGridLayout()
        grid.setSpacing(20)
        direct_access_box.setLayout(grid)

        # set combo box for pmbus commands
        self.pmbus_cb = QtGui.QComboBox()
        self.pmbus_cb.setStatusTip('\Select PmBus command from the list')
        for key, value in self.dict.iteritems():
            self.pmbus_cb.addItem(key)
        self.pmbus_cb.currentIndexChanged.connect(self.selection_pmbus_commands)

        # set widgets for direct_access_box
        self.code = self.create_line_edit("0x01")
        self.code.setStatusTip('Command in hex')
        self.code.setReadOnly(True)
        self.size = self.create_line_edit("1")
        self.size.setStatusTip('Data size in bytes')
        self.size.setReadOnly(True)

        self.read_hex = self.create_hex_line_edit("0x")
        self.read_hex.setStatusTip('Data in linear format')
        self.read_hex.setReadOnly(True)
        self.read_dec = self.create_hex_line_edit("0")
        self.read_dec.setStatusTip('Data in linear format')
        self.read_dec.setReadOnly(True)
        self.read_l11 = self.create_hex_line_edit("0")
        self.read_l11.setStatusTip('Data in linear format')
        self.read_l11.setReadOnly(True)
        self.read_l16 = self.create_hex_line_edit("0")
        self.read_l16.setStatusTip('Data in linear format')
        self.read_l16.setReadOnly(True)

        self.write_hex = self.create_hex_line_edit("0x0")
        self.write_hex.setStatusTip('Enter here data to write in linear format')
        self.read_direct = QtGui.QPushButton(direct_access_box)
        self.read_direct.setText("Read")
        self.write_direct = QtGui.QPushButton(direct_access_box)
        self.write_direct.setText("Write")

        # add widgets to direct_access_box
        grid.addWidget(self.pmbus_cb, 0, 0, 1, 3)
        grid.addWidget(QtGui.QLabel("Code:"), 1, 0)
        grid.addWidget(self.code, 1, 1)
        grid.addWidget(QtGui.QLabel("Size in Bytes:"), 2, 0)
        grid.addWidget(self.size, 2, 1)
        grid.addWidget(QtGui.QLabel("Decimal:"), 3, 0)
        grid.addWidget(self.read_dec, 3, 1)
        grid.addWidget(self.read_direct, 3, 2)
        grid.addWidget(QtGui.QLabel("Hex:"), 4, 0)
        grid.addWidget(self.read_hex, 4, 1)
        grid.addWidget(QtGui.QLabel("L11:"), 5, 0)
        grid.addWidget(self.read_l11, 5, 1)
        grid.addWidget(QtGui.QLabel("L16:"), 6, 0)
        grid.addWidget(self.read_l16, 6, 1)
        grid.addWidget(QtGui.QLabel("Write:"), 7, 0)
        grid.addWidget(self.write_hex, 7, 1)
        grid.addWidget(self.write_direct, 7, 2)

        # set layout for l11_calc_box
        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(20)
        l11_calc_box.setLayout(grid2)

        # set widgets for l11_calc_box
        self.rwv_l11 = self.create_line_edit("0")
        self.encoded_hex_l11 = self.create_hex_line_edit("0x0000")

        grid2.addWidget(QtGui.QLabel("Format:\t\t      L11"), 0, 0, 1, 2)
        grid2.addWidget(QtGui.QLabel("Real world value:"), 1, 0)
        grid2.addWidget(self.rwv_l11, 1, 1)
        grid2.addWidget(QtGui.QLabel("Encoded hex value:"), 2, 0)
        grid2.addWidget(self.encoded_hex_l11, 2, 1)
        grid2.addWidget(QtGui.QLabel("  "), 3, 0)

        # set layout for l16_calc_box
        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(20)
        l16_calc_box.setLayout(grid3)

        # set widgets for l11_calc_box
        self.rwv_l16 = self.create_line_edit("0")
        self.encoded_hex_l16 = self.create_hex_line_edit("0x0000")

        grid3.addWidget(QtGui.QLabel("Format:\t\t      L16"), 0, 0, 1, 2)
        grid3.addWidget(QtGui.QLabel("Real world value:"), 1, 0)
        grid3.addWidget(self.rwv_l16, 1, 1)
        grid3.addWidget(QtGui.QLabel("Encoded hex value:"), 2, 0)
        grid3.addWidget(self.encoded_hex_l16, 2, 1)
        grid3.addWidget(QtGui.QLabel("  "), 3, 0)

        self.stacked_widget.addWidget(self.page_3)

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
        if pmbus.device == None:
            self.read_direct.setEnabled(False)
        elif code_val is not self.write_only:
            self.read_direct.setEnabled(True)
            self.read_direct.clicked.connect(arg1)
        else:
            self.read_direct.setEnabled(False)

        # set write button
        arg2 = functools.partial(self.handle_wr_direct, cmd_hex)
        if pmbus.device == None:
            self.write_direct.setEnabled(False)
        elif code_val is not self.read_only:
            self.write_direct.setEnabled(True)
            self.write_direct.clicked.connect(arg2)
        else:
            self.write_direct.setEnabled(False)

    def handle_rd_direct(self, arg, size):
        if size > 2:
            size += 1
        response = pmbus.configure_command(pmbus.device, "iq_3f010" + str(size) + str(arg))
        a = response[-4:]
        b = response[1:3]
        a = a.rstrip()
        b = b.rstrip()
        hex_value = "0x" + a + b
        decimal_value = int(hex_value, 16)
        self.read_dec.setText(str(decimal_value))
        self.read_hex.setText(hex_value)

        response_l11 = pmbus.l11_query_command(pmbus.device, "iq_3f010" + str(size) + str(arg))
        response_l16 = pmbus.l16_query_command(pmbus.device, "iq_3f010" + str(size) + str(arg))
        self.read_l11.setText(response_l11)
        self.read_l16.setText(response_l16)

    def handle_wr_direct(self, arg):
        pmbus.write_direct(pmbus.device, "iw_3f003" + arg, self.write_hex.text())

    def page4_protection(self):

        # create page 4
        self.page_4 = QtGui.QWidget()

        # create protection group box
        protection_box = QtGui.QGroupBox(self.page_4)
        self.size_and_name(protection_box, 19, 9, 970, 400, "PMBus Protection Parameters")

        # check boxes
        self.vout_ov_enable = self.create_checkbox()
        self.vout_uv_enable = self.create_checkbox()
        self.vin_ov_enable = self.create_checkbox()
        self.vin_uv_enable = self.create_checkbox()
        self.temp_ot_enable = self.create_checkbox()
        self.iout_oc_enable = self.create_checkbox()
        self.vout_ov_walert = self.create_checkbox()
        self.vout_uv_walert = self.create_checkbox()
        self.vin_ov_walert = self.create_checkbox()
        self.vin_uv_walert = self.create_checkbox()
        self.iout_oc_walert = self.create_checkbox()
        self.temp_ot_walert = self.create_checkbox()
        self.vout_ov_falert = self.create_checkbox()
        self.vout_uv_falert = self.create_checkbox()
        self.vin_ov_falert = self.create_checkbox()
        self.vin_uv_falert = self.create_checkbox()
        self.iout_oc_falert = self.create_checkbox()
        self.temp_ot_falert = self.create_checkbox()

        #  PMBus variables
        vout_ov_war_val = pmbus.l16_query_command(pmbus.device, "iq_3f010242")
        vout_uv_war_val = pmbus.l16_query_command(pmbus.device, "iq_3f010243")
        vin_ov_war_val = pmbus.l11_query_command(pmbus.device, "iq_3f010257")
        vin_uv_war_val = pmbus.l11_query_command(pmbus.device, "iq_3f010258")
        vout_ov_fal_val = pmbus.l16_query_command(pmbus.device, "iq_3f010240")
        vout_uv_fal_val = pmbus.l16_query_command(pmbus.device, "iq_3f010244")
        vin_ov_fal_val = pmbus.l11_query_command(pmbus.device, "iq_3f010255")
        vin_uv_fal_val = pmbus.l11_query_command(pmbus.device, "iq_3f010259")
        iout_oc_war_val = pmbus.l11_query_command(pmbus.device, "iq_3f01024A")
        temp_ot_war_val = pmbus.l11_query_command(pmbus.device, "iq_3f010251")
        temp_ot_fal_val = pmbus.l11_query_command(pmbus.device, "iq_3f01024F")
        iout_oc_fal_val = pmbus.l11_query_command(pmbus.device, "iq_3f010246")

        # text fields
        self.vout_ov_warning = self.create_line_edit(vout_ov_war_val)
        self.vout_ov_warning.setStatusTip('Enter here output over-voltage warning threshold')
        self.vout_uv_warning = self.create_line_edit(vout_uv_war_val)
        self.vout_uv_warning.setStatusTip('Enter here output under-voltage warning threshold')
        self.vin_ov_warning = self.create_line_edit(vin_ov_war_val)
        self.vin_ov_warning.setStatusTip('Enter here input over-voltage warning threshold')
        self.vin_uv_warning = self.create_line_edit(vin_uv_war_val)
        self.vin_uv_warning.setStatusTip('Enter here input under-voltage warning threshold')
        self.iout_oc_warning = self.create_line_edit(iout_oc_war_val)
        self.iout_oc_warning.setStatusTip('Enter here output over-current warning threshold')
        self.temp_ot_warning = self.create_line_edit(temp_ot_war_val)
        self.temp_ot_warning.setStatusTip('Enter here over-temperature warning threshold')

        self.vout_ov_fault = self.create_line_edit(vout_ov_fal_val)
        self.vout_ov_fault.setStatusTip('Enter here output over-voltage fault threshold')
        self.vout_uv_fault = self.create_line_edit(vout_uv_fal_val)
        self.vout_uv_fault.setStatusTip('Enter here output under-voltage fault threshold')
        self.vin_ov_fault = self.create_line_edit(vin_ov_fal_val)
        self.vin_ov_fault.setStatusTip('Enter here input over-voltage fault threshold')
        self.vin_uv_fault = self.create_line_edit(vin_uv_fal_val)
        self.vin_uv_fault.setStatusTip('Enter here input under-voltage fault threshold')
        self.iout_oc_fault = self.create_line_edit(iout_oc_fal_val)
        self.iout_oc_fault.setStatusTip('Enter here output over-current fault threshold')
        self.temp_ot_fault = self.create_line_edit(temp_ot_fal_val)
        self.temp_ot_fault.setStatusTip('Enter here over-temperature fault threshold')

        self.vout_ov_delay = self.create_line_edit("0.00")
        self.vout_ov_delay.setStatusTip('Enter here output over-voltage delay')
        self.vout_uv_delay = self.create_line_edit("0.00")
        self.vout_uv_delay.setStatusTip('Enter here output under-voltage delay')
        self.vin_ov_delay = self.create_line_edit("0.00")
        self.vin_ov_delay.setStatusTip('Enter here input over-voltage delay')
        self.vin_uv_delay = self.create_line_edit("0.00")
        self.vin_uv_fault.setStatusTip('Enter here input under-voltage delay')
        self.iout_oc_delay = self.create_line_edit("0.00")
        self.iout_oc_delay.setStatusTip('Enter here output over-current delay')
        self.temp_ot_delay = self.create_line_edit("0.00")
        self.temp_ot_delay.setStatusTip('Enter here over-temperature delay')

        grid = QtGui.QGridLayout()

        grid.setSpacing(20)
        grid.addWidget(QtGui.QLabel(" "), 0, 1, 1, 1, QtCore.Qt.AlignTop)

        # First row
        grid.addWidget(QtGui.QLabel("Enable"), 1, 2, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("Warning Limit"), 1, 3, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("\t"), 1, 4, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("Fault Limit"), 1, 5, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("\t"), 1, 6, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("Time Delay"), 1, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("\t"), 1, 8, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("Alert (W/F)"), 1, 9, 1, 1, QtCore.Qt.AlignCenter)

        #grid.setVerticalSpacing(40)
        grid.setRowMinimumHeight(5, 5)

        titles = ["VOUT OV", "VOUT UV", "VIN OV", "VIN UV", "IOUT", "TEMP"]
        widgets = [self.vout_ov_enable, self.vout_ov_warning, self.vout_ov_fault, self.vout_ov_delay,
                   self.vout_ov_walert, self.vout_ov_falert, self.vout_uv_enable, self.vout_uv_warning,
                   self.vout_uv_fault, self.vout_uv_delay, self.vout_uv_walert, self.vout_uv_falert,
                   self.vin_ov_enable, self.vin_ov_warning, self.vin_ov_fault, self.vin_ov_delay,
                   self.vin_ov_walert, self.vin_ov_falert, self.vin_uv_enable, self.vin_uv_warning,
                   self.vin_uv_fault, self.vin_uv_delay, self.vin_uv_walert, self.vin_uv_falert,
                   self.iout_oc_enable, self.iout_oc_warning, self.iout_oc_fault, self.iout_oc_delay,
                   self.iout_oc_walert, self.iout_oc_falert, self.temp_ot_enable, self.temp_ot_warning,
                   self.temp_ot_fault, self.temp_ot_delay, self.temp_ot_walert, self.temp_ot_falert]

        items = [2, 3, 4, 5, 6, 7]
        cols = [2, 3, 5, 7, 9, 10]
        rows = [2, 2, 2, 2, 2, 2,
                3, 3, 3, 3, 3, 3,
                4, 4, 4, 4, 4, 4,
                5, 5, 5, 5, 5, 5,
                6, 6, 6, 6, 6, 6,
                7, 7, 7, 7, 7, 7]

        for title, i in zip(titles, items):
            grid.addWidget(QtGui.QLabel("  "), i, 0)
            grid.addWidget(QtGui.QLabel(title), i, 1)
            if i == 6:
                grid.addWidget(QtGui.QLabel("A"), 6, 4)
            elif i == 7:
                grid.addWidget(QtGui.QLabel(u"\u00b0" + "C"), 7, 4)
            else:
                grid.addWidget(QtGui.QLabel("V"), i, 4)
            if i == 6:
                grid.addWidget(QtGui.QLabel("A"), 6, 6)
            elif i == 7:
                grid.addWidget(QtGui.QLabel(u"\u00b0" + "C"), 7, 6)
            else:
                grid.addWidget(QtGui.QLabel("V"), i, 6)
            grid.addWidget(QtGui.QLabel("ms"), i, 8)
            grid.addWidget(QtGui.QLabel("  "), i, 11)


        for value, r, c in zip(widgets, rows, itertools.cycle(cols)):
            grid.addWidget(value, r, c)

        grid.addWidget(QtGui.QLabel(" "), 8, 0)

        # create on/off levels group box
        on_off_lvl_box = QtGui.QGroupBox(self.page_4)
        self.size_and_name(on_off_lvl_box, 19, 420, 650, 125, "ON/OFF Levels")

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)

        power_on_val = pmbus.l16_query_command(pmbus.device, "iq_3f01025E")
        power_off_val = pmbus.l16_query_command(pmbus.device, "iq_3f01025F")
        vin_on_val = pmbus.l11_query_command(pmbus.device, "iq_3f010235")
        vin_off_val = pmbus.l11_query_command(pmbus.device, "iq_3f010236")

        self.power_on = self.create_line_edit(power_on_val)
        self.vin_on = self.create_line_edit(vin_on_val)
        self.power_off = self.create_line_edit(power_off_val)
        self.vin_off = self.create_line_edit(vin_off_val)

        grid2.addWidget(QtGui.QLabel(" "), 0, 1, 1, 1, QtCore.Qt.AlignCenter)
        grid2.addWidget(QtGui.QLabel("ON Level Value"), 0, 3, 1, 1, QtCore.Qt.AlignCenter)
        grid2.addWidget(QtGui.QLabel("OFF Level Value"), 0, 6, 1, 1, QtCore.Qt.AlignCenter)
        grid2.addWidget(QtGui.QLabel("  "), 1, 0)
        grid2.addWidget(QtGui.QLabel("POWER OK"), 1, 1, 1, 2)
        grid2.addWidget(self.power_on, 1, 3)
        grid2.addWidget(QtGui.QLabel("V"), 1, 4)
        grid2.addWidget(QtGui.QLabel("  "), 1, 5)
        grid2.addWidget(self.power_off, 1, 6)
        grid2.addWidget(QtGui.QLabel("V"), 1, 7)
        grid2.addWidget(QtGui.QLabel("  "), 1, 8)
        grid2.addWidget(QtGui.QLabel("  "), 2, 0)
        grid2.addWidget(QtGui.QLabel("VIN"), 2, 1, 1, 2)
        grid2.addWidget(self.vin_on, 2, 3)
        grid2.addWidget(QtGui.QLabel("V"), 2, 4)
        grid2.addWidget(QtGui.QLabel("  "), 2, 5)
        grid2.addWidget(self.vin_off, 2, 6)
        grid2.addWidget(QtGui.QLabel("V"), 2, 7)
        grid2.addWidget(QtGui.QLabel("  "), 2, 8)
        grid2.addWidget(QtGui.QLabel("  "), 3, 0)

        on_off_lvl_box.setLayout(grid2)

        protection_box.setLayout(grid)
        self.stacked_widget.addWidget(self.page_4)

    def page5_monitor(self):

        # create page 5
        self.page_5 = QtGui.QWidget()

        # create monitoring box
        self.monitoring_box = QtGui.QGroupBox(self.page_5)
        self.size_and_name(self.monitoring_box, 19, 9, 970, 535, "PMBus Status Information")

        # clear faults button
        self.clear_faults_but = QtGui.QPushButton(self.monitoring_box)
        self.clear_faults_but.setGeometry(QtCore.QRect(20, 240, 100, 23))
        self.clear_faults_but.setText("Clear Faults")

        # device startup
        self.control_pin = QtGui.QPushButton(self.monitoring_box)
        self.control_pin.setGeometry(QtCore.QRect(20, 280, 100, 23))
        self.control_pin.setText("Control Pin")
        self.control_pin.clicked.connect(self.handle_control_pin)
        self.index_pin = 1

        # device startup - OPERATION command
        self.operation_cmd = QtGui.QPushButton(self.monitoring_box)
        self.operation_cmd.setGeometry(QtCore.QRect(20, 320, 100, 23))
        self.operation_cmd.setText("OPERATION_CMD")
        self.operation_cmd.setEnabled(False)
        self.operation_cmd.clicked.connect(self.handle_operation_cmd)
        self.index_oper_cmd = 1

        self.cb_mon = QtGui.QComboBox(self.monitoring_box)
        self.cb_mon.setGeometry(QtCore.QRect(20, 360, 170, 23))
        self.cb_mon.addItem("Immediate off w/o sequencing")
        self.cb_mon.addItem("Soft off with sequencing")
        self.cb_mon.addItem("On")
        self.cb_mon.addItem("Margin Low w/o fault")
        self.cb_mon.addItem("Margin Low with fault")
        self.cb_mon.addItem("Margin High w/o fault")
        self.cb_mon.addItem("Margin High w/o fault")
        self.cb_mon.setEnabled(False)

        # monitoring on/off
        self.monitoring_but = QtGui.QPushButton(self.monitoring_box)
        self.monitoring_but.setGeometry(QtCore.QRect(20, 400, 100, 23))
        self.monitoring_but.setText("Monitoring")
        self.monitoring_but.clicked.connect(self.mon_on_off)

        self.led = QtGui.QLabel(self.monitoring_box)
        self.led.setGeometry(QtCore.QRect(140, 400, 24, 24))
        self.pix_map = QtGui.QPixmap('icons/green.jpg')
        self.led.setPixmap(self.pix_map)
        self.index = 1

        # write volatile button
        self.write_volatile = QtGui.QPushButton(self.monitoring_box)
        self.write_volatile.setGeometry(QtCore.QRect(20, 440, 100, 23))
        self.write_volatile.setText("Write volatile")
        self.write_volatile.setStyleSheet("background-color: yellow")
        self.write_volatile.clicked.connect(self.write_to_device)

        # define labels
        self.vin_average_label = self.create_label(self.monitoring_box, 20, 40, 80, 21, "VIN:  0 V")  # read vin
        self.vout_average_label = self.create_label(self.monitoring_box, 20, 90, 80, 21, "VOUT:  0 V")  # read vout
        self.iout_average_label = self.create_label(self.monitoring_box, 20, 140, 80, 21, "IOUT:  0 A")  # read iout
        self.temp_average_label = self.create_label(self.monitoring_box, 20, 190, 80, 21, "TEMP:  0 " + u"\u00b0" + "C")  # read temp 2

        # create frames for monitoring graphs
        self.monitoring_frame = QtGui.QFrame(self.monitoring_box)
        self.monitoring_frame.setGeometry(QtCore.QRect(200, 20, 755, 500))

        self.scroll_layout = QtGui.QVBoxLayout()
        scroll_widget = QtGui.QWidget()
        scroll_widget.setLayout(self.scroll_layout)

        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)

        plots = ["vin", "vout", "temp"]
        names = ["Input Voltage (V)", "Output Voltage (V)", "Temperature (" + u"\u00b0" + "C)"]
        for plot, name in zip(plots, names):
            self.display_plot(name, plot)
            self.do_pause()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(scroll)
        self.monitoring_frame.setLayout(layout)
        self.stacked_widget.addWidget(self.page_5)

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

    def write_to_device(self):
        #  WRITE NEW CONFIGURATION TO THE DEVICE
        #  GET INFO FROM ALL TEXT FIELDS
        #
        values_l11 = [self.ton_delay.text(), self.ton_rise.text(), self.ton_max.text(),
                      self.toff_delay.text(), self.toff_fall.text(), self.toff_max.text(),
                      self.iout_oc_fault.text(), self.iout_oc_warning.text(), self.temp_ot_fault.text(),
                      self.temp_ot_warning.text(), self.vin_ov_fault.text(), self.vin_ov_warning.text(),
                      self.vin_uv_warning.text(), self.vin_uv_fault.text(), self.vin_on.text(),
                      self.vin_off.text()]

        values_l16 = [self.vout_nom.text(), self.vout_ov_fault.text(), self.vout_ov_warning.text(),
                      self.vout_uv_warning.text(), self.vout_uv_fault.text(), self.power_on.text(),
                      self.power_off.text()]

        pmbus_l11_hex_codes = ["60", "61", "62", "64", "65", "66", "66", "46", "4A",
                               "4F", "51", "55", "57", "58", "59", "35", "36"]
        pmbus_l16_hex_codes = ["21", "40", "42", "43", "44", "5E", "5F"]

        for value, code in zip(values_l11, pmbus_l11_hex_codes):
            pmbus.l11_write_command(pmbus.device, "iw_3f003" + code, float(value))

        for value, code in zip(values_l16, pmbus_l16_hex_codes):
            pmbus.l16_write_command(pmbus.device, "iw_3f003" + code, float(value))

    def update_monitoring_labels(self):
        vin_average = pmbus.l11_query_command(pmbus.device, "iq_3f010288")
        self.vin_average_label.setText("VIN:  " + vin_average + " V")
        vout_average = pmbus.l16_query_command(pmbus.device, "iq_3f01028B")
        self.vout_average_label.setText("VOUT:  " + vout_average + " V")
        iout_average = pmbus.l11_query_command(pmbus.device, "iq_3f01028C")
        self.iout_average_label.setText("IOUT:  " + iout_average + " A")
        temp_average = pmbus.l11_query_command(pmbus.device, "iq_3f01028E")
        self.temp_average_label.setText("TEMP:  " + temp_average + " " + u"\u00b0" + "C")

    def do_pause(self):
        self.monitoring_but.clicked.connect(self.graph.stop_timer)


    def handle_control_pin(self):
        pmbus.configure_command(pmbus.device, "iw_3f0020216")  # set ON_OFF_CONFIG to 0x16 for Control Pin
        if self.index_pin:
            pmbus.configure_command(pmbus.device, "ip_1")
        else:
            pmbus.configure_command(pmbus.device, "ip_0")
        self.index_pin = not self.index_pin

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

    def display_plot(self, name, value):
        group_box = QtGui.QGroupBox(name)
        group_layout = QtGui.QHBoxLayout()
        # add plot diagram to graph_frame
        self.graph = Monitoring.GraphCanvas(value)
        self.graph.setMinimumSize(200, 400)
        group_layout.addWidget(self.graph)
        group_box.setLayout(group_layout)
        self.scroll_layout.addWidget(group_box)

    def info_panel(self):

        self.info_frame = QtGui.QFrame(self.central_widget)
        self.info_frame.setGeometry(QtCore.QRect(10, 10, 161, 645))
        #version = pmbus.configure_command(pmbus.device, "v")
        version = "0"
        self.create_label(self.info_frame, 20, 30, 61, 20, "Device Info:")
        self.text_browser = QtGui.QTextBrowser(self.info_frame)
        self.text_browser.setGeometry(QtCore.QRect(20, 70, 121, 192))
        self.create_label(self.text_browser, 10, 40, 100, 100, "EM2130L\nPMW Controller\n")

    def setupUi(self, main_window):

        # set style of the main window
        self.set_style(main_window)
        main_window.setWindowTitle("PMBus Power GUI")

        # create central widget
        self.central_widget = QtGui.QWidget(main_window)

        # set menu buttons
        self.menu()

        # create stackedWidget (tabbed)
        self.stacked_widget = QtGui.QStackedWidget(self.central_widget)
        self.stacked_widget.setGeometry(QtCore.QRect(180, 90, 1010, 565))
        self.stacked_widget.setAutoFillBackground(False)

        # create page1
        self.page1_main()

        # create page2
        self.page2_configuration()

        # create page3
        self.page3_pin()

        # create page4
        self.page4_protection()

        # create page5
        self.page5_monitor()

        # device info - left panel
        self.info_panel()

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        # menu bar & status bar
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtGui.QMenuBar(main_window)
        self.menu_bar.addMenu('&File')
        self.menu_bar.addAction(exitAction)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 901, 21))
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtGui.QStatusBar(main_window)
        main_window.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(main_window)

    def page1(self):
        self.stacked_widget.setCurrentIndex(0)

    def page2(self):
        self.stacked_widget.setCurrentIndex(1)

    def page3(self):
        self.stacked_widget.setCurrentIndex(2)

    def page4(self):
        self.stacked_widget.setCurrentIndex(3)

    def page5(self):
        self.stacked_widget.setCurrentIndex(4)
