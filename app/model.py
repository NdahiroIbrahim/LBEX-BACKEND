from app import db

class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Business {self.name}>"