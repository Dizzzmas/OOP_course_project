from ocp.db import db


def drop_all_tables(app):
    if not app.config["DEV_DB_SCRIPTS_ENABLED"]:
        raise Exception("Please don't wipe production DB")
    db.engine.execute("DROP SCHEMA public CASCADE")
    db.engine.execute("CREATE SCHEMA public")


def init_cli(app, manager):
    if app.debug:
        # seed
        from ocp.db.fixtures import seed_db

        @app.cli.command("seed", help="Seed DB with test data")
        def seed_db_cmd():
            seed_db()

        manager.add_command(seed_db_cmd)

        # init-db
        @app.cli.command(
            "init-db", help="Reinitialize database from scratch (deletes all data)"
        )
        def init_db_cmd():
            print(f"Initializing {db.engine.url}")
            db.drop_all(app=app)
            db.create_all(app=app)
            print("Initialized DB")

        manager.add_command(init_db_cmd)

        @app.cli.command("drop-db", help="Drop every table in the database")
        def drop_db_cmd():
            print(f"Dropping all tables in {db.engine.url}")
            db.reflect(app=app)
            db.drop_all(app=app)
            print("Success")

        manager.add_command(drop_db_cmd)

        # config check
        @app.cli.command("config", help="View configuration")
        def config_cmd():
            import pprint

            pprint.pprint(app.config)

        manager.add_command(config_cmd)
