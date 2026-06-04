"""Tests for PhotoEditorWidget annotation state machine, tool switching, and persistence."""
from __future__ import annotations

from pathlib import Path

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication

from preprocessor.core.model import PhotoData, ProjectData
from preprocessor.gui.model import QPhotoModel, QProjectModel
from preprocessor.gui.photo_editor_widget import PhotoEditorWidget, Tool
from pytestqt.qtbot import QtBot


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def ensure_qapp(qapp: QApplication) -> QApplication:
    return qapp


def _make_photo(path: str = "/nonexistent/photo.jpg") -> QPhotoModel:
    """Minimal QPhotoModel with no real image file on disk."""
    return QPhotoModel(PhotoData(image_id="test_img", original_filename=Path(path)))


def _make_project() -> QProjectModel:
    return QProjectModel(ProjectData())


@pytest.fixture
def widget(qtbot: QtBot) -> PhotoEditorWidget:
    """Bare widget with no photo loaded (800x600)."""
    w = PhotoEditorWidget()
    qtbot.addWidget(w)
    w.resize(800, 600)
    return w


@pytest.fixture
def widget_with_photo(qtbot: QtBot) -> tuple[PhotoEditorWidget, QPhotoModel]:
    """Widget loaded with a minimal photo (null pixmap, no real image).

    Because the image file does not exist the pixmap is null and
    _original_img is None, so no async undistort job is started.
    With a null pixmap, _current_pixmap_info returns ratio=1.0 and
    offset=(0,0), meaning image coordinates == widget coordinates.
    """
    w = PhotoEditorWidget()
    qtbot.addWidget(w)
    w.resize(800, 600)
    photo = _make_photo()
    w.show_photo(photo, _make_project())
    return w, photo


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _press_left(widget: PhotoEditorWidget, x: int, y: int) -> None:
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtCore import QPointF

    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mousePressEvent(event)


def _press_right(widget: PhotoEditorWidget, x: int, y: int) -> None:
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtCore import QPointF

    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.RightButton,
        Qt.MouseButton.RightButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mousePressEvent(event)


