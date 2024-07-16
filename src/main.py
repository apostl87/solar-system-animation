import pyglet
import random
import numpy as np
import datetime
import sys
import threading
import time
from utils.resource_path import *
from classes import CelestialBody
from lib_calculation import *
from lib_plotting import *
from create_celestial_bodies import *

##################### Units and Constants ########################

# For constants, please refer to create_celestial_bodies.py

# Chosen units for computation
# 1 m0 = 1 sun mass = 1
# 1 A.U. (astronomical unit = 1
# 1 day = 1
G = 2.95912208286e-4  # Gravitational constant [AU^3 sunmass^-1 day^-2]

##################### Variables & Parameters ########################

# # Simulation parameters
t_step = 1  # Time step of simulation in days

# # View parameters
global current_date
window_width = 1000
window_height = 600
navigation_width = 100  # Width of the navigation area in pixels
field_of_view_AU = 12  # Size of the field of view in A.U.
viewplane_normal_vector = np.array((0, 1, 2 / 3))  # Normal vector of the projection plane
viewplane_vector1, viewplane_vector2 = generate_perpendicular_vectors(viewplane_normal_vector)

# # Animation parameters
global is_animating, speed, steps_per_frame
is_animating = True
speed = 60
steps_per_frame = 1  # Number of steps taken per frame
rel_history_length = 2/3  # Length of tail in orbital periods

# # Variables for setting an arbitrary date
global computation_progress  # When calculating to a target date
computation_progress = 0
target_date_error = None

##################### Planetary data ########################
# These units are to be used for inputs to CelestialBody:
# masses in sun masses
# positions in astronomical units (A.U.)
# velocities in A.U./day
#############################################################

celestial_bodies, current_date = create_celestial_bodies('inner')  # Take the inner solar system (plus Jupiter) for now

#################### Helper Functions ########################


def position_in_view(position):
    """
    Calculates the position of a celestial body in the view.

    Parameters:
    position (numpy.ndarray): The 3D position of the celestial body.

    Returns:
    tuple: A tuple (x, y) representing the 2D position of the celestial body in the view.
    """
    relative_position = position - celestial_bodies[0].position  # center the view w.r.t. the Sun
    # Projection
    xproj, yproj = orthogonal_projection(relative_position, viewplane_vector1, viewplane_vector2)
    # Scaling
    x, y = apply_scaling(xproj, yproj, window, navigation_width, field_of_view_AU)
    return (x, y)

# Perform simulation to target date without animation
def do_computation(target_date):
    """
    Performs the computation to reach the target date. Aimed to run asynchronously.

    Parameters:
    target_date (datetime.date): The date to which the computation is performed.

    Returns:
    None.
    """
    global current_date, computation_progress, is_animating
    is_animating = False
    pyglet.clock.unschedule(animate)
    print("Calculating to target date")

    delta_days = (target_date - current_date).days
    t_step = 1 if target_date > current_date else -1
    delta_days = abs(delta_days)
    
    progress_step = 0.01
    next_progress_to_report = progress_step  # shift register for computation_progress
    for k in range(delta_days):
        current_date = compute_timestep(celestial_bodies, G, current_date, t_step=t_step)
        if (k + 1) / delta_days >= next_progress_to_report:
            computation_progress = next_progress_to_report
            next_progress_to_report += progress_step
    computation_progress = 0
    pyglet.clock.schedule_once(refresh_plot, 0.1) 

    
def analyze_invalid_target_date_input():
    """
    This function analyzes the input values for the target date and returns an error message if necessary.
    It assumes that the input data failed when passed to datetime.datetime(*args) 

    Parameters:
    None

    Returns:
    str: An error message of the first detected error.
    """
    if not year_entry.value.isnumeric():
        return "Year must be a number"
    if not (1 <= int(year_entry.value) <= 9999):
        return "Year must be a value from 1 to 9999"
    if not month_entry.value.isnumeric():
        return "Month must be a number"
    if not (1 <= int(year_entry.value) <= 9999):
        return "Month must be a value from 1 to 12"
    if not day_entry.value.isnumeric():
        return "Day must be a number"
    return f"Day ({day_entry.value}) does not exist in month {month_entry.value}/{year_entry.value}"

######################### VIEW ###############################
# Unfortunately, pyglet architecture does not
# fully support outsourcing the following code section.
# This is why I decided to leave everything here
##############################################################

############## Basic structure of the View ###################


# Window
window = pyglet.window.Window(window_width, window_height, caption='Solar System Animation')

# Main batch component
main_batch = pyglet.graphics.Batch()

# A Frame instance to hold all widgets, and provide spacial hashing to avoid sending all the Window events to every widget.
frame = pyglet.gui.Frame(window, order=4)

##################### Initialization of View elements #########

