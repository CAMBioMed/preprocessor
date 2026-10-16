# Agent Guidance

# This Repository

- `README.md` is the product overview.
- `pyproject.toml` is the authority for Python metadata, dependencies, build configuration, pytest, Ruff, `ty`, and mypy policy.
- `mise.toml` is the routine command entry point. Use `mise tasks ls` to discover supported tasks.
- `tests/` contains the behavioral test suite.
- Before editing, inspect the relevant implementation and adjacent tests. Reuse established patterns; do not introduce a second convention beside an existing one.

- `src/preprocessor/main.py` is the app entrypoint: creates the Qt app, loads `QApplicationState`, opens
  or creates a project, then shows `MainWindow`.
- Architecture splits persisted Pydantic data from Qt wrapper models:
  - `src/preprocessor/core/model/`: persisted state such as `ProjectData`, `PhotoData`, `MetadataData`.
  - `src/preprocessor/gui/model/`: `QObject` wrappers such as `QProjectModel`, `QPhotoModel`,
    `QApplicationState`, with signals and dirty tracking.
- Project files are `*.pbproj` JSON files saved and loaded through `ProjectData.save_to_file()` /
  `load_from_file()`. `ProjectPath` keeps paths relative to the project directory when possible.
- Image processing lives in `src/preprocessor/core/transform/transform_image.py`: load `ImageRGB`, apply
  ordered transforms, optionally save.
- Main flows:
  - Add photos: `MainWindow._handle_add_photos_action()` → `AddPhotoJob` → `PhotoData` + EXIF →
    `QPhotoModel`.
  - Export photos: `MainWindow._handle_export_all_action()` → `PhotoData.group_photos()` →
    `ExportPhotoJob` → `transform_image()`.
  - Quadrat detection: `MainWindow._handle_detect_quadrat_action()` → `DetectQuadratAnalysisJob` →
    `QPhotoModel.quadrat_corners`.
- Do not create or mutate `QObject` instances in worker threads. Use plain Pydantic data off-thread;
  construct Qt models on the main thread.
- In Qt wrappers, use `QModel._set_field(...)` so validation, field signals, and dirty tracking stay
  consistent.
- Update project/photo state through `QProjectModel` and `QPhotoModel`; do not replace _`data` directly.
- Prefer `ImageRGB`, `ImageBGR`, and `ImageGreyscale` from `src/preprocessor/core/types.py` at module
  boundaries.
- Use `MessageReporter` and `ProgressReporter` for processing status; avoid ad-hoc prints.
- There are two job APIs. Match surrounding code:
  - `gui/jobs/qjobs.py`: current batch-dialog path.
  - `gui/jobs/qjobs2.py` + `core/jobs/jobs.py`: newer generic abstraction.
- Qt Designer `.ui` files live in `src/preprocessor/gui/`; generated `ui_*.py` files are tracked but
  should not be hand-edited unless unavoidable.
- Useful commands:
  - Discover tasks: `nix develop path:$PWD -c mise tasks ls`
  - Sync deps: `nix develop path:$PWD -c mise run sync`
  - Run app: `nix develop path:$PWD -c mise run run`
  - Test: `nix develop path:$PWD -c mise run test`
  - Coverage / lint / format / typecheck: `nix develop path:$PWD -c mise run test-coverage`, `nix develop path:$PWD -c mise run lint`, `nix develop path:$PWD -c mise run format`, `nix develop path:$PWD -c mise run typecheck`
  - Build package + UI: `nix develop path:$PWD -c mise run build`
- Testing gotchas: pytest uses importlib mode, warnings-as-errors, and `pythonpath = ["src"];` Qt
  tests may force run_in_thread=False.

## Development environment

- Prefer `nix develop` for an interactive shell.
- Prefer `nix develop -c <command>` for one command in the repository toolchain.
- If Nix is unavailable, use mise directly according to `mise.toml`.
- Make Python dependency changes in `pyproject.toml`.
- Change `flake.nix` or `flake.lock` only when the development toolchain itself intentionally changes.

## Implementation rules

- Keep changes narrowly scoped to the task.
- Favor straightforward existing abstractions over speculative generalization.
- Preserve public behavior unless the task intentionally changes it.
- During intentional cutovers, remove obsolete code instead of adding compatibility shims.
- Use Python type annotations for new or changed Python code.
- Use Pydantic validation at data boundaries.
- Use `pathlib.Path` for filesystem paths.
- For models carrying `ProjectPath` values, preserve project-context-aware validation and serialization; inspect the existing implementations rather than restating schemas here.
- Document all Python modules, fields, methods, functions, classes, data types, interfaces, and other public caller-facing entities with PEP 287 reST-style docstrings.
- Prefer documentation on individual members to documenting at the class level, and avoid duplication. 
- Docstrings must describe behavior relevant to users and callers of the entity, not implementation details.
- Docstrings must describe behavior relevant to users and callers of the entity, not implementation details.
- Docstrings should briefly describe any special values such as `None`, except when a function returns only `None`.
- Make error behavior explicit. Do not swallow exceptions or suppress warnings/failures instead of fixing them.
- Avoid unrelated formatting churn.
- Do not add a dependency without demonstrated task-related need.

## Testing and completion

- Every behavior change needs a focused test.
- Every bug fix needs a regression test that fails before the fix.
- Test observable behavior, boundaries, and error cases rather than implementation details.
- Follow Arrange / Act / Assert and comment these phases in each unit test.
- Keep one logical action per test.
- Tests should have names of the form `should X, when Y`. 
- While iterating, run the narrowest relevant pytest command.
- Before completion, run `nix develop path:$PWD -c mise run test`.
- Run `nix develop path:$PWD -c mise run build` when packaging or entry points change.
- Exercise the actual CLI for CLI behavior changes.
- Treat formatter, linter, type-checker, test warnings, and failures as work to resolve rather than suppress.
