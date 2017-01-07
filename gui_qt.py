# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import plot

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


class Ui_MainWindow(object):
    PaintPanel = 0

    def __init__(self):
        self.vout_off = QtGui.QLineEdit

    def setstyle(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(901, 577)
        MainWindow.setStyleSheet(_fromUtf8("QFrame{\n"
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

    def menu(self, centralwidget):

        # create new buttons_frame and put menu buttons in there
        self.buttons_frame = QtGui.QFrame(self.centralwidget)
        self.buttons_frame.setGeometry(QtCore.QRect(180, 10, 711, 71))
        self.buttons_frame.setStyleSheet(_fromUtf8(""))
        self.buttons_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.buttons_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.buttons_frame.setObjectName(_fromUtf8("buttons_frame"))

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

    def page1_main(self, stackedWidget):
        # create page
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))

        # create group box
        self.power_stage_box = QtGui.QGroupBox(self.page)
        self.size_and_name(self.power_stage_box, 19, 9, 671, 401, "Power Stage")

        # frame for block diagram of EM2130
        self.block_diagram_frame = QtGui.QFrame(self.power_stage_box)
        self.block_diagram_frame.setGeometry(QtCore.QRect(20, 20, 451, 371))
        self.block_diagram_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.block_diagram_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.block_diagram_frame.setObjectName(_fromUtf8("block_diagram_frame"))

        # voltage group box
        self.voltage_box = QtGui.QGroupBox(self.power_stage_box)
        self.size_and_name(self.voltage_box, 480, 20, 181, 241, "Voltage")

        # text fields for voltage group
        self.vin_value_main = QtGui.QLineEdit(self.voltage_box)
        self.vin_value_main.setGeometry(QtCore.QRect(60, 50, 81, 21))
        self.vin_value_main.setObjectName(_fromUtf8("vin_value_main"))
        self.text_validation(self.vin_value_main)  # validate user input

        self.vout_value_main = QtGui.QLineEdit(self.voltage_box)
        self.vout_value_main.setGeometry(QtCore.QRect(60, 90, 81, 21))
        self.vout_value_main.setObjectName(_fromUtf8("vout_value_main"))
        self.text_validation(self.vout_value_main)  # validate user input

        self.margin_high = QtGui.QLineEdit(self.voltage_box)
        self.margin_high.setGeometry(QtCore.QRect(90, 170, 51, 21))
        self.margin_high.setObjectName(_fromUtf8("margin_high"))
        self.text_validation(self.margin_high)  # validate user input

        self.margin_low = QtGui.QLineEdit(self.voltage_box)
        self.margin_low.setGeometry(QtCore.QRect(90, 210, 51, 21))
        self.margin_low.setObjectName(_fromUtf8("margin_low"))
        self.text_validation(self.margin_low)  # validate user input

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

        self.stackedWidget.addWidget(self.page)

    def page2_configuration(self, stackedWidget):

        # create page 2
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))

        # create configuration group box
        self.configuration_box = QtGui.QGroupBox(self.page_2)
        self.size_and_name(self.configuration_box, 19, 9, 671, 401, "Sequencing")

        # define labels
        self.create_label(self.configuration_box, 10, 330, 61, 20, "Device Rise:")
        self.create_label(self.configuration_box, 10, 360, 61, 20, "Device Fall:")
        self.create_label(self.configuration_box, 90, 290, 31, 20, "Delay")
        self.create_label(self.configuration_box, 90, 330, 61, 20, "TON_DELAY:")
        self.create_label(self.configuration_box, 90, 360, 61, 20, "TOFF_DELAY:")
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
        self.ton_delay = QtGui.QLineEdit(self.configuration_box)
        self.ton_delay.setGeometry(QtCore.QRect(160, 330, 41, 21))
        self.ton_delay.setObjectName(_fromUtf8("ton_delay"))
        self.text_validation(self.ton_delay)  # validate user input
        self.ton_delay.textChanged.connect(self.handleEditingFinished)

        self.toff_delay = QtGui.QLineEdit(self.configuration_box)
        self.toff_delay.setGeometry(QtCore.QRect(160, 360, 41, 21))
        self.toff_delay.setObjectName(_fromUtf8("toff_delay"))
        self.text_validation(self.toff_delay)  # validate user input
        self.toff_delay.textChanged.connect(self.handleEditingFinished)

        self.ton_rise = QtGui.QLineEdit(self.configuration_box)
        self.ton_rise.setGeometry(QtCore.QRect(320, 330, 41, 21))
        self.ton_rise.setObjectName(_fromUtf8("ton_rise"))
        self.text_validation(self.ton_rise)  # validate user input
        self.ton_rise.textChanged.connect(self.handleEditingFinished)

        self.toff_fall = QtGui.QLineEdit(self.configuration_box)
        self.toff_fall.setGeometry(QtCore.QRect(320, 360, 41, 21))
        self.toff_fall.setObjectName(_fromUtf8("toff_fall"))
        self.text_validation(self.toff_fall)  # validate user input
        self.toff_fall.textChanged.connect(self.handleEditingFinished)

        self.ton_max = QtGui.QLineEdit(self.configuration_box)
        self.ton_max.setGeometry(QtCore.QRect(480, 330, 41, 21))
        self.ton_max.setObjectName(_fromUtf8("ton_max"))
        self.text_validation(self.ton_max)  # validate user input
        self.ton_max.textChanged.connect(self.handleEditingFinished)

        self.toff_max = QtGui.QLineEdit(self.configuration_box)
        self.toff_max.setGeometry(QtCore.QRect(480, 360, 41, 21))
        self.toff_max.setObjectName(_fromUtf8("toff_max"))
        self.text_validation(self.toff_max)  # validate user input
        self.toff_max.textChanged.connect(self.handleEditingFinished)

        self.vout_on = QtGui.QLineEdit(self.configuration_box)
        self.vout_on.setGeometry(QtCore.QRect(600, 330, 41, 21))
        self.vout_on.setObjectName(_fromUtf8("vout_on"))
        self.text_validation(self.vout_on)  # validate user input
        self.vout_on.textChanged.connect(self.handleEditingFinished)

        self.vout_off = QtGui.QLineEdit(self.configuration_box)
        self.vout_off.setGeometry(QtCore.QRect(600, 360, 41, 21))
        self.vout_off.setObjectName(_fromUtf8("vout_off"))
        self.text_validation(self.vout_off)  # validate user input
        self.vout_off.textChanged.connect(self.handleEditingFinished)

        self.graph_frame = QtGui.QFrame(self.configuration_box)
        self.graph_frame.setGeometry(QtCore.QRect(20, 20, 631, 251))
        self.graph_frame.setStyleSheet(_fromUtf8(""))
        self.graph_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.graph_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.graph_frame.setObjectName(_fromUtf8("graph_frame"))

        self.main_layout = QtGui.QGridLayout()
        self.graph_frame.setLayout(self.main_layout)

        # add plot diagram to graph_frame
        self.PaintPanel = plot.Graph()
        self.PaintPanel.close()
        self.main_layout.addWidget(self.PaintPanel, 0, 0)

        #add labels to graph
        self.create_label(self.configuration_box, 95, 231, 65, 20, "TON_DELAY")
        self.create_label(self.configuration_box, 374, 231, 65, 20, "TOFF_DELAY")
        self.create_label(self.configuration_box, 172, 231, 65, 20, "TON_RISE")
        self.create_label(self.configuration_box, 450, 231, 65, 20, "TOFF_FALL")
        self.create_label(self.configuration_box, 600, 220, 65, 20, "Time")

        self.tonmax_label = QtGui.QLabel(self.configuration_box)
        self.tonmax_label.setGeometry(QtCore.QRect(180, 250, 100, 20))
        self.tonmax_label.setText("TON_MAX = 0.00")

        self.toffmax_label = QtGui.QLabel(self.configuration_box)
        self.toffmax_label.setGeometry(QtCore.QRect(465, 250, 100, 20))
        self.toffmax_label.setText("TOFF_MAX = 0.00")

        self.tondelay_label = QtGui.QLabel(self.configuration_box)
        self.tondelay_label.setGeometry(QtCore.QRect(115, 200, 65, 20))
        self.tondelay_label.setText("0.00")

        self.tonrise_label = QtGui.QLabel(self.configuration_box)
        self.tonrise_label.setGeometry(QtCore.QRect(189, 200, 65, 20))
        self.tonrise_label.setText("0.00")

        self.toffdelay_label = QtGui.QLabel(self.configuration_box)
        self.toffdelay_label.setGeometry(QtCore.QRect(397, 200, 65, 20))
        self.toffdelay_label.setText("0.00")

        self.tofffall_label = QtGui.QLabel(self.configuration_box)
        self.tofffall_label.setGeometry(QtCore.QRect(465, 200, 65, 20))
        self.tofffall_label.setText("0.00")

        self.voutoff_label = QtGui.QLabel(self.configuration_box)
        self.voutoff_label.setGeometry(QtCore.QRect(30, 180, 100, 30))
        self.voutoff_label.setText("VOUT OFF \n 0.00 V")

        self.vouton_label = QtGui.QLabel(self.configuration_box)
        self.vouton_label.setGeometry(QtCore.QRect(30, 60, 100, 30))
        self.vouton_label.setText("VOUT ON \n 0.00 V")


        self.stackedWidget.addWidget(self.page_2)

    def handleEditingFinished(self):
        if self.toff_max.isModified():
            self.toffmax_label.setText("TOFF_MAX = " + self.toff_max.text())
        if self.ton_max.isModified():
            self.tonmax_label.setText("TON_MAX = " + self.ton_max.text())
        if self.ton_delay.isModified():
            self.tondelay_label.setText(self.ton_delay.text())
        if self.toff_delay.isModified():
            self.toffdelay_label.setText(self.toff_delay.text())
        if self.ton_rise.isModified():
            self.tonrise_label.setText(self.ton_rise.text())
        if self.toff_fall.isModified():
            self.tofffall_label.setText(self.toff_fall.text())
        if self.vout_on.isModified():
            self.vouton_label.setText("VOUT ON \n " + self.vout_on.text() + " V")
        if self.vout_off.isModified():
            self.voutoff_label.setText("VOUT OFF \n " + self.vout_off.text() + " V")
        self.toff_max.setModified(False)
        self.ton_max.setModified(False)
        self.ton_delay.setModified(False)
        self.toff_delay.setModified(False)
        self.ton_rise.setModified(False)
        self.toff_fall.setModified(False)
        self.vout_off.setModified(False)
        self.vout_on.setModified(False)

    def page3_pin(self, stackedWidget):

        # create page 3 (empty yet)
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.stackedWidget.addWidget(self.page_3)

    def page4_protection(self, stackedWidget):

        # create page 4
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName(_fromUtf8("page_4"))

        # create protection group box
        self.protection_box = QtGui.QGroupBox(self.page_4)
        self.size_and_name(self.protection_box, 19, 9, 671, 401, "PMBus Protection Parameters")

        # check boxes
        self.vout_ov_enable = QtGui.QCheckBox(self.protection_box)
        self.vout_ov_enable.setGeometry(QtCore.QRect(90, 90, 16, 17))
        self.vout_ov_enable.setText(_fromUtf8(""))
        self.vout_ov_enable.setObjectName(_fromUtf8("vout_ov_enable"))
        self.vout_uv_enable = QtGui.QCheckBox(self.protection_box)
        self.vout_uv_enable.setGeometry(QtCore.QRect(90, 140, 16, 17))
        self.vout_uv_enable.setText(_fromUtf8(""))
        self.vout_uv_enable.setObjectName(_fromUtf8("vout_uv_enable"))
        self.vin_ov_enable = QtGui.QCheckBox(self.protection_box)
        self.vin_ov_enable.setGeometry(QtCore.QRect(90, 190, 16, 17))
        self.vin_ov_enable.setText(_fromUtf8(""))
        self.vin_ov_enable.setObjectName(_fromUtf8("vin_ov_enable"))
        self.vin_uv_enable = QtGui.QCheckBox(self.protection_box)
        self.vin_uv_enable.setGeometry(QtCore.QRect(90, 240, 16, 17))
        self.vin_uv_enable.setText(_fromUtf8(""))
        self.vin_uv_enable.setObjectName(_fromUtf8("vin_uv_enable"))
        self.temp_ot_enable = QtGui.QCheckBox(self.protection_box)
        self.temp_ot_enable.setGeometry(QtCore.QRect(90, 340, 16, 17))
        self.temp_ot_enable.setText(_fromUtf8(""))
        self.temp_ot_enable.setObjectName(_fromUtf8("temp_ot_enable"))
        self.iout_oc_enable = QtGui.QCheckBox(self.protection_box)
        self.iout_oc_enable.setGeometry(QtCore.QRect(90, 290, 16, 17))
        self.iout_oc_enable.setText(_fromUtf8(""))
        self.iout_oc_enable.setObjectName(_fromUtf8("iout_oc_enable"))
        self.vout_ov_walert = QtGui.QCheckBox(self.protection_box)
        self.vout_ov_walert.setGeometry(QtCore.QRect(580, 90, 16, 17))
        self.vout_ov_walert.setText(_fromUtf8(""))
        self.vout_ov_walert.setObjectName(_fromUtf8("vout_ov_walert"))
        self.vout_uv_walert = QtGui.QCheckBox(self.protection_box)
        self.vout_uv_walert.setGeometry(QtCore.QRect(580, 140, 16, 17))
        self.vout_uv_walert.setText(_fromUtf8(""))
        self.vout_uv_walert.setObjectName(_fromUtf8("vout_uv_walert"))
        self.vin_ov_walert = QtGui.QCheckBox(self.protection_box)
        self.vin_ov_walert.setGeometry(QtCore.QRect(580, 190, 16, 17))
        self.vin_ov_walert.setText(_fromUtf8(""))
        self.vin_ov_walert.setObjectName(_fromUtf8("vin_ov_walert"))
        self.vin_uv_walert = QtGui.QCheckBox(self.protection_box)
        self.vin_uv_walert.setGeometry(QtCore.QRect(580, 240, 16, 17))
        self.vin_uv_walert.setText(_fromUtf8(""))
        self.vin_uv_walert.setObjectName(_fromUtf8("vin_uv_walert"))
        self.iout_oc_walert = QtGui.QCheckBox(self.protection_box)
        self.iout_oc_walert.setGeometry(QtCore.QRect(580, 290, 16, 17))
        self.iout_oc_walert.setText(_fromUtf8(""))
        self.iout_oc_walert.setObjectName(_fromUtf8("iout_oc_walert"))
        self.temp_ot_walert = QtGui.QCheckBox(self.protection_box)
        self.temp_ot_walert.setGeometry(QtCore.QRect(580, 340, 16, 17))
        self.temp_ot_walert.setText(_fromUtf8(""))
        self.temp_ot_walert.setObjectName(_fromUtf8("temp_ot_walert"))
        self.vout_ov_falert = QtGui.QCheckBox(self.protection_box)
        self.vout_ov_falert.setGeometry(QtCore.QRect(620, 90, 16, 17))
        self.vout_ov_falert.setText(_fromUtf8(""))
        self.vout_ov_falert.setObjectName(_fromUtf8("vout_ov_falert"))
        self.vout_uv_falert = QtGui.QCheckBox(self.protection_box)
        self.vout_uv_falert.setGeometry(QtCore.QRect(620, 140, 16, 17))
        self.vout_uv_falert.setText(_fromUtf8(""))
        self.vout_uv_falert.setObjectName(_fromUtf8("vout_uv_falert"))
        self.vin_ov_falert = QtGui.QCheckBox(self.protection_box)
        self.vin_ov_falert.setGeometry(QtCore.QRect(620, 190, 16, 17))
        self.vin_ov_falert.setText(_fromUtf8(""))
        self.vin_ov_falert.setObjectName(_fromUtf8("vin_ov_falert"))
        self.vin_uv_falert = QtGui.QCheckBox(self.protection_box)
        self.vin_uv_falert.setGeometry(QtCore.QRect(620, 240, 16, 17))
        self.vin_uv_falert.setText(_fromUtf8(""))
        self.vin_uv_falert.setObjectName(_fromUtf8("vin_uv_falert"))
        self.iout_oc_falert = QtGui.QCheckBox(self.protection_box)
        self.iout_oc_falert.setGeometry(QtCore.QRect(620, 290, 16, 17))
        self.iout_oc_falert.setText(_fromUtf8(""))
        self.iout_oc_falert.setObjectName(_fromUtf8("iout_oc_falert"))
        self.temp_oc_falert = QtGui.QCheckBox(self.protection_box)
        self.temp_oc_falert.setGeometry(QtCore.QRect(620, 340, 16, 17))
        self.temp_oc_falert.setText(_fromUtf8(""))
        self.temp_oc_falert.setObjectName(_fromUtf8("temp_oc_falert"))

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
        self.create_label(self.protection_box, 250, 340, 21, 20, "°C")
        self.create_label(self.protection_box, 250, 290, 21, 20, "A")
        self.create_label(self.protection_box, 530, 290, 21, 20, "ms")
        self.create_label(self.protection_box, 530, 340, 21, 20, "ms")
        self.create_label(self.protection_box, 390, 340, 21, 20, "°C")
        self.create_label(self.protection_box, 390, 290, 21, 20, "A")
        self.create_label(self.protection_box, 580, 60, 21, 20, "W")
        self.create_label(self.protection_box, 620, 60, 21, 20, "F")

        # text fields
        self.vout_ov_warning = QtGui.QLineEdit(self.protection_box)
        self.vout_ov_warning.setGeometry(QtCore.QRect(160, 90, 81, 21))
        self.vout_ov_warning.setObjectName(_fromUtf8("vout_ov_warning"))
        self.text_validation(self.vout_ov_warning)  # validate user input

        self.vout_uv_warning = QtGui.QLineEdit(self.protection_box)
        self.vout_uv_warning.setGeometry(QtCore.QRect(160, 140, 81, 21))
        self.vout_uv_warning.setObjectName(_fromUtf8("vout_uv_warning"))
        self.text_validation(self.vout_uv_warning)  # validate user input

        self.vin_ov_warning = QtGui.QLineEdit(self.protection_box)
        self.vin_ov_warning.setGeometry(QtCore.QRect(160, 190, 81, 21))
        self.vin_ov_warning.setObjectName(_fromUtf8("vin_ov_warning"))
        self.text_validation(self.vin_ov_warning)  # validate user input

        self.vin_uv_warning = QtGui.QLineEdit(self.protection_box)
        self.vin_uv_warning.setGeometry(QtCore.QRect(160, 240, 81, 21))
        self.vin_uv_warning.setObjectName(_fromUtf8("vin_uv_warning"))
        self.text_validation(self.vin_uv_warning)  # validate user input

        self.vout_ov_fault = QtGui.QLineEdit(self.protection_box)
        self.vout_ov_fault.setGeometry(QtCore.QRect(300, 90, 81, 21))
        self.vout_ov_fault.setObjectName(_fromUtf8("vout_ov_fault"))
        self.text_validation(self.vout_ov_fault)  # validate user input

        self.vout_uv_fault = QtGui.QLineEdit(self.protection_box)
        self.vout_uv_fault.setGeometry(QtCore.QRect(300, 140, 81, 21))
        self.vout_uv_fault.setObjectName(_fromUtf8("vout_uv_fault"))
        self.text_validation(self.vout_uv_fault)  # validate user input

        self.vin_ov_fault = QtGui.QLineEdit(self.protection_box)
        self.vin_ov_fault.setGeometry(QtCore.QRect(300, 190, 81, 21))
        self.vin_ov_fault.setObjectName(_fromUtf8("vin_ov_fault"))
        self.text_validation(self.vin_ov_fault)  # validate user input

        self.vin_uv_fault = QtGui.QLineEdit(self.protection_box)
        self.vin_uv_fault.setGeometry(QtCore.QRect(300, 240, 81, 21))
        self.vin_uv_fault.setObjectName(_fromUtf8("vin_uv_fault"))
        self.text_validation(self.vin_uv_fault)  # validate user input

        self.vout_ov_delay = QtGui.QLineEdit(self.protection_box)
        self.vout_ov_delay.setGeometry(QtCore.QRect(440, 90, 81, 21))
        self.vout_ov_delay.setObjectName(_fromUtf8("vout_ov_delay"))
        self.text_validation(self.vout_ov_delay)  # validate user input

        self.vout_uv_delay = QtGui.QLineEdit(self.protection_box)
        self.vout_uv_delay.setGeometry(QtCore.QRect(440, 140, 81, 21))
        self.vout_uv_delay.setObjectName(_fromUtf8("vout_uv_delay"))
        self.text_validation(self.vout_uv_delay)  # validate user input

        self.vin_ov_delay = QtGui.QLineEdit(self.protection_box)
        self.vin_ov_delay.setGeometry(QtCore.QRect(440, 190, 81, 21))
        self.vin_ov_delay.setObjectName(_fromUtf8("vin_ov_delay"))
        self.text_validation(self.vin_ov_delay)  # validate user input

        self.iout_oc_delay = QtGui.QLineEdit(self.protection_box)
        self.iout_oc_delay.setGeometry(QtCore.QRect(440, 290, 81, 21))
        self.iout_oc_delay.setObjectName(_fromUtf8("iout_oc_delay"))
        self.text_validation(self.iout_oc_delay)  # validate user input

        self.iout_oc_warning = QtGui.QLineEdit(self.protection_box)
        self.iout_oc_warning.setGeometry(QtCore.QRect(160, 290, 81, 21))
        self.iout_oc_warning.setObjectName(_fromUtf8("iout_oc_warning"))
        self.text_validation(self.iout_oc_warning)  # validate user input

        self.temp_ot_warning = QtGui.QLineEdit(self.protection_box)
        self.temp_ot_warning.setGeometry(QtCore.QRect(160, 340, 81, 21))
        self.temp_ot_warning.setObjectName(_fromUtf8("temp_ot_warning"))
        self.text_validation(self.temp_ot_warning)  # validate user input

        self.temp_ot_fault = QtGui.QLineEdit(self.protection_box)
        self.temp_ot_fault.setGeometry(QtCore.QRect(300, 340, 81, 21))
        self.temp_ot_fault.setObjectName(_fromUtf8("temp_ot_fault"))
        self.text_validation(self.temp_ot_fault)  # validate user input

        self.iout_oc_fault = QtGui.QLineEdit(self.protection_box)
        self.iout_oc_fault.setGeometry(QtCore.QRect(300, 290, 81, 21))
        self.iout_oc_fault.setObjectName(_fromUtf8("iout_oc_fault"))
        self.text_validation(self.iout_oc_fault)  # validate user input

        self.vin_uv_delay = QtGui.QLineEdit(self.protection_box)
        self.vin_uv_delay.setGeometry(QtCore.QRect(440, 240, 81, 21))
        self.vin_uv_delay.setObjectName(_fromUtf8("vin_uv_delay"))
        self.text_validation(self.vin_uv_delay)  # validate user input

        self.temp_ot_delay = QtGui.QLineEdit(self.protection_box)
        self.temp_ot_delay.setGeometry(QtCore.QRect(440, 340, 81, 21))
        self.temp_ot_delay.setObjectName(_fromUtf8("temp_ot_delay"))
        self.text_validation(self.temp_ot_delay)  # validate user input

        self.stackedWidget.addWidget(self.page_4)

    def page5_monitor(self, stackedWidget):

        # create page 5
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName(_fromUtf8("page_5"))

        # create monitoring box
        self.monitoring_box = QtGui.QGroupBox(self.page_5)
        self.size_and_name(self.monitoring_box, 19, 9, 671, 401, "PMBus Status Information")

        # clear faults button
        self.clear_faults_but = QtGui.QPushButton(self.monitoring_box)
        self.clear_faults_but.setGeometry(QtCore.QRect(10, 240, 71, 23))
        self.clear_faults_but.setText(_translate("MainWindow", "Clear Faults", None))

        # define labels
        self.create_label(self.monitoring_box, 10, 40, 31, 21, "VIN:")
        self.create_label(self.monitoring_box, 10, 90, 41, 20, "VOUT:")
        self.create_label(self.monitoring_box, 10, 140, 31, 20, "IOUT:")
        self.create_label(self.monitoring_box, 10, 190, 41, 20, "TEMP:")
        self.create_label(self.monitoring_box, 60, 40, 46, 21, "0 V")
        self.create_label(self.monitoring_box, 60, 90, 46, 21, "0 V")
        self.create_label(self.monitoring_box, 60, 140, 46, 21, "0 A")
        self.create_label(self.monitoring_box, 60, 190, 46, 21, "0 °C")

        # create frames for monitoring graphs
        self.input_voltage_graph = QtGui.QFrame(self.monitoring_box)
        self.input_voltage_graph.setGeometry(QtCore.QRect(90, 20, 281, 181))
        self.input_voltage_graph.setFrameShape(QtGui.QFrame.StyledPanel)
        self.input_voltage_graph.setFrameShadow(QtGui.QFrame.Raised)
        self.input_voltage_graph.setObjectName(_fromUtf8("input_voltage_graph"))
        self.output_current_graph = QtGui.QFrame(self.monitoring_box)
        self.output_current_graph.setGeometry(QtCore.QRect(90, 210, 281, 181))
        self.output_current_graph.setFrameShape(QtGui.QFrame.StyledPanel)
        self.output_current_graph.setFrameShadow(QtGui.QFrame.Raised)
        self.output_current_graph.setObjectName(_fromUtf8("output_current_graph"))
        self.temp_graph = QtGui.QFrame(self.monitoring_box)
        self.temp_graph.setGeometry(QtCore.QRect(380, 210, 281, 181))
        self.temp_graph.setFrameShape(QtGui.QFrame.StyledPanel)
        self.temp_graph.setFrameShadow(QtGui.QFrame.Raised)
        self.temp_graph.setObjectName(_fromUtf8("temp_graph"))
        self.output_voltage_graph = QtGui.QFrame(self.monitoring_box)
        self.output_voltage_graph.setGeometry(QtCore.QRect(380, 20, 281, 181))
        self.output_voltage_graph.setFrameShape(QtGui.QFrame.StyledPanel)
        self.output_voltage_graph.setFrameShadow(QtGui.QFrame.Raised)
        self.output_voltage_graph.setObjectName(_fromUtf8("output_voltage_graph"))
        self.stackedWidget.addWidget(self.page_5)

    def info_panel(self, centralWidget):
        self.info_frame = QtGui.QFrame(self.centralwidget)
        self.info_frame.setGeometry(QtCore.QRect(10, 10, 161, 511))
        self.info_frame.setStyleSheet(_fromUtf8(""))
        self.info_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.info_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.info_frame.setObjectName(_fromUtf8("info_frame"))

        self.create_label(self.info_frame, 20, 30, 61, 20, "Device Info:")

        self.textBrowser = QtGui.QTextBrowser(self.info_frame)
        self.textBrowser.setGeometry(QtCore.QRect(20, 70, 121, 192))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

    def setupUi(self, MainWindow):

        # set style of the main window
        self.setstyle(MainWindow)
        MainWindow.setWindowTitle(_translate("MainWindow", "PMBus Power GUI", None))

        # create central widget
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # set menu buttons
        self.menu(self.centralwidget)

        # create stackedWidget (tabbed)
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(180, 90, 711, 431))
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet(_fromUtf8(""))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))

        # create page1
        self.page1_main(self.stackedWidget)

        # create page2
        self.page2_configuration(self.stackedWidget)

        # create page3
        self.page3_pin(self.stackedWidget)

        # create page4
        self.page4_protection(self.stackedWidget)

        # create page5
        self.page5_monitor(self.stackedWidget)

        # device info - left panel
        self.info_panel(self.centralwidget)

        # menu bar & status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 901, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def page1(self):
        self.stackedWidget.setCurrentIndex(0)

    def page2(self):
        self.stackedWidget.setCurrentIndex(1)

    def page3(self):
        self.stackedWidget.setCurrentIndex(2)

    def page4(self):
        self.stackedWidget.setCurrentIndex(3)

    def page5(self):
        self.stackedWidget.setCurrentIndex(4)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

