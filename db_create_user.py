from app import app
from app import db
from models import User

with app.app_context(): 
    # Delete all data rows in table "users" including the referenced data such as in the table "posts". 
    db.session.execute(db.text('TRUNCATE TABLE users CASCADE'))
    # insert data for quick demo
    db.session.add(User("JosephChuang", "chuang@iu.edu", "chuang@iu.edu", "josephchuang"))
    db.session.add(User("JosephChuang", "JosephChuang123", "chuang2@iu.edu", "josephchuang"))
    db.session.add(User("StephCurry", "StephCurry", "curry@gmail.com", "stephcurry"))
    db.session.add(User("BabeRuth", "BabeRuth", "ruth@gmail.com", "baberuth"))
    db.session.add(User("TomBrady", "TomBrady", "brady@hotmail.com", "tombrady"))
    db.session.add(User("NikolaJokic", "NikolaJokic", "jokic@yahoo.com", "nikolajokic"))
    db.session.add(User("ShoheiOhtani", "ShoheiOhtani", "ohtani@gmail.com", "shoheiohtani"))
    db.session.add(User("KevinDurant", "KevinDurant", "durant@hotmail.com", "kevindurant"))

    # db.session.add(User("Bill Gates", "Bill Gates", "gates@hotmail.com", "Microsoft1#"))

    # commit the changes
    db.session.commit()