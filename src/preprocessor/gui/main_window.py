import warnings

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QKeySequence, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox, QDialog
from pathlib import Path

from preprocessor import app_formal_name
from preprocessor.gui.about_dialog import show_about_dialog
from preprocessor.gui.editor_dock_widget import EditorDockWidget
from preprocessor.gui.export_dialog import ExportDialog
from preprocessor.gui.launch_dialog import (
    new_project_dialog,
    open_project_dialog,
    save_project_dialog,
    save_project_as_dialog,
)
from preprocessor.gui.photo_editor_widget import PhotoEditorWidget
from preprocessor.gui.properties_dock_widget import PropertiesDockWidget
from preprocessor.gui.thumbnail_dock_widget import ThumbnailDockWidget
from preprocessor.gui.ui_main import Ui_Main
from preprocessor.gui.utils import icon_from_resource
from preprocessor.model.application_model import ApplicationModel
from preprocessor.model.photo_model import PhotoModel
from preprocessor.model.project_model import ProjectModel
from preprocessor.processing.detect_quadrat import detect_quadrat
from preprocessor.processing.load_image import load_image
from preprocessor.processing.params import defaultParams


class MainWindow(QMainWindow):
    ui: Ui_Main
    model: ApplicationModel

    properties_dock: PropertiesDockWidget
    """The dock widget showing properties."""
    thumbnail_dock: ThumbnailDockWidget
    """The dock widget showing image thumbnails."""
    editor_dock: EditorDockWidget
    """The dock widget with edit controls."""
    central_widget: PhotoEditorWidget
    """The central widget showing the image."""
    _bound_project: ProjectModel | None = None

    def __init__(self, model: ApplicationModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.setWindowTitle(app_formal_name)
        self._setup_icons()
        self._setup_keyboard_shortcuts()
        self._create_thumbnail_dock()
        self._create_editor_dock()
        self._create_photo_editor()

        self.model = model
        self._connect_signals()

        self.read_settings()
        self._handle_current_project_changed(self.model.current_project)

    def _update_project_actions(self) -> None:
        """Enable or disable file actions depending on whether a project is open."""
        has_project = self.model.current_project is not None
        self.ui.menuFile_SaveProject.setEnabled(has_project)
        self.ui.menuFile_SaveProjectAs.setEnabled(has_project)
        self.ui.menuFile_ExportAll.setEnabled(has_project)
        self.thumbnail_dock.ui.addPhotoAction.setEnabled(has_project)
        self.thumbnail_dock.ui.removePhotoAction.setEnabled(has_project)

    def _bind_project_signals(self, project: ProjectModel) -> None:
        """Connect/disconnect signals for the currently bound project."""
        # Disconnect previous project
        old_project = self._bound_project
        if old_project is not None:
            with warnings.catch_warnings():
                # Raises a RuntimeWarning when the old project was never connected (i.e. the initial empty project)
                warnings.filterwarnings("ignore", category=RuntimeWarning)
                old_project.on_file_changed.disconnect(self._handle_project_file_changed)
                old_project.on_dirty_changed.disconnect(self._handle_dirty_changed)
                old_project.photos.on_changed.disconnect(self._handle_photos_changed)

        self._bound_project = project
        # Connect new project
        if project is not None:
            project.on_file_changed.connect(self._handle_project_file_changed)
            project.on_dirty_changed.connect(self._handle_dirty_changed)
            project.photos.on_changed.connect(self._handle_photos_changed)

    def _handle_project_file_changed(self, _path: Path | None) -> None:
        """Handle when the project's file changes."""
        self._update_window_title()

    def _update_window_title(self) -> None:
        """Set the window title to include the current project's name, if any."""
        base_title = "Cambiomed Preprocessor"
        proj = self.model.current_project
        if proj is None:
            self.setWindowTitle(base_title)
            return
        fp = proj.file
        name = Path(fp).name if fp else "Untitled Project"
        photo_count = len(proj.photos)
        dirty_marker = "*" if proj.dirty else ""
        project_title = f"{name} ({photo_count} photos){dirty_marker}"
        photo_title = f"{self.model.current_photo.name}" if self.model.current_photo else "<none>"
        self.setWindowTitle(f"{base_title} — {project_title} {photo_title}")

    def _update_thumbnails(self) -> None:
        if self.model.current_project is not None:
            self.thumbnail_dock.update_thumbnails(self.model.current_project.photos, self.model.current_project)

    def _setup_icons(self) -> None:
        """Set up icons for actions."""
        # File menu
        self.ui.menuFile_NewProject.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew)))
        self.ui.menuFile_OpenProject.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)))
        # prefer packaged resource icon if available
        self.ui.menuFile_OpenProject.setIcon(icon_from_resource("icons/fugue16/folder-open-image.png"))
        self.ui.menuFile_SaveProject.setIcon(icon_from_resource("icons/fugue16/disk-black.png"))
        self.ui.menuFile_SaveProjectAs.setIcon(icon_from_resource("icons/fugue16/disks-black.png"))
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

    def _create_editor_dock(self) -> None:
        """Create the editor dock widget."""
        self.editor_dock = EditorDockWidget(self)
        self.editor_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.editor_dock)

    def _create_photo_editor(self) -> None:
        """Create the central photo editor widget."""
        self.central_widget = PhotoEditorWidget(self)
        self.setCentralWidget(self.central_widget)

    def _connect_signals(self) -> None:
        """Connect signals to slots."""
        # File menu
        self.ui.menuFile_NewProject.triggered.connect(self._handle_new_project_action)
        self.ui.menuFile_OpenProject.triggered.connect(self._handle_open_project_action)
        self.ui.menuFile_SaveProject.triggered.connect(self._handle_save_project_action)
        self.ui.menuFile_SaveProjectAs.triggered.connect(self._handle_save_project_as_action)
        self.ui.menuFile_ExportAll.triggered.connect(self._handle_export_all_action)
        self.ui.menuFile_Exit.triggered.connect(self.close)

        # Edit menu
        self.ui.menuEdit_DetectQuadrat.triggered.connect(self._handle_detect_quadrat_action)

        # Window menu
        self.ui.menuWindow_ShowThumbnailsPanel.triggered.connect(lambda: self.thumbnail_dock.setVisible(True))
        self.ui.menuWindow_ShowEditorPanel.triggered.connect(lambda: self.editor_dock.setVisible(True))

        # Help menu
        self.ui.menuHelp_About.triggered.connect(self._handle_help_about_action)

        # Editor dock
        self.editor_dock.on_autodetect_quadrat_clicked.connect(self._handle_detect_quadrat_action)

        # Thumbnail dock
        self.thumbnail_dock.on_add_photos_action.connect(self._handle_add_photos_action)
        self.thumbnail_dock.on_remove_photos_action.connect(self._handle_remove_photos_action)
        self.thumbnail_dock.on_selection_changed.connect(self._handle_photo_selection_changed)

        # Model
        self.model.on_current_project_changed.connect(self._handle_current_project_changed)
        self.model.on_current_photo_changed.connect(self._handle_current_photo_changed)

    def _handle_new_project_action(self) -> None:
        new_project = new_project_dialog(self, self.model.current_project)
        if new_project is not None:
            self.model.current_project = new_project

    def _handle_open_project_action(self) -> None:
        new_project = open_project_dialog(self, self.model.current_project)
        if new_project is not None:
            self.model.current_project = new_project

    def _handle_save_project_action(self) -> None:
        save_project_dialog(self, self.model.current_project, self.model.current_project.file)

    def _handle_save_project_as_action(self) -> None:
        save_project_as_dialog(self, self.model.current_project)

    def _handle_export_all_action(self) -> None:
        dialog = ExportDialog(self.model.current_project, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass

    def _handle_detect_quadrat_action(self) -> None:
        if self.model.current_photo is None:
            return

        # Prefer using the undistorted image currently shown in the editor (if available)
        img = None
        try:
            img = self.central_widget.get_processing_image()
        except Exception:
            img = None
        if img is None:
            original_path = self.model.current_project.get_absolute_path(self.model.current_photo.original_filename)
            img = load_image(str(original_path))
        if img is None:
            QMessageBox.critical(
                self,
                "Load Image Failed",
                f"Failed to load image:\n{original_path}",
            )
            return

        params = defaultParams

        result = detect_quadrat(img, params)
        if result is None or result.corners is None:
            # No corners detected
            return

        self.model.current_photo.quadrat_corners = result.corners
        # Trigger updating the opened editor
        self._handle_current_photo_changed(self.model.current_photo)

    def _handle_help_about_action(self) -> None:
        show_about_dialog(self)

    def _handle_add_photos_action(self) -> None:
        assert self.model.current_project is not None
        paths, _ = QFileDialog.getOpenFileNames(self, "Add Photo", "", "Photos (*.jpg;*.jpeg);;All Files (*)")
        if not paths:
            return
        project = self.model.current_project
        for path in paths:
            project.append_photo_model(Path(path))

    def _handle_remove_photos_action(self, selected: list[PhotoModel]) -> None:
        assert self.model.current_project is not None
        for photo in selected:
            self.model.current_project.photos.remove(photo)

    def _handle_dirty_changed(self) -> None:
        """Handle when the current project's dirty state changes."""
        self._update_window_title()

    def _handle_photos_changed(self) -> None:
        """Handle when the current project's photos change."""
        self._update_window_title()
        self._update_thumbnails()

    def _handle_photo_selection_changed(self, selected: list[PhotoModel]) -> None:
        """Handle when the selected photo changes."""
        # TODO: Support multiple selection?
        self.model.current_photo = selected[0] if selected else None

    def _handle_current_project_changed(self, project: ProjectModel) -> None:
        """Handle when the current project changes."""
        self._bind_project_signals(project)
        self._update_project_actions()
        self._update_window_title()
        self._update_thumbnails()
        self._handle_current_photo_changed(self.model.current_photo)

    def _handle_current_photo_changed(self, photo: PhotoModel | None) -> None:
        """Handle when the current photo changes."""
        self.central_widget.show_photo(photo, self.model.current_project)
        self.editor_dock.update_with_photo(photo)
        self._update_window_title()

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
        self.restoreGeometry(self.model.main_window_geometry)
        self.restoreState(self.model.main_window_state)
