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
import click
from flask.cli import FlaskGroup
from flask_migrate import Migrate
import datetime

from app import app, db
from blueprints.LoginApp.models import User

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)

# Create the FlaskGroup instance
cli = FlaskGroup(app)

@app.cli.command("create_admin")
@click.argument("name", required=False, default="admin")
def create_admin(name):
    """Creates the admin user."""
    db.session.add(User(name=name, username="ad@min.com", email="ad@min.com", password="admin", admin=True, is_confirmed=True,
        confirmed_on=datetime.datetime.now())) # admin doesn't need email confirmation
    db.session.commit()

if __name__ == '__main__':
    cli()