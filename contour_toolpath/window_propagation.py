from contour_toolpath.mesh import Mesh, Triangle
from contour_toolpath.window import Window


def propagate_window_through_triangle(window: Window, triangle: Triangle, mesh: Mesh) -> list[Window]:
    


def propagate_window(window: Window, mesh: Mesh) -> list[Window]:
    """
    Propagate the window through the triangle.
    """
    edge = window.edge_id
    triangles = [f for f in mesh.faces if edge in f.edges]

    new_windows: list[Window] = []
    for triangle in triangles:
        # Check if the window is inside the triangle
        new_windows.extend(propagate_window_through_triangle(window, triangle, mesh))

    return new_windows
    
