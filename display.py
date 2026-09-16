from flask import Flask, render_template, jsonify, request
from simulator import Simulator
from celestial_body import Body

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('website.html')

earth = Body("Planet B",6e24,0,29783,1.6e11,0)
sun = Body("Planet A", 2e30,0,0,0,0)

sim = Simulator([earth, sun],50000) #this creates an object inside the Simulator class with the bodies in them and with a time step

@app.route('/sim')
def simulate():
    positions = []
    sim.step()
    for body in sim.bodies:
        pos_holder = {"x": body.p_x, "y": body.p_y}
        positions.append(pos_holder)
    return jsonify(positions)

@app.route('/update_planet', methods=['POST'])
def update_planet():
    data = request.get_json()
    for body in sim.bodies:
        if body.name == data["planet_name"]:
            body.mass = data["data"]["mass"]
            body.v_x = data["data"]["v_x"]
            body.v_y = data["data"]["v_y"]
            body.p_x = data["data"]["pos_x"]
            body.p_y = data["data"]["pos_y"]
    return jsonify({"status": "ok"})

@app.route('/reset',methods=['POST'])
def reset():
    earth.mass = 6e24
    earth.v_x = 0
    earth.v_y = 29783
    earth.p_x = 1.6e11
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

if __name__ == '__main__':
    app.run(debug = True)