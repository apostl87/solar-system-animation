import numpy as np
from ..src.main import *
from ..src.classes import CelestialBody
import datetime
import pytest
import mock


def test_position_in_view_edge_cases():

    # Test cases at the edge of view
    positions = [
        # At the boundary of the window 
        celestial_bodies[0].position + np.array([field_of_view_AU / 2, 0, 0]),
        celestial_bodies[0].position + np.array([-field_of_view_AU / 2, 0, 0]),
        celestial_bodies[0].position + np.array([0, field_of_view_AU / 2, 0]),
        celestial_bodies[0].position + np.array([0, -field_of_view_AU / 2, 0]),
    ]

    for position in positions:
        x, y = position_in_view(position)
        
        assert navigation_width - 1 <= x <= window_width + 1, f"x={x} is out of range for position={position}"
        assert -1 <= y <= window_height + 1 , f"y={y} is out of range for position={position}"

        
def test_compute_timestep_new_date():
    body = CelestialBody(1, np.random.random((3)), np.random.random((3)))
    bodies = [body]
    new_date = compute_timestep(bodies, 1, datetime.date(2022, 1, 1), t_step=1)
    
    assert new_date == datetime.date(2022, 1, 2), "Date is not as expected"

    
def test_analyze_invalid_target_date_input():

    # Set the input values for the year, month, and day entries
    year = "2022"
    month = "2"
    day = "30"
    
    error_message = analyze_invalid_target_date_input(year, month, day)
    
    assert error_message == "Day (30) does not exist in month 2/2022", "Error message is not as expected"


def test_set_speed_handler():
    value = "30"
    
    speed = set_speed_handler(value)
    
    assert speed == 30, "Speed is not as expected"

    
def test_set_steps_per_frame_handler():
    value = "20"
    
    steps_per_frame = set_steps_per_frame_handler(value)
    
    assert steps_per_frame == 20, "Steps per frame is not as expected"

