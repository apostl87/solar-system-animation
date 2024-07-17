import numpy as np
import pytest
from ..src.lib_plotting import *
from .Struct import Struct

def test_apply_scaling():
    x = 1
    y = 0.5
    window = {'width': 500, 'height': 300}
    window = Struct(**window)
    
    navigation_width = 100
    field_of_view_AU = 8

    result = apply_scaling(x, y, window, navigation_width, field_of_view_AU)
    expected_result = (350, 175)

    assert np.allclose(result, expected_result)
    
def test_orthogonal_projection():
    pos_3d = np.array([1.25, 2.5, 343])
    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])
    result = orthogonal_projection(pos_3d, v1, v2)
    expected_result = (1.25, 2.5)
    
    assert np.allclose(result, expected_result)
    
def test_generate_perpendicular_vectors():
    v1 = np.array([1.25, 2.5, 3.73])
    v2, v3 = generate_perpendicular_vectors(v1)
    assert np.dot(v1, v2) < 1e-5
    assert np.dot(v1, v3) < 1e-5
    
    v1 = np.array([0, 0, 2])
    v2, v3 = generate_perpendicular_vectors(v1)
    assert np.dot(v1, v2) < 1e-5
    assert np.dot(v1, v3) < 1e-5
    
    v1 = np.array([0, 0, 0])
    with pytest.raises(ValueError) as e:
        generate_perpendicular_vectors(v1)
        assert str(e.value) == "The zero vector does not have a well-defined perpendicular vector.", "Expected ValueError with appropriate error message."
