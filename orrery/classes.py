import numpy as np

class CelestialBody:
    def __init__(self, mass, position, velocity, radius_px=None, name='body'):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.radius_px = radius_px # for plotting purposes
        self.name = name # for plotting purposes
        
    def reposition(self, position):
        self.position = np.array(position)
    
    def accelerate(self, a, time):
        self.velocity += a * time