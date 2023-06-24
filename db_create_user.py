from app import app
from app import db
from models import User

with app.app_context(): 
    # Delete all data rows in table "users" including the referenced data such as in the table "posts". 
    db.session.execute(db.text('TRUNCATE TABLE users CASCADE'))
    # insert data for quick demo
    db.session.add(User("JosephChuang", "chuang@iu.edu", "josephchuang"))
    db.session.add(User("StephCurry", "curry@gmail.com", "stephcurry"))
    db.session.add(User("BabeRuth", "ruth@gmail.com", "baberuth"))
    db.session.add(User("TomBrady", "brady@hotmail.com", "tombrady"))
    db.session.add(User("NikolaJokic", "jokic@yahoo.com", "nikolajokic"))
    db.session.add(User("ShoheiOhtani", "ohtani@gmail.com", "shoheiohtani"))
    db.session.add(User("KevinDurant", "durant@hotmail.com", "kevindurant"))
    # db.session.add(User("admin", "ad@min.com", "admin"))
    # db.session.add(User("Bill Gates", "gates@hotmail.com", "Microsoft1#"))

    # commit the changes
    db.session.commit()