def _move(widget: PhotoEditorWidget, x: int, y: int) -> None:
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtCore import QPointF

    event = QMouseEvent(
        QMouseEvent.Type.MouseMove,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mouseMoveEvent(event)


def _release_left(widget: PhotoEditorWidget, x: int, y: int) -> None:
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtCore import QPointF

    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mouseReleaseEvent(event)


# ---------------------------------------------------------------------------
# Bare widget (no photo) tests
# ---------------------------------------------------------------------------


class TestWidgetNoPhoto:
    def test_initial_tool_is_move(self, widget: PhotoEditorWidget) -> None:
        assert widget._current_tool == Tool.Move

    def test_widget_points_empty_without_photo(self, widget: PhotoEditorWidget) -> None:
        assert widget._widget_points(Tool.DrawQuadrat) == []
        assert widget._widget_points(Tool.Ruler) == []

    def test_find_handle_index_returns_none_without_photo(self, widget: PhotoEditorWidget) -> None:
        assert widget._find_handle_index(QPoint(100, 100), Tool.DrawQuadrat) is None
        assert widget._find_handle_index(QPoint(100, 100), Tool.Ruler) is None

    def test_tool_drag_index_returns_none_initially(self, widget: PhotoEditorWidget) -> None:
        assert widget._tool_drag_index(Tool.DrawQuadrat) is None
        assert widget._tool_drag_index(Tool.Ruler) is None

    def test_annotation_cursor_not_visible_without_mouse(self, widget: PhotoEditorWidget) -> None:
        widget._mouse_position = None
        assert not widget._is_annotation_cursor_visible(Tool.DrawQuadrat)
        assert not widget._is_annotation_cursor_visible(Tool.Ruler)

    def test_commit_tool_edits_noop_without_active_edit(self, widget: PhotoEditorWidget) -> None:
        """_commit_tool_edits is a no-op when no active edit is in progress."""
        widget._commit_tool_edits(Tool.DrawQuadrat)
        widget._commit_tool_edits(Tool.Ruler)
        assert widget._edit_points is None
        assert widget._edit_tool is None

    def test_tool_max_points(self, widget: PhotoEditorWidget) -> None:
        assert widget._tool_max_points(Tool.DrawQuadrat) == 4
        assert widget._tool_max_points(Tool.Ruler) == 2
        assert widget._tool_max_points(Tool.Move) == 0


# ---------------------------------------------------------------------------
# Widget point helpers with photo
# ---------------------------------------------------------------------------


class TestWidgetPoints:
    def test_returns_empty_when_no_corners_set(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        assert photo.quadrat_corners is None
        assert w._widget_points(Tool.DrawQuadrat) == []

    def test_returns_corners_from_model(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        # Set two corners — with null pixmap, image coords == widget coords.
        photo.quadrat_corners = [(10.0, 20.0), (200.0, 300.0)]
        pts = w._widget_points(Tool.DrawQuadrat)
        assert len(pts) == 2
        assert pts[0] == QPoint(10, 20)
        assert pts[1] == QPoint(200, 300)

    def test_returns_edit_buffer_when_editing_quadrat(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(10.0, 10.0)]
        # Manually push an edit buffer for DrawQuadrat.
        w._edit_tool = Tool.DrawQuadrat
        w._edit_points = [QPoint(50, 60)]
        pts = w._widget_points(Tool.DrawQuadrat)
        assert pts == [QPoint(50, 60)]

    def test_edit_buffer_not_used_for_different_tool(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(10.0, 10.0)]
        # Buffer owned by Ruler, not DrawQuadrat.
        w._edit_tool = Tool.Ruler
        w._edit_points = [QPoint(99, 99)]
        pts = w._widget_points(Tool.DrawQuadrat)
        # Should still return model data, not the ruler buffer.
        assert len(pts) == 1
        assert pts[0] == QPoint(10, 10)

    def test_returns_ruler_points_from_model(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(50.0, 60.0), (150.0, 160.0)]
        pts = w._widget_points(Tool.Ruler)
        assert len(pts) == 2
        assert pts[0] == QPoint(50, 60)
        assert pts[1] == QPoint(150, 160)

    def test_returns_ruler_edit_buffer_when_editing_ruler(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(50.0, 60.0)]
        w._edit_tool = Tool.Ruler
        w._edit_points = [QPoint(5, 6), QPoint(7, 8)]
        pts = w._widget_points(Tool.Ruler)
        assert pts == [QPoint(5, 6), QPoint(7, 8)]


# ---------------------------------------------------------------------------
# Hit-testing
# ---------------------------------------------------------------------------


class TestFindHandleIndex:
    def test_hit_within_radius(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 200.0)]
        r = w._handle_radius  # 8
        # Exactly on the point.
        assert w._find_handle_index(QPoint(100, 200), Tool.DrawQuadrat) == 0
        # On the edge of the radius (distance == r).
        assert w._find_handle_index(QPoint(100 + r, 200), Tool.DrawQuadrat) == 0

    def test_miss_outside_radius(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 200.0)]
        r = w._handle_radius
        # One pixel outside radius.
        assert w._find_handle_index(QPoint(100 + r + 1, 200), Tool.DrawQuadrat) is None

    def test_returns_first_hit_when_multiple_handles(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0), (200.0, 200.0)]
        assert w._find_handle_index(QPoint(200, 200), Tool.DrawQuadrat) == 1

    def test_ruler_hit(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(50.0, 50.0), (300.0, 300.0)]
        assert w._find_handle_index(QPoint(50, 50), Tool.Ruler) == 0
        assert w._find_handle_index(QPoint(300, 300), Tool.Ruler) == 1
        assert w._find_handle_index(QPoint(1, 1), Tool.Ruler) is None


