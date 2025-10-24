# PyCharm Run Configuration

## Interpreter
Import the project into PyCharm, then set it to use UV as the Python interpreter.

1.  Install UV.
    ```shell
    make install-uv
    ```
2.  Create the virtual environment.
    ```shell
    make sync
    ```
3.  Open PyCharm settings, and go to 'Project: <project_name>' → 'Python Interpreter'
4.  Click 'Add Interpreter' and select 'Add Local Interpreter...'
5.  Select 'Existing environment' and select:
    - Type: `uv`
    - Path to uv: the locally installed `uv` binary, e.g.:
      - On Nix: `/home/<username>/.nix-profile/bin/uv` 
      - On MacOS: `/usr/local/bin/uv`
    - UV env use: `preprocessor/.venv/bin/python` (the Python symlink from the `.venv` folder in the project directory)
6.  Click 'OK'.


## External Tool 'UV Sync'
1.  Open PyCharm settings, and go to 'Tools' → 'External Tools'
2. Click the '+' button to add a new external tool
3. Fill in the fields as follows:
    - Name: `UV Sync`
    - Program: `uv`
    - Arguments: `sync`
    - Working directory: `$ProjectFileDir$`
4. Click 'OK' to save the external tool


## Run Configuration
Create a new 'Python' Run Configuration:

- Module: `preprocessor.main`
- Script parameters: `ui`
- Before launch: Run external tool 'UV Sync' (create this external tool as described below)
