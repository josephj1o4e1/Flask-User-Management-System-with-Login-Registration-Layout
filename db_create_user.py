from app import app
from app import db
from models import User

with app.app_context(): 
    # Delete all data rows in table "users" including the referenced data such as in the table "posts". 
    db.session.execute(db.text('TRUNCATE TABLE users CASCADE'))
    # insert data for quick demo
    db.session.add(User(name="JosephChuang", username="chuang@iu.edu", email="chuang@iu.edu", password="josephchuang"))
    db.session.add(User(name="JosephChuang", username="JosephChuang123", email="chuang2@iu.edu", password="josephchuang"))
    db.session.add(User(name="StephCurry", username="StephCurry", email="curry@gmail.com", password="stephcurry"))
    db.session.add(User(name="BabeRuth", username="BabeRuth", email="ruth@gmail.com", password="baberuth"))
    db.session.add(User(name="TomBrady", username="TomBrady", email="brady@hotmail.com", password="tombrady"))
    db.session.add(User(name="NikolaJokic", username="NikolaJokic", email="jokic@yahoo.com", password="nikolajokic"))
    db.session.add(User(name="ShoheiOhtani", username="ShoheiOhtani", email="ohtani@gmail.com", password="shoheiohtani"))
    db.session.add(User(name="KevinDurant", username="KevinDurant", email="durant@hotmail.com", password="kevindurant"))

    # db.session.add(User("Bill Gates", "Bill Gates", "gates@hotmail.com", "Microsoft1#"))
    # Zz00000#

    # commit the changes
    db.session.commit()