circles = []
labels = []
histories = []
tails = []
for i, body in enumerate(celestial_bodies):
    # color = tuple(np.random.randint(0, 255, (3)))

    # Circles
    circle = pyglet.shapes.Circle(x=0, y=0, radius=body.radius_px, color=body.color, batch=main_batch)
    circles.append(circle)

    # Labels
    label = pyglet.text.Label(body.name,
                          font_name='Roboto',
                          font_size=12,
                          x=0, y=0,
                          anchor_x='center', anchor_y='bottom',
                          batch=main_batch)
    labels.append(label)
    
    # Histories and tails
    histories.append([])
    tails.append(None)

# Current date label
date_label = pyglet.text.Label("Date: " + current_date.strftime("%d %B, %Y"),
                          font_name='Roboto', font_size=12,
                          x=navigation_width + 10, y=window.height - 20,
                          anchor_x='left', anchor_y='top',
                          batch=main_batch)

##################### Navigation UI #####################
x_margin = 10  # Margin to the left of the screen


# # Callback functions
def press_play_pause_button_handler():
    global is_animating, computation_progress
    if is_animating:
        pyglet.clock.unschedule(animate)
    else:
        if computation_progress > 0:
            return
        pyglet.clock.schedule_interval(animate, 1 / speed)
    is_animating = not is_animating


def press_set_date_button_handler():
    global target_date_error
    target_date_error = None
    try:
        target_date = datetime.date(int(year_entry.value), int(month_entry.value), int(day_entry.value))
    except Exception as e:
        # print(e)
        target_date_error = analyze_invalid_target_date_input()
        return
        
    if target_date_error is None:
        threading.Thread(target=do_computation, args=([target_date])).start()
        for history in histories:
            history.clear()

        
def set_speed_handler(text):
    global speed
    if text.isnumeric() and 1 <= float(text) <= 60:
        speed = float(text)
        pyglet.clock.unschedule(animate)
        pyglet.clock.schedule_interval(animate, 1 / speed)

        
def set_steps_per_frame_handler(text):
    global steps_per_frame
    if text.isnumeric() and 1 <= float(text) <= 50:
        val = int(round(float(text)))
        steps_per_frame = val
        steps_per_frame_entry.text = str(val)
        # pyglet.clock.unschedule(animate)
        # pyglet.clock.schedule_interval(animate, 1 / speed)

# # Widgets and labels


# Play/Pause button
img_set_date = pyglet.image.load(resource_path('../resources/button-play-pause-white.png'))
y_play_pause = window.height - 50
play_pause_button = pyglet.gui.PushButton(x=(navigation_width - 70) // 2, y=y_play_pause,
                                          pressed=img_set_date, depressed=img_set_date, hover=img_set_date,
                                          batch=main_batch)
play_pause_button.set_handler('on_press', press_play_pause_button_handler)
frame.add_widget(play_pause_button)

# Info label 1
y_info_label1 = y_play_pause - 15
info_label1 = pyglet.text.Label("",
                          font_name='Roboto', font_size=11,
                          x=x_margin, y=y_info_label1,
                          anchor_x='left', anchor_y='top', align="center",
                          multiline=True, width=navigation_width - x_margin,
                          batch=main_batch)

# Text entries for year, month, day
y_year = y_info_label1 - 70
year_entry_label = pyglet.text.Label("Year",
                                     x=x_margin, y=y_year, font_size=11,
                                     batch=main_batch, anchor_x='left', anchor_y='bottom',
                                     color=(255, 255, 255, 255))
year_entry = pyglet.gui.TextEntry(str(current_date.year),
                                  x=(navigation_width - x_margin) // 2 + x_margin, y=y_year,
                                  width=40, batch=main_batch)
frame.add_widget(year_entry)

y_month = y_year - 30
month_entry_label = pyglet.text.Label("Month",
                                     x=x_margin, y=y_month, font_size=11,
                                     batch=main_batch, anchor_x='left', anchor_y='bottom',
                                     color=(255, 255, 255, 255))
month_entry = pyglet.gui.TextEntry(str(current_date.month),
                                   x=(navigation_width - x_margin) // 2 + x_margin, y=y_month,
                                   width=40, batch=main_batch)
frame.add_widget(month_entry)

y_day = y_month - 30
day_entry_label = pyglet.text.Label("Day",
                                     x=x_margin, y=y_day, font_size=11,
                                     batch=main_batch, anchor_x='left', anchor_y='bottom',
                                     color=(255, 255, 255, 255))
day_entry = pyglet.gui.TextEntry(str(current_date.day),
                                 x=(navigation_width - x_margin) // 2 + x_margin, y=y_day,
                                 width=40, batch=main_batch)
frame.add_widget(day_entry)

# Set Date button
y_set_date_button = y_day - 50
img_play_pause = pyglet.image.load(resource_path('../resources/button-set-date-white.png'))    
set_date_button = pyglet.gui.PushButton(x=(navigation_width - 70) // 2, y=y_set_date_button,
                                          pressed=img_play_pause, depressed=img_play_pause, hover=img_play_pause,
                                          batch=main_batch)
set_date_button.set_handler('on_press', press_set_date_button_handler)
frame.add_widget(set_date_button)

