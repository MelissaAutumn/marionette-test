# Marionette Test

A proof of concept of running a marionette script against a headless Thunderbird ESR in a github actions workflow.

The output is saved as an artifact.

![An example screenshot of the output from the github actions runner.](docs/out.png)

## Setup

This project uses [rye](https://rye.astral.sh/). Alternatively just run `pip install -r requirements.lock` to get started.

## Running

Run any Thunderbird application with the arguments `--headless --marionette` and then run the python script located in `src/marionette/main.py`.