import logging
import os
from typing import Optional
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from nplusone.ext.flask_sqlalchemy import NPlusOne
from ocp.commands import init_cli
from ocp.db import db
from ocp.flaskapp import App

log = logging.getLogger(__name__)


def create_app(test_config: Optional[dict] = None) -> App:
    app = App("OCP")

    configure(app=app, test_config=test_config)

    CORS(app)
    configure_database(app)
    NPlusOne(app)

    # CLI
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)  # migrations under "flask db"
    init_cli(app, manager)

    return app


def configure_class(app: App) -> None:
    """Load class-based app configuration from config.py."""
    config_class = os.getenv("OCP_CONFIG".upper())

    if not config_class:
        config_class = "ocp.config.Config"

    app.config.from_object(config_class)


def configure_instance(app: App) -> None:
    """Loda instance.cfg if it exists as our local instance configuration override"""
    app.config.from_pyfile("instance.cfg", silent=True)


def configure(app: App, test_config=None) -> None:
    configure_class(app)
    config = app.config
    if test_config:
        config.update(test_config)
    else:
        configure_instance(app)

    if config.get("SQLALCHEMY_ECHO"):
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    from .config import check_valid

    if not check_valid(config):
        raise Exception("Configuration is not valid.")


def configure_database(app: App) -> None:
    """Set up flask with SQLAlchemy."""
    # configure options for create_engine
    engine_opts = app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {})

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = engine_opts

    db.init_app(app)  # init sqlalchemy
    app.migrate = Migrate(app, db)  # alembic

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Close session after request.

        Ensures no open transactions remain.
        """
        db.session.remove()

    if app.config.get("TESTING"):
        return

    test_db(app)


def test_db(app: App) -> None:
    # verify DB works
    try:
        with app.app_context():
            db.session.execute("SELECT 1").scalar()
    except Exception as ex:
        log.error(
            f"Database configuration is invalid. Using URI: {app.config['SQLALCHEMY_DATABASE_URI']}"
        )
        raise ex
