import numpy as np

class CelestialBody:
    def __init__(self, mass, position, velocity, radius_px=None, name='body', color=(150, 150, 150), period=-1):
        """
        Parameters:
        mass (float): The mass of the celestial body in kilograms.
        position (list or numpy.ndarray): The initial position of the celestial body in 3D space.
        velocity (list or numpy.ndarray): The initial velocity of the celestial body in 3D space.
        radius_px (float, optional): The radius of the celestial body. Default: None.
        name (str, optional): The name of the celestial body. Default: 'body'.
        color (tuple, optional): The color of the celestial body. Default: (150, 150, 150).
        period (float, optional): The orbital period of the celestial body. Default: -1.
        """
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.radius_px = radius_px # for plotting purposes
        self.name = name # for plotting purposes
        self.color = color # for plotting purposes
        self.period = period # orbital period (also needed for plotting)
        
    def reposition(self, position):
        """
        Updates the position of the celestial body.

        Parameters:
        position (list or numpy.ndarray): The new position of the celestial body in 3D space.

        Returns:
        None. The function updates the 'position' attribute of the celestial body instance.
        """
        self.position = np.array(position)
    
    def accelerate(self, a, time):
        """
        Updates the velocity of the celestial body by applying a constant acceleration.

        Parameters:
        a (numpy.ndarray): The acceleration vector in 3D space.
        time (float): The time duration for which the acceleration is applied.

        Returns:
        None. The function updates the 'velocity' attribute of the celestial body instance.
        """
        self.velocity += a * time