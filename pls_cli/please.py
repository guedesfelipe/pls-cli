import datetime
import json
import os
import shutil

import typer
from rich import box
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule
from rich.table import Table

from pls_cli import __version__
from pls_cli.utils.quotes import get_rand_quote
from pls_cli.utils.settings import Settings

app = typer.Typer()
console = Console()

error_line_style = os.getenv('PLS_ERROR_LINE_STYLE', '#e56767')
error_text_style = os.getenv('PLS_ERROR_TEXT_STYLE', '#ff0000 bold')

warning_line_style = os.getenv('PLS_WARNING_LINE_STYLE', '#FFBF00')
warning_text_style = os.getenv('PLS_WARNING_TEXT_STYLE', '#FFBF00 bold')

update_line_style = os.getenv('PLS_UPDATE_LINE_STYLE', '#61E294')
update_text_style = os.getenv('PLS_UPDATE_TEXT_STYLE', '#61E294 bold')

insert_or_delete_line_style = os.getenv(
    'PLS_INSERT_DELETE_LINE_STYLE', '#bb93f2'
)
insert_or_delete_text_style = os.getenv(
    'PLS_INSERT_DELETE_TEXT_STYLE', '#a0a0a0'
)

msg_pending_style = os.getenv('PLS_MSG_PENDING_STYLE', '#61E294')
table_header_style = os.getenv('PLS_TABLE_HEADER_STYLE', '#844191')
table_header_style = os.getenv('PLS_TABLE_HEADER_STYLE', '#d77dd8')
task_done_style = os.getenv('PLS_TASK_DONE_STYLE', '#a0a0a0')
task_pending_style = os.getenv('PLS_TASK_PENDING_STYLE', '#bb93f2')
header_greetings_style = os.getenv('PLS_HEADER_GREETINGS_STYLE', '#FFBF00')
quote_style = os.getenv('PLS_QUOTE_STYLE', '#a0a0a0')
author_style = os.getenv('PLS_AUTHOR_STYLE', '#a0a0a0')


def center_print(text, style: str = None, wrap: bool = False) -> None:
    """Print text with center alignment.
    Args:
        text (Union[str, Rule, Table]): object to center align
        style (str, optional): styling of the object. Defaults to None.
    """
    if wrap:
        width = shutil.get_terminal_size().columns // 2
    else:
        width = shutil.get_terminal_size().columns

    console.print(Align.center(text, style=style, width=width))


def print_no_pending_tasks() -> None:
    center_print(
        f'[{msg_pending_style}]Looking good, no pending tasks[/] ✨ 🍰 ✨'
    )


def print_tasks(force_print: bool = False) -> None:
    if not Settings().all_tasks_done() or force_print:
        showtasks()
    else:
        print_no_pending_tasks()


@app.command(short_help='Show all Tasks')
def showtasks() -> None:
    """Display the list of tasks."""
    task_table = Table(
        header_style=table_header_style,
        style=table_header_style,
        box=box.SIMPLE_HEAVY,
    )

    task_table.add_column('ID', justify='center')
    task_table.add_column('TASK')
    task_table.add_column('STATUS', justify='center')

    for index, task in enumerate(Settings().get_tasks()):
        if task['done']:
            task_name = f'[{task_done_style}][s]{task["name"]}[/][/]'
            task_status = '[#bbf2b3]✓[/]'
            task_id = f'[{task_done_style}][s]{str(index + 1)}[/][/]'
        else:
            task_name = f'[{task_pending_style}]{task["name"]}[/]'
            task_status = f'[{task_pending_style}]○[/]'
            task_id = f'[{task_pending_style}]{str(index + 1)}[/]'

        task_table.add_row(task_id, task_name, task_status)
    center_print(task_table)

    if Settings().all_tasks_done():
        print_no_pending_tasks()


