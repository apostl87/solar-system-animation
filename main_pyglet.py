import pyglet
import random
import numpy as np
from orrery.classes import CelestialBody
from orrery.lib_calculation import *
from orrery.lib_plotting import *

# Constants in SI
AU_SI = 1.496e11 # Astronomical unit [m]; set to one for computational purposes
m0_SI = 1.989e30 # Mass of the sun [kg]; set to one for computational purposes
G_SI = 6.67430e-11 # Gravitational constant [m^3 kg^-1 s^-2]
day_SI = 3600 * 24

# Chosen units for computation
# 1 m0 = 1 sun mass = 1
# 1 A.U. (astronomical unit = 1
# 1 day = 1
G = 2.95912208286e-4 # Gravitational constant [AU^3 sunmass^-1 day^-2]

# Planetary data (mass in sun masses, initial position in AU, initial velocity in AU/day)
sun = CelestialBody(1, np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]), radius_px=10, name="Sun")
earth = CelestialBody(3.0025e-06, np.array([1.0, 0.0, 0.0]), np.array([0.0, 29780/AU_SI*day_SI, 0.0]), radius_px=3, name="Earth")
mars = CelestialBody(3.2127e-07, np.array([1.524, 0.0, 0.0]), np.array([0.0, 24077/AU_SI*day_SI, 0.0]), radius_px=2, name="Mars")
bodies = [sun, earth, mars]

# Time step in days
delta_t = 1  # One day

# Defining window
window = pyglet.window.Window(800, 600)
au_in_view = 4

# Defining main batch components ## TODO: later refactor to classes
main_batch = pyglet.graphics.Batch()

circles = []
labels = []
for body in bodies:
    color = tuple(np.random.randint(0, 255, (3)))

    # Projection
    xproj, yproj = body.position[0], body.position[1] ## TODO make orthogonal projection here

    # Scaling
    x, y = applyScaling(xproj, yproj, window, au_in_view)

    # Label position
    label_x = x
    label_y = y + body.radius_px + 2

    # Circles
    circle = pyglet.shapes.Circle(x=x, y=y, radius=body.radius_px, color=color, batch=main_batch)
    circles.append(circle)

    # Labels
    label = pyglet.text.Label(body.name,
                          font_name='Roboto',
                          font_size=12,
                          x=label_x, y=label_y,
                          anchor_x='center', anchor_y='bottom',
                            batch=main_batch)
    labels.append(label)

def update(dt):
    computeTimestep(bodies, delta_t, G)
    
    for (body, circle, label) in zip(bodies, circles, labels):

        # Projection
        xproj, yproj = body.position[0], body.position[1] ## TODO make orthogonal projection here

        # Scaling
        x, y = applyScaling(xproj, yproj, window, au_in_view)

        # Label position
        label_x = x
        label_y = y + body.radius_px + 2
    
        circle.x, circle.y = x, y
        label.x, label.y = label_x, label_y

@window.event
def on_draw():
    window.clear();
    main_batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed')

# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/10.0)
    pyglet.app.run()
