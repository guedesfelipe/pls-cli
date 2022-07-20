import datetime
import json
import os
import shutil
from typing import Union

import typer
from rich import box
from rich.align import Align
from rich.console import Console, RenderableType
from rich.markdown import Markdown
from rich.progress import BarColumn, MofNCompleteColumn, Progress
from rich.rule import Rule
from rich.table import Table

from pls_cli import __version__
from pls_cli.utils.quotes import get_rand_quote
from pls_cli.utils.settings import Settings

app = typer.Typer(rich_markup_mode='rich')
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
table_header_style = os.getenv('PLS_TABLE_HEADER_STYLE', '#d77dd8')
task_done_style = os.getenv('PLS_TASK_DONE_STYLE', '#a0a0a0')
task_pending_style = os.getenv('PLS_TASK_PENDING_STYLE', '#bb93f2')
header_greetings_style = os.getenv('PLS_HEADER_GREETINGS_STYLE', '#FFBF00')
quote_style = os.getenv('PLS_QUOTE_STYLE', '#a0a0a0')
author_style = os.getenv('PLS_AUTHOR_STYLE', '#a0a0a0')

background_bar_style = os.getenv('PLS_BACKGROUND_BAR_STYLE', 'bar.back')
complete_bar_style = os.getenv('PLS_COMPLETE_BAR_STYLE', 'bar.complete')
finished_bar_style = os.getenv('PLS_FINISHED_BAR_STYLE', 'bar.done')


def get_terminal_full_width() -> int:
    return shutil.get_terminal_size().columns


def get_terminal_center_width() -> int:
    return shutil.get_terminal_size().columns // 2


def center_print(
    text, style: Union[str, None] = None, wrap: bool = False
) -> None:
    """Print text with center alignment.
    Args:
        text (Union[str, Rule, Table]): object to center align
        style (str, optional): styling of the object. Defaults to None.
    """
    width = get_terminal_full_width() if wrap else get_terminal_full_width()

    if isinstance(text, Rule):
        console.print(text, style=style, width=width)
    else:
        console.print(Align.center(text, style=style, width=width))


def print_no_pending_tasks() -> None:
    center_print(
        f'[{msg_pending_style}]Looking good, no pending tasks[/] ✨ 🍰 ✨'
    )


class CenteredProgress(Progress):
    def get_renderable(self) -> RenderableType:
        return Align.center(super().get_renderable())


def print_tasks_progress() -> None:
    if Settings().show_tasks_progress():
        with CenteredProgress(
            BarColumn(
                bar_width=get_terminal_center_width(),
                style=background_bar_style,
                complete_style=complete_bar_style,
                finished_style=finished_bar_style,
            ),
            MofNCompleteColumn(),
        ) as progress:
            qty_done = Settings().count_tasks_done()
            qty_undone = Settings().count_tasks_undone()
            task1 = progress.add_task('Progress', total=qty_done + qty_undone)
            progress.update(task1, advance=qty_done)


@app.command('tasks-progress', rich_help_panel='Utils and Configs')
def tasks_progress(show: bool = True) -> None:
    """Show tasks progress 🎯"""
    settings = Settings().get_settings()
    settings['show_task_progress'] = show
    Settings().write_settings(settings)
    center_print(
        Rule(
            'Thanks for letting me know that!',
            style=insert_or_delete_line_style,
        ),
        style=insert_or_delete_text_style,
    )


@app.command('quotes', rich_help_panel='Utils and Configs')
def quotes(show: bool = True) -> None:
    """Show quotes 🏷"""
    settings = Settings().get_settings()
    settings['show_quotes'] = show
    Settings().write_settings(settings)
    center_print(
        Rule(
            'Thanks for letting me know that!',
            style=insert_or_delete_line_style,
        ),
        style=insert_or_delete_text_style,
    )


@app.command('tasks', short_help='Show all Tasks :open_book:')
@app.command(short_help='[s]Show all Tasks :open_book:[/]', deprecated=True)
def showtasks() -> None:
    """Show all Tasks :open_book:"""
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

    print_tasks_progress()


def print_tasks(force_print: bool = False) -> None:
    center_print(' ')
    if not Settings().all_tasks_done() or force_print:
        showtasks()
    else:
        print_no_pending_tasks()
        print_tasks_progress()


@app.command()
def add(task: str) -> None:
    """[bold green]Add[/bold green] a Task :sparkles: [light_slate_grey italic](Add task name inside quotes)[/]"""
    new_task = {'name': task, 'done': False}
    settings = Settings().get_settings()
    settings['tasks'].append(new_task)
    Settings().write_settings(settings)
    center_print(
        Rule(f'Added "{task}" to the list', style=insert_or_delete_line_style),
        style=insert_or_delete_text_style,
    )
    print_tasks()


@app.command()
def done(taks_id: int) -> None:
    """Mark a task as [#bbf2b3]done ✓[/]"""
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


