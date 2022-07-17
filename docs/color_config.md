<h1 align="center">
  🎨 Color Configuration
</h1>

You can configure all colors with envs!!

=== "Linux, macOS, Windows Bash"

    ```sh
    export PLS_ERROR_LINE_STYLE="#e56767"
    ```

=== "Windows PowerShell"

    ```sh
    $Env:PLS_ERROR_LINE_STYLE = "#e56767"
    ```


All envs:
```sh
export PLS_ERROR_LINE_STYLE="#e56767"
export PLS_ERROR_TEXT_STYLE="#ff0000 bold"

export PLS_WARNING_LINE_STYLE="#FFBF00"
export PLS_WARNING_TEXT_STYLE="#FFBF00 bold"

export PLS_UPDATE_LINE_STYLE="#61E294"
export PLS_UPDATE_TEXT_STYLE="#61E294 bold"

export PLS_INSERT_DELETE_LINE_STYLE="#bb93f2"

export PLS_INSERT_DELETE_TEXT_STYLE="#a0a0a0"

export PLS_MSG_PENDING_STYLE="#61E294"
export PLS_TABLE_HEADER_STYLE="#844191"
export PLS_TABLE_HEADER_STYLE="#d77dd8"
export PLS_TASK_DONE_STYLE="#a0a0a0"
export PLS_TASK_PENDING_STYLE="#bb93f2"
export PLS_HEADER_GREETINGS_STYLE="#FFBF00"
export PLS_QUOTE_STYLE="#a0a0a0"
export PLS_AUTHOR_STYLE="#a0a0a0"
```


???+ tip "You can specify the background color like this:"


    ```sh
    export PLS_QUOTE_STYLE="#a0a0a0 on blue"
    ```

If you create some theme, share with us <a href="https://github.com/guedesfelipe/pls-cli/discussions/1#discussion-4174647" target="_blank">here</a> :heart:.

## 💄 Formatting a task

???+ info "You can format your tasks with:"


    ```sh
    pls add "[b]Bold[/], [i]Italic[/], [s]Strikethrough[/], [d]Dim[/], [r]Reverse[/], [red]Color Red[/], [#FFBF00 on green]Color exa with background[/], :star:, ✨"
    ```

    <img src="https://user-images.githubusercontent.com/25853920/175835339-8059bc7e-0538-4e2d-aed8-80487d7b2478.png" />