# Info label 2
y_info_label2 = y_set_date_button - 15
info_label2 = pyglet.text.Label("",
                          font_name='Roboto', font_size=11,
                          x=x_margin, y=y_info_label2,
                          anchor_x='left', anchor_y='top', align="center",
                          multiline=True, width=navigation_width - x_margin,
                          batch=main_batch)

# # Text entries for speed, number of steps/days per frame
# Speed
y_speed = y_info_label2 - 60
width_of_entry = 40
img_set = pyglet.image.load(resource_path('../resources/button-set-white.png'))

speed_entry_label = pyglet.text.Label("Speed (1-60)",
                                     x=x_margin, y=y_speed, font_size=11,
                                     batch=main_batch, anchor_x='left', anchor_y='bottom',
                                     color=(255, 255, 255, 255))
speed_entry = pyglet.gui.TextEntry(str(speed),
                                  x=x_margin, y=y_speed - 25,
                                  width=width_of_entry, batch=main_batch)
speed_entry.set_handler('on_commit', set_speed_handler)
frame.add_widget(speed_entry)
set_speed_button = pyglet.gui.PushButton(x=x_margin + width_of_entry + 10, y=y_speed - 30,
                                          pressed=img_set, depressed=img_set, hover=img_set,
                                          batch=main_batch)
set_speed_button.set_handler('on_press', lambda: set_speed_handler(speed_entry.value))
frame.add_widget(set_speed_button)

# Number of steps/days per frame
y_steps_per_frame = y_speed - 70
width_of_entry = 40
img_set = pyglet.image.load(resource_path('../resources/button-set-white.png'))

steps_per_frame_entry_label = pyglet.text.Label("Days per frame (1-50)",
                                     x=x_margin, y=y_steps_per_frame, font_size=11,
                                     batch=main_batch, anchor_x='left', anchor_y='bottom',
                                     multiline=True, width=navigation_width - x_margin,
                                     color=(255, 255, 255, 255))
steps_per_frame_entry = pyglet.gui.TextEntry(str(steps_per_frame),
                                  x=x_margin, y=y_steps_per_frame - 25,
                                  width=width_of_entry, batch=main_batch)
steps_per_frame_entry.set_handler('on_commit', set_steps_per_frame_handler)
frame.add_widget(steps_per_frame_entry)
set_steps_per_frame_button = pyglet.gui.PushButton(x=x_margin + width_of_entry + 10, y=y_steps_per_frame - 30,
                                          pressed=img_set, depressed=img_set, hover=img_set,
                                          batch=main_batch)
set_steps_per_frame_button.set_handler('on_press', lambda: set_steps_per_frame_handler(steps_per_frame_entry.value))
frame.add_widget(set_steps_per_frame_button)

# Info label 3 (bottom of the view)
info_label3 = pyglet.text.Label("",
                                     x=window.width//2, y=5, font_size=11,
                                     batch=main_batch, anchor_x='center', anchor_y='bottom',
                                     color=(255, 255, 255, 255))

##################### Animation ########################


def animate(dt):
    """
    Animation function to animate a number of steps_per_frame steps
    """
    global current_date, steps_per_frame
    
    for i in range(steps_per_frame):
        current_date = compute_timestep(celestial_bodies, G, current_date, t_step=t_step)
        for (body, history) in zip(celestial_bodies, histories):
            x, y = position_in_view(body.position)
            history.append([x, y])
            if len(history) > np.ceil(rel_history_length * body.period):
                del history[0]
    
    refresh_plot(dt)

##################### Refresh functions ########################


def refresh_info_labels(dt):
    """
    Refresh all purely informational labels
    """
    info_label1.text = "Running" if is_animating else ("Paused" if computation_progress == 0 else "Calculation in progress")
    
    if computation_progress > 0:
    # if computation_progress > 0:
        info_label2.text = "Calculating: " + str(round(computation_progress * 100)) + "%"
    elif target_date_error is not None:
        info_label2.text = target_date_error
    else:
        info_label2.text = ""
        
    info_label3.text = f"Target animation speed: {speed} frames/s   Elapsed days per frame: {steps_per_frame}"
        
    
def refresh_plot(dt):
    """
    Refresh the plot with new positions of celestial bodies and their tails.
    """
    date_label.text = "Date: " + current_date.strftime("%d %B, %Y")
    
    for i, (body, circle, label, history) in enumerate(zip(celestial_bodies, circles, labels, histories)):
        if len(history) == 0:
            x, y = position_in_view(body.position)
        else:
            x, y = history[-1]
        # Label position
        label_x = x
        label_y = y + body.radius_px + 2
        # Update of circles and labels
        circle.x, circle.y = x, y
        label.x, label.y = label_x, label_y
        # Tails
        if len(history) >= 2:
            tails[i] = pyglet.shapes.MultiLine(*history, thickness=2, color=body.color, batch=main_batch)
        else:
            tails[i] = None

##################### Listeners ########################


@window.event
def on_draw():
    window.clear()
    main_batch.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(animate, 1 / speed)
    pyglet.clock.schedule_interval(refresh_info_labels, 1 / speed * 2)
    pyglet.app.run()
