from pytestqt.qtbot import QWidget


class _FakeMsgBox:
    """Minimal fake QMessageBox used to control the clicked button in tests."""

    class _Btn:
        def __init__(self, text: str, role: object) -> None:
            self.text = text

        def __repr__(self) -> str:  # pragma: no cover - helper
            return f"Btn({self.text!r})"

    next_clicked_text: str | None = None
    _buttons: list[tuple[str, _Btn]]

    class Icon:
        Warning = object()

    class ButtonRole:
        AcceptRole = object()
        DestructiveRole = object()
        RejectRole = object()

    def __init__(self, parent: QWidget | None = None) -> None:
        self._buttons = []

    def setIcon(self, *args: object, **kwargs: object) -> None:
        return None

    def setWindowTitle(self, *args: object, **kwargs: object) -> None:
        return None

    def setText(self, *args: object, **kwargs: object) -> None:
        return None

    def addButton(self, text: str, role: object) -> _Btn:
        btn = _FakeMsgBox._Btn(text, role)
        self._buttons.append((text, btn))
        return btn

    def exec(self) -> None:
        return None

    def clickedButton(self) -> _Btn | None:
        for text, btn in self._buttons:
            if text == _FakeMsgBox.next_clicked_text:
                return btn
        return None

    @staticmethod
    def critical(parent: object, title: object, msg: object) -> None:
        # emulate QMessageBox.critical (no-op for tests)
        return None
