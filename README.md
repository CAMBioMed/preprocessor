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
- Install tools: `mise install`
- Sync dependencies: `mise run sync`
- Sync the opt-in Linux Torch dependency set for source installs: `uv sync --extra torch`
- Run: `mise run run`
- Run the GUI: `mise run gui`
- Run tests: `mise run test`
- Run tests with coverage: `mise run test-coverage`
- Determine version: `mise run version`
- Format code: `mise run format`
- Lint code: `mise run lint`
- Lint code and fix violations: `mise run lint --fix`
- Type check: `mise run typecheck`
- Build UI files and package artifacts: `mise run build`
- Build and test the Briefcase app: `mise run app-check`
- Run the Briefcase app: `mise run app-run`

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


## License
Copyright (C) 2025-2026 - Daniel A. A. Pelsmaeker

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **without any warranty**; without even the implied warranty of **merchantability** or **fitness for a particular purpose**.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
