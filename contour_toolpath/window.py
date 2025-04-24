
import math
from typing import NamedTuple

from contour_toolpath.mesh import EdgeId, Mesh, get_edge_length
from mathutil.vector import Vec2D


class WindowCircular(NamedTuple):
    """
    A circular window is emitted by a single point. The source is the center of that point
    """

    edge_id: EdgeId
    
    start_t: float
    """
    How far along the edge this window starts (from 0.0 being `Edge.start` to 1.0 being `Edge.end`)
    """
    end_t: float
    """
    How far along the edge this window ends (from 0.0 being `Edge.start` to 1.0 being `Edge.end`)
    """

    cumulative_distance: float
    """ 
    Offset from the real source to the virual source. This is because if the propagation goes around a corner, then
    the distance to the source is not the same as the distance to the center of the circular window
    In the paper this is called "sigma" 
    """

    source_point: Vec2D
    """
    The coordinates of the virtual source in local edge coordinates.
    Ie (0,0) is at the start point and the end point is at ([edge_length],0):

      Y ^
        |
        |
        -----> X
    (start) ---------------------- (end)

    """


class WindowLinear(NamedTuple):
    """
    A linear window is emitted by an edge. The source is the ray direction towards the window
    """

    edge_id: EdgeId
    
    start_t: float
    """
    How far along the edge this window starts (from 0.0 being `Edge.start` to 1.0 being `Edge.end`)
    """
    end_t: float
    """
    How far along the edge this window ends (from 0.0 being `Edge.start` to 1.0 being `Edge.end`)
    """

    source_direction: float
    """
    The direction that the ray extends from the window. Represented as an angle in radians
    """

    start_distance: float
    """
    The distance from the edge start point to the zero isoline of the distance field
    """


Window = WindowCircular | WindowLinear





def get_start_distance(window: Window, mesh: Mesh) -> float:
    """
    Get the distance from the edge start to the start of the window
    """
    if isinstance(window, WindowCircular):
        edge_length = get_edge_length(window.edge_id, mesh)
        start_point = Vec2D(window.start_t * edge_length, 0)
        source_to_start = start_point - window.source_point
        return window.cumulative_distance + source_to_start.length()
    assert isinstance(window, WindowLinear)
    edge_to_start_t = get_edge_length(window.edge_id, mesh) * window.start_t
    return window.start_distance + edge_to_start_t * math.cos(window.source_direction)   


def get_end_distance(window: Window, mesh: Mesh) -> float:
    """
    Get the distance from the edge start to the end of the window
    """
    if isinstance(window, WindowCircular):
        edge_length = get_edge_length(window.edge_id, mesh)
        end_point = Vec2D(window.end_t * edge_length, 0)
        source_to_end = end_point - window.source_point
        return window.cumulative_distance + source_to_end.length()
    assert isinstance(window, WindowLinear)
    edge_to_end_t = get_edge_length(window.edge_id, mesh) * window.end_t
    return window.start_distance + edge_to_end_t * math.cos(window.source_direction)   