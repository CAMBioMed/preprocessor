# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QToolBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.menuFile_Open = QAction(MainWindow)
        self.menuFile_Open.setObjectName(u"menuFile_Open")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.menuFile_Open.setIcon(icon)
        self.menuFile_Exit = QAction(MainWindow)
        self.menuFile_Exit.setObjectName(u"menuFile_Exit")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit))
        self.menuFile_Exit.setIcon(icon1)
        self.menuHelp_About = QAction(MainWindow)
        self.menuHelp_About.setObjectName(u"menuHelp_About")
        self.menuView_ShowOriginal = QAction(MainWindow)
        self.menuView_ShowOriginal.setObjectName(u"menuView_ShowOriginal")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.InsertImage))
        self.menuView_ShowOriginal.setIcon(icon2)
        self.menuView_ShowLensCorrected = QAction(MainWindow)
        self.menuView_ShowLensCorrected.setObjectName(u"menuView_ShowLensCorrected")
        self.menuView_ShowLensCorrected.setIcon(icon2)
        self.menuView_ShowColorCorrected = QAction(MainWindow)
        self.menuView_ShowColorCorrected.setObjectName(u"menuView_ShowColorCorrected")
        self.menuView_ShowColorCorrected.setIcon(icon2)
        self.menuView_ShowPerspectiveCorrected = QAction(MainWindow)
        self.menuView_ShowPerspectiveCorrected.setObjectName(u"menuView_ShowPerspectiveCorrected")
        self.menuView_ShowPerspectiveCorrected.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        self.menu_View = QMenu(self.menubar)
        self.menu_View.setObjectName(u"menu_View")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menu_File.addAction(self.menuFile_Open)
        self.menu_File.addAction(self.menuFile_Exit)
        self.menu_Help.addAction(self.menuHelp_About)
        self.menu_View.addAction(self.menuView_ShowOriginal)
        self.menu_View.addAction(self.menuView_ShowLensCorrected)
        self.menu_View.addAction(self.menuView_ShowColorCorrected)
        self.menu_View.addAction(self.menuView_ShowPerspectiveCorrected)
        self.toolBar.addAction(self.menuFile_Open)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.menuView_ShowOriginal)
        self.toolBar.addAction(self.menuView_ShowLensCorrected)
        self.toolBar.addAction(self.menuView_ShowColorCorrected)
        self.toolBar.addAction(self.menuView_ShowPerspectiveCorrected)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuFile_Open.setText(QCoreApplication.translate("MainWindow", u"&Open...", None))
#if QT_CONFIG(shortcut)
        self.menuFile_Open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile_Exit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.menuHelp_About.setText(QCoreApplication.translate("MainWindow", u"&About...", None))
        self.menuView_ShowOriginal.setText(QCoreApplication.translate("MainWindow", u"Show &Original", None))
        self.menuView_ShowLensCorrected.setText(QCoreApplication.translate("MainWindow", u"Show &Lens Corrected", None))
        self.menuView_ShowColorCorrected.setText(QCoreApplication.translate("MainWindow", u"Show &Color Corrected", None))
        self.menuView_ShowPerspectiveCorrected.setText(QCoreApplication.translate("MainWindow", u"Show &Perspective Corrected", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.menu_View.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

