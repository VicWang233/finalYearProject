# -*- coding: utf-8 -*-
#####################################################################
#                                                                   #
#                               Gui.py                              #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#             Description: GUI Application Layout Class             #
#                                                                   #
#####################################################################

from PyQt4 import QtCore, QtGui
import SequencingPlot
from PMBusCall import pmbus
import itertools
from collections import OrderedDict
from operator import itemgetter
import functools
import ftd2xx

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

    ###############################################################################################################
    #                                            CLASS INIT DEFINITION                                            #
    #                                                                                                             #
    #  Description: set GuiMainWindow as super class                                                              #
    #  Arguments: parent=None                                                                                     #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def __init__(self, parent=None):
        super(GuiMainWindow, self).__init__(parent)
        self.setParent(parent)

    ###############################################################################################################
    #                                            SET STYLE                                                        #
    #                                                                                                             #
    #  Description: set size, colour and style of the application                                                 #
    #  Arguments: main_window - main application frame                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

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
                                            "border: 1px solid rgb(147, 147, 147)}\n"))

    ###############################################################################################################
    #                                                  MENU                                                       #
    #                                                                                                             #
    #  Description: set button menu                                                                               #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

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

    ###############################################################################################################
    #                                                  PAGE 1                                                     #
    #                                                                                                             #
    #  Description: create first page of the GUI                                                                  #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def page1_main(self):

        # PMBus variables
        vout_val = pmbus.l16_query_command(pmbus.device, "iq_3f010221")  # vout_command L16
        margin_high = pmbus.l16_query_command(pmbus.device, "iq_3f010225")
        margin_low = pmbus.l16_query_command(pmbus.device, "iq_3f010226")

        perc_decrease = 0
        perc_increase = 0

        # margin high and margin low to percent conversion
        if float(vout_val) != 0:
            perc_decrease = ((float(vout_val) - float(margin_low)) / float(vout_val)) * 100
            perc_increase = ((float(margin_high) - float(vout_val)) / float(vout_val)) * 100

        # create page
        self.page = QtGui.QWidget()

        # create group box
        self.power_stage_box = QtGui.QGroupBox(self.page)
        self.size_and_name(self.power_stage_box, 19, 9, 970, 535, "Power Stage")

        # frame for block diagram of EM2130
        self.schematic = QtGui.QLabel(self.power_stage_box)
        self.schematic.setGeometry(QtCore.QRect(20, 20, 695, 409))
        pix_map = QtGui.QPixmap('diagrams/blockdiagram-em2130.png')
        self.schematic.setPixmap(pix_map)
        self.schematic.setStatusTip('EM2130L recommended application circuit')
        self.schematic.setStyleSheet('border: 1px solid rgb(147, 147, 147)')

        # voltage group box
        self.voltage_box = QtGui.QGroupBox(self.power_stage_box)
        self.size_and_name(self.voltage_box, 750, 20, 181, 241, "Voltage")

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        self.voltage_box.setLayout(grid)

        # text fields for voltage group
        self.vin_nom = self.create_line_edit("12")
        self.vin_nom.setReadOnly(True)
        self.vin_nom.setStatusTip('Nominal input voltage is 12V')
        self.vout_nom = self.create_line_edit(vout_val)
        self.vout_nom.textChanged.connect(self.check_range)
        self.vout_nom.setStatusTip('Enter here the nominal output voltage')
        self.marg_high = self.create_line_edit(str(round(perc_increase)))
        self.marg_high.textChanged.connect(self.check_range)
        self.marg_high.setStatusTip('Enter here the increase of VOUT')
        self.marg_low = self.create_line_edit(str(round(perc_decrease)))
        self.marg_low.textChanged.connect(self.check_range)
        self.marg_low.setStatusTip('Enter here the decrease of VOUT')

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

    ###############################################################################################################
    #                                                  PAGE 2                                                     #
    #                                                                                                             #
    #  Description: create second page of the GUI                                                                 #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

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
        self.ton_delay.textChanged.connect(self.check_range)
        self.ton_delay.setStatusTip('Enter here turn on delay interval')
        self.toff_delay = self.create_line_edit(toff_delay_val)
        self.toff_delay.textChanged.connect(self.check_range)
        self.toff_delay.setStatusTip('Enter here turn off delay interval')
        self.ton_rise = self.create_line_edit(ton_rise_val)
        self.ton_rise.textChanged.connect(self.check_range)
        self.ton_rise.setStatusTip('Enter here turn on rise interval')
        self.toff_fall = self.create_line_edit(toff_fall_val)
        self.toff_fall.textChanged.connect(self.check_range)
        self.toff_fall.setStatusTip('Enter here turn off fall interval')
        self.ton_max = self.create_line_edit(ton_max_val)
        self.ton_max.textChanged.connect(self.check_range)
        self.ton_max.setStatusTip('Enter here turn on max interval')
        self.toff_max = self.create_line_edit(toff_max_val)
        self.toff_max.textChanged.connect(self.check_range)
        self.toff_max.setStatusTip('Enter here turn off max interval')
        self.vout_on = self.create_line_edit(vout_on_val)
        self.vout_on.textChanged.connect(self.check_range)
        self.vout_on.setStatusTip('Enter here the desired output voltage')
        self.vout_off = self.create_line_edit(vout_off_val)
        self.vout_off.textChanged.connect(self.check_range)
        self.vout_off.setStatusTip('Enter here the terminal value of the output voltage')

        # set combo box
        self.cb = QtGui.QComboBox()
        self.cb.setStatusTip('Select the starting condition for the sequencer')
        self.cb.addItem("CTRL_POS")
        self.cb.setItemData(0, "Device turn on/off by CONTROL pin, upon positive transition detection", QtCore.Qt.ToolTipRole)
        self.cb.addItem("CTRL_NEG")
        self.cb.setItemData(1, "Device turn on/off by CONTROL pin, upon negative transition detection", QtCore.Qt.ToolTipRole)
        self.cb.addItem("OPERATION_CMD")
        self.cb.setItemData(2, "Device turn on/off controlled by PMBus" + u"\u2122" + " OPERATION command", QtCore.Qt.ToolTipRole)
        self.cb.currentIndexChanged.connect(self.startup_selection_change)

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

    ###############################################################################################################
    #                                                  PAGE 3                                                     #
    #                                                                                                             #
    #  Description: create third page of the GUI                                                                  #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def page3_tuning(self):

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
        self.pmbus_cb.setStatusTip("Select PmBus command" + u"\u2122" + " from the list")
        for key, value in self.dict.iteritems():
            self.pmbus_cb.addItem(key)
        self.pmbus_cb.currentIndexChanged.connect(self.selection_pmbus_commands)

        # set widgets for direct_access_box
        self.code = self.create_hex_line_edit("0x01")
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
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.read_direct.setEnabled(False)
        else:
            self.read_direct.setEnabled(True)
        self.write_direct = QtGui.QPushButton(direct_access_box)
        self.write_direct.setText("Write")
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.write_direct.setEnabled(False)
        else:
            self.write_direct.setEnabled(True)

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

    ###############################################################################################################
    #                                                  PAGE 4                                                     #
    #                                                                                                             #
    #  Description: create fourth page of the GUI                                                                 #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def page4_protection(self):

        # create page 4
        self.page_4 = QtGui.QWidget()

        first_tip = 'The device continues operation without interruption.'
        second_tip = ('The device continues operation for the delay time specified.\n'
                      'If the fault condition is still present at the end of the delay time,\n'
                      'the unit responds as programmed in the retry setting.')
        third_tip = 'The device shuts down and responds according to the retry setting.'
        fourth_tip = ('The device\'s output is disabled while the fault is present.\n'
                      'Operation resumes and the output is enabled when the fault condition no longer exists.')

        retries = ['None', '1', '2', '3', '4', '5', '6', 'Infinity']
        resposes = ['Continue', 'Delay and retry', 'Retry only', 'Device shutdown']
        item_data = [first_tip, second_tip, third_tip, fourth_tip]
        delays = ['0.00', '1.50', '3.00', '4.50', '6.00', '7.50', '9.00', '10.50']

        # create protection group box
        protection_box = QtGui.QGroupBox(self.page_4)
        self.size_and_name(protection_box, 19, 9, 970, 400, "PMBus Protection Parameters")

        # check boxes
        self.vout_ov_enable = self.create_checkbox()
        self.vout_ov_enable.setStatusTip(
            'Enable VOUT_OV protection settings. When disabled'
            ' VOUT_OV protection settings will not be written to the device')
        self.vout_uv_enable = self.create_checkbox()
        self.vout_uv_enable.setStatusTip(
            'Enable VOUT_UV protection settings. When disabled'
            ' VOUT_UV protection settings will not be written to the device')
        self.vin_ov_enable = self.create_checkbox()
        self.vin_ov_enable.setStatusTip(
            'Enable VIN_OV protection settings. When disabled'
            ' VIN_OV protection settings will not be written to the device')
        self.vin_uv_enable = self.create_checkbox()
        self.vin_uv_enable.setStatusTip(
            'Enable VIN_UV protection settings. When disabled'
            ' VIN_UV protection settings will not be written to the device')
        self.temp_ot_enable = self.create_checkbox()
        self.temp_ot_enable.setStatusTip(
            'Enable TEMP_OT protection settings. When disabled'
            ' TEMP_OT protection settings will not be written to the device')
        self.iout_oc_enable = self.create_checkbox()
        self.iout_oc_enable.setStatusTip(
            'Enable IOUT_OC protection settings. When disabled'
            ' IOUT_OC protection settings will not be written to the device')

        # combo-boxes for delay time units
        self.vout_ov_delay = QtGui.QComboBox()
        self.vout_uv_delay = QtGui.QComboBox()
        self.vin_ov_delay = QtGui.QComboBox()
        self.vin_uv_delay = QtGui.QComboBox()
        self.iout_oc_delay = QtGui.QComboBox()
        self.temp_ot_delay = QtGui.QComboBox()

        self.widgets_delays = [self.vout_ov_delay, self.vout_uv_delay, self.vin_ov_delay,
                          self.vin_uv_delay, self.iout_oc_delay, self.temp_ot_delay]

        # combo-boxes for retries
        self.vout_ov_retry = QtGui.QComboBox()
        self.vout_uv_retry = QtGui.QComboBox()
        self.vin_ov_retry = QtGui.QComboBox()
        self.vin_uv_retry = QtGui.QComboBox()
        self.iout_oc_retry = QtGui.QComboBox()
        self.temp_ot_retry = QtGui.QComboBox()

        self.widgets_retries = [self.vout_ov_retry, self.vout_uv_retry, self.vin_ov_retry,
                   self.vin_uv_retry, self.iout_oc_retry, self.temp_ot_retry]

        # combo-boxes for response type
        self.vout_ov_resp = QtGui.QComboBox()
        self.vout_uv_resp = QtGui.QComboBox()
        self.vin_ov_resp = QtGui.QComboBox()
        self.vin_uv_resp = QtGui.QComboBox()
        self.iout_oc_resp = QtGui.QComboBox()
        self.temp_ot_resp = QtGui.QComboBox()

        self.widgets_responses = [self.vout_ov_resp, self.vout_uv_resp, self.vin_ov_resp,
                             self.vin_uv_resp, self.iout_oc_resp, self.temp_ot_resp]

        for item in delays:
            self.vout_ov_delay.addItem(item)
            self.vout_uv_delay.addItem(item)
            self.vin_ov_delay.addItem(item)
            self.vin_uv_delay.addItem(item)
            self.iout_oc_delay.addItem(item)
            self.temp_ot_delay.addItem(item)

        for widget in self.widgets_delays:
            arg = functools.partial(self.handle_delays, widget)
            widget.setEnabled(False)
            widget.currentIndexChanged.connect(arg)

        for item in retries:
            self.vout_ov_retry.addItem(item)
            self.vout_uv_retry.addItem(item)
            self.vin_ov_retry.addItem(item)
            self.vin_uv_retry.addItem(item)
            self.iout_oc_retry.addItem(item)
            self.temp_ot_retry.addItem(item)

        for widget in self.widgets_retries:
            arg = functools.partial(self.handle_retries, widget)
            widget.setEnabled(False)
            widget.currentIndexChanged.connect(arg)

        for item, i, data in zip(resposes, range(len(item_data)), item_data):
            self.vout_ov_resp.addItem(item)
            self.vout_ov_resp.setItemData(i, data, QtCore.Qt.ToolTipRole)
            self.vout_uv_resp.addItem(item)
            self.vout_uv_resp.setItemData(i, data, QtCore.Qt.ToolTipRole)
            self.vin_ov_resp.addItem(item)
            self.vin_ov_resp.setItemData(i, data, QtCore.Qt.ToolTipRole)
            self.vin_uv_resp.addItem(item)
            self.vin_uv_resp.setItemData(i, data, QtCore.Qt.ToolTipRole)
            self.iout_oc_resp.addItem(item)
            self.iout_oc_resp.setItemData(i, data, QtCore.Qt.ToolTipRole)
            self.temp_ot_resp.addItem(item)
            self.temp_ot_resp.setItemData(i, data, QtCore.Qt.ToolTipRole)

        for widget in self.widgets_responses:
            arg = functools.partial(self.handle_responses, widget)
            widget.currentIndexChanged.connect(arg)

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
        self.vout_ov_warning.textChanged.connect(self.check_range)
        self.vout_ov_warning.setStatusTip('Enter here output over-voltage warning threshold')
        self.vout_uv_warning = self.create_line_edit(vout_uv_war_val)
        self.vout_uv_warning.textChanged.connect(self.check_range)
        self.vout_uv_warning.setStatusTip('Enter here output under-voltage warning threshold')
        self.vin_ov_warning = self.create_line_edit(vin_ov_war_val)
        self.vin_ov_warning.textChanged.connect(self.check_range)
        self.vin_ov_warning.setStatusTip('Enter here input over-voltage warning threshold')
        self.vin_uv_warning = self.create_line_edit(vin_uv_war_val)
        self.vin_uv_warning.textChanged.connect(self.check_range)
        self.vin_uv_warning.setStatusTip('Enter here input under-voltage warning threshold')
        self.iout_oc_warning = self.create_line_edit(iout_oc_war_val)
        self.iout_oc_warning.textChanged.connect(self.check_range)
        self.iout_oc_warning.setStatusTip('Enter here output over-current warning threshold')
        self.temp_ot_warning = self.create_line_edit(temp_ot_war_val)
        self.temp_ot_warning.textChanged.connect(self.check_range)
        self.temp_ot_warning.setStatusTip('Enter here over-temperature warning threshold')
        self.vout_ov_fault = self.create_line_edit(vout_ov_fal_val)
        self.vout_ov_fault.textChanged.connect(self.check_range)
        self.vout_ov_fault.setStatusTip('Enter here output over-voltage fault threshold')
        self.vout_uv_fault = self.create_line_edit(vout_uv_fal_val)
        self.vout_uv_fault.textChanged.connect(self.check_range)
        self.vout_uv_fault.setStatusTip('Enter here output under-voltage fault threshold')
        self.vin_ov_fault = self.create_line_edit(vin_ov_fal_val)
        self.vin_ov_fault.textChanged.connect(self.check_range)
        self.vin_ov_fault.setStatusTip('Enter here input over-voltage fault threshold')
        self.vin_uv_fault = self.create_line_edit(vin_uv_fal_val)
        self.vin_uv_fault.textChanged.connect(self.check_range)
        self.vin_uv_fault.setStatusTip('Enter here input under-voltage fault threshold')
        self.iout_oc_fault = self.create_line_edit(iout_oc_fal_val)
        self.iout_oc_fault.textChanged.connect(self.check_range)
        self.iout_oc_fault.setStatusTip('Enter here output over-current fault threshold')
        self.temp_ot_fault = self.create_line_edit(temp_ot_fal_val)
        self.temp_ot_fault.textChanged.connect(self.check_range)
        self.temp_ot_fault.setStatusTip('Enter here over-temperature fault threshold')

        grid = QtGui.QGridLayout()

        grid.setSpacing(20)
        grid.addWidget(QtGui.QLabel(" "), 0, 1, 1, 1, QtCore.Qt.AlignTop)

        # First row
        grid.addWidget(QtGui.QLabel("Enable"), 1, 2, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("Warning Limit"), 1, 3, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("\t"), 1, 4, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("Fault Limit"), 1, 5, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("\t"), 1, 6, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("Delay"), 1, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("\t"), 1, 8, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(QtGui.QLabel("Number of Retries"), 1, 9, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(QtGui.QLabel("Type of Response"), 1, 10, 1, 1, QtCore.Qt.AlignCenter)

        grid.setRowMinimumHeight(5, 5)

        titles = ["VOUT OV", "VOUT UV", "VIN OV", "VIN UV", "IOUT", "TEMP"]
        widgets = [self.vout_ov_enable, self.vout_ov_warning, self.vout_ov_fault, self.vout_ov_delay,
                   self.vout_ov_retry, self.vout_ov_resp, self.vout_uv_enable, self.vout_uv_warning,
                   self.vout_uv_fault, self.vout_uv_delay, self.vout_uv_retry, self.vout_uv_resp,
                   self.vin_ov_enable, self.vin_ov_warning, self.vin_ov_fault, self.vin_ov_delay,
                   self.vin_ov_retry, self.vin_ov_resp, self.vin_uv_enable, self.vin_uv_warning,
                   self.vin_uv_fault, self.vin_uv_delay, self.vin_uv_retry, self.vin_uv_resp,
                   self.iout_oc_enable, self.iout_oc_warning, self.iout_oc_fault, self.iout_oc_delay,
                   self.iout_oc_retry, self.iout_oc_resp, self.temp_ot_enable, self.temp_ot_warning,
                   self.temp_ot_fault, self.temp_ot_delay, self.temp_ot_retry, self.temp_ot_resp]

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
            grid.addWidget(QtGui.QLabel("us"), i, 8)
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
        self.power_on.textChanged.connect(self.check_range)
        self.power_on.setStatusTip('Enter here Power OK on level')
        self.vin_on = self.create_line_edit(vin_on_val)
        self.vin_on.textChanged.connect(self.check_range)
        self.vin_on.setStatusTip('Enter here VIN on level')
        self.power_off = self.create_line_edit(power_off_val)
        self.power_off.textChanged.connect(self.check_range)
        self.power_off.setStatusTip('Enter here Power OK off level')
        self.vin_off = self.create_line_edit(vin_off_val)
        self.vin_off.textChanged.connect(self.check_range)
        self.vin_off.setStatusTip('Enter here VIN off level')

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

    ###############################################################################################################
    #                                                  PAGE 5                                                     #
    #                                                                                                             #
    #  Description: create fifth page of the GUI                                                                  #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def page5_monitor(self):

        # create page 5
        self.page_5 = QtGui.QWidget()

        # create monitoring box
        self.monitoring_box = QtGui.QGroupBox(self.page_5)
        self.size_and_name(self.monitoring_box, 19, 9, 970, 535, "Real Time Readings")

        # clear faults button
        self.clear_faults_but = QtGui.QPushButton(self.monitoring_box)
        self.clear_faults_but.setGeometry(QtCore.QRect(20, 240, 100, 23))
        self.clear_faults_but.setText("Clear Faults")
        self.clear_faults_but.setStatusTip('Clears all of the warning or fault bits set in the status registers')
        self.clear_faults_but.clicked.connect(self.handle_clear_faults)
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.clear_faults_but.setEnabled(False)
        else:
            self.clear_faults_but.setEnabled(True)

        # device startup
        self.control_pin = QtGui.QPushButton(self.monitoring_box)
        self.control_pin.setGeometry(QtCore.QRect(20, 280, 100, 23))
        self.control_pin.setText("Control Pin")
        self.control_pin.setStatusTip('Turn on/off the device by toggling the Control Pin')
        self.control_pin.clicked.connect(self.handle_control_pin)
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.control_pin.setEnabled(False)
        else:
            self.control_pin.setEnabled(True)
        self.index_pin = 1

        # device startup - OPERATION command
        self.operation_cmd = QtGui.QPushButton(self.monitoring_box)
        self.operation_cmd.setGeometry(QtCore.QRect(20, 320, 100, 23))
        self.operation_cmd.setText("OPERATION_CMD")
        self.operation_cmd.setEnabled(False)
        self.operation_cmd.setStatusTip('Turn on/off the device by sending PMBus OPERATION command')
        self.operation_cmd.clicked.connect(self.handle_operation_cmd)
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.operation_cmd.setEnabled(False)
        else:
            self.operation_cmd.setEnabled(True)
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
        self.monitoring_but.setStatusTip('Turn on/off the real time plotting')
        self.monitoring_but.clicked.connect(self.mon_on_off)
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.monitoring_but.setEnabled(False)
        else:
            self.monitoring_but.setEnabled(True)

        self.led = QtGui.QLabel(self.monitoring_box)
        self.led.setGeometry(QtCore.QRect(140, 400, 24, 24))
        self.pix_map = QtGui.QPixmap('icons/green.png')
        self.led.setPixmap(self.pix_map)
        self.index = 1

        # write volatile button
        self.write_volatile = QtGui.QPushButton(self.monitoring_box)
        self.write_volatile.setGeometry(QtCore.QRect(20, 440, 100, 23))
        self.write_volatile.setText("Write volatile")
        self.operation_cmd.setStatusTip('Save all new settings to the device\'s volatile memory')
        self.write_volatile.setStyleSheet("background-color: yellow")
        self.write_volatile.clicked.connect(self.write_to_device)
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.write_volatile.setEnabled(False)
        else:
            self.write_volatile.setEnabled(True)

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

    ###############################################################################################################
    #                                              INFO PANEL                                                     #
    #                                                                                                             #
    #  Description: create side info panel of the GUI                                                             #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def info_panel(self):

        info = ("EM2130L\n"
                "Step-Down DC-DC\n"
                "Switching Converter\n"
                "with\nIntegrated Inductor,\n"
                "Featuring\nDigital Control\n"
                "with PMBus" + u"\u2122" + " v1.2\n"
                "compliant Interface\n")
        not_connected = ("PMBus" + u"\u2122" + " device\n"
                         "not connected!")
        self.info_frame = QtGui.QFrame(self.central_widget)
        self.info_frame.setGeometry(QtCore.QRect(10, 10, 161, 645))
        self.create_label(self.info_frame, 20, 30, 61, 20, "Device Info:")
        self.text_browser = QtGui.QTextBrowser(self.info_frame)
        self.text_browser.setGeometry(QtCore.QRect(20, 70, 121, 192))
        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.create_label(self.text_browser, 10, 10, 100, 200, not_connected)
        else:
            self.create_label(self.text_browser, 10, 10, 100, 200, info)

    ###############################################################################################################
    #                                               SETUP GUI                                                     #
    #                                                                                                             #
    #  Description: generate all components of the GUI                                                            #
    #  Arguments: main_window - main application frame                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def setup_gui(self, main_window):

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
        self.page3_tuning()

        # create page4
        self.page4_protection()

        # create page5
        self.page5_monitor()

        # device info - left panel
        self.info_panel()

        # menu bar & status bar
        main_window.setCentralWidget(self.central_widget)

        self.status_bar = QtGui.QStatusBar(main_window)
        main_window.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(main_window)

    ###############################################################################################################
    #                                              PAGE 1 - 5                                                     #
    #                                                                                                             #
    #  Description: connect each page with the correct index of the Qt stacked-widget                             #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

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
