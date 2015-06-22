# Behave Toolkit
BehaveToolkit provides integration between Sublime Text 3 and Behave.

## Features:

* Run specific scenarios
* Go to step definition
* Generate step definitions

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

git clone https://github.com/mixxorz/sublime-behave-toolkit
```

## Setup

BehaveToolkit requires `behave` to be installed. If you haven't already, you can
install it using `pip`.

```

$ pip install behave

```

If you're installing inside a virtualenv, you need to update the
"python_interpreter" setting in your project file.

```

{
  "settings":
  {
    "python_interpreter": "/path/to/virtualenv/bin/python"
  }
}

```

You can now start using BehaveToolkit by opening your command palette
`Super + Shift + P`(`Ctrl + Shift + P` on Windows), typing `Behave` and
selecting the action you want to do.

Certain actions can only be done when certain files are open. (e.g. "Go to step
definition" only shows up when you have a feature file open.)

## How to Contribute

Please read the [contributing guide](CONTRIBUTING.md).


