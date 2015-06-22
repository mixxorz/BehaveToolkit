# Behave Toolkit
BehaveToolkit provides integration between Sublime Text 3 and Behave.

## Features:

* Run specific scenarios
* Generate step definitions
* Go to step definition
* Highlight undefined steps

## Highlights

<table>
    <tr>
        <th>Highlight Undefined Steps</th>
        <th>Generate Step Definition</th>
    </tr>
    <tr>
        <td width="50%">
            <a href="http://zippy.gfycat.com/NiceBlackandwhiteGreyhounddog.webm">
                <img src="http://fat.gfycat.com/NiceBlackandwhiteGreyhounddog.gif" alt="Highlight Undefined Steps">
            </a>
        </td>
        <td width="50%">
            <a href="http://zippy.gfycat.com/CalmWarmheartedBufflehead.webm">
                <img src="http://giant.gfycat.com/CalmWarmheartedBufflehead.gif" alt="Generate Step Definition">
            </a>
        </td>
    </tr>
</table>
<table>
    <tr>
        <th>Generate Missing Step Definitions</th>
        <th>Run Specific Scenario</th>
    </tr>
    <tr>
        <td width="50%">
            <a href="http://zippy.gfycat.com/InferiorIllinformedClingfish.webm">
                <img src="http://giant.gfycat.com/InferiorIllinformedClingfish.gif" alt="Generate Missing Step Definitions">
            </a>
        </td>
        <td width="50%">
            <a href="http://zippy.gfycat.com/ScrawnyNegligibleAlligator.webm">
                <img src="http://giant.gfycat.com/ScrawnyNegligibleAlligator.gif" alt="Run Specific Scenario">
            </a>
        </td>
    </tr>
</table>

## Installation

### Package Control

1. Install the [Sublime Text Package Control](https://packagecontrol.io/) plugin if you don't have it already.
2. Open the command palette and start typing `Package Control: Install Package`.
3. Enter `BehaveToolkit`.

### Via Git

You can also clone the repo directly to your Packages folder if you so wish:

```
# on a Mac
cd "$HOME/Library/Application Support/Sublime Text 3/Packages"
# on Linux
cd $HOME/.config/sublime-text-3/Packages
# on Windows (PowerShell)
cd "$env:appdata\Sublime Text 3\Packages\"

git clone https://github.com/mixxorz/BehaveToolkit
```

## Setup

BehaveToolkit requires `behave` to be installed. If you haven't already, you can install it using `pip`.

```

$ pip install behave

```

By default, behave will be launched using the value returned by `which behave`. If you want to modify the way behave gets launched (if you're using a virtualenv, for example), you need to update the "behave_command" setting in your project file.

```

{
  "settings":
  {
    "behave_command": ["/path/to/virtualenv/bin/behave"]
  }
}

```

You can now start using BehaveToolkit by opening your command palette, typing `Behave` and selecting the action you want to do. Certain actions can only be done when certain files are open. (e.g. "Go to step definition" only shows up when you have a feature file open.)

## How to Contribute

Please read the [contributing guide](CONTRIBUTING.md).


