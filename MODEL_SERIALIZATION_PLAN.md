## Context

Replace every production and test use of the legacy `MetadataData`, `PhotoData`, and `ProjectData` models under `src/preprocessor/core/model/` with the established serialization models under `src/preprocessor/core/serialization/`, then remove the obsolete model package. The end state uses `Photo`, `Project`, metadata dictionaries, and serialization parameter accessors directly across persistence, transforms, and the GUI, with focused behavioral coverage for add/save/reopen and metadata/parameter editing.

## Findings

- The clean mapping is `PhotoData` → `serialization.Photo`, `ProjectData` → `serialization.Project`, and `MetadataData` → `Photo.metadata: dict[str, JsonValue]`. `Photo` already contains filename generation/grouping; `Project` already contains direct JSON/file and CSV APIs matching the legacy project API.
- `Photo` requires `id`, `image_path`, positive `width`/`height`, and metadata; processing parameters live in `params` and are accessed through `get_*_param`/`set_*_param`. The import job already reads dimensions but discards them.
- `Project` requires UUID `id`, `name`, `metadata`, `photos`, and `folders`. It does not contain the GUI-only `project_file`, last import path, or last export path, so those belong on `QProjectModel`, not in project metadata (project metadata is inherited into photo CSV rows).
- Runtime references span GUI adapters/jobs/widgets, `ImageTransformWorkItem` and transforms, application state, and the main-window add/export flows. Symbol-aware reference checks found no external production consumer beyond these repository call sites.
- `MetadataModel` has no production consumer other than its package export; metadata dialogs/widgets currently mutate the legacy metadata object directly and must instead update a copied dictionary through `QPhotoModel` so Pydantic validation, dirty state, and Qt signals still run.
- Existing serialization tests already cover model validation, path context, grouping/filename generation, parameter accessors, nested projects, storage, and CSV output. Legacy core-model tests duplicate that behavior and should be removed rather than translated.
- Routine checks are defined in `mise.toml`; the repository-preferred shell is `nix develop path:$PWD -c …`.


## Approach

1. Cut core processing over to `Photo`.
   - Change `ImageTransformWorkItem.params`, `transform_image(..., params: Photo, ...)`, `DisplayPhotoJob.photo`, and `ExportPhotoJob.photo` to `preprocessor.core.serialization.Photo`; use `photo.id` and `photo.image_path` everywhere, with no `image_id`/`original_filename` aliases.
   - In `LensCorrectTransform` and `PerspectiveCropTransform`, fetch the last applicable parameter once with `get_lens_correction_params(photo)` and `get_crop_param(photo)`. Preserve the current skip/warning/error behavior when a parameter is absent, disabled, empty, or geometrically invalid.
   - Keep crop-corner editing backed by `CropParams.quadrat`, because that established model permits the GUI’s observable 0–4-point intermediate state; leave `Photo.quadrat` as the separate strict four-corner serialized annotation already defined by the serialization schema.

2. Rebase the Qt photo adapter and metadata surfaces on `Photo`.
   - Change `QPhotoModel` to `QModel[Photo]` and expose the actual model fields `id`, `image_path`, `width`, `height`, `metadata`, `quadrat`, and `params`. Rename every GUI/widget/tree/thumbnail caller from `original_filename` to `image_path`; remove the old `image_id`/`original_filename` signals and properties.
   - Retain the derived `lens_correction`, `crop`, and `ruler` GUI properties, but implement their getters with the serialization accessors and return a new disabled default parameter when absent. Implement setters by copying the current `params`, applying the matching `set_*_param` helper to a copied `Photo`, assigning the validated list through `_set_field("params", ...)`, and emitting the existing derived-property signal only when its effective value changes. This preserves parameter order and the “last parameter wins” rule without bypassing dirty tracking.
   - Keep `quadrat_corners`, ruler-point, camera-matrix, and distortion-coefficient GUI helpers, now layered on those accessor-backed properties. Add no legacy data-field aliases.
   - Add `metadata_value(key: str) -> JsonValue | None` and `set_metadata_value(key: str, value: JsonValue | date | datetime | None) -> None`. The setter must copy the metadata dictionary, serialize dates/times with `isoformat()`, trim strings, remove keys for `None` or blank strings, then assign through `_set_field("metadata", ...)`; this is the only production path for per-key edits and therefore emits `on_metadata_changed`, `on_changed`, and dirty state.
   - Update `MetadataDialog` and `EditorDockWidget` to read dictionary values through `metadata_value`, parse display dates with `parse_date_or_datetime`, and write through `set_metadata_value`. Remove `MetadataModel`, its export from `preprocessor.gui.model`, and its standalone test because no runtime code uses it.

