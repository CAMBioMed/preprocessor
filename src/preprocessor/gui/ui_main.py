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
        self.menuFile_NewProject = QAction(Main)
        self.menuFile_NewProject.setObjectName(u"menuFile_NewProject")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.menuFile_NewProject.setIcon(icon2)
        self.menuFile_SaveProject = QAction(Main)
        self.menuFile_SaveProject.setObjectName(u"menuFile_SaveProject")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.menuFile_SaveProject.setIcon(icon3)
        self.menuFile_SaveProjectAs = QAction(Main)
        self.menuFile_SaveProjectAs.setObjectName(u"menuFile_SaveProjectAs")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.menuFile_SaveProjectAs.setIcon(icon4)
        self.menuFile_CloseProject = QAction(Main)
        self.menuFile_CloseProject.setObjectName(u"menuFile_CloseProject")
        self.menuFile_ExportAll = QAction(Main)
        self.menuFile_ExportAll.setObjectName(u"menuFile_ExportAll")
        self.menuEdit_DetectQuadrat = QAction(Main)
        self.menuEdit_DetectQuadrat.setObjectName(u"menuEdit_DetectQuadrat")
        self.menuWindow_ShowThumbnailsPanel = QAction(Main)
        self.menuWindow_ShowThumbnailsPanel.setObjectName(u"menuWindow_ShowThumbnailsPanel")
        self.menuWindow_ShowEditorPanel = QAction(Main)
        self.menuWindow_ShowEditorPanel.setObjectName(u"menuWindow_ShowEditorPanel")
        self.menuFile_ProjectSettings = QAction(Main)
        self.menuFile_ProjectSettings.setObjectName(u"menuFile_ProjectSettings")
        self.menuFile_ProjectSettings.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(Main)
        self.centralwidget.setObjectName(u"centralwidget")
        Main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        Main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Main)
        self.statusbar.setObjectName(u"statusbar")
        Main.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(Main)
        self.toolBar.setObjectName(u"toolBar")
        Main.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menuFile.addAction(self.menuFile_NewProject)
        self.menuFile.addAction(self.menuFile_OpenProject)
        self.menuFile.addAction(self.menuFile_SaveProject)
        self.menuFile.addAction(self.menuFile_SaveProjectAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuFile_ProjectSettings)
        self.menuFile.addAction(self.menuFile_ExportAll)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuFile_Exit)
        self.menuHelp.addAction(self.menuHelp_About)
        self.menuEdit.addAction(self.menuEdit_DetectQuadrat)
        self.menuWindow.addAction(self.menuWindow_ShowThumbnailsPanel)
        self.menuWindow.addAction(self.menuWindow_ShowEditorPanel)
        self.toolBar.addAction(self.menuFile_OpenProject)
        self.toolBar.addAction(self.menuFile_SaveProject)

        self.retranslateUi(Main)

        QMetaObject.connectSlotsByName(Main)
    # setupUi

    def retranslateUi(self, Main):
        self.menuFile_OpenProject.setText(QCoreApplication.translate("Main", u"&Open Project...", None))
#if QT_CONFIG(statustip)
        self.menuFile_OpenProject.setStatusTip(QCoreApplication.translate("Main", u"Open an existing project.", None))
#endif // QT_CONFIG(statustip)
        self.menuFile_Exit.setText(QCoreApplication.translate("Main", u"E&xit", None))
#if QT_CONFIG(statustip)
        self.menuFile_Exit.setStatusTip(QCoreApplication.translate("Main", u"Exit the application.", None))
#endif // QT_CONFIG(statustip)
        self.menuHelp_About.setText(QCoreApplication.translate("Main", u"&About...", None))
#if QT_CONFIG(statustip)
        self.menuHelp_About.setStatusTip(QCoreApplication.translate("Main", u"About this application.", None))
#endif // QT_CONFIG(statustip)
        self.menuFile_NewProject.setText(QCoreApplication.translate("Main", u"&New Project...", None))
#if QT_CONFIG(statustip)
        self.menuFile_NewProject.setStatusTip(QCoreApplication.translate("Main", u"Create a new project.", None))
#endif // QT_CONFIG(statustip)
        self.menuFile_SaveProject.setText(QCoreApplication.translate("Main", u"&Save Project", None))
#if QT_CONFIG(statustip)
        self.menuFile_SaveProject.setStatusTip(QCoreApplication.translate("Main", u"Save the current project.", None))
#endif // QT_CONFIG(statustip)
        self.menuFile_SaveProjectAs.setText(QCoreApplication.translate("Main", u"Save Project &As...", None))
#if QT_CONFIG(statustip)
        self.menuFile_SaveProjectAs.setStatusTip(QCoreApplication.translate("Main", u"Save the current project under a new name.", None))
#endif // QT_CONFIG(statustip)
        self.menuFile_CloseProject.setText(QCoreApplication.translate("Main", u"&Close Project", None))
#if QT_CONFIG(statustip)
        self.menuFile_CloseProject.setStatusTip(QCoreApplication.translate("Main", u"Close the current project.", None))
#endif // QT_CONFIG(statustip)
        self.menuFile_ExportAll.setText(QCoreApplication.translate("Main", u"E&xport All...", None))
        self.menuEdit_DetectQuadrat.setText(QCoreApplication.translate("Main", u"Detect &quadrat", None))
        self.menuWindow_ShowThumbnailsPanel.setText(QCoreApplication.translate("Main", u"Thumbnails panel", None))
        self.menuWindow_ShowEditorPanel.setText(QCoreApplication.translate("Main", u"Editor panel", None))
        self.menuFile_ProjectSettings.setText(QCoreApplication.translate("Main", u"Project Se&ttings...", None))
        self.menuFile.setTitle(QCoreApplication.translate("Main", u"&File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("Main", u"&Help", None))
        self.menuEdit.setTitle(QCoreApplication.translate("Main", u"&Edit", None))
        self.menuWindow.setTitle(QCoreApplication.translate("Main", u"&Window", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("Main", u"toolBar", None))
        pass
    # retranslateUi

