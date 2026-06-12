import logging

import click
import uvicorn
from passlib import hosts

from src.infrastructure.config import settings


@click.group()
def cli():
    pass


@cli.command()
def start_api():
    uvicorn.run(
        "src.main:create_app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        factory=True,
    )


if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    cli()
