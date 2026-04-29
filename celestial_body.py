import math
G = 6.674e-11

class Body:
    def __init__(self, mass, v_x, v_y, p_x, p_y): 
        self.mass = mass
        self.v_x = v_x
        self.v_y = v_y
        self.p_x = p_x
        self.p_y = p_y

    def calculate_force(self, other):
        distance = (((self.p_x - other.p_x)**2) + ((self.p_y - other.p_y)**2)) ** 0.5
        if distance == 0:
            raise ValueError("Bodies occupied the same position. Haven't made collisions yet")
        force = ( G * self.mass * other.mass) / (distance ** 2)
        return force
    
    def update_position(self, dt):
        self.p_x = self.p_x + (self.v_x * dt)
        self.p_y = self.p_y + (self.v_y * dt)

    def update_velocity(self,force_x,force_y, dt):
        acc_x = force_x / self.mass
        acc_y = force_y / self.mass

        self.v_x = self.v_x + (acc_x * dt)
        self.v_y = self.v_y + (acc_y * dt)

    def split_force(self, other):
        theta = math.atan2((self.p_y - other.p_y) , (self.p_x - other.p_x))
        force = self.calculate_force(other)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)

        return force_x, force_y
    