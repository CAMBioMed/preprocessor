# Benthic Image Preprocessor

[Annotation Guide](https://cambiomed-biodiversa.com/guide/)

## Installation
Download the latest release:

1.  Go to the latest [release](https://github.com/CAMBioMed/preprocessor/releases/latest).
2.  Download the appropriate artifact for your system, one of:

    - Windows (`CAMBioMed.Preprocessor.msi`)
    - MacOS (`CAMBioMed.Preprocessor.dmg`)
    - Ubuntu (`preprocessor.ubuntu-noble_amd64.deb`)
    - Fedora (`preprocessor.fc40.x86_64.rpm `)


## Developer tasks
- Sync dependencies: `uv sync` (`make sync`)
- Run: `uv run preprocessor` (`make run`)
- Run tests: `uv run pytest -q` (`make test`)
- Run tests with coverage: `uv run pytest -q --cov` (`make test-coverage`)
- Determine version: `uv run hatch version` (`make version`)
- Format code: `uv run ruff format .` (`make format`)
- Lint code: `uv run ruff check .` (`make lint`)
- Build app and UI files: `uv run pyside6-project build` and `uv build` (`make build`)
- Mypy type checking: `uv run mypy src tests` (`make typecheck`)
- Run briefcase app with app update and updating dependencies: `uvx briefcase run -u -r` (`make app-run`)

## Release
To release a version of this project:

1.  Update the version number in `pyproject.toml`.
2.  Regenerate the lock file.

    ```shell
    uv lock
    ```
    
3.  Tag, commit, push.

    ```shell
    VERSION=<version>
    git commit --all -m "Release $VERSION"
    git tag -a $VERSION -m "Release $VERSION"
    git push --atomic origin main $VERSION
    ```
    
4.  Publish the draft release on GitHub.
