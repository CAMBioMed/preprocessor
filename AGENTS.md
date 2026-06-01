# AGENTS.md

## Big picture
- `src/preprocessor/main.py` is the real entrypoint: it initializes Qt, loads `QApplicationState`, opens a project (or `LaunchDialog`), then shows `MainWindow`.
- The codebase is intentionally split into **pure data** vs **Qt wrappers**:
  - `src/preprocessor/core/model/`: persisted Pydantic models (`ProjectData`, `PhotoData`, `MetadataData`, etc.)
  - `src/preprocessor/gui/model/`: `QObject` wrappers (`QProjectModel`, `QPhotoModel`, `QApplicationState`) that add signals + dirty tracking for the UI
- Persisted project files (`*.pbproj`) are JSON from `ProjectData.save_to_file()` / `load_from_file()`. Paths use `ProjectPath`, which stores paths relative to the project directory when possible.
- Image export flows through `src/preprocessor/core/transform/transform_image.py`: load `ImageRGB` -> apply ordered transforms -> optionally save output.

## Data and control flow to understand first
- Adding photos: `MainWindow._handle_add_photos_action()` -> `AddPhotoJob` -> create `PhotoData` + EXIF in a worker thread -> create `QPhotoModel` on the **main thread** and append to `project.photos`.
- Exporting photos: `MainWindow._handle_export_all_action()` -> group photos via `PhotoData.group_photos()` -> `ExportPhotoJob` -> `transform_image()` -> `LensCorrectTransform` + `PerspectiveCropTransform`.
- Quadrat detection currently runs synchronously from the UI (`MainWindow._handle_detect_quadrat_action()`), using `core/transform/detect_quadrat_analysis.py` and then writing corners back through `QPhotoModel.quadrat_corners`.

## Threading and job conventions
- Do not create or mutate `QObject` instances in worker threads. This project explicitly computes plain Pydantic data in workers and constructs Qt models back on the UI thread (`AddPhotoJob` is the reference pattern).
- There are **two job systems**:
  - `src/preprocessor/gui/jobs/qjobs.py`: the older/current batch UI job API used by `ProgressDialog`, `AddPhotoJob`, `ExportPhotoJob`, and most of `MainWindow`.
  - `src/preprocessor/gui/jobs/qjobs2.py` + `src/preprocessor/core/jobs/jobs.py`: newer generic job abstraction, already used in tests and in `photo_editor_widget.py`.
- When editing async code, match the local subsystem instead of mixing both job APIs in one feature.
- `qjobs.py` disables `QRunnable.autoDelete`; keep that behavior unless you verify signal lifetime issues are resolved.

## Project-specific coding patterns
- `QModel` (`src/preprocessor/gui/model/_QModel.py`) is the base for Qt wrappers: use `_set_field(...)` so validation, per-field signals, and dirty tracking all happen together.
- `QProjectModel` keeps an interactive `QListModel[QPhotoModel]` in sync with underlying `ProjectData.photos`; edits should usually go through the Qt model layer, not by replacing `_data` directly.
- `QApplicationState` owns persistent app settings via `QSettings` (window geometry, last project path, etc.).
- Image types are wrapped in `ImageRGB` / `ImageBGR` / `ImageGreyscale` in `src/preprocessor/core/types.py`; prefer those wrappers over raw OpenCV arrays at module boundaries.
- Processing/reporting code uses structured message and progress interfaces (`MessageReporter`, `ProgressReporter`) instead of ad-hoc prints/log-only signaling.

## UI files and generated code
- Qt Designer `.ui` files live in `src/preprocessor/gui/`; generated `ui_*.py` files are tracked in git.
- Regenerate UI code with `uv run pyside6-project build` or `make build-ui`.
- Do **not** hand-edit generated `ui_*.py` files unless there is no alternative; change the `.ui` or owning widget class instead.
- `ui_*.py` files are intentionally excluded from Ruff/MyPy in `pyproject.toml`.

## Developer workflows
- Install/sync deps: `uv sync` or `make sync`
- Run app: `uv run preprocessor` or `make run`
- Test: `uvx --with tox-uv tox run -e 3.12 -q --` or `make test`
- Coverage: `make test-coverage`
- Lint/format/typecheck: `make lint`, `make format`, `make typecheck`
- Build package + regenerate UI: `make build`
- App packaging uses Briefcase (`make app-run`, `make app-build`, `make app-package`)

## Testing and debugging details that are easy to miss
- Pytest runs with `--import-mode=importlib`, warnings-as-errors, and `pythonpath = ["src"]` from `pyproject.toml`.
- Qt tests often force deterministic main-thread execution by passing `run_in_thread=False`; see `tests/conftest.py` and `tests/preprocessor/gui/test_qjobs2.py`.
- `ProgressDialog` has an `auto_close_on_finish` hook used by tests; preserve it when changing dialog lifecycle behavior.
- If you change dependencies, keep `dependency-groups.test` and `tool.briefcase.app.preprocessor.test_requires` in sync (`pyproject.toml` notes this explicitly).

## Useful reference files
- App bootstrap: `src/preprocessor/main.py`
- Main UI orchestration: `src/preprocessor/gui/main_window.py`
- Persistent data: `src/preprocessor/core/model/_ProjectData.py`, `_PhotoData.py`, `_ProjectPath.py`
- Qt model wrappers: `src/preprocessor/gui/model/_QApplicationState.py`, `_QProjectModel.py`, `_QPhotoModel.py`
- Export pipeline: `src/preprocessor/gui/jobs/export_photo_job.py`, `src/preprocessor/core/transform/transform_image.py`
- EXIF ingestion: `src/preprocessor/processing/exif.py`

