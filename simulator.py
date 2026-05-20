from celestial_body import Body

class Simulator:
    def __init__(self,bodies,dt):
        self.bodies = bodies #creates the class
        self.dt = dt
    
    def step(self):
        acceleration = {}
        for body in self.bodies:
            total_force_x = 0
            total_force_y = 0
            for other in self.bodies:
                if body is other:
                    continue #skips this loop if checking one body against itself as thats pointless
                fx, fy = body.split_force(other) #calculates the horizontal and vertical components of the force acting on the body other
                total_force_x = total_force_x + fx #adds the forces to the total force
                total_force_y = total_force_y + fy
            acceleration[id(body)] = ((total_force_x/ body.mass), (total_force_y/body.mass)) #calculates the vertical and horizontal acceleration components

        for body in self.bodies:
            acceleration_x, acceleration_y = acceleration[id(body)]
            body.p_x = body.p_x + body.v_x * self.dt + 0.5 * acceleration_x * (self.dt)**2 #uses suvat equations to calculate a body's new position off their acceleration and velocities
            body.p_y = body.p_y + body.v_y * self.dt + 0.5 * acceleration_y * (self.dt)**2

        new_acceleration = {}
        for body in self.bodies: #this finds the new acceleration AFTER a planet has moved, as the acc will not stay the same and it needs to get updated before the next step
            total_force_x = 0
            total_force_y = 0
            for other in self.bodies:
                if body is other:
                    continue
                fx, fy = body.split_force(other)
                total_force_x = total_force_x + fx
                total_force_y = total_force_y + fy 
            new_acceleration[id(body)] = ((total_force_x/body.mass),(total_force_y/body.mass))

        for body in self.bodies:
            acceleration_x, acceleration_y = acceleration[id(body)]
            new_acceleration_x, new_acceleration_y = new_acceleration[id(body)]
            body.v_x = body.v_x + 0.5 * (acceleration_x + new_acceleration_x) * self.dt
            body.v_y = body.v_y + 0.5 * (acceleration_y + new_acceleration_y) * self.dt

    def run(self, steps):
        for i in range(0, steps):
            self.step()