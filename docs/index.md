<h1 align="center">
  💻  PLS-CLI
</h1>
<p align="center">
    <a href="https://github.com/guedesfelipe/pls-cli/actions/workflows/ci.yml" target="_blank">
        <img src="https://github.com/guedesfelipe/pls-cli/actions/workflows/ci.yml/badge.svg?branch=main" />
    </a>
    <a href="https://github.com/guedesfelipe/pls-cli/actions/workflows/security.yml" target="_blank">
        <img src="https://github.com/guedesfelipe/pls-cli/actions/workflows/security.yml/badge.svg?branch=main" />
    </a>
    <a href="https://codecov.io/gh/guedesfelipe/pls-cli" > 
      <img src="https://codecov.io/gh/guedesfelipe/pls-cli/branch/main/graph/badge.svg"/> 
    </a>
    <a href="https://pypi.org/project/pls-cli/" target="_blank">
      <img src="https://img.shields.io/pypi/v/pls-cli?label=pypi%20package" />
    </a>
    <a href="" target="_blank">
      <img src="https://img.shields.io/pypi/pyversions/pls-cli.svg?color=green&logo=python&logoColor=yellow" />
    </a>
    <img src="https://img.shields.io/badge/platforms-windows%7C%20linux%7C%20macos-lightgrey" />
</p>

<p align="center">
  <em>If you are like me, and your terminal is your home, this CLI will make your life better, I hope 😄</em>
  <br>
  <br>
  <img src="https://user-images.githubusercontent.com/25853920/175831710-20fa013d-5b83-4fe0-baf9-f035345c9192.gif" />
</p>

## 🛠 Installation

!!! success "Recommended: Using pipx (isolated environment)"

    [pipx](https://pipx.pypa.io/) installs the CLI in an isolated environment, avoiding conflicts with other packages:

    ```sh
    # Install pipx if you haven't already
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath

    # Install pls-cli
    pipx install pls-cli
    ```

!!! info "Alternative: Using pip"

    ```sh
    pip install pls-cli
    ```

    !!! warning
        Installing with pip may cause dependency conflicts with other packages. We recommend using pipx for CLI tools.

!!! tip "Upgrade Version"

    === "With pipx (recommended)"

        ```sh
        pipx upgrade pls-cli
        ```

    === "With pip"

        ```sh
        pip install pls-cli --upgrade
        ```

## 🧑‍💻 Run from source

To run or develop the version of PLS-CLI in a cloned repository, install
Python 3.9+ and [uv](https://docs.astral.sh/uv/), then run:

```sh
git clone https://github.com/guedesfelipe/pls-cli.git
cd pls-cli
uv sync --only-group test
uv run pls --help
```

`uv sync` creates a project-local `.venv` environment from
`pyproject.toml` and `uv.lock`. The `.venv` directory should not be
committed; it can be recreated from those files.

!!! tip "Verify changes"

    Run the automated tests before sharing a change:

    ```sh
    uv run pytest -q
    ```

## ⚙️ Configuration

To run **`pls-cli`** everytime you open your shell's:


=== "Bash"

    ```sh
    echo 'pls' >> ~/.bashrc
    ```

=== "Zsh"

    ```sh
    echo 'pls' >> ~/.zshrc
    ```

=== "Fish"

    ```sh
    echo 'pls' >> ~/.config/fish/config.fish
    ```

=== "Ion"

    ```sh
    echo 'pls' >> ~/.config/ion/initrc
    ```

=== "Tcsh"

    ```sh
    echo 'pls' >> ~/.tcshrc
    ```

=== "Xonsh"

    ```sh
    echo 'pls' >> ~/.xonshrc
    ```

=== "Powershell"

    Add the following to the end of `Microsoft.PowerShell_profile.ps1`. You can check the location of this file by querying the `$PROFILE` variable in PowerShell. Typically the path is `~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` or `~/.config/powershell/Microsoft.PowerShell_profile.ps1` on -Nix.
     
    ```txt
    pls
    ```

!!! attention

    Restart your terminal to apply the changes and start configuring your PLS-CLI. 🎉

## 🤝 Special thanks

**PLS-CLI** stands on the shoulders of giants:

* <a href="https://github.com/tiangolo/typer" target="_blank">Typer</a> for the CLI tool.
* <a href="https://github.com/Textualize/rich" target="_blank">Rich</a> for the beautiful formatting in terminal.

---

<p align="center">
  <a href="https://github.com/sponsors/guedesfelipe" target="_blank">
    <img src="https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github" />
  </a>
</p>
