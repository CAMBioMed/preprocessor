# See: https://gist.github.com/Virtlink/b713707ede3f74bee2d902cf18f8d110

SHELL         := /bin/bash
#SHELL         := /usr/bin/bash
.SHELLFLAGS   := -eu -o pipefail -c
.DEFAULT_GOAL := help
.ONESHELL:
.DELETE_ON_ERROR:
.SILENT:
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --warn-undefined-variables

# Allow passing extra args to underlying commands, e.g.:
#   make lint ARGS="--fix"
ARGS ?=

# Colors and formatting
NC     := $(shell printf "\033[0m")
BOLD   := $(shell printf "\033[1m")
DIM    := $(shell printf "\033[2m")
ITALIC := $(shell printf "\033[3m")
ULINE  := $(shell printf "\033[4m")
RED    := $(shell printf "\033[1;31m")
GREEN  := $(shell printf "\033[1;32m")
YELLOW := $(shell printf "\033[1;33m")
BLUE   := $(shell printf "\033[1;34m")
MAGENTA:= $(shell printf "\033[1;35m")
CYAN   := $(shell printf "\033[1;36m")
INFO   := $(shell printf "$(BLUE)ℹ$(NC)")
OK     := $(shell printf "$(GREEN)✓$(NC)")
WARN   := $(shell printf "$(YELLOW)⚠$(NC)")
ERROR  := $(shell printf "$(RED)✖$(NC)")

# Note: targets followed by `##` are documented in the help output
#       lines starting with `##@` are used to group targets in the help output
.PHONY: help
help:                                  ## Display this help text for this Makefile
	awk 'BEGIN {FS = ":.*##";\
 		printf "\nUsage:  make ${CYAN}<target>${NC}\n"}\
 		/^[a-zA-Z0-9_-]+:.*?##/ { printf "  ${CYAN}%-15s${NC} %s\n", $$1, $$2 }\
 		/^##@/ { printf "\n${BOLD}%s${NC}\n", substr($$0, 5) } '\
 		$(MAKEFILE_LIST)

### =============================================================================
##@ Execute
### =============================================================================
.PHONY: run
run:                                ## Run the application
	uv run preprocessor


### =============================================================================
##@ Development
### =============================================================================
.PHONY: build-ui
build-ui:                           ## Build the UI files
	echo "${INFO} Building UI files..."
	uv run pyside6-project build
	echo "${OK} Built UI files"

.PHONY: build
build: build-ui app-check           ## Build and check the project
	echo "${INFO} Building..."
	uv build
	echo "${OK} Built"

.PHONY: test
test:                             	## Test the project
	echo "${INFO} Testing..."
	uvx --with tox-uv tox -e 3.12 -- $(ARGS)
	echo "${OK} Tested"

.PHONY: test-coverage
test-coverage:                      ## Test the project with coverage
	echo "${INFO} Testing with coverage..."
	uvx --with tox-uv tox -e 3.12 -- $(ARGS) --cov
	echo "${OK} Tested with coverage"

.PHONY: typecheck
typecheck:                          ## Type check the project
	echo "${INFO} Type checking (mypy)..."
	uv run mypy $(ARGS) src --pretty
	echo "${OK} Checked types"

.PHONY: lint
lint:                               ## Lint the project
	echo "${INFO} Linting (ruff)..."
	uvx ruff check $(ARGS) .
	echo "${OK} Linted"

.PHONY: format
format:                             ## Format the code files
	echo "${INFO} Formatting (ruff)..."
	uvx ruff format $(ARGS) .
	echo "${OK} Formatted"

.PHONY: check
check: test lint          ## Check and lint the project
#check: test typecheck lint          ## Check and lint the project

### =============================================================================
##@ Dependencies
### =============================================================================
.PHONY: sync
sync:                               ## Sync dependencies
	echo "${INFO} Syncing..."
	uv sync
	echo "${OK} Synced"

.PHONY: upgrade
upgrade:                            ## Upgrade locked dependencies
	echo "${INFO} Upgrading dependencies..."
	uv lock --upgrade
	echo "${OK} Dependencies upgraded"

### =============================================================================
##@ Application
### =============================================================================
.PHONY: app-update
app-update:                          ## Update the app to match the current project state
	echo "${INFO} Updating app..."
	uvx briefcase update --update-requirements --update-resources $(ARGS)
	echo "${OK} App updated"

.PHONY: app-build
app-build:                          ## Build the updated app
	echo "${INFO} Building app..."
	uvx briefcase build --test --no-input --no-update $(ARGS)
	echo "${OK} App built"

.PHONY: app-test
app-test:                          ## Test the built app
	echo "${INFO} Testing app..."
	uvx briefcase run --test --no-input --no-update $(ARGS)
	echo "${OK} App tested"

.PHONY: app-run
app-run:                            ## Run the built app
	echo "${INFO} Running app..."
	uvx briefcase run $(ARGS)
	echo "${OK} App ran"

.PHONY: app-package
app-package:                        ## Package the built app
	echo "${INFO} Packaging app..."
	uvx briefcase package --adhoc-sign $(ARGS)
	echo "${OK} App packaged"

.PHONY: app-clean
app-clean:                          ## Clean the app artifacts
	echo "${INFO} Cleaning app artifacts..."
	-rm -r .briefcase/ 2> /dev/null
	-rm -r build/ 2> /dev/null
	-rm -r logs/ 2> /dev/null
	-find . -type d -name "*.dist-info" -exec rm -r {} +
	echo "${OK} App artifacts cleaned"

.PHONY: app-check
app-check: check app-build app-test ## Check and lint the app

### =============================================================================
##@ Meta
### =============================================================================
.PHONY: version
version:                            ## Print the project version
	uvx hatch version
