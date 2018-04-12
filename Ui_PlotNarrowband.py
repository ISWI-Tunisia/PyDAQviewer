# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_PlotNarrowband.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(722, 544)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("docs/imgs/ISWI_Logo_sm.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName("timeEdit")
        self.horizontalLayout.addWidget(self.timeEdit)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.horizontalLayout.addWidget(self.timeEdit_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.view_raw = QtWidgets.QCheckBox(self.centralwidget)
        self.view_raw.setChecked(True)
        self.view_raw.setObjectName("view_raw")
        self.horizontalLayout.addWidget(self.view_raw)
        self.view_average = QtWidgets.QCheckBox(self.centralwidget)
        self.view_average.setChecked(True)
        self.view_average.setObjectName("view_average")
        self.horizontalLayout.addWidget(self.view_average)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.mplwidget = MPL_WIDGET_2D(self.centralwidget)
        self.mplwidget.setObjectName("mplwidget")
        self.verticalLayout.addWidget(self.mplwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyDAQviewer: Plot Narrowband Data"))
        self.label.setText(_translate("MainWindow", "Start Time"))
        self.timeEdit.setDisplayFormat(_translate("MainWindow", "HH:mm:ss"))
        self.label_2.setText(_translate("MainWindow", "End Time"))
        self.timeEdit_2.setDisplayFormat(_translate("MainWindow", "HH:mm:ss"))
        self.view_raw.setText(_translate("MainWindow", "View Raw DATA"))
        self.view_average.setText(_translate("MainWindow", "Vew Arerage DATA"))

from mplwidget import MPL_WIDGET_2D

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

