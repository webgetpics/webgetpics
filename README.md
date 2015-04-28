# webgetpics

Command line tool to put pictures from web search to X desktop background.
For more information please see [homepage](http://www.webgetpics.org).

# Installation

There's a [package](https://aur.archlinux.org/packages/webgetpics) for Arch
Linux. Feel free to use it as a reference when installing on your target
platform.

# Running

Create working directory where all program files will be stored:
```
mkdir <<<my-work-dir>>>
cd <<<my-work-dir>>>
```

Copy and edit config file:
```
cp /usr/lib/webgetpics/config.py .
vi config.py
```

Run: `webgetpics`

To exit press `Ctrl-C`.
This may take some time, you might want to track progress in logs.

# Commands

All interactions with webgetpics are done through file system.
Some commands may take time to apply, you might want to track progress in logs.
This sections describe how to do some typical operations.

View logs: `tail -f log/*.log`

Change web search string: `echo pablo picasso paintings > query.txt`

Show current web search string: `cat query.txt`

Download original version of currently shown picture:
  `wget $(cat show/out/current.url)`

Show next picture: `touch show/cmd/skip`

Never show current picture for current web search string:
  `touch show/cmd/hide-query`

Never show current picture for any web search strings:
  `touch show/cmd/hide/global`

# Contact

Oleg Plakhotniuk: contact@webgetpics.org
