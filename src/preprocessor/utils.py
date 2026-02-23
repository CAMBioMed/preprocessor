from pathlib import Path


def update_basepath(old_basepath: Path | None, new_basepath: Path | None, path: Path) -> Path:
    """
    Update a single file path that is relative to a base path that has changed.

    If the path is absolute, it is returned unchanged.
    If it is relative, it is updated to be relative to the new base path, unless that base path is not an
    ancestor of the old full path, in which case the absolute path is returned.
    """
    if old_basepath is None and not path.is_absolute():
        # If the old base path is not known, we can't reliably update the relative path, so we return it unchanged.
        return path
    old_full_path = path if old_basepath is None else (old_basepath / path).resolve()
    if new_basepath is None:
        # If the new base path is not known, we can't reliably update the relative path, so we return the absolute path.
        return old_full_path
    try:
        # We don't walk up. If this fails, we'll just use the absolute path
        return old_full_path.relative_to(new_basepath)
    except ValueError:
        return old_full_path
