import math
G = 6.674e-11

class Body:
    def __init__(self, mass, v_x, v_y, p_x, p_y):  #creating the class of a planet and its attributes within it
        self.mass = mass
        self.v_x = v_x
        self.v_y = v_y
        self.p_x = p_x
        self.p_y = p_y

    def calculate_force(self, other):
        distance = (((self.p_x - other.p_x)**2) + ((self.p_y - other.p_y)**2)) ** 0.5 #calculating the distance through pythagoras
        if distance == 0:
            raise ValueError("Bodies occupied the same position. Haven't made collisions yet") #will come back to this later when the first version is done
        force = ( G * self.mass * other.mass) / (distance ** 2) #newtons gravity equation to find force
        return force
    
#   def update_position(self, dt):
#        self.p_x = self.p_x + (self.v_x * dt)
#        self.p_y = self.p_y + (self.v_y * dt)
#
#    def update_velocity(self,force_x,force_y, dt):
#        acc_x = force_x / self.mass                 This all got removed because of switching from Euler to Verlert
#        acc_y = force_y / self.mass
#        self.v_x = self.v_x + (acc_x * dt)
#        self.v_y = self.v_y + (acc_y * dt) 

    def split_force(self, other):
        theta = math.atan2((other.p_y - self.p_y) , (other.p_x - self.p_x)) #calculating the angle the planets make with each other based on their distance apart
        force = self.calculate_force(other)
        force_x = force * math.cos(theta) #resolving forces into vertical and horizontal components
        force_y = force * math.sin(theta)
        return force_x, force_y
    