from PySide6.QtGui import QIcon


class GuiIcons:
    """GUI icons used in the application."""
    ProjectNew = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
    ProjectOpen = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
    ProjectSave = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
    ProjectSaveAs = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))

    HelpAbout = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))

    ApplicationExit = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit))

    AddPhotos = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.InsertImage))
