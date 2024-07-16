import numpy as np
from .parse_data import *
from .classes import CelestialBody
from .utils.resource_path import *


def create_celestial_bodies(which='inner'):
    """
    This function creates a list of celestial bodies based on the provided data.
    The celestial bodies are represented by the CelestialBody class.

    Parameters:
    which (str): A string indicating whether to create celestial bodies for the 'inner' or 'outer' solar system.
                 Default is 'inner'.
                 
    Returns:
    list: A list of CelestialBody objects representing the celestial bodies.
    date: The date of the input data.
    """
    # Constants in SI
    AU_SI = 1.496e11  # Astronomical unit [m]; set to one for computational purposes
    m0_SI = 1.989e30  # Mass of the sun [kg]; set to one for computational purposes
    G_SI = 6.67430e-11  # Gravitational constant [m^3 kg^-1 s^-2]
    day_SI = 3600 * 24  # One day [s]
    
    current_datetime, input_bodies = parse_data(resource_path("../resources/2024-Jan-01.txt"))
    current_date = current_datetime.date()
    radii_px = [15, 3, 3, 5, 4, 12, 10, 9, 7, 2]  # radii in pixels
    colors = (
            (255, 223, 0),  # Sun: Bright yellow
            (169, 169, 169),  # Mercury: Dark gray
            (255, 204, 153),  # Venus: Pale yellowish-brown
            (0, 102, 204),  # Earth: Blue (ocean) with hints of green (land)
            (210, 105, 30),  # Mars: Reddish-brown
            (255, 165, 0),  # Jupiter: Orange with bands
            (194, 178, 128),  # Saturn: Pale gold with bands
            (173, 216, 230),  # Uranus: Light blue
            (0, 0, 139),  # Neptune: Deep blue
            (169, 169, 169)  # Pluto: Light brown or gray
    )
    periods = ( 1,
                87.97,
                224.70,
                365.25,
                686.98,
                4332.82,
                10755.70,
                30687.15,
                60190.03,
                90560
                )
    
    celestial_bodies = []
    for i, input_body in enumerate(input_bodies):
        m = input_body['mass'] / m0_SI
        position = np.array(input_body['position']) * 1e3 / AU_SI
        velocity = np.array(input_body['velocity']) * 1e3 / AU_SI * day_SI
        name = input_body['name']
        celestial_bodies.append(CelestialBody(m, position, velocity,
                                              name=name, radius_px=radii_px[i], color=colors[i], period=periods[i]))
    
    if which == 'inner':
        celestial_bodies = [*celestial_bodies[:6]]  # until Jupiter, even though Jupiter is no inner planet
    elif which == 'outer':
        celestial_bodies = [celestial_bodies[0], *celestial_bodies[6:]]  # from Jupiter outwards
    
    return celestial_bodies, current_date