@app.command(short_help=f'Mark a task as [{task_pending_style}]undone ○[/]')
def undone(task_id: int) -> None:
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


@app.command('del', short_help='[bright_red]Delete[/] a Task')
@app.command(short_help='[s]Delete a Task[/s]', deprecated=True)
def delete(task_id: int) -> None:
    """[bright_red]Delete[/] a Task"""
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


@app.command()
def move(old_id: int, new_id: int) -> None:
    """Change task order 🔀"""
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


@app.command()
def clear() -> None:
    """Clear all tasks :wastebasket:"""
    typer.confirm('Are you sure you want to delete all tasks?', abort=True)
    settings = Settings().get_settings()
    settings['tasks'] = []
    Settings().write_settings(settings)
    center_print(
        Rule('Task List Deleted', style=update_line_style),
        style=update_text_style,
    )


@app.command()
def clean() -> None:
    """Clean up tasks marked as done :broom:"""
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


@app.command(rich_help_panel='Integration')
def count_done() -> None:
    """Count done tasks :chart_increasing:"""
    typer.echo(Settings().count_tasks_done())


@app.command(rich_help_panel='Integration')
def count_undone() -> None:
    """Count undone tasks :chart_decreasing:"""
    typer.echo(Settings().count_tasks_undone())


@app.command(rich_help_panel='Utils and Configs')
def callme(name: str) -> None:
    """Change name :name_badge: [light_slate_grey italic](without resetting data)[/]"""
    settings = Settings().get_settings()
    settings['user_name'] = name
    Settings().write_settings(settings)
    center_print(
        Rule(
            'Thanks for letting me know your name!',
            style=insert_or_delete_line_style,
        ),
        style=insert_or_delete_text_style,
    )


@app.command(rich_help_panel='Utils and Configs')
def setup() -> None:
    """Reset all data and run setup :wrench:"""
    settings: dict = {}
    settings['user_name'] = typer.prompt(
        typer.style('Hello! What can I call you?', fg=typer.colors.CYAN)
    )

    show_tasks_progress = typer.prompt(
        typer.style(
            'Do you want show tasks progress? (Y/n)', fg=typer.colors.CYAN
        )
    )

    show_quotes = typer.prompt(
        typer.style('Do you want show quotes? (Y/n)', fg=typer.colors.CYAN)
    )

    code_markdown = Markdown(
        """
            pls callme <Your Name Goes Here>
        """
    )

    center_print(
        'If you wanna change your name later, please use:', style='red'
    )
    console.print(code_markdown)

    code_markdown = Markdown(
        """
            pls tasks-progress <--show or --no-show>
        """
    )
    center_print(
        'If you need to disable or enable the task progress bar later, please use:',
        style='red',
    )
    console.print(code_markdown)

    code_markdown = Markdown(
        """
            pls quotes <--show or --no-show>
        """
    )
    center_print(
        'If you need to disable or enable quotes later, please use:',
        style='red',
    )
    console.print(code_markdown)

    center_print(
        'To apply the changes restart the terminal or use this command:',
        style='red',
    )
    code_markdown = Markdown(
        """
            pls
        """
    )
    console.print(code_markdown)

    settings['initial_setup_done'] = True
    if show_tasks_progress in ('n', 'N'):
        settings['show_task_progress'] = False
    else:
        settings['show_task_progress'] = True

    if show_quotes in ('n', 'N'):
        settings['show_quotes'] = False
    else:
        settings['show_quotes'] = True

    settings['tasks'] = []
    Settings().write_settings(settings)


@app.callback(
    invoke_without_command=True,
    epilog='Made with [red]:heart:[/red] by [link=https://github.com/guedesfelipe/pls-cli]Felipe Guedes[/link]',
)
def show(ctx: typer.Context) -> None:
    """
    💻 [bold]PLS-CLI[/]

    ・[i]Minimalist and full configurable greetings and TODO list[/]・
    """
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
                if Settings().show_quotes():
                    center_print(
                        f'[{quote_style}]"{quote["content"]}"[/]', wrap=True
                    )
                    center_print(
                        f'[{author_style}][i]・{quote["author"]}・[/i][/]',
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


@app.command(rich_help_panel='Utils and Configs')
def version():
    """Show version :bookmark:"""
    typer.echo(f'pls CLI Version: {__version__}')
    raise typer.Exit()


@app.command(rich_help_panel='Utils and Configs')
def docs():
    """Launch docs Website :globe_with_meridians:"""
    center_print(Rule('・Opening [#FFBF00]PLS-CLI[/] docs・', style='#d77dd8'))
    typer.launch('https://guedesfelipe.github.io/pls-cli/')


@app.command(rich_help_panel='Utils and Configs')
def config():
    """Launch config directory :open_file_folder:"""
    center_print(Rule('・Opening config directory・', style='#d77dd8'))
    typer.launch(Settings().get_full_settings_path(), locate=True)
