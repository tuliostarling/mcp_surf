import uvicorn
import config.gunicorn_runner as gunicorn_runner
import config.settings as settings


def main():
    if settings.AppSettings().reload:
        uvicorn.run(
            "web.application:get_app",
            host=settings.AppSettings().host,
            port=settings.AppSettings().port,
            reload=settings.AppSettings().reload,
            log_level=settings.AppSettings().log_level.value.lower(),
            factory=True,
        )
    else:
        gunicorn_runner.GunicornApplication(
            "web.application:get_app",
            host=settings.AppSettings().host,
            port=settings.AppSettings().port,
            workers=settings.AppSettings().workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.AppSettings().log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',
        ).run()


if __name__ == "__main__":
    main()
