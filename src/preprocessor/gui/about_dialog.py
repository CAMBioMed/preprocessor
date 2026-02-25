from PySide6.QtWidgets import QWidget, QMessageBox

from preprocessor import app_version, app_formal_name, app_author


def show_about_dialog(parent: QWidget | None = None) -> None:
    """Show the About dialog."""
    text = f"""
        <center>
          <h1>{app_formal_name}</h1>
        </center>
        <p>
          Version {app_version}<br/>
          Copyright &copy; {app_author}
        </p>
        """
    QMessageBox.about(parent, f"About {app_formal_name}", text)
