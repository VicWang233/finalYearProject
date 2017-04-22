#####################################################################
#                                                                   #
#                         SequencingPlot.py                         #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#             Description: Draw Sequencing Diagram Class            #
#                                                                   #
#####################################################################

from PyQt4 import QtGui, QtCore


class Graph(QtGui.QWidget):

    ###############################################################################################################
    #                                            CLASS INIT DEFINITION                                            #
    #                                                                                                             #
    #  Description: initialize pixmap                                                                             #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def __init__(self):

        super(Graph, self).__init__()
        self.pixmap = QtGui.QPixmap(970, 351)
        self.pixmap.fill(QtCore.Qt.transparent)

    ###############################################################################################################
    #                                                 GENERATE GRAPH                                              #
    #                                                                                                             #
    #  Description: generate graph                                                                                #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def generate_graph(self):

        paint = QtGui.QPainter(self.pixmap)
        self.draw_lines(paint)

    ###############################################################################################################
    #                                                   PAINT EVENT                                               #
    #                                                                                                             #
    #  Description: overwritten function paintEvent to draw a graph on the application                            #
    #  Arguments: none                                                                                            #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def paintEvent(self, e):

        qp = QtGui.QPainter(self)
        self.generate_graph()
        qp.drawPixmap(0, 0, self.pixmap)  # load graph from Bitmap

    ###############################################################################################################
    #                                                    DRAW LINES                                               #
    #                                                                                                             #
    #  Description: method to draw axis and each line of the Sequencing Diagram                                   #
    #  Arguments: gp (QPainter)                                                                                   #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def draw_lines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(60, 20, 60, 230)  # y axis
        self.draw_arrow_head(qp, 55, 20, 65, 20, 60, 15)
        qp.drawLine(60, 230, 850, 230)  # x axis
        self.draw_arrow_head(qp, 850, 225, 850, 235, 855, 230)

        pen = QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.SolidLine)  # horizontal dashed
        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(60, 40, 850, 40)
        qp.drawLine(60, 189, 850, 189)

        pen = QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.SolidLine)  # vertical dashed
        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(172, 40, 172, 230)
        qp.drawLine(284, 40, 284, 230)
        qp.drawLine(396, 40, 396, 230)
        qp.drawLine(508, 40, 508, 230)
        qp.drawLine(620, 40, 620, 230)
        qp.drawLine(732, 40, 732, 230)
        qp.drawLine(844, 40, 844, 230)

        pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(62, 105, 192)), 2.5,  QtCore.Qt.SolidLine)  # draw graph
        qp.setPen(pen)
        qp.drawLine(60, 227, 172, 227)
        qp.drawLine(172, 230, 284, 40)

        qp.drawLine(620, 40, 732, 189)
        qp.drawLine(732, 189, 844, 189)

        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([45, 15, 15, 15])
        qp.setPen(pen)
        qp.drawLine(284, 40, 620, 40)

        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)  # draw bottom legend lines
        qp.setPen(pen)
        qp.drawLine(60, 240, 60, 270)
        qp.drawLine(172, 240, 172, 270)
        qp.drawLine(284, 240, 284, 260)
        qp.drawLine(396, 240, 396, 270)
        qp.drawLine(508, 240, 508, 270)
        qp.drawLine(620, 240, 620, 270)
        qp.drawLine(732, 240, 732, 260)
        qp.drawLine(844, 240, 844, 270)

        # draw arrows
        qp.drawLine(70, 245, 162, 245)
        self.draw_arrow_head(qp, 70, 240, 70, 250, 65, 245)
        self.draw_arrow_head(qp, 157, 240, 157, 250, 162, 245)
        qp.drawLine(182, 245, 274, 245)
        self.draw_arrow_head(qp, 182, 240, 182, 250, 177, 245)
        self.draw_arrow_head(qp, 269, 240, 269, 250, 274, 245)
        qp.drawLine(182, 265, 386, 265)
        self.draw_arrow_head(qp, 182, 260, 182, 270, 177, 265)
        self.draw_arrow_head(qp, 381, 260, 381, 270, 386, 265)
        qp.drawLine(518, 245, 610, 245)
        self.draw_arrow_head(qp, 518, 240, 518, 250, 513, 245)
        self.draw_arrow_head(qp, 605, 240, 605, 250, 610, 245)
        qp.drawLine(630, 245, 722, 245)
        self.draw_arrow_head(qp, 630, 240, 630, 250, 625, 245)
        self.draw_arrow_head(qp, 717, 240, 717, 250, 722, 245)
        qp.drawLine(630, 265, 834, 265)
        self.draw_arrow_head(qp, 630, 260, 630, 270, 625, 265)
        self.draw_arrow_head(qp, 829, 260, 829, 270, 834, 265)

    ###############################################################################################################
    #                                                 DRAW ARROW HEAD                                             #
    #                                                                                                             #
    #  Description: method to draw arrow head with specific coordinates                                           #
    #  Arguments: gp (QPainter), x1, y1, x2, y2, x3, y3 (coordinates)                                             #
    #  Returns: none                                                                                              #
    ###############################################################################################################

    def draw_arrow_head(self, qp, x1, y1, x2, y2, x3, y3):

        # draw arrow head
        qp.setBrush(QtGui.QBrush(QtCore.Qt.black))
        points = [QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2), QtCore.QPoint(x3, y3)]
        needle = QtGui.QPolygon(points)
        qp.drawPolygon(needle)

