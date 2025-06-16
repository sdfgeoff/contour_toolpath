import math
from typing import NamedTuple, Tuple

from matplotlib.collections import PolyCollection
from matplotlib.tri import Triangulation
from contour_toolpath.mesh import Edge, EdgeId, Mesh, Triangle, get_edge_length
from contour_toolpath.window import Window, WindowCircular, WindowLinear
from mathutil.vector import Vec2D, Vec3D




def intersection_from_edge_direction_and_angle(
    edge: Vec3D,
    other_edge_direction: Vec3D,
    angle: float,
) -> float | None:
    """
    Given:
     - an edge of known direction/length
     - The direction of another edge that has the same start point as the first edge
     - The angle from the end of the first edge to the end of the second edge

    Returns the distance from the start of the first edge to the intersection point when travelling along the other_edge_direction
```




               ----  X 
              /
   returns   /
    this    /
   length  /
          /                
         /                  
       \\      ^           
        \\    /                 \\    \\
  other      /           angle  /\\   /
 direction  /                  |  \\ /
           X-----------------------X
              ^      edge
              |
            Angle Between   
``` 
    """
    edge_length = edge.length()
    if edge_length == 0:
        # It's in the corner
        return 0.0
    # Interior angles of a triangle sum to 180 degrees (math.pi), so we can figure out all the interior angles
    angle_between = math.acos(edge.dot(other_edge_direction) / (edge_length * other_edge_direction.length()))
    opposite_angle = math.pi - angle - angle_between

    if opposite_angle == 0:
        return None

    # Sine rule: a/sin(A) = b/sin(B) = c/sin(C)
    # We can use this to find the length of the other edge
    edge_length = edge.length()
    other_edge_length = edge_length / math.sin(opposite_angle) * math.sin(angle)

    return other_edge_length



def calculate_intersection_on_triangle(
    vcorner: Vec3D,
    vfree: Vec3D,
    vedge: Vec3D,
    angle: float,
    dist: float,
) -> float | None:
    """
                       * vfree
                      /
                     /
                    /
            -----  * 
  Returns  /      /  \\
   this   /      /    \\
 length  /      /      \\
        /      /        \\
       /      /          \\
        \\   /     angle /\\
         \\ /           |  \\
           X-----------------X--------------*
       vcorner                               vedge
           |                 |
           <---- dist ------->

    """
    return intersection_from_edge_direction_and_angle(
        edge=(vedge - vcorner).normalized() * dist,
        other_edge_direction=vfree - vcorner,
        angle=angle
    )



import matplotlib.pyplot as plt


def flip_edges(edge1: Edge, edge2: Edge, distance_along_edge1: float, angle_relative_to_edge_1: float) -> Tuple[Edge, Edge, float, float]:
    """ Flip the edges to that both edges share a start vertex""" 
    flipped_edge1 = Edge(start=edge1.end, end=edge1.start)
    flipped_edge2 = Edge(start=edge2.end, end=edge2.start)
    flipped_distance = 1.0 - distance_along_edge1
    flipped_angle = math.pi - angle_relative_to_edge_1

    if edge1.start == edge2.start:
        return edge1, edge2, distance_along_edge1, angle_relative_to_edge_1
    elif edge1.start == edge2.end:
        return edge1, flipped_edge2, distance_along_edge1, angle_relative_to_edge_1
    elif edge1.end == edge2.start:
        return flipped_edge1, edge2, flipped_distance, flipped_angle
    elif edge1.end == edge2.end:
        return flipped_edge1, flipped_edge2, flipped_distance, flipped_angle
    else:
        raise ValueError("Edges do not share a vertex, cannot flip edges.")



class Intercept(NamedTuple):
    distance_t: float
    angle: float
    


