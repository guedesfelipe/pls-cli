<h1 align="center">
  ⌨️ Commands
</h1>

```sh
pls --help
```

```
 Usage: pls [OPTIONS] COMMAND [ARGS]...

 💻 PLS-CLI
 ・Minimalist and full configurable greetings and TODO list・

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ add          Add a Task ✨ (Add task name inside quotes)                     │
│ clean        Clean up tasks marked as done 🧹                                │
│ clear        Clear all tasks 🗑                                              │
│ del          Delete a Task                                                   │
│ done         Mark a task as done ✓                                           │
│ edit         Edit a task by id ✏️  (Add task name inside quotes)             │
│ insert       Insert a task after an existing task                            │
│ move         Change task position by floating 🎈 or sinking ⚓              │
│ swap         Swap the positions of two tasks 🔀                              │
│ tasks        Show all Tasks 📖                                               │
│ undone       Mark a task as undone ○                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Utils and Configs ──────────────────────────────────────────────────────────╮
│ callme         Change name 📛 (without resetting data)                       │
│ config         Show config directory path 📂                                 │
│ docs           Launch docs Website 🌐                                        │
│ quotes         Show quotes 🏷                                                │
│ tasks-progress Show tasks progress 🎯                                        │
│ setup          Reset all data and run setup 🔧                               │
│ version        Show version 🔖                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Integration ────────────────────────────────────────────────────────────────╮
│ count-done                    Count done tasks 📈                            │
│ count-undone                  Count undone tasks 📉                          │
╰──────────────────────────────────────────────────────────────────────────────╯

 Made with ❤ by Felipe Guedes
```

## ➕ Insert a task

Insert a task after an existing task by using its current ID:

```sh
pls insert 2 "third task"
```

This inserts `third task` after task `2`. Tasks that were after task `2`
automatically receive their new displayed IDs. Task names with spaces must be
wrapped in quotes.

!!! note

    The ID must be an existing task ID, from `1` through the current number of
    tasks. Inserting into an empty list, using `0`, or using an ID beyond the last
    task displays an error.

PLS-CLI asks for confirmation before changing the list. Enter `y` to insert
and save the task, or `N` to leave the list unchanged.

## ✏️ Edit a task

```sh
pls edit 1 "new task name"
```

PLS-CLI asks for confirmation before editing. Answering `N` keeps the task
unchanged.

## 🎈 Move vs 🔀 Swap

```sh
pls move 1 3   # moves task 1 to position 3, shifting the tasks in between
pls swap 1 3   # exchanges the positions of tasks 1 and 3
```

## 📂 Config directory

```sh
pls config
```

Shows the path of the directory where PLS-CLI stores its settings and tasks.
