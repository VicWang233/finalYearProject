#####################################################################
#                                                                   #
#                              Main.py                              #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#        Description: Main file for PMBus Power Application         #
#                                                                   #
#####################################################################

from PyQt4 import QtGui
import GuiFunctionality


def run():
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    ui = GuiFunctionality.GuiFunctionality()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
