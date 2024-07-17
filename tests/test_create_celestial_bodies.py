import numpy as np
import datetime
import pytest
import mock
from ..src.create_celestial_bodies import create_celestial_bodies
#from ..src.parse_data import parse_data
    
def test_create_celestial_bodies_default():
    celestial_bodies, current_date = create_celestial_bodies()
    assert type(current_date) == datetime.date
    assert len(celestial_bodies) == 6, "Expected 6 celestial bodies for 'inner' solar system (including Jupiter)"
    assert celestial_bodies[0].name == "Sun", "Expected 'Sun' as the first celestial body"
    assert celestial_bodies[-1].name == "Jupiter", "Expected 'Jupiter' as the last celestial body"

    
def test_create_celestial_bodies_outer():
    celestial_bodies, current_date = create_celestial_bodies('outer')
    assert len(celestial_bodies) == 6, "Expected 6 celestial bodies for 'outer' solar system"
    assert celestial_bodies[0].name == "Sun", "Expected 'Sun' as the first celestial body"
    assert celestial_bodies[-1].name == "Pluto", "Expected 'Pluto' as the last celestial body"

    
def test_create_celestial_bodies_all():
    celestial_bodies, current_date = create_celestial_bodies('all')
    assert len(celestial_bodies) == 10, "Expected 10 celestial bodies for entire solar system"
    assert celestial_bodies[0].name == "Sun", "Expected 'Sun' as the first celestial body"
    assert celestial_bodies[-1].name == "Pluto", "Expected 'Pluto' as the last celestial body"

    
def test_create_celestial_bodies_invalid_which():
    with pytest.raises(ValueError) as e:
        create_celestial_bodies('invalid')
    assert str(e.value) == "Invalid value for 'which' parameter. Expected 'inner' or 'outer'.", "Expected ValueError with appropriate message"

# TODO fix this test case
# @mock.patch('create_celestial_bodies.parse_data')
# def test_create_celestial_bodies_valid_input(mock_func):
#     input_bodies = [
#         {'name': 'Earth', 'mass': 5.972e24, 'position': [0, 0, 0], 'velocity': [0, 0, 0]},
#         {'name': 'Mars', 'mass': 6.417e23, 'position': [1, 0, 0], 'velocity': [0, 1, 0]},
#     ]
#     date_time = datetime.datetime.now()
#     mock_func.return_value = (date_time, input_bodies)
#     celestial_bodies, current_date = create_celestial_bodies('all')
#     assert len(celestial_bodies) == 2, "Expected 2 celestial bodies when input data is valid"
#     assert celestial_bodies[0].name == "Earth", "Expected 'Earth' as the first celestial body"
#     assert celestial_bodies[1].name == "Mars", "Expected 'Mars' as the second celestial body"