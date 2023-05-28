from app import db

class BlogPost(db.Model):
    
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self): # specify how we want the object be represented when it's printed. 
        return '<title {}, desc {}'.format(self.title, self.description)
    