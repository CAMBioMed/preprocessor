# AGENTS.md

## Big picture
- `src/preprocessor/main.py` is the real app entrypoint: create Qt app, load `QApplicationState`, open/create a project, then show `MainWindow`.
- The main architectural split is **persisted Pydantic data** vs **Qt wrapper models**:
  - `src/preprocessor/core/model/` stores persisted state (`ProjectData`, `PhotoData`, `MetadataData`, etc.)
  - `src/preprocessor/gui/model/` wraps that state in `QObject` models (`QProjectModel`, `QPhotoModel`, `QApplicationState`) with signals + dirty tracking
- Project files (`*.pbproj`) are JSON via `ProjectData.save_to_file()` / `load_from_file()`. `ProjectPath` serializes paths relative to the project directory when possible.
- Image processing flows through `src/preprocessor/core/transform/transform_image.py`: load `ImageRGB`, apply ordered transforms, optionally save.

## Key flows
- Add photos: `MainWindow._handle_add_photos_action()` -> `AddPhotoJob` computes `PhotoData` + EXIF in a worker -> UI thread creates `QPhotoModel` and appends to `project.photos`.
- Export photos: `MainWindow._handle_export_all_action()` -> `PhotoData.group_photos()` -> `ExportPhotoJob` -> `transform_image()` -> `LensCorrectTransform` + `PerspectiveCropTransform`.
- Quadrat detection is still synchronous in the UI: `MainWindow._handle_detect_quadrat_action()` -> `DetectQuadratAnalysisJob` -> write corners back via `QPhotoModel.quadrat_corners`.

## Conventions that matter
- Never create or mutate `QObject` instances in worker threads; use plain Pydantic data off-thread and construct Qt models back on the main thread (`AddPhotoJob` is the reference pattern).
- Use `QModel._set_field(...)` in Qt wrappers so Pydantic validation, per-field signals, and dirty tracking all happen together.
- Update project/photo state through the Qt model layer (`QProjectModel`, `QPhotoModel`) instead of replacing `_data` directly.
- Prefer `ImageRGB` / `ImageBGR` / `ImageGreyscale` from `src/preprocessor/core/types.py` at module boundaries instead of raw OpenCV arrays.
- Processing code reports through `MessageReporter` and `ProgressReporter`; avoid ad-hoc prints for pipeline status.

## Async/job systems
- There are two job APIs; match the surrounding code instead of mixing them:
  - `src/preprocessor/gui/jobs/qjobs.py`: current batch-dialog path used by `ProgressDialog`, `AddPhotoJob`, `ExportPhotoJob`, and most of `MainWindow`
  - `src/preprocessor/gui/jobs/qjobs2.py` + `src/preprocessor/core/jobs/jobs.py`: newer generic abstraction used in tests and `photo_editor_widget.py`
- `qjobs.py` deliberately disables `QRunnable.autoDelete`; preserve that unless you have verified signal lifetime behavior.

## UI and generated files
- Qt Designer files live in `src/preprocessor/gui/*.ui`; generated `ui_*.py` files are tracked.
- Regenerate UI code with `uv run pyside6-project build` or `make build-ui`.
- Do not hand-edit generated `ui_*.py` files unless unavoidable; prefer changing the `.ui` file or the owning widget class.

## Developer workflow
- Sync deps: `uv sync` or `make sync`
- Run app: `uv run preprocessor` or `make run`
- Test: `uvx --with tox-uv tox run -e 3.12 -q --` or `make test`
- Coverage / lint / format / typecheck: `make test-coverage`, `make lint`, `make format`, `make typecheck`
- Build package + UI: `make build`

## Testing/debugging gotchas
- Pytest uses `--import-mode=importlib`, warnings-as-errors, and `pythonpath = ["src"]` from `pyproject.toml`.
- Qt tests often force deterministic execution with `run_in_thread=False`; see `tests/conftest.py` and `tests/preprocessor/gui/test_qjobs2.py`.
- `ProgressDialog.auto_close_on_finish` is used by tests; preserve it when changing dialog lifecycle behavior.
- If you change dependencies, keep `dependency-groups.test` and `tool.briefcase.app.preprocessor.test_requires` in sync.

## Reference files
- `src/preprocessor/main.py`, `src/preprocessor/gui/main_window.py`, `src/preprocessor/gui/model/_QModel.py`
- `src/preprocessor/core/model/_ProjectData.py`, `src/preprocessor/core/model/_PhotoData.py`, `src/preprocessor/core/model/_ProjectPath.py`
- `src/preprocessor/gui/jobs/add_photo_job.py`, `src/preprocessor/gui/jobs/export_photo_job.py`, `src/preprocessor/core/transform/transform_image.py`


