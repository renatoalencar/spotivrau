import click
import mongoengine as db

from .app import app, worker, setup_app


@app.cli.command()
def work():
    click.echo('Starting worker')
    worker.work_loop()
