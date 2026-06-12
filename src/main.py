from src.app_injector import app_injector
from src.serve_api import ServeApi


def create_app():
    return ServeApi(injector=app_injector).create_app()
