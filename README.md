# Marionette Test

A proof of concept of running a marionette script against a headless Thunderbird ESR in a github actions workflow.

The output is saved as an artifact.

![An example screenshot of the output from the github actions runner.](docs/out.png)

## Setup

This project uses [rye](https://rye.astral.sh/). Alternatively just run `pip install -r requirements.lock` to get started.

## Running


``` bash
M_THUNDERBIRD_BIN=<path to thunderbird-bin> M_THUNDERBIRD_PROFILE=./profiles/website python src/marionette/main.py` 
```

## Fake Mailserver

Create a user in the UI with:
* User: me@example.org
* Pass: test

`docker run --rm -it -p 5000:80 -p 2525:25 -p 143:143 rnwood/smtp4dev`

Adjust `src/marionette/fake_mail.yml` to your liking, and then run `src/marionette/send_fake_mail.py`.