import numpy as np
import datetime

def compute_force(body1, body2, G):
    """Compute gravitational force exerted on body1 by body2. (vectorial) """
    delta_x = body2.position - body1.position
    r = np.linalg.norm(delta_x)
    F_magnitude = G * body1.mass * body2.mass / r**2
    F_direction_normalized = delta_x / r
    return F_magnitude * F_direction_normalized

def compute_force_matrix(bodies, G):
    """Compute the force matrix for all bodies.
    Output: np.ndarray with 3 dimensions: (coordinate, row, column)"""
    num_bodies = len(bodies)
    forces = np.zeros((3, num_bodies, num_bodies))
    for i in range(num_bodies):
        for j in range(i + 1, num_bodies):
            Fij = compute_force(bodies[i], bodies[j], G)
            forces[:, i, j] = Fij
            forces[:, j, i] = -Fij
    return forces

def total_force(forces, row):
    """Calculation of the total force on a given body/row."""
    force = [sum(forces[coordinate, row, :]) for coordinate in [0, 1, 2]]
    return np.array(force)

def compute_timestep(bodies, G, current_datetime, t_step = 1):
    """Update positions and velocities of planets. Computation of a timestep"""
    """t_step is the time of a simulation step in (!) days. It should be lower than or equal to 1"""
    forces = compute_force_matrix(bodies, G)
    for i, body in enumerate(bodies):
        # Acceleration
        a = total_force(forces, i) / body.mass
        ## Simple method for time integration
        # Save velocity before acceleration
        v_before = body.velocity
        body.accelerate(a, t_step)
        # Position after the timestep
        x_afterwards = body.position + (body.velocity + v_before)/2 * t_step
        body.reposition(x_afterwards)
        
    return current_datetime + datetime.timedelta(days=t_step)

