# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import Painter
import Monitoring
import PMBus_Comms


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


class GuiMainWindow(object):

    def __init__(self):
        self.paint_panel = 0

    def setstyle(self, main_window):
        main_window.resize(901, 577)
        main_window.setStyleSheet(_fromUtf8("QFrame{\n"
                                           "background-color:rgb(255, 255, 255);\n"
                                           "border: 1px solid rgb(147, 147, 147)\n"
                                           "}\n"
                                           "\n"
                                           "QLabel{\n"
                                           "border:none;\n"
                                           "background-color:transparent;\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton{\n"
                                           "background-color:transparent;\n"
                                           "border:none;\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton:pressed{\n"
                                           "background-color:rgb(231, 226, 221);\n"
                                           "border: 1px solid rgb(147, 147, 147);\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton:checked{\n"
                                           "background-color:rgb(231, 226, 221);\n"
                                           "border: 1px solid rgb(147, 147, 147);\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton:hover {\n"
                                           "background-color:rgb(188, 188, 188);\n"
                                           "}\n"
                                           "\n"
                                           "QStackedWidget {\n"
                                           "background-color:rgb(220, 228, 244);\n"
                                           "border: 1px solid rgb(147, 147, 147)\n"
                                           "}"))

    def menu(self):

        # create new buttons_frame and put menu buttons in there
        self.buttons_frame = QtGui.QFrame(self.central_widget)
        self.buttons_frame.setGeometry(QtCore.QRect(180, 10, 711, 71))
        self.buttons_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.buttons_frame.setFrameShadow(QtGui.QFrame.Raised)

        # "main" button
        self.create_button_tab(self.buttons_frame, 10, 10, 131, 51, "Main", self.page1)
        # "configuration" button
        self.create_button_tab(self.buttons_frame, 150, 10, 131, 51, "Configuration", self.page2)
        # "pin" button
        self.create_button_tab(self.buttons_frame, 290, 10, 131, 51, "Pin", self.page3)
        # "protection" button
        self.create_button_tab(self.buttons_frame, 430, 10, 131, 51, "Protection", self.page4)
        # "monitor" button
        self.create_button_tab(self.buttons_frame, 570, 10, 131, 51, "Monitoring", self.page5)

    def text_validation(self, text_field):

        # !! ReGex implementation !!
        reg_ex = QtCore.QRegExp("[0-9]\.?[0-9]\.?[0-9]+")
        text_validator = QtGui.QRegExpValidator(reg_ex, text_field)
        text_field.setValidator(text_validator)
        # !! ReGex implementation End !!

    def create_label(self, group, x, y, w, h, text):

        label = QtGui.QLabel(group)
        label.setGeometry(QtCore.QRect(x, y, w, h))
        label.setText(text)
        return label

    def create_button_tab(self, frame, x, y, w, h, text, page):

        button_tab = QtGui.QToolButton(frame)
        button_tab.setGeometry(QtCore.QRect(x, y, w, h))
        button_tab.setCheckable(True)
        button_tab.setAutoExclusive(True)
        button_tab.clicked.connect(page)
        button_tab.setText(_translate("MainWindow", text, None))

    def size_and_name(self, component, x, y, w, h, name):

        component.setGeometry(QtCore.QRect(x, y, w, h))
        component.setTitle(_translate("MainWindow", name, None))

    def create_line_edit(self, frame, x, y, w, h, text):

        line_edit = QtGui.QLineEdit(frame)
        line_edit.setGeometry(QtCore.QRect(x, y, w, h))
        line_edit.setAlignment(QtCore.Qt.AlignRight)
        line_edit.setText(text)
        self.text_validation(line_edit)  # validate user input
        line_edit.textChanged.connect(self.handle_editing_finished)
        return line_edit

    def create_checkbox(self, frame, x, y, w, h):

        checkbox = QtGui.QCheckBox(frame)
        checkbox.setGeometry(QtCore.QRect(x, y, w, h))
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.state_changed)
        return checkbox

    def handle_editing_finished(self):

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

    def state_changed(self):
        if self.vout_ov_enable.isChecked():
            self.vout_ov_warning.setEnabled(True)
            self.vout_ov_fault.setEnabled(True)
            self.vout_ov_delay.setEnabled(True)
        else:
            self.vout_ov_warning.setEnabled(False)
            self.vout_ov_fault.setEnabled(False)
            self.vout_ov_delay.setEnabled(False)

        if self.vout_uv_enable.isChecked():
            self.vout_uv_warning.setEnabled(True)
            self.vout_uv_fault.setEnabled(True)
            self.vout_uv_delay.setEnabled(True)
        else:
            self.vout_uv_warning.setEnabled(False)
            self.vout_uv_fault.setEnabled(False)
            self.vout_uv_delay.setEnabled(False)

        if self.vin_uv_enable.isChecked():
            self.vin_uv_warning.setEnabled(True)
            self.vin_uv_fault.setEnabled(True)
            self.vin_uv_delay.setEnabled(True)
        else:
            self.vin_uv_warning.setEnabled(False)
            self.vin_uv_fault.setEnabled(False)
            self.vin_uv_delay.setEnabled(False)

        if self.vin_ov_enable.isChecked():
            self.vin_ov_warning.setEnabled(True)
            self.vin_ov_fault.setEnabled(True)
            self.vin_ov_delay.setEnabled(True)
        else:
            self.vin_ov_warning.setEnabled(False)
            self.vin_ov_fault.setEnabled(False)
            self.vin_ov_delay.setEnabled(False)

        if self.iout_oc_enable.isChecked():
            self.iout_oc_warning.setEnabled(True)
            self.iout_oc_fault.setEnabled(True)
            self.iout_oc_delay.setEnabled(True)
        else:
            self.iout_oc_warning.setEnabled(False)
            self.iout_oc_fault.setEnabled(False)
            self.iout_oc_delay.setEnabled(False)

        if self.temp_ot_enable.isChecked():
            self.temp_ot_warning.setEnabled(True)
            self.temp_ot_fault.setEnabled(True)
            self.temp_ot_delay.setEnabled(True)
        else:
            self.temp_ot_warning.setEnabled(False)
            self.temp_ot_fault.setEnabled(False)
            self.temp_ot_delay.setEnabled(False)

    def page1_main(self):

        # create page
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))

        # create group box
        self.power_stage_box = QtGui.QGroupBox(self.page)
        self.size_and_name(self.power_stage_box, 19, 9, 671, 401, "Power Stage")

        # frame for block diagram of EM2130
        self.schematic = QtGui.QLabel(self.power_stage_box)
        self.schematic.setGeometry(QtCore.QRect(20, 20, 451, 371))
        pixmap = QtGui.QPixmap('blockdiagram-em2130.jpg')
        self.schematic.setPixmap(pixmap)
        self.schematic.setStyleSheet('border: 1px solid rgb(147, 147, 147)')

        x = PMBus_Comms.PMbusComms()
        vout_val = x.vout_query_command(self.device, "iq_3f010221")  # vout_command L16

        # voltage group box
        self.voltage_box = QtGui.QGroupBox(self.power_stage_box)
        self.size_and_name(self.voltage_box, 480, 20, 181, 241, "Voltage")

        # text fields for voltage group
        self.create_line_edit(self.voltage_box, 60, 50, 81, 21, "12")
        self.create_line_edit(self.voltage_box, 60, 90, 81, 21, vout_val)
        self.create_line_edit(self.voltage_box, 90, 170, 51, 21, "5")
        self.create_line_edit(self.voltage_box, 90, 210, 51, 21, "5")

        # define labels
        self.create_label(self.voltage_box, 20, 50, 21, 20, "VIN")
        self.create_label(self.voltage_box, 20, 90, 31, 20, "VOUT")
        self.create_label(self.voltage_box, 150, 50, 21, 20, "V")
        self.create_label(self.voltage_box, 150, 90, 21, 20, "V")
        self.create_label(self.voltage_box, 150, 170, 21, 20, "%")
        self.create_label(self.voltage_box, 150, 210, 21, 20, "%")
        self.create_label(self.voltage_box, 60, 20, 61, 20, "Nominal")
        self.create_label(self.voltage_box, 20, 170, 61, 20, "Margin High")
        self.create_label(self.voltage_box, 20, 210, 61, 20, "Margin Low")

        self.stacked_widget.addWidget(self.page)

    def page2_configuration(self):

        # create page 2
        self.page_2 = QtGui.QWidget()

        x = PMBus_Comms.PMbusComms()
        ton_delay_val = x.vin_query_command(self.device, "iq_3f010260")
        toff_delay_val = x.vin_query_command(self.device, "iq_3f010264")
        ton_rise_val = x.vin_query_command(self.device, "iq_3f010261")
        toff_fall_val = x.vin_query_command(self.device, "iq_3f010265")
        ton_max_val = x.vin_query_command(self.device, "iq_3f010262")  # ton max fault limit L11
        toff_max_val = x.vin_query_command(self.device, "iq_3f010266")  # toff_max warn limit L11
        vout_on_val = x.vout_query_command(self.device, "iq_3f010221")  # vout command L16
        vout_off_val = x.vout_query_command(self.device, "iq_3f0102E0")  # mfr_vout_off L16

        # create configuration group box
        self.configuration_box = QtGui.QGroupBox(self.page_2)
        self.size_and_name(self.configuration_box, 19, 9, 671, 401, "Sequencing")

        # define labels
        self.create_label(self.configuration_box, 10, 330, 61, 20, "Device Rise:")
        self.create_label(self.configuration_box, 10, 360, 61, 20, "Device Fall:")
        self.create_label(self.configuration_box, 90, 290, 31, 20, "Delay")
        self.create_label(self.configuration_box, 90, 330, 61, 20, "TON_DELAY:")
        self.create_label(self.configuration_box, 90, 360, 65, 20, "TOFF_DELAY:")
        self.create_label(self.configuration_box, 250, 330, 61, 20, "TON_RISE:")
        self.create_label(self.configuration_box, 250, 360, 61, 20, "TOFF_FALL:")
        self.create_label(self.configuration_box, 410, 330, 51, 20, "TON_MAX:")
        self.create_label(self.configuration_box, 410, 360, 61, 20, "TOFF_MAX:")
        self.create_label(self.configuration_box, 210, 330, 21, 20, "ms")
        self.create_label(self.configuration_box, 210, 360, 21, 20, "ms")
        self.create_label(self.configuration_box, 370, 330, 21, 20, "ms")
        self.create_label(self.configuration_box, 370, 360, 21, 20, "ms")
        self.create_label(self.configuration_box, 530, 330, 21, 20, "ms")
        self.create_label(self.configuration_box, 530, 360, 21, 20, "ms")
        self.create_label(self.configuration_box, 570, 330, 21, 20, "ON:")
        self.create_label(self.configuration_box, 570, 360, 31, 20, "OFF:")
        self.create_label(self.configuration_box, 650, 330, 21, 20, "V")
        self.create_label(self.configuration_box, 650, 360, 21, 20, "V")
        self.create_label(self.configuration_box, 250, 290, 51, 20, "Ramping")
        self.create_label(self.configuration_box, 410, 290, 61, 20, "Max Timing")
        self.create_label(self.configuration_box, 570, 290, 31, 20, "VOUT")

        # set text fields
        self.ton_delay = self.create_line_edit(self.configuration_box, 160, 330, 41, 21, ton_delay_val)
        self.toff_delay = self.create_line_edit(self.configuration_box, 160, 360, 41, 21, toff_delay_val)
        self.ton_rise = self.create_line_edit(self.configuration_box, 320, 330, 41, 21, ton_rise_val)
        self.toff_fall = self.create_line_edit(self.configuration_box, 320, 360, 41, 21, toff_fall_val)
        self.ton_max = self.create_line_edit(self.configuration_box, 480, 330, 41, 21, ton_max_val)
        self.toff_max = self.create_line_edit(self.configuration_box, 480, 360, 41, 21, toff_max_val)
        self.vout_on = self.create_line_edit(self.configuration_box, 600, 330, 41, 21, vout_on_val)
        self.vout_off = self.create_line_edit(self.configuration_box, 600, 360, 41, 21, vout_off_val)

        self.graph_frame = QtGui.QFrame(self.configuration_box)
        self.graph_frame.setGeometry(QtCore.QRect(20, 20, 631, 251))

        self.main_layout = QtGui.QGridLayout()
        self.graph_frame.setLayout(self.main_layout)

        # add plot diagram to graph_frame
        self.paint_panel = Painter.Graph()
        self.paint_panel.close()
        self.main_layout.addWidget(self.paint_panel, 0, 0)

        #  add labels to graph
        self.create_label(self.configuration_box, 95, 231, 65, 20, "TON_DELAY")
        self.create_label(self.configuration_box, 374, 231, 65, 20, "TOFF_DELAY")
        self.create_label(self.configuration_box, 172, 231, 65, 20, "TON_RISE")
        self.create_label(self.configuration_box, 450, 231, 65, 20, "TOFF_FALL")
        self.create_label(self.configuration_box, 600, 220, 65, 20, "Time")
        self.tonmax_label = self.create_label(self.configuration_box, 180, 250, 100, 20, "TON_MAX = " + ton_max_val)
        self.toffmax_label = self.create_label(self.configuration_box, 465, 250, 100, 20, "TOFF_MAX = " + toff_max_val)
        self.tondelay_label = self.create_label(self.configuration_box, 115, 200, 65, 20, ton_delay_val)
        self.tonrise_label = self.create_label(self.configuration_box, 189, 200, 65, 20, ton_rise_val)
        self.toffdelay_label = self.create_label(self.configuration_box, 397, 200, 65, 20, toff_delay_val)
        self.tofffall_label = self.create_label(self.configuration_box, 465, 200, 65, 20, toff_fall_val)
        self.voutoff_label = self.create_label(self.configuration_box, 30, 180, 100, 30,
                                               "VOUT OFF \n" + vout_off_val + " V")
        self.vouton_label = self.create_label(self.configuration_box, 30, 60, 100, 30,
                                              "VOUT ON \n" + vout_on_val + " V")

        self.stacked_widget.addWidget(self.page_2)

    def page3_pin(self):

        # create page 3 (empty yet)
        self.page_3 = QtGui.QWidget()
        self.stacked_widget.addWidget(self.page_3)

    def page4_protection(self):

        # create page 4
        self.page_4 = QtGui.QWidget()

        # create protection group box
        self.protection_box = QtGui.QGroupBox(self.page_4)
        self.size_and_name(self.protection_box, 19, 9, 671, 401, "PMBus Protection Parameters")

        # check boxes
        self.vout_ov_enable = self.create_checkbox(self.protection_box, 90, 90, 16, 17)
        self.vout_uv_enable = self.create_checkbox(self.protection_box, 90, 140, 16, 17)
        self.vin_ov_enable = self.create_checkbox(self.protection_box, 90, 190, 16, 17)
        self.vin_uv_enable = self.create_checkbox(self.protection_box, 90, 240, 16, 17)
        self.temp_ot_enable = self.create_checkbox(self.protection_box, 90, 340, 16, 17)
        self.iout_oc_enable = self.create_checkbox(self.protection_box, 90, 290, 16, 17)
        self.vout_ov_walert = self.create_checkbox(self.protection_box, 580, 90, 16, 17)
        self.vout_uv_walert = self.create_checkbox(self.protection_box, 580, 140, 16, 17)
        self.vin_ov_walert = self.create_checkbox(self.protection_box, 580, 190, 16, 17)
        self.vin_uv_walert = self.create_checkbox(self.protection_box, 580, 240, 16, 17)
        self.iout_oc_walert = self.create_checkbox(self.protection_box, 580, 290, 16, 17)
        self.temp_ot_walert = self.create_checkbox(self.protection_box, 580, 340, 16, 17)
        self.vout_ov_falert = self.create_checkbox(self.protection_box, 620, 90, 16, 17)
        self.vout_uv_falert = self.create_checkbox(self.protection_box, 620, 140, 16, 17)
        self.vin_ov_falert = self.create_checkbox(self.protection_box, 620, 190, 16, 17)
        self.vin_uv_falert = self.create_checkbox(self.protection_box, 620, 240, 16, 17)
        self.iout_oc_falert = self.create_checkbox(self.protection_box, 620, 290, 16, 17)
        self.temp_oc_falert = self.create_checkbox(self.protection_box, 620, 340, 16, 17)


        # define labels
        self.create_label(self.protection_box, 20, 90, 61, 20, "VOUT OV")
        self.create_label(self.protection_box, 20, 190, 46, 13, "VIN OV")
        self.create_label(self.protection_box, 170, 30, 71, 16, "Warning Limit")
        self.create_label(self.protection_box, 20, 290, 46, 13, "IOUT")
        self.create_label(self.protection_box, 80, 30, 41, 16, "Enable")
        self.create_label(self.protection_box, 20, 340, 46, 13, "TEMP")
        self.create_label(self.protection_box, 310, 30, 51, 16, "Fault Limit")
        self.create_label(self.protection_box, 450, 30, 61, 16, "Time Delay")
        self.create_label(self.protection_box, 250, 90, 21, 20, "V")
        self.create_label(self.protection_box, 250, 140, 21, 20, "V")
        self.create_label(self.protection_box, 250, 190, 21, 20, "V")
        self.create_label(self.protection_box, 250, 240, 21, 20, "V")
        self.create_label(self.protection_box, 390, 90, 21, 20, "V")
        self.create_label(self.protection_box, 390, 140, 21, 20, "V")
        self.create_label(self.protection_box, 390, 190, 21, 20, "V")
        self.create_label(self.protection_box, 390, 240, 21, 20, "V")
        self.create_label(self.protection_box, 530, 90, 21, 20, "ms")
        self.create_label(self.protection_box, 530, 140, 21, 20, "ms")
        self.create_label(self.protection_box, 530, 190, 21, 20, "ms")
        self.create_label(self.protection_box, 530, 240, 21, 20, "ms")
        self.create_label(self.protection_box, 590, 30, 31, 16, "Alert")
        self.create_label(self.protection_box, 20, 140, 51, 16, "VOUT UV")
        self.create_label(self.protection_box, 20, 240, 46, 13, "VIN UV")
        self.create_label(self.protection_box, 250, 340, 21, 20, "C")
        self.create_label(self.protection_box, 250, 290, 21, 20, "A")
        self.create_label(self.protection_box, 530, 290, 21, 20, "ms")
        self.create_label(self.protection_box, 530, 340, 21, 20, "ms")
        self.create_label(self.protection_box, 390, 340, 21, 20, "C")
        self.create_label(self.protection_box, 390, 290, 21, 20, "A")
        self.create_label(self.protection_box, 580, 60, 21, 20, "W")
        self.create_label(self.protection_box, 620, 60, 21, 20, "F")

        x = PMBus_Comms.PMbusComms()
        vout_ov_war_val = x.vout_query_command(self.device, "iq_3f010242")
        vout_uv_war_val = x.vout_query_command(self.device, "iq_3f010243")
        vin_ov_war_val = x.vin_query_command(self.device, "iq_3f010257")
        vin_uv_war_val = x.vin_query_command(self.device, "iq_3f010258")
        vout_ov_fal_val = x.vout_query_command(self.device, "iq_3f010240")
        vout_uv_fal_val = x.vout_query_command(self.device, "iq_3f010244")
        vin_ov_fal_val = x.vin_query_command(self.device, "iq_3f010255")
        vin_uv_fal_val = x.vin_query_command(self.device, "iq_3f010259")
        iout_oc_war_val = x.vin_query_command(self.device, "iq_3f01024A")
        temp_ot_war_val = x.vin_query_command(self.device, "iq_3f010251")
        temp_ot_fal_val = x.vin_query_command(self.device, "iq_3f01024F")
        iout_oc_fal_val = x.vin_query_command(self.device, "iq_3f010246")

        # text fields
        self.vout_ov_warning = self.create_line_edit(self.protection_box, 160, 90, 81, 21, vout_ov_war_val)
        self.vout_uv_warning = self.create_line_edit(self.protection_box, 160, 140, 81, 21, vout_uv_war_val)
        self.vin_ov_warning = self.create_line_edit(self.protection_box, 160, 190, 81, 21, vin_ov_war_val)
        self.vin_uv_warning = self.create_line_edit(self.protection_box, 160, 240, 81, 21, vin_uv_war_val)
        self.iout_oc_warning = self.create_line_edit(self.protection_box, 160, 290, 81, 21, iout_oc_war_val)
        self.temp_ot_warning = self.create_line_edit(self.protection_box, 160, 340, 81, 21, temp_ot_war_val)

        self.vout_ov_fault = self.create_line_edit(self.protection_box, 300, 90, 81, 21, vout_ov_fal_val)
        self.vout_uv_fault = self.create_line_edit(self.protection_box, 300, 140, 81, 21, vout_uv_fal_val)
        self.vin_ov_fault = self.create_line_edit(self.protection_box, 300, 190, 81, 21, vin_ov_fal_val)
        self.vin_uv_fault = self.create_line_edit(self.protection_box, 300, 240, 81, 21, vin_uv_fal_val)
        self.temp_ot_fault = self.create_line_edit(self.protection_box, 300, 340, 81, 21, temp_ot_fal_val)
        self.iout_oc_fault = self.create_line_edit(self.protection_box, 300, 290, 81, 21, iout_oc_fal_val)

        self.vout_ov_delay = self.create_line_edit(self.protection_box, 440, 90, 81, 21, "0.00")
        self.vout_uv_delay = self.create_line_edit(self.protection_box, 440, 90, 81, 21, "0.00")
        self.vout_uv_delay = self.create_line_edit(self.protection_box, 440, 140, 81, 21, "0.00")
        self.vin_ov_delay = self.create_line_edit(self.protection_box, 440, 190, 81, 21, "0.00")
        self.iout_oc_delay = self.create_line_edit(self.protection_box, 440, 290, 81, 21, "0.00")
        self.vin_uv_delay = self.create_line_edit(self.protection_box, 440, 240, 81, 21, "0.00")
        self.temp_ot_delay = self.create_line_edit(self.protection_box, 440, 340, 81, 21, "0.00")


        self.stacked_widget.addWidget(self.page_4)

    def page5_monitor(self):

        # create page 5
        self.page_5 = QtGui.QWidget()

        # create monitoring box
        self.monitoring_box = QtGui.QGroupBox(self.page_5)
        self.size_and_name(self.monitoring_box, 19, 9, 671, 401, "PMBus Status Information")

        # clear faults button
        self.clear_faults_but = QtGui.QPushButton(self.monitoring_box)
        self.clear_faults_but.setGeometry(QtCore.QRect(10, 240, 71, 23))
        self.clear_faults_but.setText("Clear Faults")

        # device startup
        self.device_startup_but = QtGui.QPushButton(self.monitoring_box)
        self.device_startup_but.setGeometry(QtCore.QRect(10, 280, 71, 23))
        self.device_startup_but.setText("Control Pin")


        x = PMBus_Comms.PMbusComms()
        vin_average = x.vin_query_command(self.device, "iq_3f010288")
        vout_average = x.vout_query_command(self.device, "iq_3f010221")
        iout_average = x.vin_query_command(self.device, "iq_3f01028C")
        temp_average = x.vin_query_command(self.device, "iq_3f01028E")

        # define labels
        self.create_label(self.monitoring_box, 10, 40, 80, 21, "VIN:  " + vin_average + " V")  # read vin
        self.create_label(self.monitoring_box, 10, 90, 80, 21, "VOUT:  " + vout_average + " V")  # vout command
        self.create_label(self.monitoring_box, 10, 140, 80, 21, "IOUT:  " + iout_average + " A")  # read iout
        self.create_label(self.monitoring_box, 10, 190, 80, 21, "TEMP:  " + temp_average + " C")  # read temp 2

        # create frames for monitoring graphs
        self.monitoring_frame = QtGui.QFrame(self.monitoring_box)
        self.monitoring_frame.setGeometry(QtCore.QRect(90, 20, 565, 365))

        self.scroll_layout = QtGui.QVBoxLayout()
        scroll_widget = QtGui.QWidget()
        scroll_widget.setLayout(self.scroll_layout)

        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)

        self.display_plot("Input Voltage (V)")
        self.display_plot("Output Voltage (V)")
        self.display_plot("Temperature (T)")

        layout = QtGui.QHBoxLayout()
        layout.addWidget(scroll)
        self.monitoring_frame.setLayout(layout)
        self.stacked_widget.addWidget(self.page_5)

    def display_plot(self, name):

        group_box = QtGui.QGroupBox(name)
        group_layout = QtGui.QHBoxLayout()
        # add plot diagram to graph_frame
        graph = Monitoring.GraphCanvas()
        graph.setMinimumSize(200, 300)
        group_layout.addWidget(graph)
        group_box.setLayout(group_layout)
        self.scroll_layout.addWidget(group_box)

    def info_panel(self):
        self.info_frame = QtGui.QFrame(self.central_widget)
        self.info_frame.setGeometry(QtCore.QRect(10, 10, 161, 511))

        self.create_label(self.info_frame, 20, 30, 61, 20, "Device Info:")

        self.text_browser = QtGui.QTextBrowser(self.info_frame)
        self.text_browser.setGeometry(QtCore.QRect(20, 70, 121, 192))

    def setupUi(self, main_window):

        # set style of the main window
        self.setstyle(main_window)
        main_window.setWindowTitle("PMBus Power GUI")

        # create central widget
        self.central_widget = QtGui.QWidget(main_window)

        # set menu buttons
        self.menu()

        # create stackedWidget (tabbed)
        self.stacked_widget = QtGui.QStackedWidget(self.central_widget)
        self.stacked_widget.setGeometry(QtCore.QRect(180, 90, 711, 431))
        self.stacked_widget.setAutoFillBackground(False)

        #  connect with device
        x = PMBus_Comms.PMbusComms()
        self.device = x.process()

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

        # menu bar & status bar
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtGui.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 901, 21))
        main_window.setMenuBar(self.menu_bar)
        self.statusbar = QtGui.QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

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


