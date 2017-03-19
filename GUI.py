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
import SequencingPlot
import Monitoring
from PMBusCall import pmbus

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
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_label)
        timer.start(1000)

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
        main = self.create_button_tab(10, 10, 190, 51, "Main", self.page1, "main.png")
        main.setStatusTip('Power Stage')
        # "configuration" button
        conf = self.create_button_tab(210, 10, 190, 51, "Configuration", self.page2, "conf.png")
        conf.setStatusTip('Startup and shutdown parameters configuration')
        # "pin" button
        pin = self.create_button_tab(410, 10, 190, 51, "Pin", self.page3, "pin.png")
        pin.setStatusTip('Pin layout')
        # "protection" button
        prot = self.create_button_tab(610, 10, 190, 51, "Protection", self.page4, "prot.png")
        prot.setStatusTip("Set device's protection parameters")
        # "monitor" button
        mon = self.create_button_tab(810, 10, 190, 51, "Monitoring", self.page5, "mon.png")
        mon.setStatusTip("Device's monitoring")



    def text_validation(self, text_field):

        reg_ex = QtCore.QRegExp("[0-9]\.?[0-9]\.?[0-9]+")
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
        #line_edit.setGeometry(QtCore.QRect(x, y, w, h))
        line_edit.setAlignment(QtCore.Qt.AlignRight)
        line_edit.setText(text)
        self.text_validation(line_edit)  # validate user input
        line_edit.textChanged.connect(self.handle_editing_finished)
        return line_edit

    def create_checkbox(self):

        checkbox = QtGui.QCheckBox()
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

    def selection_change(self, i):

        if self.cb.currentText() == "OPERATION_CMD":
            self.control_pin.setEnabled(False)
            self.operation_cmd.setEnabled(True)
            self.cb_mon.setEnabled(True)
            # pmbus.write_command(pmbus.device, " ")  # write operation cmd + 0x40
        elif self.cb.currentText() == "CTRL_POS":
            self.control_pin.setEnabled(True)
            self.operation_cmd.setEnabled(False)
            self.cb_mon.setEnabled(False)
            # pmbus.write_command(pmbus.device, " ")  # write ctrl_pos 0x16
        else:
            self.control_pin.setEnabled(True)
            self.operation_cmd.setEnabled(False)
            self.cb_mon.setEnabled(False)
            # pmbus.write_command(pmbus.device, " ")  # write ctrl_neg 0x14

        print "Current index", i, "selection changed ", self.cb.currentText()

    def operation_selection_change(self, i):

        print "Current index", i, "selection changed ", self.cb_mon.currentText()
        #  CMD_OPERATION command
        if i == 0:
            pmbus.write_command(pmbus.device, " ")  # 0x00 immediate off w/o sequencing
        elif i == 1:
            pmbus.write_command(pmbus.device, " ")  # 0x40 soft off with sequencing
        elif i == 2:
            pmbus.write_command(pmbus.device, " ")  # 0x80 on
        elif i == 3:
            pmbus.write_command(pmbus.device, " ")  # 0x94 margin low w/o fault
        elif i == 4:
            pmbus.write_command(pmbus.device, " ")  # 0x98 margin low with fault
        elif i == 5:
            pmbus.write_command(pmbus.device, " ")  # 0xA4 margin high w/o fault
        elif i == 6:
            pmbus.write_command(pmbus.device, " ")  # 0xA8 margin high with fault

    def page1_main(self):

        # create page
        self.page = QtGui.QWidget()

        # create group box
        self.power_stage_box = QtGui.QGroupBox(self.page)
        self.size_and_name(self.power_stage_box, 19, 9, 970, 535, "Power Stage")

        # frame for block diagram of EM2130
        self.schematic = QtGui.QLabel(self.power_stage_box)
        self.schematic.setGeometry(QtCore.QRect(20, 20, 695, 409))
        pix_map = QtGui.QPixmap('blockdiagram-em2130.jpg')
        self.schematic.setPixmap(pix_map)
        self.schematic.setStyleSheet('border: 1px solid rgb(147, 147, 147)')

        # PMBus variables
        vout_val = pmbus.vout_query_command(pmbus.device, "iq_3f010221")  # vout_command L16

        # voltage group box
        self.voltage_box = QtGui.QGroupBox(self.power_stage_box)
        self.size_and_name(self.voltage_box, 750, 20, 181, 241, "Voltage")

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        self.voltage_box.setLayout(grid)

        # text fields for voltage group
        self.vin_nom = self.create_line_edit("12")
        self.vout_nom = self.create_line_edit(vout_val)
        self.marg_high = self.create_line_edit("5")
        self.marg_low = self.create_line_edit("5")

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
        ton_delay_val = pmbus.vin_query_command(pmbus.device, "iq_3f010260")
        toff_delay_val = pmbus.vin_query_command(pmbus.device, "iq_3f010264")
        ton_rise_val = pmbus.vin_query_command(pmbus.device, "iq_3f010261")
        toff_fall_val = pmbus.vin_query_command(pmbus.device, "iq_3f010265")
        ton_max_val = pmbus.vin_query_command(pmbus.device, "iq_3f010262")  # ton max fault limit L11
        toff_max_val = pmbus.vin_query_command(pmbus.device, "iq_3f010266")  # toff_max warn limit L11
        vout_on_val = pmbus.vout_query_command(pmbus.device, "iq_3f010221")  # vout command L16
        vout_off_val = pmbus.vout_query_command(pmbus.device, "iq_3f0102E0")  # mfr_vout_off L16

        # create configuration group box
        self.configuration_box = QtGui.QGroupBox(self.page_2)
        self.size_and_name(self.configuration_box, 19, 9, 970, 350, "Sequencing Diagram")

        self.param_box = QtGui.QGroupBox(self.page_2)
        self.size_and_name(self.param_box, 19, 360, 970, 190, "Parameters")

        # set text fields
        self.ton_delay = self.create_line_edit(ton_delay_val)
        self.toff_delay = self.create_line_edit(toff_delay_val)
        self.ton_rise = self.create_line_edit(ton_rise_val)
        self.toff_fall = self.create_line_edit(toff_fall_val)
        self.ton_max = self.create_line_edit(ton_max_val)
        self.toff_max = self.create_line_edit(toff_max_val)
        self.vout_on = self.create_line_edit(vout_on_val)
        self.vout_off = self.create_line_edit(vout_off_val)

        # set combo box
        self.cb = QtGui.QComboBox()
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

        # create page 3 (empty yet)
        self.page_3 = QtGui.QWidget()
        self.stacked_widget.addWidget(self.page_3)

    def page4_protection(self):

        # create page 4
        self.page_4 = QtGui.QWidget()

        # create protection group box
        self.protection_box = QtGui.QGroupBox(self.page_4)
        self.size_and_name(self.protection_box, 19, 9, 970, 535, "PMBus Protection Parameters")

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
        vout_ov_war_val = pmbus.vout_query_command(pmbus.device, "iq_3f010242")
        vout_uv_war_val = pmbus.vout_query_command(pmbus.device, "iq_3f010243")
        vin_ov_war_val = pmbus.vin_query_command(pmbus.device, "iq_3f010257")
        vin_uv_war_val = pmbus.vin_query_command(pmbus.device, "iq_3f010258")
        vout_ov_fal_val = pmbus.vout_query_command(pmbus.device, "iq_3f010240")
        vout_uv_fal_val = pmbus.vout_query_command(pmbus.device, "iq_3f010244")
        vin_ov_fal_val = pmbus.vin_query_command(pmbus.device, "iq_3f010255")
        vin_uv_fal_val = pmbus.vin_query_command(pmbus.device, "iq_3f010259")
        iout_oc_war_val = pmbus.vin_query_command(pmbus.device, "iq_3f01024A")
        temp_ot_war_val = pmbus.vin_query_command(pmbus.device, "iq_3f010251")
        temp_ot_fal_val = pmbus.vin_query_command(pmbus.device, "iq_3f01024F")
        iout_oc_fal_val = pmbus.vin_query_command(pmbus.device, "iq_3f010246")

        # text fields
        self.vout_ov_warning = self.create_line_edit(vout_ov_war_val)
        self.vout_uv_warning = self.create_line_edit(vout_uv_war_val)
        self.vin_ov_warning = self.create_line_edit(vin_ov_war_val)
        self.vin_uv_warning = self.create_line_edit(vin_uv_war_val)
        self.iout_oc_warning = self.create_line_edit(iout_oc_war_val)
        self.temp_ot_warning = self.create_line_edit(temp_ot_war_val)

        self.vout_ov_fault = self.create_line_edit(vout_ov_fal_val)
        self.vout_uv_fault = self.create_line_edit(vout_uv_fal_val)
        self.vin_ov_fault = self.create_line_edit(vin_ov_fal_val)
        self.vin_uv_fault = self.create_line_edit(vin_uv_fal_val)
        self.temp_ot_fault = self.create_line_edit(temp_ot_fal_val)
        self.iout_oc_fault = self.create_line_edit(iout_oc_fal_val)

        self.vout_ov_delay = self.create_line_edit("0.00")
        self.vout_uv_delay = self.create_line_edit("0.00")
        self.vout_uv_delay = self.create_line_edit("0.00")
        self.vin_ov_delay = self.create_line_edit("0.00")
        self.iout_oc_delay = self.create_line_edit("0.00")
        self.vin_uv_delay = self.create_line_edit("0.00")
        self.temp_ot_delay = self.create_line_edit("0.00")

        grid = QtGui.QGridLayout()

        grid.setSpacing(20)
        grid.addWidget(QtGui.QLabel(" "), 0, 1)
        # First row
        grid.addWidget(QtGui.QLabel("Enable"), 1, 2)
        grid.addWidget(QtGui.QLabel("Warning Limit"), 1, 3)
        grid.addWidget(QtGui.QLabel("\t"), 1, 4)
        grid.addWidget(QtGui.QLabel("Fault Limit"), 1, 5)
        grid.addWidget(QtGui.QLabel("\t"), 1, 6)
        grid.addWidget(QtGui.QLabel("Time Delay"), 1, 7)
        grid.addWidget(QtGui.QLabel("\t"), 1, 8)
        grid.addWidget(QtGui.QLabel("Alert (W/F)"), 1, 9)


        # Second row
        #grid.addWidget(QtGui.QLabel("W          F"), 1, 9)
        grid.setVerticalSpacing(40)
        grid.setRowMinimumHeight(5, 5)

        # Third row
        grid.addWidget(QtGui.QLabel("VOUT OV"), 2, 1)
        grid.addWidget(self.vout_ov_enable, 2, 2)
        grid.addWidget(self.vout_ov_warning, 2, 3)
        grid.addWidget(QtGui.QLabel("V"), 2, 4)
        grid.addWidget(self.vout_ov_fault, 2, 5)
        grid.addWidget(QtGui.QLabel("V"), 2, 6)
        grid.addWidget(self.vout_ov_delay, 2, 7)
        grid.addWidget(QtGui.QLabel("ms"), 2, 8)
        grid.addWidget(self.vout_ov_walert, 2, 9)
        grid.addWidget(self.vout_ov_falert, 2, 10)
        grid.addWidget(QtGui.QLabel("  "), 2, 11)

        # Fourth row
        grid.addWidget(QtGui.QLabel("VOUT UV"), 3, 1)
        grid.addWidget(self.vout_uv_enable, 3, 2)
        grid.addWidget(self.vout_uv_warning, 3, 3)
        grid.addWidget(QtGui.QLabel("V"), 3, 4)
        grid.addWidget(self.vout_uv_fault, 3, 5)
        grid.addWidget(QtGui.QLabel("V"), 3, 6)
        grid.addWidget(self.vout_uv_delay, 3, 7)
        grid.addWidget(QtGui.QLabel("ms"), 3, 8)
        grid.addWidget(self.vout_uv_walert, 3, 9)
        grid.addWidget(self.vout_uv_falert, 3, 10)
        grid.addWidget(QtGui.QLabel(" "), 3, 11)

        # Fifth row
        grid.addWidget(QtGui.QLabel("VIN OV"), 4, 1)
        grid.addWidget(self.vin_ov_enable, 4, 2)
        grid.addWidget(self.vin_ov_warning, 4, 3)
        grid.addWidget(QtGui.QLabel("V"), 4, 4)
        grid.addWidget(self.vin_ov_fault, 4, 5)
        grid.addWidget(QtGui.QLabel("V"), 4, 6)
        grid.addWidget(self.vin_ov_delay, 4, 7)
        grid.addWidget(QtGui.QLabel("ms"), 4, 8)
        grid.addWidget(self.vin_ov_walert, 4, 9)
        grid.addWidget(self.vin_ov_falert, 4, 10)
        grid.addWidget(QtGui.QLabel(" "), 4, 11)

        # Sixth row
        grid.addWidget(QtGui.QLabel("VIN UV"), 5, 1)
        grid.addWidget(self.vin_uv_enable, 5, 2)
        grid.addWidget(self.vin_uv_warning, 5, 3)
        grid.addWidget(QtGui.QLabel("V"), 5, 4)
        grid.addWidget(self.vin_uv_fault, 5, 5)
        grid.addWidget(QtGui.QLabel("V"), 5, 6)
        grid.addWidget(self.vin_uv_delay, 5, 7)
        grid.addWidget(QtGui.QLabel("ms"), 5, 8)
        grid.addWidget(self.vin_uv_walert, 5, 9)
        grid.addWidget(self.vin_uv_falert, 5, 10)
        grid.addWidget(QtGui.QLabel(" "), 5, 11)

        # Seventh row
        grid.addWidget(QtGui.QLabel("IOUT"), 6, 1)
        grid.addWidget(self.iout_oc_enable, 6, 2)
        grid.addWidget(self.iout_oc_warning, 6, 3)
        grid.addWidget(QtGui.QLabel("V"), 6, 4)
        grid.addWidget(self.iout_oc_fault, 6, 5)
        grid.addWidget(QtGui.QLabel("V"), 6, 6)
        grid.addWidget(self.iout_oc_delay, 6, 7)
        grid.addWidget(QtGui.QLabel("ms"), 6, 8)
        grid.addWidget(self.iout_oc_walert, 6, 9)
        grid.addWidget(self.iout_oc_falert, 6, 10)
        grid.addWidget(QtGui.QLabel(" "), 6, 11)

        # Eight row
        grid.addWidget(QtGui.QLabel("TEMP"), 7, 1)
        grid.addWidget(self.temp_ot_enable, 7, 2)
        grid.addWidget(self.temp_ot_warning, 7, 3)
        grid.addWidget(QtGui.QLabel("V"), 7, 4)
        grid.addWidget(self.temp_ot_fault, 7, 5)
        grid.addWidget(QtGui.QLabel("V"), 7, 6)
        grid.addWidget(self.temp_ot_delay, 7, 7)
        grid.addWidget(QtGui.QLabel("ms"), 7, 8)
        grid.addWidget(self.temp_ot_walert, 7, 9)
        grid.addWidget(self.temp_ot_falert, 7, 10)
        grid.addWidget(QtGui.QLabel(" "), 7, 11)
        grid.addWidget(QtGui.QLabel(" "), 8, 0)

        self.protection_box.setLayout(grid)
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

        # device startup - OPERATION command
        self.operation_cmd = QtGui.QPushButton(self.monitoring_box)
        self.operation_cmd.setGeometry(QtCore.QRect(20, 320, 100, 23))
        self.operation_cmd.setText("OPERATION_CMD")
        self.operation_cmd.setEnabled(False)
        #self.operation_cmd.clicked.connect(self.handle_operation_cmd)

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
        self.cb_mon.currentIndexChanged.connect(self.operation_selection_change)

        # monitoring on/off
        self.monitoring_but = QtGui.QPushButton(self.monitoring_box)
        self.monitoring_but.setGeometry(QtCore.QRect(20, 400, 100, 23))
        self.monitoring_but.setText("Monitoring")

        # write volatile button
        self.write_volatile = QtGui.QPushButton(self.monitoring_box)
        self.write_volatile.setGeometry(QtCore.QRect(20, 440, 100, 23))
        self.write_volatile.setText("Write volatile")
        self.write_volatile.setStyleSheet("background-color: yellow")


        # define labels
        self.vin_average_label = self.create_label(self.monitoring_box, 20, 40, 80, 21, "VIN:  0 V")  # read vin
        self.vout_average_label = self.create_label(self.monitoring_box, 20, 90, 80, 21, "VOUT:  0 V")  # read vout
        self.iout_average_label = self.create_label(self.monitoring_box, 20, 140, 80, 21, "IOUT:  0 A")  # read iout
        self.temp_average_label = self.create_label(self.monitoring_box, 20, 190, 80, 21, "TEMP:  0 C")  # read temp 2

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
        names = ["Input Voltage (V)", "Output Voltage (V)", "Temperature (C)"]
        for plot, name in zip(plots, names):
            self.display_plot(name, plot)
            self.do_pause()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(scroll)
        self.monitoring_frame.setLayout(layout)
        self.stacked_widget.addWidget(self.page_5)

    def update_label(self):
        vin_average = pmbus.vin_query_command(pmbus.device, "iq_3f010288")
        self.vin_average_label.setText("VIN:  " + vin_average + " V")
        vout_average = pmbus.vout_query_command(pmbus.device, "iq_3f01028B")
        self.vout_average_label.setText("VOUT:  " + vout_average + " V")
        iout_average = pmbus.vin_query_command(pmbus.device, "iq_3f01028C")
        self.iout_average_label.setText("IOUT:  " + iout_average + " A")
        temp_average = pmbus.vin_query_command(pmbus.device, "iq_3f01028E")
        self.temp_average_label.setText("TEMP:  " + temp_average + " C")

    def do_pause(self):
        self.monitoring_but.clicked.connect(self.graph.stop_timer)


    def handle_control_pin(self):
        pmbus.write_command(pmbus.device, "iw_3f0020216")  # set ON_OFF_CONFIG to 0x16 for Control Pin
        if self.index:
            pmbus.write_command(pmbus.device, "ip_1")
        else:
            pmbus.write_command(pmbus.device, "ip_0")
        self.index = not self.index

    def display_plot(self, name, value):
        group_box = QtGui.QGroupBox(name)
        group_layout = QtGui.QHBoxLayout()
        # add plot diagram to graph_frame
        self.graph = Monitoring.GraphCanvas(value)
        #graph.init_figure(value)
        #graph.init_timer(value)
        self.graph.setMinimumSize(200, 400)
        group_layout.addWidget(self.graph)
        group_box.setLayout(group_layout)
        self.scroll_layout.addWidget(group_box)

    def info_panel(self):

        self.info_frame = QtGui.QFrame(self.central_widget)
        self.info_frame.setGeometry(QtCore.QRect(10, 10, 161, 645))
        self.create_label(self.info_frame, 20, 30, 61, 20, "Device Info:")
        self.text_browser = QtGui.QTextBrowser(self.info_frame)
        self.text_browser.setGeometry(QtCore.QRect(20, 70, 121, 192))

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
