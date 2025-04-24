import math
from contour_toolpath.mesh import Edge, EdgeId, Mesh, Vertex, VertexId
from contour_toolpath.window import WindowLinear, WindowCircular, get_end_distance, get_start_distance
from mathutil.vector import Vec2D, Vec3D

def test_start_end_distance_linear_window():
    """
    Test that the start and end distance is correct.
    """
    mesh = Mesh(
        vertices=[
            Vertex(position=Vec3D(0.0, 0.0, 0.0), d=0.0),
            Vertex(position=Vec3D(1.0, 0.0, 0.0), d=1.0),
        ],
        edges=[
            Edge(start=VertexId(0), end=VertexId(1)),
        ],
        faces=[],
    )
    window = WindowLinear(
        edge_id=EdgeId(0),
        start_t=0.0,
        end_t=1.0,
        start_distance=1.0,
        source_direction=math.pi / 2
    )

    assert get_start_distance(window, mesh) == 1.0
    assert get_end_distance(window, mesh) == 1.0  # Window is perpendicular to the edge
    
    window = WindowLinear(
        edge_id=EdgeId(0),
        start_t=0.0,
        end_t=1.0,
        start_distance=1.0,
        source_direction=math.pi / 4
    )

    assert get_start_distance(window, mesh) == 1.0
    assert get_end_distance(window, mesh) == 1.0 + math.sqrt(2) / 2.0


    # Test when not spanning the whole edge
    window = WindowLinear(
        edge_id=EdgeId(0),
        start_t=0.0,
        end_t=0.5,
        start_distance=1.0,
        source_direction=math.pi / 4
    )
    assert get_start_distance(window, mesh) == 1.0
    assert get_end_distance(window, mesh) == 1.0 + math.sqrt(2) / 2.0 / 2.0

    window = WindowLinear(
        edge_id=EdgeId(0),
        start_t=0.25,
        end_t=0.5,
        start_distance=1.0,
        source_direction=math.pi / 4
    )
    assert get_start_distance(window, mesh) == 1.0 + math.sqrt(2) / 2.0 / 4.0
    assert get_end_distance(window, mesh) == 1.0 + math.sqrt(2) / 2.0 / 2.0

    
def test_start_end_distance_circular_window():
    """
    Test that the start and end distance is correct.
    """
    mesh = Mesh(
        vertices=[
            Vertex(position=Vec3D(0.0, 0.0, 0.0), d=0.0),
            Vertex(position=Vec3D(1.0, 0.0, 0.0), d=1.0),
        ],
        edges=[
            Edge(start=VertexId(0), end=VertexId(1)),
        ],
        faces=[],
    )
    window = WindowCircular(
        edge_id=EdgeId(0),
        start_t=0.0,
        end_t=1.0,
        cumulative_distance=1.0,
        source_point=Vec2D(0.0, 0.0),
    )

    assert get_start_distance(window, mesh) == 1.0
    assert get_end_distance(window, mesh) == 1.0 + 1.0

    window = WindowCircular(
        edge_id=EdgeId(0),
        start_t=0.0,
        end_t=1.0,
        cumulative_distance=1.0,
        source_point=Vec2D(0.0, 1.0),
    )

    assert get_start_distance(window, mesh) == 1.0 + 1.0
    assert get_end_distance(window, mesh) == 1.0 + math.sqrt(2)