from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
    
class Simulation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    name = db.Column(db.String(100), nullable=False)

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulation.id'))
    name = db.Column(db.String(30), nullable = False)
    mass = db.Column(db.Float, nullable=False)
    pos_x = db.Column(db.Float, nullable=False)
    pos_y = db.Column(db.Float, nullable=False)
    v_x = db.Column(db.Float, nullable=False)
    v_y = db.Column(db.Float, nullable=False)

