import numpy as np
import pytest
from ..src.lib_calculation import *
from .Struct import Struct

G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
body1 = {'position': np.array([0, 0, 0]), 'mass': 5.972e24}  # Earth
body2 = {'position': np.array([1.496e11, 0, 0]), 'mass': 7.342e22}  # Moon
body3 = {'position': np.array([0, 2e12, 3e12]), 'mass': 2e24}  # Imagined body
        
def test_force_between_two_point_masses():

    force = compute_force(Struct(**body1), Struct(**body2), G)

    expected_force = np.array([1.3076e15, 0, 0])  # Expected force in Newtons    
    np.testing.assert_allclose(force, expected_force, rtol=1e-3)

    
def test_force_matrix_symmetry():
    # Test if the force matrix is symmetric
    bodies = [
        Struct(**body1),
        Struct(**body2),
        Struct(**body3)
    ]
    forces = compute_force_matrix(bodies, G)
    assert np.allclose(forces, np.transpose(-forces, axes=(0, 2, 1)), atol=1e-10)


def test_total_force_out_of_range():
    bodies = [
        Struct(**body1),
        Struct(**body2),
        Struct(**body3)
    ]
    forces = compute_force_matrix(bodies, G)

    # Test with an out-of-range row index
    try:
        total_force(forces, 3)
        assert False, "Expected an IndexError"
    except IndexError:
        assert True