"""Bounds validation for `pls edit`.

Task IDs are 1-based, and every sibling command (`done`, `undone`, `del`,
`swap`) validates `1 <= task_id <= len(tasks)`. `edit` used to check only
`task_id and task_id <= len(tasks)`, so a negative ID slipped through and
Python's negative indexing silently edited the wrong task
(`tasks[task_id - 1]`). Negative IDs are rejected now.
"""

import json

from typer.testing import CliRunner

from pls_cli.please import app
from pls_cli.utils.settings import Settings

runner = CliRunner()

SEED_TASKS = [
    {"name": "first", "done": False},
    {"name": "second", "done": False},
]


def _seed_settings(tmp_path, monkeypatch):
    monkeypatch.setattr(
        Settings, "get_config_path", lambda self: str(tmp_path)
    )
    config = {
        "user_name": "Test",
        "tasks": [dict(task) for task in SEED_TASKS],
        "show_task_progress": False,
        "show_quotes": False,
        "initial_setup_done": True,
    }
    (tmp_path / "config.json").write_text(json.dumps(config), encoding="utf-8")


def _read_tasks(tmp_path):
    return json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))[
        "tasks"
    ]


def test_edit_negative_id_is_rejected(tmp_path, monkeypatch):
    _seed_settings(tmp_path, monkeypatch)
    result = runner.invoke(app, ["edit", "--", "-1", "hacked"], input="y\n")
    assert "was not found" in result.output
    assert _read_tasks(tmp_path) == SEED_TASKS


def test_edit_zero_id_is_rejected(tmp_path, monkeypatch):
    _seed_settings(tmp_path, monkeypatch)
    result = runner.invoke(app, ["edit", "0", "hacked"], input="y\n")
    assert "was not found" in result.output
    assert _read_tasks(tmp_path) == SEED_TASKS


def test_edit_valid_id_still_works(tmp_path, monkeypatch):
    _seed_settings(tmp_path, monkeypatch)
    result = runner.invoke(app, ["edit", "1", "renamed"], input="y\n")
    assert result.exit_code == 0
    tasks = _read_tasks(tmp_path)
    assert tasks[0]["name"] == "renamed"
    assert tasks[1] == SEED_TASKS[1]
