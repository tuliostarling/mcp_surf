from gunicorn.app.base import BaseApplication
from gunicorn.util import import_app
from uvicorn.workers import UvicornWorker as BaseUvicornWorker

try:
    import uvloop
except ImportError:
    uvloop = None


class UvicornWorker(BaseUvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop" if uvloop else "asyncio",
        "http": "httptools",
        "lifespan": "on",
        "factory": True,
        "proxy_headers": True,
    }


class GunicornApplication(BaseApplication):
    def __init__(self, app, host, port, workers, **kwargs):
        self.options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "worker_class": "config.gunicorn_runner.UvicornWorker",
            "timeout": 120,
            "keepalive": 5,
            **kwargs,
        }
        self.app = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return import_app(self.app)
