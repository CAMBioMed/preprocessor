from importlib import metadata as importlib_metadata
from importlib.metadata import PackageMetadata

# App metadata
app_module: str = "preprocessor"
try:
    app_metadata: PackageMetadata | None = importlib_metadata.metadata(app_module)
except importlib_metadata.PackageNotFoundError:
    app_metadata = None
app_organisation: str = "CAMBioMed"
app_name: str = app_metadata["Name"] if app_metadata else "no-name"
app_formal_name: str = app_metadata["Formal-Name"] if app_metadata and "Formal-Name" in app_metadata else app_name
app_version: str = app_metadata["Version"] if app_metadata and "Version" in app_metadata else "?.?.?"
app_domain: str = "cambiomed-biodiversa.com"
app_homepage: str | None = app_metadata["Home-page"] if app_metadata and "Home-page" in app_metadata else None
app_author: str | None = app_metadata["Author"] if app_metadata and "Author" in app_metadata else None
app_author_email: str | None = app_metadata["Author-email"] if app_metadata and "Author-email" in app_metadata else None
