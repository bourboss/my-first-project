from flask import Flask, render_template, jsonify #importing flask and rendertemplate so that flask can display a web page
from simulator import Simulator
from celestial_body import Body

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

earth = Body(6e24,0,29783,1.5e11,0)
sun = Body(2e30,0,0,0,0)

sim = Simulator([earth, sun],3600) #this creates an object inside the Simulator class with the bodies in them and with a time step

@app.route('/sim')
def simulate():
    positions = []
    sim.step()
    for body in sim.bodies:
        pos_holder = {"x": body.p_x, "y": body.p_y}
        positions.append(pos_holder)
    return jsonify(positions)


if __name__ == '__main__':
    app.run()