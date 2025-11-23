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
    assert 'Show this message and exit' in result.stdout


def test_version_command():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert result.stdout == f'pls CLI Version: {__version__}\n'


@patch('pls_cli.utils.settings.Settings.exists_settings', return_value=False)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_first_usage(mock_write_settings, mock_exists_settings):
    result = runner.invoke(app, input='test\ny\nY\n')
    assert result.exit_code == 0
    assert 'Hello! What can I call you?: test' in result.stdout
    assert 'pls callme <Your Name Goes Here>' in result.stdout
    assert 'If you wanna change your name later, please use:' in result.stdout
    assert (
        'To apply the changes restart the terminal or use this command:'
        in result.stdout
    )
    assert (
        'If you need to disable or enable the task progress bar later, please use:'
        in result.stdout
    )
    assert (
        'If you need to disable or enable quotes later, please use:'
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


@patch('pls_cli.utils.settings.Settings.exists_settings', return_value=True)
@patch(
    'pls_cli.utils.settings.Settings.get_tasks',
    return_value=[{'name': 'Task 1', 'done': True}],
)
def test_config_ok_no_tasks_pending_with_progress(
    mock_get_tasks, mock_exists_settings
):
    result = runner.invoke(app)
    assert result.exit_code == 0


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


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_edit_task_with_invalid_id(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['edit', '1', 'Edited'])
    assert 'Currently, you have no tasks' in result.stdout
    assert result.exit_code == 0


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_edit_not_found_task(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['edit', '2', 'Task 2 edited'])
    assert result.exit_code == 0
    assert 'Task #2 was not found, pls choose an existing ID' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': False},
            {'name': 'Old task text', 'done': False},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_edit_task_success(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['edit', '2', 'New task text'], input='y')
    output = result.stdout
    assert result.exit_code == 0
    assert 'Old Task: Old task text' in output
    assert 'Edited Task: New task text' in output
    assert 'Are you sure you want to edit Task #2? [y/N]: y' in output
    assert '1    Task 1            ○' in output
    assert '2    New task text     ○' in output


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': False},
            {'name': 'Task 2', 'done': False},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_edit_task_aborted(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['edit', '2', 'Task 2 edited'], input='N\n')
    output = result.stdout
    assert result.exit_code == 0
    assert 'Old Task: Task 2' in output
    assert 'Edited Task: Task 2 edited' in output
    assert 'Are you sure you want to edit Task #2? [y/N]: N' in output
    assert '1    Task 1            ○' in output
    assert '2    Task 2 edited     ○' in output


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_edit_empty_tasks(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['edit', '1', 'Task 1 edited'])
    output = result.stdout
    assert result.exit_code == 0
    assert 'Currently, you have no tasks to edit 📝' in output


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': False},
            {'name': 'Task 2', 'done': False},
            {'name': 'Task 3', 'done': False},
            {'name': 'Task 4', 'done': False},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_move_task_success(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['move', '1', '3'])
    output = result.stdout
    assert result.exit_code == 0
    assert 'Updated Task List' in output
    single_spaces = ' '.join(output.split())
    assert '1 Task 2 ○' in single_spaces
    assert '2 Task 3 ○' in single_spaces
    assert '3 Task 1 ○' in single_spaces
    assert '4 Task 4 ○' in single_spaces

    result = runner.invoke(app, ['move', '4', '2'])
    output = result.stdout
    assert result.exit_code == 0
    assert 'Updated Task List' in output
    single_spaces = ' '.join(output.split())
    assert '1 Task 2 ○' in single_spaces
    assert '2 Task 4 ○' in single_spaces
    assert '3 Task 3 ○' in single_spaces
    assert '4 Task 1 ○' in single_spaces
