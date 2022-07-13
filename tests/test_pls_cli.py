from unittest.mock import patch

import pkg_resources
from freezegun import freeze_time
from typer.testing import CliRunner

from pls_cli import __version__
from pls_cli.please import app

runner = CliRunner()


def test_version():
    assert __version__ == pkg_resources.get_distribution('pls-cli').version


def test_error_invalid_command():
    result = runner.invoke(app, ['test'])
    assert result.exit_code == 2
    assert "No such command 'test'" in result.stdout


def test_help():
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0


def test_version_command():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert result.stdout == f'pls CLI Version: {__version__}\n'


@patch('pls_cli.utils.settings.Settings.exists_settings', return_value=False)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_first_usage(mock_write_settings, mock_exists_settings):
    result = runner.invoke(app, input='test\n')
    assert result.exit_code == 0
    assert 'Hello! What can I call you?: test' in result.stdout
    assert 'pls callme <Your Name Goes Here>' in result.stdout
    assert 'Thanks for letting me know your name!' in result.stdout
    assert 'If you wanna change your name later, please use:' in result.stdout
    assert (
        'to apply the changes restart the terminal or use this command:'
        in result.stdout
    )


@freeze_time('2022-01-14 03:21:34')
@patch('pls_cli.utils.settings.Settings.exists_settings', return_value=True)
@patch('pls_cli.utils.settings.Settings.get_name', return_value='Test name')
@patch('pls_cli.utils.settings.Settings.all_tasks_done', return_value=False)
@patch(
    'pls_cli.utils.settings.Settings.get_tasks',
    return_value=[{'name': 'Task 1', 'done': False}],
)
def test_config_ok_show_tasks(
    mock_get_tasks, mock_all_tasks_done, mock_get_name, mock_exists_settings
):
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Test name! It's 14 Jan | 03:21 AM" in result.stdout
    assert 'ID   TASK     STATUS' in result.stdout
    assert '1    Task 1     ○' in result.stdout


@freeze_time('2022-01-14 03:21:34')
@patch('pls_cli.utils.settings.Settings.exists_settings', return_value=True)
@patch('pls_cli.utils.settings.Settings.get_name', return_value='Test name')
@patch('pls_cli.utils.settings.Settings.all_tasks_done', return_value=True)
@patch(
    'pls_cli.utils.settings.Settings.get_tasks',
    return_value=[{'name': 'Task 1', 'done': False}],
)
def test_config_ok_no_tasks_pending(
    mock_get_tasks, mock_all_tasks_done, mock_get_name, mock_exists_settings
):
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Test name! It's 14 Jan | 03:21 AM" in result.stdout
    assert 'Looking good, no pending tasks ✨ 🍰 ✨' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
@patch('pls_cli.utils.settings.Settings.all_tasks_done', return_value=False)
@patch(
    'pls_cli.utils.settings.Settings.get_tasks',
    return_value=[
        {'name': 'Task 1', 'done': True},
        {'name': 'New task', 'done': False},
    ],
)
def test_add_task(
    mock_get_tasks, mock_all_tasks_done, mock_write_settings, mock_get_settings
):
    result = runner.invoke(app, ['add', 'New task'])
    assert result.exit_code == 0
    assert 'Added "New task" to the list' in result.stdout
    assert 'ID   TASK       STATUS' in result.stdout
    assert '1    Task 1       ✓' in result.stdout
    assert '2    New task     ○' in result.stdout
