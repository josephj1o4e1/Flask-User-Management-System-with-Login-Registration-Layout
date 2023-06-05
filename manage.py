# import click
# from flask.cli import FlaskGroup

# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
# import os

# from app import app, db

# app.config.from_object(os.environ['APP_SETTINGS'])
# migrate = Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)

# if __name__ == '__main__':
#     manager.run()


import os
from flask import Flask
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)

# Create the FlaskGroup instance
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()