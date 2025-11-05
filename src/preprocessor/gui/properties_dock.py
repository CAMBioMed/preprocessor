# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties_dock.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QFormLayout, QLabel,
    QSizePolicy, QSlider, QToolBox, QVBoxLayout,
    QWidget)

class Ui_PropertiesDock(object):
    def setupUi(self, PropertiesDock):
        if not PropertiesDock.objectName():
            PropertiesDock.setObjectName(u"PropertiesDock")
        PropertiesDock.resize(400, 300)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.toolBox = QToolBox(self.dockWidgetContents)
        self.toolBox.setObjectName(u"toolBox")
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.page1.setGeometry(QRect(0, 0, 382, 198))
        self.formLayout_2 = QFormLayout(self.page1)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.page1)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.horizontalSlider = QSlider(self.page1)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximum(500)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.horizontalSlider)

        self.label_2 = QLabel(self.page1)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.horizontalSlider_2 = QSlider(self.page1)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setMaximum(500)
        self.horizontalSlider_2.setValue(150)
        self.horizontalSlider_2.setOrientation(Qt.Orientation.Horizontal)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.horizontalSlider_2)

        self.toolBox.addItem(self.page1, u"Values")
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.page2.setGeometry(QRect(0, 0, 382, 198))
        self.toolBox.addItem(self.page2, u"Extra")

        self.verticalLayout.addWidget(self.toolBox)

        PropertiesDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(PropertiesDock)

        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PropertiesDock)
    # setupUi

    def retranslateUi(self, PropertiesDock):
        PropertiesDock.setWindowTitle(QCoreApplication.translate("PropertiesDock", u"Properties", None))
        self.label.setText(QCoreApplication.translate("PropertiesDock", u"V1", None))
        self.label_2.setText(QCoreApplication.translate("PropertiesDock", u"V2", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page1), QCoreApplication.translate("PropertiesDock", u"Values", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page2), QCoreApplication.translate("PropertiesDock", u"Extra", None))
    # retranslateUi

