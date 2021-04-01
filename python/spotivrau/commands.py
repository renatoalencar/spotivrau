import click
import mongoengine as db

from spotivrau.app import app, setup_app
from spotivrau.jobs import worker

@app.cli.command()
def work():
    click.echo('Starting worker')
    worker.work_loop()