# ---------------------------------------------------------------------------
# Cursor visibility
# ---------------------------------------------------------------------------


class TestAnnotationCursorVisibility:
    def test_not_visible_when_mouse_position_none(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0)]
        w._mouse_position = None
        assert not w._is_annotation_cursor_visible(Tool.DrawQuadrat)

    def test_not_visible_when_not_over_handle(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0)]
        w._mouse_position = QPoint(400, 400)
        assert not w._is_annotation_cursor_visible(Tool.DrawQuadrat)

    def test_visible_when_over_handle(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0)]
        w._mouse_position = QPoint(100, 100)
        assert w._is_annotation_cursor_visible(Tool.DrawQuadrat)

    def test_visible_for_ruler_handle(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(200.0, 200.0)]
        w._mouse_position = QPoint(200, 200)
        assert w._is_annotation_cursor_visible(Tool.Ruler)


# ---------------------------------------------------------------------------
# Tool switching
# ---------------------------------------------------------------------------


class TestToolSwitching:
    def test_set_tool_commits_in_progress_quadrat_edit(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.DrawQuadrat)
        # Manually inject an in-progress edit (two points).
        w._edit_tool = Tool.DrawQuadrat
        w._edit_points = [QPoint(10, 10), QPoint(200, 200)]

        # Switch away — should commit.
        w.set_tool(Tool.Ruler)

        assert w._edit_tool is None
        assert w._edit_points is None
        assert photo.quadrat_corners is not None
        assert len(photo.quadrat_corners) == 2

    def test_set_tool_commits_in_progress_ruler_edit(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.Ruler)
        w._edit_tool = Tool.Ruler
        w._edit_points = [QPoint(30, 40), QPoint(300, 400)]

        w.set_tool(Tool.DrawQuadrat)

        assert w._edit_tool is None
        assert w._edit_points is None
        assert len(photo.ruler_points) == 2

    def test_set_tool_does_not_commit_other_tools_edit(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        # Ruler edit active, switch to Ruler itself — quadrat should not be committed.
        w._edit_tool = Tool.Ruler
        w._edit_points = [QPoint(1, 2)]
        w.set_tool(Tool.Ruler)
        # Still has edit buffer (wasn't cleared by switching to same tool).
        assert w._edit_tool == Tool.Ruler


# ---------------------------------------------------------------------------
# DrawQuadrat: annotation state machine via mouse events
# ---------------------------------------------------------------------------


class TestDrawQuadratMouseEvents:
    def test_left_press_adds_new_point(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.DrawQuadrat)
        _press_left(w, 100, 150)
        assert w._edit_points is not None
        assert len(w._edit_points) == 1
        assert w._edit_points[0] == QPoint(100, 150)
        assert w._drag_index == 0

    def test_left_press_starts_drag_on_existing_handle(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0)]
        w.set_tool(Tool.DrawQuadrat)
        _press_left(w, 100, 100)
        assert w._drag_index == 0

    def test_left_press_stops_at_max_four_points(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.DrawQuadrat)
        for i in range(6):
            # Click somewhere well away from existing handles.
            _press_left(w, 50 + i * 100, 50 + i * 10)
            _release_left(w, 50 + i * 100, 50 + i * 10)

        assert photo.quadrat_corners is not None
        assert len(photo.quadrat_corners) == 4

    def test_drag_moves_edit_point(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.DrawQuadrat)
        _press_left(w, 100, 100)
        _move(w, 150, 200)
        assert w._edit_points is not None
        assert w._edit_points[0] == QPoint(150, 200)
        # Model not yet updated while dragging.
        assert photo.quadrat_corners is None

    def test_release_commits_edit_to_model(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.DrawQuadrat)
        _press_left(w, 100, 100)
        _move(w, 150, 200)
        _release_left(w, 150, 200)
        # Edit buffer should be cleared.
        assert w._edit_points is None
        assert w._edit_tool is None
        # Model should have the committed corner.
        assert photo.quadrat_corners is not None
        assert len(photo.quadrat_corners) == 1
        assert photo.quadrat_corners[0] == pytest.approx((150.0, 200.0))

    def test_right_press_removes_point(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0), (300.0, 300.0)]
        w.set_tool(Tool.DrawQuadrat)
        _press_right(w, 100, 100)
        # Only the second point should remain.
        assert photo.quadrat_corners is not None
        assert len(photo.quadrat_corners) == 1

    def test_right_press_clears_corners_when_last_point_removed(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0)]
        w.set_tool(Tool.DrawQuadrat)
        _press_right(w, 100, 100)
        assert photo.quadrat_corners is None

    def test_right_press_on_empty_area_does_nothing(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(100.0, 100.0)]
        w.set_tool(Tool.DrawQuadrat)
        _press_right(w, 400, 400)
        assert photo.quadrat_corners == [(100.0, 100.0)]

    def test_release_not_on_left_button_does_not_commit_ruler_but_does_commit_quadrat(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        """DrawQuadrat commits on any release (not only left button), per mouseReleaseEvent logic."""
        from PySide6.QtGui import QMouseEvent
        from PySide6.QtCore import QPointF

        w, photo = widget_with_photo
        w.set_tool(Tool.DrawQuadrat)
        _press_left(w, 50, 50)

        # Simulate a right-button release (unusual but should still commit for DrawQuadrat).
        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPointF(50, 50),
            QPointF(50, 50),
            Qt.MouseButton.RightButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier,
        )
        w.mouseReleaseEvent(event)

        assert w._edit_points is None
        assert photo.quadrat_corners is not None


