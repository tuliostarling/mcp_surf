import multiprocessing, uvicorn
from config import settings, gunicorn_runner


def run_mcp():
    uvicorn.run(
        "services.mcp.application:get_app",
        host="0.0.0.0",
        port=9000,
        reload=False,
        factory=True,
        log_level="info",
    )


def run_web(dev: bool):
    if dev:
        uvicorn.run(
            "services.web.application:get_app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            factory=True,
            log_level="info",
        )
    else:
        cfg = settings.AppSettings()
        gunicorn_runner.GunicornApplication(
            "services.web.application:get_app",
            host=cfg.host,
            port=cfg.port,
            workers=cfg.workers_count,
            factory=True,
            accesslog="-",
            loglevel=cfg.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',
        ).run()


def main():
    dev_mode = settings.AppSettings().reload
    mcp_proc = multiprocessing.Process(target=run_mcp, daemon=True)
    mcp_proc.start()

    try:
        run_web(dev_mode)
    finally:
        mcp_proc.terminate()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
