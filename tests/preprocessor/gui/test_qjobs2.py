from __future__ import annotations

from typing import List

import pytest
from PySide6.QtCore import QEventLoop
from PySide6.QtWidgets import QApplication

from preprocessor.core.jobs.jobs import Job, JobContext, JobState
from preprocessor.gui.jobs.qjobs2 import QJob, QJobProcessor


@pytest.fixture(autouse=True)
def ensure_qapp(qapp: QApplication) -> QApplication:
    # ensure a QApplication exists for tests that rely on it
    return qapp


class SimpleJob(Job[str]):
    def run(self, ctx: JobContext) -> str:
        # Emit three progress updates: 0.0, 0.5, 1.0
        ctx.update_progress(0.0)
        ctx.update_progress(0.5)
        ctx.update_progress(1.0)
        return "ok"


def test_qjobprocessor_runs_job_and_emits_signals() -> None:
    processor = QJobProcessor(run_in_thread=False)

    seen: List[str] = []

    def _on_start(job: QJob) -> None:
        seen.append("start")

    def _on_finished(job: QJob, state: JobState, result: str | Exception | None) -> None:
        seen.append(f"finished:{state}:{result}")

    processor.on_job_start.connect(_on_start)
    processor.on_job_finished.connect(_on_finished)

    job = SimpleJob()
    h = processor.submit(job)
    h.await_result(1.0)  # Wait for completion

    assert seen == ["start", "finished:JobState.COMPLETED:ok"]


def test_qjob_runs_and_context_reports_result() -> None:
    job = SimpleJob()
    qjob = QJob(job)
    ctx = qjob._ctx

    # Initially no result
    assert ctx.try_result() is None

    # Run the job synchronously (simulates worker thread)
    qjob.run()

    # Now await_result should return the value produced by the job
    assert ctx.await_result() == "ok"


def test_run_subjob_maps_progress_to_parent_slice() -> None:
    parent_job = SimpleJob()
    qjob = QJob(parent_job)
    ctx = qjob._ctx

    # Simulate parent progress already at 0.2
    ctx._progress = 0.2

    seen: List[float] = []

    # collect progress updates emitted by the QJob signals
    def _collector(job, progress: float) -> None:
        seen.append(progress)

    qjob._signals.on_progress.connect(_collector)

    # Run a subjob with weight 0.4. Expect mapped progress values in [0.2, 0.6]
    child = SimpleJob()
    res = ctx.run_subjob(child, weight=0.4)

    assert res == "ok"
    # final progress must reach parent_start + weight
    assert ctx._progress == 0.2 + 0.4

    # The collected sequence should include mapped progress values
    assert seen[0] == pytest.approx(0.2)
    assert seen[1] == pytest.approx(0.2 + 0.5 * 0.4)
    assert seen[2] == pytest.approx(0.2 + 1.0 * 0.4)


def test_qjobprocessor_cancel_all() -> None:
    processor = QJobProcessor(run_in_thread=False)

    # Submit two simple jobs
    h1 = processor.submit(SimpleJob())
    h2 = processor.submit(SimpleJob())

    # Access the underlying qjobs to verify cancel token behavior
    qjobs = processor._qjobs
    assert len(qjobs) >= 2

    # Initially not cancelled
    assert not qjobs[-1]._cancel_token.is_cancelled()
    assert not qjobs[-2]._cancel_token.is_cancelled()

    processor.cancel_all()

    assert qjobs[-1]._cancel_token.is_cancelled()
    assert qjobs[-2]._cancel_token.is_cancelled()