# ---------------------------------------------------------------------------
# Ruler: annotation state machine
# ---------------------------------------------------------------------------


class TestRulerMouseEvents:
    def test_left_press_adds_ruler_point(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.Ruler)
        _press_left(w, 200, 300)
        assert w._edit_points is not None
        assert len(w._edit_points) == 1

    def test_release_commits_ruler_to_model(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.Ruler)
        _press_left(w, 200, 300)
        _release_left(w, 200, 300)
        assert w._edit_points is None
        pts = photo.ruler_points
        assert len(pts) == 1
        assert pts[0] == pytest.approx((200.0, 300.0))

    def test_left_press_adds_second_ruler_point(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.Ruler)
        _press_left(w, 10, 10)
        _release_left(w, 10, 10)
        _press_left(w, 500, 400)
        _release_left(w, 500, 400)
        pts = photo.ruler_points
        assert len(pts) == 2

    def test_ruler_max_two_points(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w.set_tool(Tool.Ruler)
        for x in [10, 200, 400]:
            _press_left(w, x, x)
            _release_left(w, x, x)
        # Third click should be ignored (max=2).
        assert len(photo.ruler_points) == 2

    def test_right_press_removes_ruler_point(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(50.0, 50.0), (400.0, 400.0)]
        w.set_tool(Tool.Ruler)
        _press_right(w, 50, 50)
        assert len(photo.ruler_points) == 1

    def test_right_press_clears_ruler_when_last_point_removed(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(50.0, 50.0)]
        w.set_tool(Tool.Ruler)
        _press_right(w, 50, 50)
        assert photo.ruler_points == []

    def test_ruler_drag_moves_endpoint(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(50.0, 50.0), (400.0, 400.0)]
        w.set_tool(Tool.Ruler)
        _press_left(w, 50, 50)   # Hit the first handle.
        _move(w, 100, 120)
        assert w._edit_points is not None
        assert w._edit_points[0] == QPoint(100, 120)

    def test_ruler_drag_release_commits_to_model(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(50.0, 50.0), (400.0, 400.0)]
        w.set_tool(Tool.Ruler)
        _press_left(w, 50, 50)
        _move(w, 100, 120)
        _release_left(w, 100, 120)
        assert w._edit_points is None
        pts = photo.ruler_points
        assert pts[0] == pytest.approx((100.0, 120.0))


# ---------------------------------------------------------------------------
# Order-by-angle (quadrat ordering)
# ---------------------------------------------------------------------------


class TestOrderPointsByAngle:
    def test_four_points_yield_simple_polygon(self) -> None:
        # Place 4 corners of a 100x100 square in a scrambled order.
        pts = [QPoint(100, 0), QPoint(0, 100), QPoint(100, 100), QPoint(0, 0)]
        result = PhotoEditorWidget._order_points_by_angle(pts)
        assert len(result) == 4
        # Adjacent pairs should not cross (verify by checking angle is monotone).
        import math

        cx = sum(p.x() for p in result) / 4
        cy = sum(p.y() for p in result) / 4
        angles = [math.atan2(p.y() - cy, p.x() - cx) for p in result]
        # Angles should be strictly increasing (CCW).
        for i in range(len(angles) - 1):
            assert angles[i] < angles[i + 1]

    def test_empty_list_returns_empty(self) -> None:
        assert PhotoEditorWidget._order_points_by_angle([]) == []

    def test_single_point_returns_same(self) -> None:
        pts = [QPoint(5, 5)]
        assert PhotoEditorWidget._order_points_by_angle(pts) == pts


# ---------------------------------------------------------------------------
# Write helpers: round-trip image <-> model
# ---------------------------------------------------------------------------


class TestWriteHelpers:
    def test_write_widget_points_stores_image_coords(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        # With null pixmap, ratio=1.0 and offset=(0,0) → image coord == widget coord.
        w._write_widget_points([QPoint(10, 20), QPoint(200, 300)])
        assert photo.quadrat_corners is not None
        assert photo.quadrat_corners[0] == pytest.approx((10.0, 20.0))
        assert photo.quadrat_corners[1] == pytest.approx((200.0, 300.0))

    def test_write_widget_points_none_clears_corners(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.quadrat_corners = [(1.0, 2.0)]
        w._write_widget_points(None)
        assert photo.quadrat_corners is None

    def test_write_ruler_widget_points_stores_image_coords(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        w._write_ruler_widget_points([QPoint(100, 200), QPoint(300, 400)])
        pts = photo.ruler_points
        assert pts[0] == pytest.approx((100.0, 200.0))
        assert pts[1] == pytest.approx((300.0, 400.0))

    def test_write_ruler_widget_points_none_clears_ruler(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, photo = widget_with_photo
        photo.ruler_points = [(1.0, 2.0)]
        w._write_ruler_widget_points(None)
        assert photo.ruler_points == []


# ---------------------------------------------------------------------------
# show_photo clears state
# ---------------------------------------------------------------------------


class TestShowPhoto:
    def test_show_photo_none_clears_state(self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]) -> None:
        w, photo = widget_with_photo
        # Inject some state.
        w._edit_tool = Tool.DrawQuadrat
        w._edit_points = [QPoint(1, 2)]
        w._drag_index = 0

        w.show_photo(None, _make_project())

        assert w._photo is None
        assert w._pixmap is None
        assert w._edit_points is None
        assert w._edit_tool is None
        assert w._drag_index is None

    def test_show_photo_sets_photo_model(self, widget: PhotoEditorWidget) -> None:
        photo = _make_photo()
        w = widget
        w.show_photo(photo, _make_project())
        assert w._photo is photo

    def test_show_photo_replaces_previous_photo(
        self, widget_with_photo: tuple[PhotoEditorWidget, QPhotoModel]
    ) -> None:
        w, _old_photo = widget_with_photo
        new_photo = _make_photo("/nonexistent/other.jpg")
        w.show_photo(new_photo, _make_project())
        assert w._photo is new_photo

