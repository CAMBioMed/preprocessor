# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QHeaderView, QLabel, QProgressBar,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        if not ProgressDialog.objectName():
            ProgressDialog.setObjectName(u"ProgressDialog")
        ProgressDialog.resize(561, 254)
        self.verticalLayout = QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblStatus = QLabel(ProgressDialog)
        self.lblStatus.setObjectName(u"lblStatus")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblStatus.sizePolicy().hasHeightForWidth())
        self.lblStatus.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.lblStatus)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.prbProgress = QProgressBar(ProgressDialog)
        self.prbProgress.setObjectName(u"prbProgress")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.prbProgress.sizePolicy().hasHeightForWidth())
        self.prbProgress.setSizePolicy(sizePolicy1)
        self.prbProgress.setValue(24)

        self.horizontalLayout.addWidget(self.prbProgress)

        self.lblProgress = QLabel(ProgressDialog)
        self.lblProgress.setObjectName(u"lblProgress")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblProgress.sizePolicy().hasHeightForWidth())
        self.lblProgress.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.lblProgress)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeItems = QTreeWidget(ProgressDialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"2");
        __qtreewidgetitem.setText(0, u"1");
        self.treeItems.setHeaderItem(__qtreewidgetitem)
        self.treeItems.setObjectName(u"treeItems")
        self.treeItems.setColumnCount(2)
        self.treeItems.setSupportedDragActions(Qt.DropAction.IgnoreAction)
        self.treeItems.header().setVisible(False)

        self.verticalLayout.addWidget(self.treeItems)

        self.btnDialogButtons = QDialogButtonBox(ProgressDialog)
        self.btnDialogButtons.setObjectName(u"btnDialogButtons")
        self.btnDialogButtons.setOrientation(Qt.Orientation.Horizontal)
        self.btnDialogButtons.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Close)

        self.verticalLayout.addWidget(self.btnDialogButtons)


        self.retranslateUi(ProgressDialog)
        self.btnDialogButtons.accepted.connect(ProgressDialog.accept)
        self.btnDialogButtons.rejected.connect(ProgressDialog.reject)

        QMetaObject.connectSlotsByName(ProgressDialog)
    # setupUi

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QCoreApplication.translate("ProgressDialog", u"Dialog", None))
        self.lblStatus.setText(QCoreApplication.translate("ProgressDialog", u"Status...", None))
        self.lblProgress.setText(QCoreApplication.translate("ProgressDialog", u"100/100 (110%)", None))
    # retranslateUi

