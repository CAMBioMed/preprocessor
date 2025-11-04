# See: https://gist.github.com/Virtlink/b713707ede3f74bee2d902cf18f8d110

SHELL         := /usr/bin/bash
.SHELLFLAGS   := -eu -o pipefail -c
.DEFAULT_GOAL := help
.ONESHELL:
.DELETE_ON_ERROR:
.SILENT:
MAKEFLAGS += --no-print-directory
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --warn-undefined-variables

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
run:                                ## Run the CLI interface
	uv run preprocessor

.PHONY: run-gui
run-gui:                            ## Run the GUI interface
	uv run preprocessor -- gui

### =============================================================================
##@ Development
### =============================================================================
.PHONY: build
build: check                        ## Build the project
	echo "${INFO} Building..."
	uv build
	echo "${OK} Built"

.PHONY: test
test:                             	## Test the project
	echo "${INFO} Testing..."
	uv run pytest -q
	echo "${OK} Tested"

.PHONY: test-coverage
test-coverage:                      ## Test the project with coverage
	echo "${INFO} Testing with coverage..."
	uv run pytest -q --cov
	echo "${OK} Tested with coverage"

.PHONY: typecheck
typecheck:                          ## Type check the project
	echo "${INFO} Type checking (mypy)..."
	uv run mypy src tests
	echo "${OK} Checked types"

.PHONY: lint
lint:                               ## Lint the project
	echo "${INFO} Linting (ruff)..."
	uv run ruff check .
	echo "${OK} Linted"

.PHONY: check
check: test typecheck lint          ## Check and lint the project

.PHONY: format
format:                             ## Format the code files
	echo "${INFO} Formatting (ruff)..."
	uv run ruff format .
	echo "${OK} Formatted"

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
##@ Meta
### =============================================================================
.PHONY: version
version:                            ## Print the project version
	uv run hatch version
