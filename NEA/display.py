from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from simulator import Simulator
from celestial_body import Body
from database import db, User, Simulation, Planets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
next_id = 3
@app.route('/')
def index():
        if 'user_id' not in session:
            return redirect(url_for('account'))
        return render_template('website.html')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orbits.db' #shows that the database is using sqlite and being stored in a file called orbits.db
app.config['SECRET_KEY'] = '49StMaur10Caboni!' 
db.init_app(app) #connetcs database to flask
with app.app_context():
    db.create_all()

earth = Body("Earth",6e24,0,29783,1.6e11,0,1)
sun = Body("Sun", 2e30,0,0,0,0,2)

sim = Simulator([earth, sun],50000) #this creates an object inside the Simulator class with the bodies in them and with a time step

@app.route('/sim')
def simulate():
        positions = []
        for body in sim.bodies:
            print(body.name, body.p_x, body.p_y)
        sim.step()
        for body in sim.bodies:
            pos_holder = {"x": body.p_x, "y": body.p_y, "id": body.id}
            positions.append(pos_holder)
        return jsonify(positions)

@app.route('/update_planet', methods=['POST'])
def update_planet():
    
    data = request.get_json()
    found = False
    for body in sim.bodies:
        global next_id
        if body.id == data["planet_id"]:
            found = True
            body.name = data["data"]["name"]
            body.mass = data["data"]["mass"]
            body.v_x = data["data"]["v_x"]
            body.v_y = data["data"]["v_y"]
            body.p_x = data["data"]["pos_x"]
            body.p_y = data["data"]["pos_y"]
    if found == False:
        new_planet = Body(data["data"]["name"], data["data"]["mass"], data["data"]["v_x"], data["data"]["v_y"], data["data"]["pos_x"], data["data"]["pos_y"], next_id)
        next_id += 1
        sim.bodies.append(new_planet)
    return jsonify({"status": "ok"})

@app.route('/reset',methods=['POST'])
def reset():
    earth.mass = 6e24
    earth.v_x = 0
    earth.v_y = 29783
    earth.p_x = 1.5e11
    earth.p_y = 0
    sun.mass = 2e30
    sun.v_x = 0
    sun.v_y = 0
    sun.p_x = 0
    sun.p_y = 0

    return jsonify({"status":"ok"})

@app.route('/update_dt',methods=['POST'])
def update_dt():
    data = request.get_json()
    sim.dt = data["dt"]
    return jsonify({"status":"ok"})

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:

            return render_template("account.html", error = "That username has been taken.")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username , password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('index'))

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password , password):
            session['user_id'] = user.id
            return redirect(url_for('index'))           
        else:
            return render_template("account.html", error = "Username or password not found") 

@app.route('/account', methods=['GET'])
def account():
    return render_template("account.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('account'))

@app.route('/save', methods=['POST'])
def save():
    planet_dictionary = request.get_json() 
    new_simulation = Simulation(
        user_id = session['user_id'],
        name = planet_dictionary.get('name'),
    )
    db.session.add(new_simulation)
    db.session.commit()
    for planet in planet_dictionary['planets'].values():
        new_record = Planets(
            simulation_id = new_simulation.id,
            name = planet['name'],
            mass = planet['mass'],
            pos_x = planet['pos_x'],
            pos_y = planet['pos_y'],
            v_x = planet['v_x'],
            v_y = planet['v_y']
        )
        db.session.add(new_record)
    db.session.commit()
    return jsonify({"status" : "success"})

@app.route('/display_saves', methods=["POST"])
def display_saves():
    saved_sims = db.session.query(Simulation).filter(Simulation.user_id == session['user_id']).all()
    sim_list = []
    for sim in saved_sims:
        sim_list.append({
            "id": sim.id,
            "name": sim.name
        })
    return jsonify(sim_list)

if __name__ == '__main__':
    app.run(debug = True)