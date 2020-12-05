# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Log(object):
    def setupUi(self, Log):
        if not Log.objectName():
            Log.setObjectName(u"Log")
        Log.resize(200, 400)
        Log.setMinimumSize(QSize(200, 400))
        Log.setMaximumSize(QSize(200, 400))
        self.centralwidget = QWidget(Log)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(0, 0, 200, 400))
        self.textEdit.setMinimumSize(QSize(0, 0))
        self.textEdit.setMaximumSize(QSize(9999999, 9999999))
        Log.setCentralWidget(self.centralwidget)

        self.retranslateUi(Log)

        QMetaObject.connectSlotsByName(Log)
    # setupUi

    def retranslateUi(self, Log):
        Log.setWindowTitle(QCoreApplication.translate("Log", u"MainWindow", None))
    # retranslateUi

