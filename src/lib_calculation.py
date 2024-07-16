import numpy as np
import datetime

def compute_force(body1, body2, G):
    """
    Compute gravitational force exerted on body1 by body2. (vectorial)

    Parameters:
    body1 (Body): The first body object with attributes: position (np.ndarray), mass (float).
    body2 (Body): The second body object with attributes: position (np.ndarray), mass (float).
    G (float): The gravitational constant.

    Returns:
    np.ndarray: The gravitational force vector acting on body1 due to body2.
    """
    delta_x = body2.position - body1.position
    r = np.linalg.norm(delta_x)
    F_magnitude = G * body1.mass * body2.mass / r**2
    F_direction_normalized = delta_x / r
    return F_magnitude * F_direction_normalized

def compute_force_matrix(bodies, G):
    """
    Compute the force matrix for all bodies.

    Parameters:
    bodies (list): A list of Body objects, each with attributes: position (np.ndarray), mass (float).
    G (float): The gravitational constant.

    Returns:
    np.ndarray: A 3-dimensional numpy array with shape (3, num_bodies, num_bodies). Each element represents the gravitational force vector acting on the corresponding body due to all other bodies. The forces are vectorial and follow Newton's law of universal gravitation. The first dimension represents the coordinate (x, y, z), the second dimension represents the row (body), and the third dimension represents the column (other bodies).
    """
    num_bodies = len(bodies)
    forces = np.zeros((3, num_bodies, num_bodies))
    for i in range(num_bodies):
        for j in range(i + 1, num_bodies):
            Fij = compute_force(bodies[i], bodies[j], G)
            forces[:, i, j] = Fij
            forces[:, j, i] = -Fij
    return forces

def total_force(forces, row):
    """
    Calculate the total gravitational force acting on a given body/row.

    Parameters:
    forces (np.ndarray): A 3-dimensional numpy array representing the gravitational forces.
                        The first dimension represents the coordinate (x, y, z),
                        the second and the third dimension each represents the indices of a bodyr
    row (int): The index of the body/row for which the total force needs to be calculated.

    Returns:
    np.ndarray: A numpy array representing the total gravitational force acting on the given body/row.
                The array has three elements corresponding to the x, y, and z components of the force.
    """
    force = [sum(forces[coordinate, row, :]) for coordinate in [0, 1, 2]]
    return np.array(force)

def compute_timestep(bodies, G, current_datetime, t_step = 1):
    """
    Update positions and velocities of planets in a gravitational simulation.

    This function computes a single timestep for the given bodies, updating their positions and velocities
    based on the gravitational forces between them.

    Parameters:
    bodies (list): A list of Body objects, each with attributes: position (np.ndarray), velocity (np.ndarray), mass (float), and accelerate(np.ndarray, float) and reposition(np.ndarray) methods.
    G (float): The gravitational constant.
    current_datetime (datetime.datetime): The current date and time of the simulation.
    t_step (float, optional): The time of a simulation step in days. It should be lower than or equal to 1. Default is 1.

    Returns:
    datetime.datetime: The updated date and time of the simulation after the timestep.
    """
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

