import numpy as np

def apply_scaling(x, y, window, navigation_width, field_of_view_AU):
    """
    Apply scaling and translation to 2D coordinates based on a given window size and A.U. in view.

    Parameters:
    x (float): The x-coordinate of the 2D point.
    y (float): The y-coordinate of the 2D point.
    window (object): An object representing the window with attributes 'width' and 'height'.
    navigation_width (float): The width of the navigation area in pixels.
    field_of_view_AU (float): The number of Astronomical Units (A.U.) that fit within the window.

    Returns:
    tuple: A tuple containing the scaled and translated x-coordinate and y-coordinate.
    """
    # scale = min(window.width - navigation_width, window.height)/field_of_view_AU # pixels per A.U.
    scale = (window.width - navigation_width)/field_of_view_AU # pixels per A.U.
    offset_x = (window.width - navigation_width)//2 + navigation_width
    offset_y = window.height//2
    return x*scale + offset_x, y*scale + offset_y

def orthogonal_projection(pos_3d, v1, v2):
    """
    Compute the orthogonal projection of a 3D point onto the plane defined by two vectors.
    IMPORTANT: v1 and v2 must have a norm of 1. (This reduces computational effort.)

    Parameters:
    pos_3d (numpy array): A 3D point represented as a numpy array.
    v1 (numpy array): The first vector defining the plane. Must be normalized to reduce computational effort.
    v2 (numpy array): The second vector defining the plane. Must be normalized to reduce computational effort.

    Returns:
    tuple: A tuple containing the x-coordinate and y-coordinate of the orthogonal projection.
    """
    # # Normalize vectors
    # v1_norm = v1 / np.linalg.norm(v1)
    # v2_norm = v2 / np.linalg.norm(v2)

    # Compute the projection of the point onto the plane
    xprime = np.dot(pos_3d, v1)
    yprime = np.dot(pos_3d, v2)

    # Subtract the projections from the original position to get the orthogonal projection
    return xprime, yprime

def generate_perpendicular_vectors(v):
    """
    Generate two vectors that are perpendicular to the given vector v.
    
    Parameters:
    v (numpy array): A 3D vector
    
    Returns:
    tuple: Two perpendicular vectors to v
    """
    if np.all(v == 0):
        raise ValueError("The zero vector does not have a well-defined perpendicular vector.")
    
    # Step 1: Find the first perpendicular vector
    if v[0] == 0 and v[1] == 0:
        # v is parallel to the z-axis, use x-axis for cross product
        perp1 = np.cross(v, np.array([1, 0, 0]))
    else:
        # v is not parallel to the z-axis, use z-axis for cross product
        perp1 = np.cross(v, np.array([0, 0, 1]))
    
    # Normalize the first perpendicular vector
    perp1 = perp1 / np.linalg.norm(perp1)
    
    # Step 2: Find the second perpendicular vector
    perp2 = np.cross(v, perp1)
    
    # Normalize the second perpendicular vector
    perp2 = perp2 / np.linalg.norm(perp2)
    
    return perp1, perp2