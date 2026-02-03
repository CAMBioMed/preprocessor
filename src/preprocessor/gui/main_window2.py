from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCloseEvent, QKeySequence, QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox, QListWidget, QListWidgetItem
from pathlib import Path

from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.image_editor import QImageEditor
from preprocessor.gui.photo_editor_widget import PhotoEditorWidget
from preprocessor.gui.properties_dock_widget import PropertiesDockWidget
from preprocessor.gui.thumbnail_dock_widget import ThumbnailDockWidget
from preprocessor.gui.ui_main import Ui_Main
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.project_model import ProjectModel


class MainWindow2(QMainWindow):
    ui: Ui_Main
    model: ApplicationModel

    properties_dock: PropertiesDockWidget
    """The dock widget showing properties."""
    thumbnail_dock: ThumbnailDockWidget
    """The dock widget showing image thumbnails."""
    central_widget: PhotoEditorWidget
    """The central widget showing the image."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self._setup_icons()
        self._setup_keyboard_shortcuts()
        self._create_thumbnail_dock()
        self._create_photo_editor()

        self.model = ApplicationModel()
        self._connect_signals()

        self.read_settings()
        self._update_project_actions()
        self._bound_project: ProjectModel | None = None
        self._bind_project_signals(self.model.current_project)
        self._update_window_title()

    def _update_project_actions(self) -> None:
        """Enable or disable file actions depending on whether a project is open."""
        has_project = self.model.current_project is not None
        self.ui.menuFile_SaveProject.setEnabled(has_project)
        self.ui.menuFile_SaveProjectAs.setEnabled(has_project)
        self.ui.menuFile_CloseProject.setEnabled(has_project)
        self.thumbnail_dock.ui.addPhotoAction.setEnabled(has_project)
        self.thumbnail_dock.ui.removePhotoAction.setEnabled(has_project)

    def _bind_project_signals(self, project: ProjectModel | None) -> None:
        """Connect/disconnect signals for the currently bound project."""
        # Disconnect previous project
        old_project = self._bound_project
        if old_project is not None:
            old_project.on_file_path_changed.disconnect(self._on_project_file_path_changed)
            old_project.on_dirty_changed.disconnect(self._handle_dirty_changed)
            old_project.photos.on_changed.disconnect(self._handle_photos_changed)

        self._bound_project = project
        # Connect new project
        if project is not None:
            project.on_file_path_changed.connect(self._on_project_file_path_changed)
            project.on_dirty_changed.connect(self._handle_dirty_changed)
            project.photos.on_changed.connect(self._handle_photos_changed)

    def _on_project_file_path_changed(self, _path: Path | None) -> None:
        """Called when the project's file_path changes."""
        self._update_window_title()

    def _update_window_title(self) -> None:
        """Set the window title to include the current project's name, if any."""
        base_title = "Cambiomed Preprocessor"
        proj = self.model.current_project
        if proj is None:
            self.setWindowTitle(base_title)
            return
        fp = proj.file_path
        if fp:
            name = Path(fp).name
        else:
            name = "Untitled Project"
        photo_count = len(proj.photos)
        dirty_marker = "*" if proj.dirty else ""
        self.setWindowTitle(f"{base_title} — {name} ({photo_count} photos){dirty_marker}")

    def _setup_icons(self) -> None:
        """Set up icons for actions."""
        # File menu
        self.ui.menuFile_NewProject.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew)))
        self.ui.menuFile_OpenProject.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)))
        self.ui.menuFile_OpenProject.setIcon(QIcon(QIcon("src/preprocessor/icons/fugue16/folder-open-image.png")))
        self.ui.menuFile_SaveProject.setIcon(QIcon(QIcon("src/preprocessor/icons/fugue16/disk-black.png")))
        self.ui.menuFile_SaveProjectAs.setIcon(QIcon(QIcon("src/preprocessor/icons/fugue16/disks-black.png")))
        self.ui.menuFile_Exit.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit)))

        # Help menu
        self.ui.menuHelp_About.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout)))

    def _setup_keyboard_shortcuts(self) -> None:
        """
        Set up keyboard shortcuts for actions.

        As Qt Creator/Designer does not support setting StandardKey shortcuts,
        we do it manually here. See:
        https://forum.qt.io/topic/6259/qt-designer-does-not-support-qkeysequence-standardkey
        """
        # File menu
        self.ui.menuFile_NewProject.setShortcut(QKeySequence.StandardKey.New)
        self.ui.menuFile_OpenProject.setShortcut(QKeySequence.StandardKey.Open)
        self.ui.menuFile_SaveProject.setShortcut(QKeySequence.StandardKey.Save)
        self.ui.menuFile_SaveProjectAs.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.ui.menuFile_Exit.setShortcut(QKeySequence.StandardKey.Quit)

        # Help menu
        self.ui.menuHelp_About.setShortcut(QKeySequence.StandardKey.HelpContents)

    def _create_thumbnail_dock(self) -> None:
        """Create the thumbnail list dock widget."""
        self.thumbnail_dock = ThumbnailDockWidget(self)
        self.thumbnail_dock.setAllowedAreas(
            Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.thumbnail_dock)

    def _create_photo_editor(self) -> None:
        """Create the central photo editor widget."""
        self.central_widget = PhotoEditorWidget(self)
        self.setCentralWidget(self.central_widget)

    def _connect_signals(self) -> None:
        """Connect signals to slots."""
        # File menu
        self.ui.menuFile_NewProject.triggered.connect(self.on_new_project)
        self.ui.menuFile_OpenProject.triggered.connect(self.on_open_project)
        self.ui.menuFile_SaveProject.triggered.connect(self.on_save_project)
        self.ui.menuFile_SaveProjectAs.triggered.connect(self.on_save_project_as)
        self.ui.menuFile_CloseProject.triggered.connect(self.on_close_project)
        self.ui.menuFile_Exit.triggered.connect(self.close)

        # Help menu
        self.ui.menuHelp_About.triggered.connect(self.on_help_about)

        # When a thumbnail is selected, either show stored result or schedule processing
        self.thumbnail_dock.on_add_photos_action.connect(self._handle_add_photos_action)
        self.thumbnail_dock.on_remove_photos_action.connect(self._handle_remove_photos_action)
        self.thumbnail_dock.on_selection_changed.connect(self._handle_photo_selection_changed)

    def on_new_project(self) -> None:
        new_project = ProjectModel()
        self.model.current_project = new_project
        self._bind_project_signals(new_project)
        self._update_project_actions()
        self._update_window_title()

    def on_open_project(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Project Files (*.pbproj);;All Files (*)")
        if not path:
            return
        if self.model.current_project is not None:
            # TODO: On unsaved changes, maybe the user doesn't want to open another project
            #  Thus cancel
            self.on_close_project()
        new_project = ProjectModel()
        self.model.current_project = new_project
        self.model.current_project.file_path = Path(path)
        self._bind_project_signals(new_project)
        try:
            new_project.load_from_file(path)
        except ValueError as exc:
            # Likely a serialization version mismatch or corrupt file — inform the user
            QMessageBox.critical(
                self,
                "Open Project Failed",
                f"Failed to open project file:\n{path}\n\n{exc}",
            )
            return
        self._update_project_actions()
        self._update_window_title()

    def on_save_project(self) -> None:
        if self.model.current_project is None:
            return
        if self.model.current_project.file_path is None:
            self.on_save_project_as()
            return
        self.model.current_project.save_to_file(self.model.current_project.file_path)

    def on_save_project_as(self) -> None:
        if self.model.current_project is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Project As", "", "Project Files (*.pbproj);;All Files (*)")
        if not path:
            return
        self.model.current_project.save_to_file(path)
        self.model.current_project.file_path = Path(path)

    def on_close_project(self) -> None:
        if self.model.current_project is not None and self.model.current_project.dirty:
            result = QMessageBox.question(
                self,
                "Unsaved Changes",
                "The current project has unsaved changes. Do you want to save them before closing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            )
            if result == QMessageBox.StandardButton.Yes:
                self.on_save_project()
            elif result == QMessageBox.StandardButton.Cancel:
                return
        self.model.current_project = None
        self._bind_project_signals(None)
        self._update_project_actions()
        self._update_window_title()

    def on_help_about(self) -> None:
        show_about_dialog(self)

    def _handle_add_photos_action(self) -> None:
        assert self.model.current_project is not None
        paths, _ = QFileDialog.getOpenFileNames(self, "Add Photo", "", "Photos (*.jpg;*.jpeg);;All Files (*)")
        if not paths:
            return
        project = self.model.current_project
        for path in paths:
            model = PhotoModel()
            model.original_filename = path
            project.photos.append(model)

    def _handle_remove_photos_action(self, selected: list[PhotoModel]) -> None:
        assert self.model.current_project is not None
        for photo in selected:
            self.model.current_project.photos.remove(photo)

    def _handle_dirty_changed(self) -> None:
        """Called when the current project's dirty state changes."""
        self._update_window_title()

    def _handle_photos_changed(self, added: list[PhotoModel], removed: list[PhotoModel]) -> None:
        """Called when the current project's photos change."""
        if self.model.current_project is None:
            return
        self._update_window_title()
        self.thumbnail_dock.update_thumbnails(self.model.current_project.photos)

    def _handle_photo_selection_changed(self, photo: PhotoModel) -> None:
        """Called when the selected photo changes."""
        self.central_widget.show_photo(photo)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.write_settings()
        super().closeEvent(event)
        event.accept()

    def write_settings(self) -> None:
        """Write window settings to persistent storage."""
        self.model.main_window_geometry = self.saveGeometry()
        self.model.main_window_state = self.saveState()
        self.model.write_settings()

    def read_settings(self) -> None:
        """Read window settings from persistent storage."""
        self.model.read_settings()
        self.restoreGeometry(self.model.main_window_geometry)
        self.restoreState(self.model.main_window_state)
