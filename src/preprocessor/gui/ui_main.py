# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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

class Ui_Main(object):
    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName(u"Main")
        Main.resize(800, 600)
        self.menuFile_OpenProject = QAction(Main)
        self.menuFile_OpenProject.setObjectName(u"menuFile_OpenProject")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.menuFile_OpenProject.setIcon(icon)
        self.menuFile_Exit = QAction(Main)
        self.menuFile_Exit.setObjectName(u"menuFile_Exit")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit))
        self.menuFile_Exit.setIcon(icon1)
        self.menuFile_Exit.setMenuRole(QAction.MenuRole.QuitRole)
        self.menuHelp_About = QAction(Main)
        self.menuHelp_About.setObjectName(u"menuHelp_About")
        self.menuHelp_About.setMenuRole(QAction.MenuRole.AboutRole)
        self.menuView_ShowOriginal = QAction(Main)
        self.menuView_ShowOriginal.setObjectName(u"menuView_ShowOriginal")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.InsertImage))
        self.menuView_ShowOriginal.setIcon(icon2)
        self.menuView_ShowLensCorrected = QAction(Main)
        self.menuView_ShowLensCorrected.setObjectName(u"menuView_ShowLensCorrected")
        self.menuView_ShowLensCorrected.setIcon(icon2)
        self.menuView_ShowColorCorrected = QAction(Main)
        self.menuView_ShowColorCorrected.setObjectName(u"menuView_ShowColorCorrected")
        self.menuView_ShowColorCorrected.setIcon(icon2)
        self.menuView_ShowPerspectiveCorrected = QAction(Main)
        self.menuView_ShowPerspectiveCorrected.setObjectName(u"menuView_ShowPerspectiveCorrected")
        self.menuView_ShowPerspectiveCorrected.setIcon(icon2)
        self.menuFile_NewProject = QAction(Main)
        self.menuFile_NewProject.setObjectName(u"menuFile_NewProject")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.menuFile_NewProject.setIcon(icon3)
        self.menuFile_SaveProject = QAction(Main)
        self.menuFile_SaveProject.setObjectName(u"menuFile_SaveProject")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.menuFile_SaveProject.setIcon(icon4)
        self.menuFile_SaveProjectAs = QAction(Main)
        self.menuFile_SaveProjectAs.setObjectName(u"menuFile_SaveProjectAs")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.menuFile_SaveProjectAs.setIcon(icon5)
        self.centralwidget = QWidget(Main)
        self.centralwidget.setObjectName(u"centralwidget")
        Main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        self.menu_View = QMenu(self.menubar)
        self.menu_View.setObjectName(u"menu_View")
        Main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Main)
        self.statusbar.setObjectName(u"statusbar")
        Main.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(Main)
        self.toolBar.setObjectName(u"toolBar")
        Main.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menu_File.addAction(self.menuFile_NewProject)
        self.menu_File.addAction(self.menuFile_OpenProject)
        self.menu_File.addAction(self.menuFile_SaveProject)
        self.menu_File.addAction(self.menuFile_SaveProjectAs)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.menuFile_Exit)
        self.menu_Help.addAction(self.menuHelp_About)
        self.menu_View.addAction(self.menuView_ShowOriginal)
        self.menu_View.addAction(self.menuView_ShowLensCorrected)
        self.menu_View.addAction(self.menuView_ShowColorCorrected)
        self.menu_View.addAction(self.menuView_ShowPerspectiveCorrected)
        self.toolBar.addAction(self.menuFile_OpenProject)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.menuView_ShowOriginal)
        self.toolBar.addAction(self.menuView_ShowLensCorrected)
        self.toolBar.addAction(self.menuView_ShowColorCorrected)
        self.toolBar.addAction(self.menuView_ShowPerspectiveCorrected)

        self.retranslateUi(Main)

        QMetaObject.connectSlotsByName(Main)
    # setupUi

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", u"CAMBioMed Preprocessor", None))
        self.menuFile_OpenProject.setText(QCoreApplication.translate("Main", u"&Open Project...", None))
#if QT_CONFIG(shortcut)
        self.menuFile_OpenProject.setShortcut(QCoreApplication.translate("Main", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile_Exit.setText(QCoreApplication.translate("Main", u"E&xit", None))
        self.menuHelp_About.setText(QCoreApplication.translate("Main", u"&About...", None))
        self.menuView_ShowOriginal.setText(QCoreApplication.translate("Main", u"Show &Original", None))
        self.menuView_ShowLensCorrected.setText(QCoreApplication.translate("Main", u"Show &Lens Corrected", None))
        self.menuView_ShowColorCorrected.setText(QCoreApplication.translate("Main", u"Show &Color Corrected", None))
        self.menuView_ShowPerspectiveCorrected.setText(QCoreApplication.translate("Main", u"Show &Perspective Corrected", None))
        self.menuFile_NewProject.setText(QCoreApplication.translate("Main", u"&New Project...", None))
#if QT_CONFIG(shortcut)
        self.menuFile_NewProject.setShortcut(QCoreApplication.translate("Main", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile_SaveProject.setText(QCoreApplication.translate("Main", u"&Save Project", None))
#if QT_CONFIG(shortcut)
        self.menuFile_SaveProject.setShortcut(QCoreApplication.translate("Main", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile_SaveProjectAs.setText(QCoreApplication.translate("Main", u"Save Project &As...", None))
        self.menu_File.setTitle(QCoreApplication.translate("Main", u"&File", None))
        self.menu_Help.setTitle(QCoreApplication.translate("Main", u"&Help", None))
        self.menu_View.setTitle(QCoreApplication.translate("Main", u"&View", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("Main", u"toolBar", None))
    # retranslateUi

