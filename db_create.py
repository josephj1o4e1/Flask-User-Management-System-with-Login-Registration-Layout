from app import app
from app import db
from models import BlogPost, User

with app.app_context(): # to establish an application context. It ensures that the necessary application context is set up before interacting with the database using `db.session`.
    # # drop tables for the default bind
    # db.drop_all(bind_key=None)
    
    # create the database and the db table
    # initializes the database based on the schema we defined in models.py
    db.create_all()
    
    # insert data
    user_curry=User.query.filter_by(name='StephCurry').first()
    user_ohtani=User.query.filter_by(name='ShoheiOhtani').first()
    user_durant=User.query.filter_by(name='KevinDurant').first()
    b1 = BlogPost("Good", "I\'m good.")
    b1.author=user_curry
    b2 = BlogPost("Well", "I\'m well.")
    b2.author=user_ohtani
    b3 = BlogPost("Excellent", "I\'m excellent.")
    b3.author=user_durant
    db.session.add(b1)
    db.session.add(b2)
    db.session.add(b3)

    # commit the changes
    db.session.commit()