import pytest
from typing import Generator, Any

import preprocessor.gui.main_window as main_window_mod
from preprocessor.gui.progress_dialog import ProgressDialog as OrigProgressDialog
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture
def auto_close_progress_dialog(monkeypatch: MonkeyPatch) -> Generator[None, Any, None]:
    """Monkeypatch MainWindow's ProgressDialog to a test variant that auto-closes.

    This fixture forces jobs to run on the Qt event loop (run_in_thread=False)
    and sets auto_close_on_finish=True so modal dialogs don't block tests.
    """

    class TestProgressDialog(OrigProgressDialog):
        def __init__(self, title: str, jobs: set, parent=None, run_in_thread: bool = True) -> None:
            # Force deterministic execution on the Qt event loop and auto-close
            super().__init__(title, jobs, parent=parent, run_in_thread=False, auto_close_on_finish=True)

    monkeypatch.setattr(main_window_mod, "ProgressDialog", TestProgressDialog)
    yield
