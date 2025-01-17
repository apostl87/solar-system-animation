import datetime
import sys


def parse_data(filename):
    """
    Parses a file containing data about celestial bodies and returns the date and time of the data,
    along with a list of dictionaries containing each body's name, mass, position, and velocity.

    Parameters:
    filename (str): The name of the file to be parsed. The file should contain data in a specific format.

    Returns:
    tuple: A tuple containing the date and time of the data (datetime object) and a list of dictionaries,
           where each dictionary represents a celestial body with keys 'name', 'mass', 'position', and 'velocity'.
    """
    with open(filename, 'r') as f:
        data = f.read()
    sections = data.split("\n\n")
    
    datesection = sections[1].splitlines()
    datestr = datesection[1]
    formatstr = datesection[3]
    date_time = datetime.datetime.strptime(datestr, formatstr)

    bodies = []
    for section in sections[2:]:
        lines = section.splitlines()
        
        name = lines[0].strip()  # name line
        mass = float(lines[1].split("=")[1].strip())  # mass line
        
        line_pos = lines[2].strip()  # position line
        position = [float(part.split("=")[1]) for part in line_pos.split()]
        
        line_vel = lines[3].strip()  # velocity line
        velocity = [float(part.split("=")[1]) for part in line_vel.split()]
        
        bodies.append({
            "name": name,
            "mass": mass,
            "position": position,
            "velocity": velocity,
        })
    
    return date_time, bodies