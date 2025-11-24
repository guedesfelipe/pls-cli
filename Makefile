#* Variables
PYTHON := python

#* uv
.PHONY: uv-download
uv-download:
	@curl -LsSf https://astral.sh/uv/install.sh | sh

#* Config git hook
.PHONY: git-config-hook
git-config-hook:
	@cp pre-commit .git/hooks/
	@chmod +x .git/hooks/pre-commit

#* Installation
.PHONY: install
install:
	@uv sync --only-group test

.PHONY: install-dev
install-dev:
	@uv sync --all-groups
	@make git-config-hook

#* Formatters
.PHONY: format
format:
	@uv run ruff format .
	@uv run ruff check --fix .

#* Linting
.PHONY: lint
lint:
	@uv run ruff format --check .
	@uv run ruff check .
	@uv run mypy pls_cli tests

#* Test
.PHONY: test
test:
	@uv run pytest -v

#* Security
.PHONY: sec
sec:
	@uv run pip-audit --desc on --progress-spinner off

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	@find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	@find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	@find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	@find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	@rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove

#* Coverage
.PHONY: coverage
coverage:
	@uv run pytest --cov --cov-fail-under 95 -v

#* Coverage HTML
.PHONY: coverage-html
coverage-html:
	@uv run pytest --cov --cov-report html -v

#* Publish
.PHONY: publish
publish:
	@uv build
	@uv publish
