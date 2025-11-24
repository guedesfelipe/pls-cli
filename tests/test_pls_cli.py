from unittest.mock import patch

from freezegun import freeze_time
from typer.testing import CliRunner

from pls_cli import __version__
from pls_cli.please import app

try:
    from importlib.metadata import version  # Python 3.8+
except ImportError:
    from importlib_metadata import version  # type: ignore[no-redef]


runner = CliRunner()


def test_version():
    assert __version__ == version('pls-cli')


def test_error_invalid_command():
    result = runner.invoke(app, ['test'])
    assert result.exit_code == 2
    assert "No such command 'test'" in result.output


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
        'If you need to disable or enable the task progress bar later, '
        'please use:'
    ) in result.stdout
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
def test_done_command_success(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['done', '1'])
    assert result.exit_code == 0
    assert 'Updated Task List' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [],
    },
)
def test_done_command_empty_tasks(mock_get_settings):
    result = runner.invoke(app, ['done', '1'])
    assert result.exit_code == 0
    assert 'Sorry, There are no tasks to mark as done' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_done_command_invalid_id(mock_get_settings):
    result = runner.invoke(app, ['done', '5'])
    assert result.exit_code == 0
    assert (
        'Are you sure you gave me the correct ID to mark as done?'
        in result.stdout
    )


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': True}],
    },
)
def test_done_command_already_done(mock_get_settings):
    result = runner.invoke(app, ['done', '1'])
    assert result.exit_code == 0
    assert 'No Updates Made, Task Already Done' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': True},
            {'name': 'Task 2', 'done': False},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_undone_command_success(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['undone', '1'])
    assert result.exit_code == 0
    assert 'Updated Task List' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [],
    },
)
def test_undone_command_empty_tasks(mock_get_settings):
    result = runner.invoke(app, ['undone', '1'])
    assert result.exit_code == 0
    assert 'Sorry, There are no tasks to mark as undone' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_undone_command_already_undone(mock_get_settings):
    result = runner.invoke(app, ['undone', '1'])
    assert result.exit_code == 0
    assert 'No Updates Made, Task Still Pending' in result.stdout


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
def test_delete_command_success(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['del', '1'])
    assert result.exit_code == 0
    assert 'Deleted "Task 1"' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [],
    },
)
def test_delete_command_empty_tasks(mock_get_settings):
    result = runner.invoke(app, ['del', '1'])
    assert result.exit_code == 0
    assert 'Sorry, There are no tasks left to delete' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_delete_command_invalid_id(mock_get_settings):
    result = runner.invoke(app, ['del', '5'])
    assert result.exit_code == 0
    assert 'Are you sure you gave me the correct ID to delete?' in result.stdout


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
def test_swap_command_success(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['swap', '1', '2'])
    assert result.exit_code == 0
    assert 'Updated Task List' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [],
    },
)
def test_swap_command_empty_tasks(mock_get_settings):
    result = runner.invoke(app, ['swap', '1', '2'])
    assert result.exit_code == 0
    assert 'cannot swap tasks as the Task list is empty' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_swap_command_same_id(mock_get_settings):
    result = runner.invoke(app, ['swap', '1', '1'])
    assert result.exit_code == 0
    assert 'No Updates Made' in result.stdout


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
def test_clear_command_success(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['clear'], input='y')
    assert result.exit_code == 0
    assert 'Task List Deleted' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': True},
            {'name': 'Task 2', 'done': False},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.get_all_tasks_undone')
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_clean_command_success(
    mock_write_settings, mock_get_all_tasks_undone, mock_get_settings
):
    mock_get_all_tasks_undone.return_value = [{'name': 'Task 2', 'done': False}]
    result = runner.invoke(app, ['clean'], input='y')
    assert result.exit_code == 0
    assert 'Done Tasks Deleted' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': True},
            {'name': 'Task 2', 'done': False},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.count_tasks_done', return_value=1)
def test_count_done_command(mock_count_tasks_done, mock_get_settings):
    result = runner.invoke(app, ['count-done'])
    assert result.exit_code == 0
    assert '1' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': True},
            {'name': 'Task 2', 'done': False},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.count_tasks_undone', return_value=1)
def test_count_undone_command(mock_count_tasks_undone, mock_get_settings):
    result = runner.invoke(app, ['count-undone'])
    assert result.exit_code == 0
    assert '1' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Old name',
        'initial_setup_done': True,
        'tasks': [],
    },
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_callme_command(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['callme', 'New name'])
    assert result.exit_code == 0
    assert 'Thanks for letting me know your name!' in result.stdout


def test_tasks_command():
    result = runner.invoke(app, ['tasks', '--help'])
    assert result.exit_code == 0


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={'show_task_progress': True},
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_tasks_progress_command(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['tasks-progress', '--no-show'])
    assert result.exit_code == 0
    assert 'Thanks for letting me know that!' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={'show_quotes': True},
)
@patch('pls_cli.utils.settings.Settings.write_settings')
def test_quotes_command(mock_write_settings, mock_get_settings):
    result = runner.invoke(app, ['quotes', '--no-show'])
    assert result.exit_code == 0
    assert 'Thanks for letting me know that!' in result.stdout


@patch('typer.launch')
def test_docs_command(mock_launch):
    result = runner.invoke(app, ['docs'])
    assert result.exit_code == 0
    assert 'Opening' in result.stdout
    assert 'PLS-CLI' in result.stdout
    assert 'docs' in result.stdout
    mock_launch.assert_called_once_with(
        'https://guedesfelipe.github.io/pls-cli/'
    )


@patch('typer.launch')
def test_config_command(mock_launch):
    result = runner.invoke(app, ['config'])
    assert result.exit_code == 0
    assert 'Opening config directory' in result.stdout
    assert mock_launch.called


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_undone_command_invalid_id(mock_get_settings):
    result = runner.invoke(app, ['undone', '5'])
    assert result.exit_code == 0
    assert (
        'Are you sure you gave me the correct ID to mark as undone?'
        in result.stdout
    )


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
def test_swap_command_invalid_id(mock_get_settings):
    result = runner.invoke(app, ['swap', '1', '5'])
    assert result.exit_code == 0
    assert 'Are you sure you gave me the correct ID to swap?' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_move_command_empty_tasks(mock_get_settings):
    mock_get_settings.return_value = {
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [],
    }
    result = runner.invoke(app, ['move', '1', '2'])
    assert result.exit_code == 0
    assert 'cannot move task as the Task list is empty' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_move_command_same_position(mock_get_settings):
    result = runner.invoke(app, ['move', '1', '1'])
    assert result.exit_code == 0
    assert 'No Updates Made' in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [{'name': 'Task 1', 'done': False}],
    },
)
def test_move_command_invalid_id(mock_get_settings):
    result = runner.invoke(app, ['move', '1', '5'])
    assert result.exit_code == 0
    assert "Please check the entered ID's values" in result.stdout


@patch(
    'pls_cli.utils.settings.Settings.get_settings',
    return_value={
        'user_name': 'Test name',
        'initial_setup_done': True,
        'tasks': [
            {'name': 'Task 1', 'done': False},
            {'name': 'Task 2', 'done': True},
        ],
    },
)
@patch('pls_cli.utils.settings.Settings.get_tasks')
def test_showtasks_command(mock_get_tasks, mock_get_settings):
    mock_get_tasks.return_value = [
        {'name': 'Task 1', 'done': False},
        {'name': 'Task 2', 'done': True},
    ]
    result = runner.invoke(app, ['tasks'])
    assert result.exit_code == 0
    assert 'TASK' in result.stdout
