#####################################################################
#                                                                   #
#                           Monitoring.py                           #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#   Description: Real Time graphs using matplotlib for plotting     #
#              input and output voltages and temperature            #
#                                                                   #
#####################################################################

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PMBusCall import pmbus
import functools
import numpy as np
import ftd2xx
from PyQt4 import QtCore
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('TkAgg')


class GraphCanvas(FigureCanvas):

    ###############################################################################################################
    #                                            CLASS INIT DEFINITION                                            #
    #                                                                                                             #
    #  Description: define variables needed                                                                       #
    #  Arguments: arg ("vin" / "vout" / "temp")                                                                   #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def __init__(self, arg):

        self.current_timer = None
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        super(GraphCanvas, self).__init__(self.fig)
        self.timer = QtCore.QTimer()
        self.init_data()
        self.init_figure(arg)
        self.init_timer(arg)

        if pmbus.device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
            self.stop_timer()

    ###############################################################################################################
    #                                               INIT TIMER                                                    #
    #                                                                                                             #
    #  Description: init timer that will take care of real-time plot updates                                      #
    #  Arguments: arg ("vin" / "vout" / "temp")                                                                   #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def init_timer(self, arg):

        # init timers
        value = functools.partial(self.update_figure, arg)
        if arg == "vin":
            self.timer.timeout.connect(value)
            self.timer.start(100)  # 1 = 1 msec , 1000 = 1 sec
        if arg == "vout":
            self.timer.timeout.connect(value)
            self.timer.start(100)  # 1 = 1 msec , 1000 = 1 sec
        if arg == "temp":
            self.timer.timeout.connect(value)
            self.timer.start(100)  # 1 = 1 msec , 1000 = 1 sec

    ###############################################################################################################
    #                                                STOP TIMER                                                   #
    #                                                                                                             #
    #  Description: this method is needed for "Monitoring" button placed on "Monitoring" tab                      #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def stop_timer(self):

        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100)

    ###############################################################################################################
    #                                                 INIT DATA                                                   #
    #                                                                                                             #
    #  Description: init arrays to store data                                                                     #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def init_data(self):

        # init data
        self.data = [0 for x in range(25)]
        self.t0 = float(self.data[0])

    ###############################################################################################################
    #                                                  INIT FIGURE                                                #
    #                                                                                                             #
    #  Description: initialise plots (axes, fonts, sizes, titles)                                                 #
    #  Arguments: arg ("vin" / "vout" / "temp")                                                                   #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def init_figure(self, arg):

        font = {
                'weight': 'normal',
                'size': 10,
                }
        plt.grid()
        plt.gcf().subplots_adjust(bottom=0.15)  # give some space for x label
        self.fig.patch.set_facecolor('#DCE4F4')  # set graph background color
        self.time_axis = np.zeros(25)
        self.y_axis = np.zeros(25)

        if arg == "vin":
            self.ax.set_ylim(0.0, 16.0)
            self.fig.canvas.draw()
            self.line = self.ax.plot(self.time_axis, self.y_axis)
            self.ax.set_xlabel("Time[ms]", font)
            self.ax.set_ylabel("Voltage[V]", font)
        if arg == "vout":
            self.ax.set_ylim(0.0, 3.0)
            self.fig.canvas.draw()
            self.line = self.ax.plot(self.time_axis, self.y_axis)
            self.ax.set_xlabel("Time[ms]", font)
            self.ax.set_ylabel("Voltage[V]", font)
        if arg == "temp":
            self.ax.set_ylim(0, 120)
            self.fig.canvas.draw()
            self.line = self.ax.plot(self.time_axis, self.y_axis)
            self.ax.set_xlabel("Time[ms]", font)
            self.ax.set_ylabel("Temperature[C]", font)

    ###############################################################################################################
    #                                                 UPDATE FIGURE                                               #
    #                                                                                                             #
    #  Description: update the real-time plot and the time axis                                                   #
    #  Arguments: arg ("vin" / "vout" / "temp")                                                                   #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def update_figure(self, arg):

        # read PMBus data
        if arg == "vin":
            vin_average = pmbus.l11_query_command(pmbus.device, "iq_3f010288")
            self.data = np.append(self.data, vin_average)
        if arg == "vout":
            vout_average = pmbus.l16_query_command(pmbus.device, "iq_3f01028B")
            self.data = np.append(self.data, vout_average)
        if arg == "temp":
            temp_average = pmbus.l11_query_command(pmbus.device, "iq_3f01028E")
            self.data = np.append(self.data, temp_average)

        # update plots
        current_xaxis = np.arange(len(self.data) - 25, len(self.data), 1)
        self.line[0].set_data(current_xaxis, np.array(self.data[-25:]))
        self.ax.set_xlim(current_xaxis.min(), current_xaxis.max())
        self.fig.canvas.draw()
        self.figure.canvas.flush_events()



