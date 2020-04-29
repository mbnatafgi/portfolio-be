# Welcome to the backend repository of my personal portfolio!

The point of this application is to serve my CLI, in which users can get more info about me (resume-like info) using some
commands and arguments, over WebSockets.

There are three main functions that make this happen (can be found under the ```src``` directory):

1. **cli.py**: acts as the custom CLI using the well-known [```click```](https://click.palletsprojects.com/en/7.x/) Python library.
2. **server.py**: acts as the WebSockets server using the [```websockets```](https://websockets.readthedocs.io/en/stable/intro.html) Python library.
3. **resume.yaml**: acts as the store of my info in which the CLI reads data from.

The trickiest part was to capture the output of the CLI (stdout) after some command into a buffer (StringIO) and send it
to the frontend in a structured manner.

## Requirements

+ Python 3.7 or later since I like using f-strings!

## Usage

You can run the server in two simple steps:
>
```
python3 -m pip install --user -r requirements.txt
python3 -m src
```