from PySide6.QtWidgets import QWidget, QMessageBox

from preprocessor._version import __version__  # type: ignore

def show_about_dialog(parent: QWidget | None = None) -> None:
    """Show the About dialog."""
    text = f"""
        <center>
          <h1>CAMBioMed Preprocessor</h1>
        </center>
        <p>
          Version {__version__}<br/>
          Copyright &copy; Daniel A. A. Pelsmaeker
        </p>
        """
    QMessageBox.about(parent, "About Preprocessor", text)