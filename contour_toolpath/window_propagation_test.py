import math
from contour_toolpath.window import WindowLinear
from contour_toolpath.window_propagation import plot_window_in_triangle, propagate_window, propagate_window_through_triangle
from contour_toolpath.mesh import Edge, EdgeId, Mesh, Triangle, Vertex, VertexId
from mathutil.vector import Vec3D
from contour_toolpath.window_propagation import intersection_from_edge_direction_and_angle



def test_intersection_from_edge_direction_and_angle():
    #        
    #      ,^
    #    /       |
    #  *---------*
    # 
    intersection_distance = intersection_from_edge_direction_and_angle(
        Vec3D(1, 0, 0), 
        Vec3D(1, 1, 0),
         math.pi / 2
    )
    assert intersection_distance is not None
    assert math.isclose(intersection_distance, 2**0.5, rel_tol=1e-9), f"Expected 1.0, got {intersection_distance}"

    # This is the same as the above, but with a longer edge
    intersection_distance = intersection_from_edge_direction_and_angle(
        Vec3D(10, 0, 0), 
        Vec3D(1, 1, 0),
        math.pi / 2
    )
    assert intersection_distance is not None
    assert math.isclose(intersection_distance, 2 ** 0.5 * 10, rel_tol=1e-9), f"Expected 1.0, got {intersection_distance}"

    # Flipped direction, with other_edge not being a unit vector
    intersection_distance = intersection_from_edge_direction_and_angle(
        Vec3D(1, 1, 0), 
        Vec3D(0, 1, 0),
        math.pi / 2
    )
    assert intersection_distance is not None
    assert math.isclose(intersection_distance, 2.0, rel_tol=1e-9), f"Expected 1.0, got {intersection_distance}"



def test_intersection_from_edge_direction_and_angle_no_solution():
    # This should return None, as the angle is too small to form a triangle
    intersection_distance = intersection_from_edge_direction_and_angle(
        Vec3D(1, 0, 0), 
        Vec3D(1, 1, 0),
        math.pi - math.pi / 2
    )
    assert intersection_distance is None, f"Expected None, got {intersection_distance}"




def test_propagate_window():
    mesh = Mesh(
        vertices=[Vertex(position=Vec3D(0,0,1), d=None), Vertex(position=Vec3D(2,0,0), d=None), Vertex(position=Vec3D(1,1,0), d=None)],
        edges=[Edge(
            start=VertexId(0),
            end=VertexId(1),
        ), Edge(
            start=VertexId(1),
            end=VertexId(2),
        ), Edge(
            start=VertexId(2),
            end=VertexId(0),
        )],
        faces=[
            Triangle(edges=(EdgeId(0), EdgeId(1), EdgeId(2))),
        ],
    )
    window = WindowLinear(
        edge_id=EdgeId(0),
        start_t=0.0,
        end_t=0.75,
        start_distance=0.0,
        source_direction=math.pi / 2,
    )
    plot_window_in_triangle(window, mesh.faces[0], mesh)

    windows = propagate_window_through_triangle(
        window=window, 
        triangle=mesh.faces[0],
        mesh=mesh
    )

    assert len(windows) == 3, f"Expected 2 windows, got {len(windows)}"
    windows_edge_1 = windows[0]
    windows_edge_2 = windows[1]