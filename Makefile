#* Variables
PYTHON := python

#* Poetry
.PHONY: poetry-download
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) - --uninstall

#* Config git hook
.PHONY: git-config-hook
git-config-hook:
	@cp pre-commit .git/hooks/
	@chmod +x .git/hooks/pre-commit

#* Installation
.PHONY: install
install:
	@poetry install -n --only main,test

.PHONY: install-dev
install-dev:
	@poetry install -n
	@make git-config-hook

#* Fromatters
.PHONY: format
format:
	@poetry run blue .
	@poetry run isort . -m3 --up --tc

#* Linting
.PHONY: lint
lint:
	@poetry run blue . --check
	@poetry run isort . -m3 --up --tc --check
	@poetry run prospector --with-tool pycodestyle --doc-warning --no-autodetect

#* Test
.PHONY: test
test:
	@poetry run pytest -v

#* Security
.PHONY: sec
sec:
	@poetry run safety check --full-report

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
	@poetry run pytest --cov --cov-fail-under 95 -v

#* Coverage HTML
.PHONY: coverage-html
coverage-html:
	@poetry run pytest --cov --cov-report html -v

#* Publish
.PHONY: publish
publish:
	@poetry publish --build