@app.command(short_help='Add a Task (Add task name inside quotes)')
def add(task: str) -> None:
    """Add new task to the list.

    Args:
        task (str): task name
    """
    new_task = {'name': task, 'done': False}
    settings = Settings().get_settings()
    settings['tasks'].append(new_task)
    Settings().write_settings(settings)
    center_print(
        Rule(f'Added "{task}" to the list', style=insert_or_delete_line_style),
        style=insert_or_delete_text_style,
    )
    print_tasks()


@app.command(short_help='Mark a task as done')
def done(taks_id: int) -> None:
    """Mark a task as "done".

    Args:
        taks_id (int): task ID
    """
    task_id = taks_id - 1
    settings = Settings().get_settings()
    if not settings['tasks']:
        center_print(
            Rule(
                'Sorry, There are no tasks to mark as done',
                style=error_line_style,
            ),
            style=error_text_style,
        )
        return

    if not 0 <= task_id < len(settings['tasks']):
        center_print(
            Rule(
                'Are you sure you gave me the correct ID to mark as done?',
                style=error_line_style,
            ),
            style=error_text_style,
        )
        return

    if settings['tasks'][task_id]['done']:
        center_print(
            Rule(
                'No Updates Made, Task Already Done', style=warning_line_style
            ),
            style=warning_text_style,
        )
        print_tasks()
        return

    if Settings().all_tasks_done():
        center_print(
            Rule('All tasks are already completed!', style=update_line_style),
            style=update_text_style,
        )
        return

    settings['tasks'][task_id]['done'] = True
    Settings().write_settings(settings)
    center_print(
        Rule('Updated Task List', style=update_line_style),
        style=update_text_style,
    )
    print_tasks()


@app.command(short_help='Mark a task as undone')
def undone(task_id: int) -> None:
    """Unmark a task as "done".

    Args:
        task_id (int): task ID
    """
    task_id = task_id - 1
    settings = Settings().get_settings()
    if not settings['tasks']:
        center_print(
            Rule(
                'Sorry, There are no tasks to mark as undone',
                style=error_line_style,
            ),
            style=error_text_style,
        )
        return

    if not 0 <= task_id < len(settings['tasks']):
        center_print(
            Rule(
                'Are you sure you gave me the correct ID to mark as undone?',
                style=error_line_style,
            ),
            style=error_text_style,
        )
        return

    if not settings['tasks'][task_id]['done']:
        center_print(
            Rule(
                'No Updates Made, Task Still Pending', style=warning_line_style
            ),
            style=warning_text_style,
        )
        print_tasks()
        return

    settings['tasks'][task_id]['done'] = False
    Settings().write_settings(settings)
    center_print(
        Rule('Updated Task List', style=update_text_style),
        style=update_text_style,
    )
    print_tasks()


@app.command(short_help='Delete a Task')
def delete(task_id: int) -> None:
    """Delete an existing task.

    Args:
        task_id (int): task ID
    """
    task_id = task_id - 1
    settings = Settings().get_settings()
    if not settings['tasks']:
        center_print(
            Rule(
                'Sorry, There are no tasks left to delete',
                style=error_line_style,
            ),
            style=error_text_style,
        )
        return

    if not 0 <= task_id < len(settings['tasks']):
        center_print(
            Rule(
                'Are you sure you gave me the correct ID to delete?',
                style=error_line_style,
            ),
            style=error_text_style,
        )
        return

    deleted_task = settings['tasks'][task_id]
    del settings['tasks'][task_id]
    Settings().write_settings(settings)
    center_print(
        Rule(
            f'Deleted "{deleted_task["name"]}"',
            style=insert_or_delete_line_style,
        ),
        style=insert_or_delete_text_style,
    )
    print_tasks(True)


