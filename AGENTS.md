# Agent Guidance

# Agent Guidance

- Follow task-specific and repository-specific instructions before this file.
- Before editing, inspect the relevant implementation, tests, configuration, and similar code.

## Implementation rules

- Reuse established patterns and repository tooling; do not introduce a second convention.
- Keep changes narrowly scoped to the task.
- Favor straightforward existing abstractions over speculative generalization.
- Preserve public behavior unless the task intentionally changes it.
- During intentional cutovers, remove obsolete code instead of adding compatibility shims.
- Preserve or improve existing type safety; use type annotations for new or changed code.
- Document public caller-facing entities such as modules, fields, methods, functions, parameters, classes, data types, 
  interfaces, errors, special values, and non-obvious invariants or error behavior.
- Prefer documentation on individual members to documenting at the class level, and avoid duplication. 
- Docstrings must describe behavior relevant to users and callers of the entity, not implementation details.
- Docstrings should briefly describe any special values.
- Make error behavior explicit. Do not swallow errors or suppress warnings to make checks pass.
- Avoid unrelated refactoring, formatting, documentation, or comment churn.
- Add dependencies only when clearly required.
- Do not invent product requirements or compatibility guarantees not supported by the task or repository.
- Investigate discrepancies between documentation and implementation.
- Update README/configuration examples and CHANGELOG.md when a user-visible command, configuration option, or behavior changes.

## Testing and completion

- Every changed executable behavior needs a focused automated test.
- Test observable behavior, boundaries, and error cases rather than implementation details.
- Keep tests focused and follow existing test patterns.
- Every bug fix needs a regression test that fails before the fix.
- Follow Arrange / Act / Assert structure and comment these phases in each unit test; label non-obvious or multi-step phases.
- While iterating, run the narrowest relevant checks first.
- Treat formatter, linter, type-checker, test warnings, and failures as work to resolve rather than suppress.
- Before completion, run the relevant formatter, linter, type checker, tests, and build/code-generation checks.
- Review the final diff for unrelated changes, stale code, debugging artifacts, and inconsistent documentation or call sites.
- If a relevant check cannot be run, state that explicitly.

## Repository safety

- Do not overwrite unrelated working-tree changes.
- Do not commit, do not perform destructive Git operations.
- Keep secrets and machine-specific state out of the repository.
- Do not read, expose, log, copy, commit, or modify secrets. Avoid opening or modifying credential files, ask the user instead.
- Do not edit generated files when an authoritative source or generator exists.
- Do not run deployment or destructive tasks.

## Repository orientation

- `README.md` is the product overview.
- `pyproject.toml` is the authority for Python metadata, dependencies, build configuration, pytest, Ruff, `ty`, and mypy policy.
- `mise.toml` is the routine command entry point. Use `mise tasks ls` to discover supported tasks.
- `tests/` contains the behavioral test suite.

## Repository-specific development environment

- Prefer `nix develop` for an interactive shell.
- Prefer `nix develop -c <command>` for one command in the repository toolchain.
- If Nix is unavailable, use mise directly according to `mise.toml`.
- Make Python dependency changes in `pyproject.toml`.
- Change `flake.nix` or `flake.lock` only when the development toolchain itself intentionally changes.

## Repository-specific implementation rules

- Use Python type annotations for new or changed Python code.
- Use Pydantic validation at data boundaries.
- Use `pathlib.Path` for filesystem paths.
- Document using PEP 287 reST-style docstrings.
- Run `nix develop path:$PWD -c mise run build` when packaging or entry points change.
- Qt Designer `.ui` files live in `src/preprocessor/gui/designer/`; generated `ui_*.py` files are tracked but
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
- Tests should have names of the form `test_should_X_when_Y`, and have a human-readable docstring of the same test name.