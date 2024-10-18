"""Models for Cupcake app."""

default_img = "https://tinyurl.com/demo-cupcake"

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """blogly user"""
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    flavor = db.Column(db.String, 
                         nullable=False)
    
    size = db.Column(db.String, 
                          nullable=False)
    
    rating = db.Column(db.Float, 
                          nullable=False)
    
    image = db.Column(db.String, 
                      nullable=False, 
                      default=default_img)

    def __repr__(self):
        c = self
        return f"<Flavor ={c.flavor} size={c.size} rating={c.rating}>"
