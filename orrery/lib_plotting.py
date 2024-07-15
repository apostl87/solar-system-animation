def applyScaling(x, y, window, au_in_view):
    scale = min(window.width, window.height)/au_in_view # pixels per A.U.
    offset_x = window.width//2
    offset_y = window.height//2
    return x*scale + offset_x, y*scale + offset_y