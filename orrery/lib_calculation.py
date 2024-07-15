import numpy as np

def F(body1, body2, G):
    """Compute gravitational force exerted on body1 by body2. (vectorial) """
    delta_x = body2.position - body1.position
    r = np.linalg.norm(delta_x)
    F_magnitude = G * body1.mass * body2.mass / r**2
    F_direction_normalized = delta_x / r
    return F_magnitude * F_direction_normalized

def computeForceMatrix(bodies, G):
    """Compute the force matrix for all bodies.
    Output: np.ndarray with 3 dimensions: (coordinate, row, column)"""
    num_bodies = len(bodies)
    forces = np.zeros((3, num_bodies, num_bodies))
    for i in range(num_bodies):
        for j in range(i + 1, num_bodies):
            Fij = F(bodies[i], bodies[j], G)
            forces[:, i, j] = Fij
            forces[:, j, i] = -Fij
    return forces

def totalForce(forces, row):
    """Calculation of the total force on a given body/row."""
    force = [sum(forces[coordinate, row, :]) for coordinate in [0, 1, 2]]
    return np.array(force)

# Computation of a timestep
def computeTimestep(bodies, delta_t, G):
    """Update positions and velocities of planets."""
    forces = computeForceMatrix(bodies, G)
    for i, body in enumerate(bodies):
        total_force = totalForce(forces, i)
        # Acceleration
        a = total_force / body.mass
        ## Simple method for time integration
        # Save velocity before acceleration
        v_before = body.velocity
        body.accelerate(a, delta_t)
        # Position after the timestep
        x_afterwards = body.position + (body.velocity + v_before)/2 * delta_t
        body.reposition(x_afterwards)

