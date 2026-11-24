import importlib

import pytest

MODEL_EXPORTS = {
    "preprocessor.core.model": {
        "MetadataData": "_metadata_data",
        "PhotoData": "_photo_data",
        "ProjectData": "_project_data",
    },
    "preprocessor.gui.model": {
        "MetadataModel": "_q_metadata_model",
        "QApplicationState": "_q_application_state",
        "QListModel": "_q_list_model",
        "QModel": "_q_model",
        "QPhotoModel": "_q_photo_model",
        "QProjectModel": "_q_project_model",
    },
}


@pytest.mark.parametrize(("package_name", "exports"), MODEL_EXPORTS.items())
def test_should_expose_expected_model_exports_when_model_package_is_imported(
    package_name: str, exports: dict[str, str]
) -> None:
    """Should expose expected model exports when the model package is imported."""
    parent = importlib.import_module(package_name)

    assert parent.__all__ == list(exports)
    for name, module_name in exports.items():
        private_module = importlib.import_module(f"{package_name}.{module_name}")
        assert getattr(parent, name) is getattr(private_module, name)