@app.command(short_help='Change task order')
def move(old_id: int, new_id: int) -> None:
    """Change the order of task.

    Args:
        old_id (int): current task ID
        new_id (int): new task ID
    """
    settings = Settings().get_settings()
    if not settings['tasks']:
        center_print(
            Rule(
                'Sorry, cannot move tasks as the Task list is empty',
                style=error_line_style,
            ),
            style=error_text_style,
        )
        return

    if old_id == new_id:
        center_print(
            Rule('No Updates Made', style=warning_line_style),
            style=warning_text_style,
        )
        return

    if (not 0 <= old_id - 1 < len(settings['tasks'])) or (
        not 0 <= new_id - 1 < len(settings['tasks'])
    ):
        center_print(
            Rule(
                'Are you sure you gave me the correct ID to delete?',
                style=error_line_style,
            ),
            style=error_text_style,
            wrap=True,
        )
        return

    try:
        settings['tasks'][old_id - 1], settings['tasks'][new_id - 1] = (
            settings['tasks'][new_id - 1],
            settings['tasks'][old_id - 1],
        )
        Settings().write_settings(settings)
        center_print(
            Rule('Updated Task List', style=update_line_style),
            style=update_text_style,
        )
        print_tasks(settings['tasks'])
    except Exception:
        center_print(
            Rule(
                "Please check the entered ID's values", style=error_line_style
            ),
            style=error_text_style,
        )
        print_tasks()


@app.command(short_help='Clear all tasks')
def clear() -> None:
    """Clear all tasks."""
    typer.confirm('Are you sure you want to delete all tasks?', abort=True)
    settings = Settings().get_settings()
    settings['tasks'] = []
    Settings().write_settings(settings)
    center_print(
        Rule('Task List Deleted', style=update_line_style),
        style=update_text_style,
    )


@app.command(short_help='Clean up tasks marked as done')
def clean() -> None:
    """Clear all tasks."""
    typer.confirm(
        'Are you sure you want to delete all done tasks?', abort=True
    )
    settings = Settings().get_settings()
    settings['tasks'] = Settings().get_all_tasks_undone()
    Settings().write_settings(settings)
    center_print(
        Rule('Done Tasks Deleted', style=update_line_style),
        style=update_text_style,
    )


@app.command(short_help='Count done tasks')
def count_done() -> None:
    """Count Done tasks"""
    typer.echo(Settings().count_tasks_done())


@app.command(short_help='Count undone tasks')
def count_undone() -> None:
    """Count Undone tasks"""
    typer.echo(Settings().count_tasks_undone())


@app.command(short_help='Reset all data and run setup')
def setup() -> None:
    """Initialize the settings file."""
    settings: dict = {}
    settings['user_name'] = typer.prompt(
        typer.style('Hello! What can I call you?', fg=typer.colors.CYAN)
    )

    code_markdown = Markdown(
        """
            pls callme <Your Name Goes Here>
        """
    )
    center_print('\nThanks for letting me know your name!')
    center_print(
        'If you wanna change your name later, please use:', style='red'
    )
    console.print(code_markdown)
    center_print(
        'to apply the changes restart the terminal or use this command:',
        style='red',
    )
    code_markdown = Markdown(
        """
            pls
        """
    )
    console.print(code_markdown)

    settings['initial_setup_done'] = True
    settings['tasks'] = []
    Settings().write_settings(settings)


@app.callback(invoke_without_command=True)
def show(ctx: typer.Context) -> None:
    """Greets the user."""
    try:
        if ctx.invoked_subcommand is None:
            if Settings().exists_settings():
                date_now = datetime.datetime.now()
                user_name = Settings().get_name()
                header_greetings = f'[{header_greetings_style}] Hello {user_name}! It\'s {date_now.strftime("%d %b | %I:%M %p")}[/]'
                center_print(
                    Rule(header_greetings, style=header_greetings_style)
                )
                quote = get_rand_quote()
                center_print(
                    f'[{quote_style}]"{quote["content"]}"[/]', wrap=True
                )
                center_print(
                    f'[{author_style}][i]・{quote["author"]}・[/i][/]\n',
                    wrap=True,
                )
                print_tasks()
            else:
                setup()
    except json.JSONDecodeError:
        console.print_exception(show_locals=True)
        center_print(
            Rule('Failed while loading configuration', style=error_line_style),
            style=error_text_style,
        )


@app.command()
def version():
    """Show version"""
    typer.echo(f'pls CLI Version: {__version__}')
    raise typer.Exit()