3. Rebase project lifecycle and persistence on `Project`.
   - Change `QProjectModel` to `QModel[Project]`. When no data is supplied, construct exactly `Project(id=uuid4(), name="Untitled Project", metadata={}, photos=[], folders=[])`; expose `id`, `name`, `metadata`, and `folders` as validated model properties while retaining the `QListModel[QPhotoModel]` binding for top-level `photos`.
   - Store `project_file`, `photos_path`, and `export_path` as typed private `QProjectModel` state, with their existing public properties/signals; never insert these GUI paths into `Project.metadata`. Accept them as keyword-only constructor arguments. `project_file` changes update path-dependent GUI state without changing serialized project data.
   - Replace `ProjectData.load_from_file`/`save_to_file` with the existing `Project.load_from_file`/`save_to_file` APIs. Continue writing the direct `Project` JSON payload—the API added to `Project` expressly mirrors the legacy calls—rather than wrapping it in `ProjectFile`.
   - On open, set `project_file` to the selected path and initialize `photos_path` to the common parent directory of loaded top-level photo paths (or `None` for no photos); initialize `export_path` to `None`. Keep both path hints session-only because the `Project` schema has no corresponding fields and storing them as metadata would leak them into inherited photo metadata/CSV.
   - Update `QApplicationState`’s placeholder to construct `QProjectModel(project_file=Path("empty"))`, and remove the stale commented `ProjectData` construction from `launch_dialog.py`.

4. Build imported photos in the serialization shape and migrate all application call sites.
   - In `AddPhotoJob`, construct `Photo(id=filepath.stem, image_path=filepath, width=width, height=height, metadata=...)`. Populate only available EXIF keys; serialize EXIF `date`/`datetime` values to ISO 8601 strings so the dictionary satisfies `JsonValue`.
   - Update main-window export grouping to `Photo.group_photos`, jobs and widgets to `image_path`, and all metadata reads/writes to dictionary/helper semantics. Preserve current add-photo path restrictions, grouping order, generated filenames, transform order, error dialogs, and dirty propagation.
   - Update the `[Unreleased]` changelog entry to state that application project/photo storage now uses the serialization `Project`/`Photo` schema and that the obsolete legacy project schema is not loaded.

5. Complete the clean cutover in tests and packages.
   - Remove `src/preprocessor/core/model/` and `tests/preprocessor/core/model/` in full; remove every `preprocessor.core.model`, `MetadataData`, `PhotoData`, and `ProjectData` import/reference rather than re-exporting or aliasing them.
   - Replace consumer fixtures with valid `Photo(id=..., image_path=..., width=..., height=..., metadata=..., params=[...])` and `Project(id=..., name=..., metadata={}, photos=..., folders=[])` instances. Update transform tests to place correction models in `Photo.params`, GUI/path assertions to use `image_path`, and metadata-dialog/EXIF assertions to use dictionary values and ISO date strings.
   - Refocus `QPhotoModel` tests on validated field changes, parameter replacement/append behavior, metadata normalization plus signal/dirty propagation, and the existing 0–4-point crop editing behavior. Refocus `QProjectModel` tests on UUID-backed new projects, top-level photo binding, transient path signals, and save/open through `Project`; do not reproduce serialization model-validation tests already under `tests/preprocessor/core/serialization/`.
   - Extend the existing main-window add/save/reopen test to assert imported dimensions/metadata survive and the saved JSON contains `id`, `image_path`, `width`, `height`, `metadata`, and `params`, with no legacy `image_id`, `original_filename`, `photos_path`, or `export_path` keys.

## Critical files & anchors

- `src/preprocessor/gui/model/_q_photo_model.py` — `QPhotoModel`: model-field renames, parameter accessor adaptation, metadata mutation boundary, and dirty/signal behavior.
- `src/preprocessor/gui/model/_q_project_model.py` — `QProjectModel.__init__`, new/open/save flows: required `Project` construction plus transient GUI paths.
- `src/preprocessor/gui/jobs/add_photo_job.py` — `AddPhotoJob.process`: the production boundary that must supply dimensions and JSON-compatible EXIF metadata.
- `src/preprocessor/gui/metadata_dialog.py` — metadata initialization/copy/apply methods: all object-attribute metadata access must become dictionary/helper access.

## Assumptions & contingencies

- This is a clean schema cutover: legacy `.pbproj` payloads containing `image_id`, `original_filename`, `photos_path`, or `export_path` are intentionally unsupported. Do not add migration logic, aliases, re-exports, or compatibility parsing.
- The GUI currently manages only `Project.photos`; existing serialized `Project.folders` remain preserved on load/save through the underlying `Project` but are not surfaced as editable `QListModel` children in this task.
- If `nix develop` is unavailable, run the same commands directly with `mise`/`uv` as defined in `mise.toml`; do not change dependencies or toolchain files.


## Verification

1. Focused automated behavior from the repository root:
   - `nix develop path:$PWD -c uv run pytest tests/preprocessor/core/serialization tests/preprocessor/core/transform tests/preprocessor/gui/model tests/preprocessor/gui/test_metadata_dialog.py tests/preprocessor/gui/test_main_window.py tests/preprocessor/test_exif_metadata.py`
   - Required observable case: add `tests/preprocessor/photos/IMG_1054.JPG` through the main-window flow, save, reopen, and observe one `Photo` with the same relative `image_path`, positive imported dimensions, ISO-8601 EXIF date metadata, and unchanged correction parameters.
2. Full repository checks after the focused suite passes:
   - `nix develop path:$PWD -c mise run check`
3. Actual GUI smoke:
   - Create a temporary directory with `mktemp -d`, copy `tests/preprocessor/photos/IMG_1054.JPG` beneath its `photos/` directory, then launch `nix develop path:$PWD -c mise run gui`.
   - Create and save a project in that directory, add the copied photo, edit metadata and lens/crop/ruler settings, save, close, reopen, and export it. Confirm the photo, metadata, and settings are restored; the preview/export paths complete without transform errors; and the `.pbproj` JSON uses the new `Project`/`Photo` field names listed above.
