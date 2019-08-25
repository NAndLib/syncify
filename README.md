# syncify

## Introduction

A tool for Spotify that syncs all saved songs to a shareable playlist.

Since Spotify doesn't give the option to share saved songs, the next best option
is to create a playlist of *all* saved songs and share that playlist. But this
quickly becomes unmanagable as the playlist is updated. This script is meant to
make that a bit more bearable.

## Installation

The script requires python 3+.

Run `pip3 install -r requirements.txt` to install all requirements.

To run it from everywhere, run:
```
python syncify.py [--install] [--install-user]
```
`--install` will create an executable file in `/usr/bin`, or `$HOME/bin/` if
`--install-user` is used.

For the script to run correctly, you'll need to edit `config.py.template` with
the appropriate values first.

Many methods require user authentication. For these requests you will need to
generate an authorization token that indicates that the user has granted
permission for your application to perform the given task. You will need to
[register your
app](https://developer.spotify.com/my-applications/#!/applications) to get the
client ID and client secret.

Even if your script does not have an accessible URL you need to specify one
after registering your application in the "Edit Settings" panel where the
spotify authentication API will redirect to after successful login. The URL
doesn’t need to work or be accessible, you can specify “http://localhost/”,
after successful login you just need to copy the “http://localhost/?code=...”
URL from your browser and paste it to the console where the script is running.

## Usage

After to you have the proper configurations, run:
```python
python3 syncify.py
```
If you've "installed" it, simply run `syncify` from anywhere.

## Arguments

- `--help`: show all command line arguments.
- `--install`: create an executable in `/usr/bin`.
- `--install-user`: create an executable in `$HOME/bin`.
- `--continuous [INTERVAL]`: run the script every INTERVAL seconds.
- `--stdout`: change the output for stdout.
- `--stderr`: change the output for stderr.
