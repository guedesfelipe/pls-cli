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

```sh
pip install pls-cli
```

!!! tip "Upgrade Version"

    ```sh
    pip install pls-cli --upgrade
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

## 🤝 Special thanks

**PLS-CLI** stands on the shouders of giants:

* <a href="https://github.com/tiangolo/typer" target="_blank">Typer</a> for the CLI tool.
* <a href="https://github.com/Textualize/rich" target="_blank">Rich</a> for the beautiful formatting in terminal.

---

<p align="center">
  <a href="https://ko-fi.com/guedesfelipe" target="_blank">
    <img src="https://user-images.githubusercontent.com/25853920/175832199-6c75d866-31b8-4209-bd1a-db116a6dd032.png" width=300 />
  </a>
</p>