def plot_window_in_triangle(window: Window, triangle: Triangle, mesh: Mesh) -> None:
    ax = plt.figure().add_subplot(projection='3d')
    edge_obj = mesh.edges[window.edge_id]
    start_vertex = mesh.vertices[edge_obj.start]
    end_vertex = mesh.vertices[edge_obj.end]
    edge_vec = end_vertex.position - start_vertex.position

    verts: set[Vec3D] = set()

    # plot all edges in the triangle
    positions: list[Vec3D] = []
    directions: list[Vec3D] = []
    for edge_id in triangle.edges:
        edge_obj2 = mesh.edges[edge_id]
        start = mesh.vertices[edge_obj2.start].position
        end = mesh.vertices[edge_obj2.end].position
        other_edge_vec = end - start

        verts.add(start)
        verts.add(end)
        positions.append(start)
        directions.append(other_edge_vec)

    xs = [v.x for v in verts]
    ys = [v.y for v in verts]
    zs = [v.z for v in verts]
    ax.scatter(xs, ys, zs, color='black')  # Plot the vertices of the triangle

    ps = [p.x for p in positions]
    qs = [p.y for p in positions]
    rs = [p.z for p in positions]

    us = [d.x for d in directions]
    vs = [d.y for d in directions]
    ws = [d.z for d in directions]
    ax.quiver(
        ps, qs, rs,  # Starting points of the arrows
        us, vs, ws,  # Direction vectors of the arrows
        color='blue',  # Color of the arrows
        arrow_length_ratio=0.03  # Ratio of arrow head length to arrow length
    )
    assert len(verts) == 3, "Triangle must have exactly 3 vertices"

    # Plot the window
    start_t = window.start_t
    end_t = window.end_t
    start_position = start_vertex.position + edge_vec * start_t
    end_position = start_vertex.position + edge_vec * end_t
    plt.plot(
        [start_position.x, end_position.x],
        [start_position.y, end_position.y],
        [start_position.z, end_position.z],
        color='red',
        linewidth=5
    )

    angle_start, angle_end = get_start_and_end_angle(window, mesh)


    windows: list[Window] = []


    for other_edge in triangle.edges:
        intercepts: list[Intercept] = []
        for angle, window_edge_t in [(angle_start, start_t), (angle_end, end_t)]:
            if other_edge == window.edge_id:
                continue

            common_edge1, common_edge2, distance_along_edge1, angle_corrected = flip_edges(
                edge_obj,
                mesh.edges[other_edge],
                window_edge_t,
                angle,
            )
            vcorner = mesh.vertices[common_edge1.start].position
            vfree = mesh.vertices[common_edge2.end].position
            vedge = mesh.vertices[common_edge1.end].position

            dist = (vcorner - vedge).length() * distance_along_edge1
            intersect_dist_1 = calculate_intersection_on_triangle(
                vcorner=vcorner,
                vfree=vfree,
                vedge=vedge,
                angle=angle_corrected,
                dist=dist
            )
            assert intersect_dist_1 is not None, "Intersection distance should not be None"

            intersect_position = vcorner + (vfree - vcorner).normalized() * intersect_dist_1


            origin_position = start_vertex.position + edge_vec * window_edge_t

            # Plot a line from start_position to intersect_position
            plt.plot(
                [origin_position.x, intersect_position.x],
                [origin_position.y, intersect_position.y],
                [origin_position.z, intersect_position.z],
                color='green',
                linewidth=2
            )
            # Plot a dot at each intercept
            ax.scatter(intersect_position.x, intersect_position.y, intersect_position.z, color='black', marker='x')  # Plot the vertices of the triangle



            intercepts.append(Intercept(
                distance_t=intersect_dist_1, # TODO: divide by edge length to get in edge-space
                angle=angle_corrected  # TODO: adjust for edge flipping I think
            ))

        # From 0 -> first intercept = circular window from window start angle
        # From first intercept to second intercept = propagate linear/circular window
        # From second intercept -> infinity = circular window from windw end angle
        # windows_untrimmed = [
        #     WindowCircular(
        #         edge_id=other_edge,
        #         start_t=0,
        #         end_t=intercepts[0].distance_t,
        #         cumulative_distance=window.cumulative_distance, # TODO: Sum this somehow
        #         source_point=Vec2D(0,0)  # TODO: start point in `other_edge`` space
        #     ),
        #     WindowCircular(
        #         edge_id=other_edge,
        #         start_t=intercepts[0].distance_t,
        #         end_t=intercepts[1].distance_t,
        #     ) if isinstance(window, WindowCircular) else WindowLinear(
        #         edge_id=other_edge,
        #         start_t=intercepts[0].distance_t,
        #         end_t=intercepts[1].distance_t,

        #     ),
        #     WindowCircular(
        #         edge_id=other_edge,
        #         start_t = intercepts[1].distance_t,
        #         end_t=float('inf'),
        #         cumulative_distance=window.cumulative_distance, # TODO: Sum this somehow
        #         source_point=Vec2D(0,0)  # TODO: end point in `other_edge` space
        #     )
        # ]


        
        

    # plot the window
    plt.show()




def get_start_and_end_angle(window: Window, mesh: Mesh) -> tuple[float, float]:
    edge_obj = mesh.edges[window.edge_id]
    start_vertex = mesh.vertices[edge_obj.start]
    end_vertex = mesh.vertices[edge_obj.end]

    edge_vec = end_vertex.position - start_vertex.position
    edge_length = edge_vec.length()

    if isinstance(window, WindowLinear):
        # Check if the window is inside the triangle
        assert isinstance(window, WindowLinear)
        angle_start = window.source_direction
        angle_end = window.source_direction
    else:
        assert isinstance(window, WindowCircular)
        local_position_start = Vec2D(window.start_t * edge_length, 0)
        local_position_end = Vec2D(window.end_t * edge_length, 0)
        dir_start = window.source_point - local_position_start
        dir_end = window.source_point - local_position_end
        angle_start = math.atan2(dir_start.y, dir_start.x)
        angle_end = math.atan2(dir_end.y, dir_end.x)
    
    return angle_start, angle_end


def propagate_window_through_triangle(window: Window, triangle: Triangle, mesh: Mesh) -> list[Window]:
    edge_obj = mesh.edges[window.edge_id]
    start_vertex = mesh.vertices[edge_obj.start]
    end_vertex = mesh.vertices[edge_obj.end]

    edge_vec = end_vertex.position - start_vertex.position
    edge_length = edge_vec.length()

    vec_to_start = edge_vec * window.start_t
    vec_to_end = edge_vec * window.end_t
    angle_start, angle_end = get_start_and_end_angle(window, mesh)

    windows: list[Window] = []
    for other_edge in triangle.edges:
        if other_edge == window.edge_id:
            continue
        other_edge_obj = mesh.edges[other_edge]
        other_start_vertex = mesh.vertices[other_edge_obj.start]
        other_end_vertex = mesh.vertices[other_edge_obj.end]
        other_edge_vec = other_end_vertex.position - other_start_vertex.position

        intersect1 = intersection_from_edge_direction_and_angle(
            edge=vec_to_start,
            other_edge_direction=other_edge_vec,
            angle=angle_start
        )
        intersect2 = intersection_from_edge_direction_and_angle(
            edge=vec_to_end,
            other_edge_direction=other_edge_vec,
            angle=angle_end
        )
        # print(edge_vec, other_edge_vec, angle_start, intersect1)
        # print(edge_vec, other_edge_vec, angle_end, intersect2)

    return windows    
    


    


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
    
