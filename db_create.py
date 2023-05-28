from app import app
from app import db
from models import BlogPost

with app.app_context(): # to establish an application context. It ensures that the necessary application context is set up before interacting with the database using `db.session`.
    # drop tables for the default bind
    db.drop_all(bind_key=None)
    
    # create the database and the db table
    # initializes the database based on the schema we defined in models.py
    db.create_all()
    
    # insert data
    db.session.add(BlogPost("Good", "I\'m good."))
    db.session.add(BlogPost("Well", "I\'m well."))
    db.session.add(BlogPost("Excellent", "I\'m excellent."))
    db.session.add(BlogPost("Okay", "I\'m okay."))
    db.session.add(BlogPost("Okay2", "I\'m okay 2."))

    # commit the changes
    db.session.commit()