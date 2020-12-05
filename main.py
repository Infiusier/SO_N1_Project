# coding: utf-8
import sys

from PySide2 import QtWidgets
import MainWindow

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    ui=MainWindow.MainLog()
    ui.show()
    sys.exit(app.exec_())