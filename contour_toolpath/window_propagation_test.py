import math
from contour_toolpath.window import WindowLinear
from contour_toolpath.window_propagation import propagate_window
from contour_toolpath.mesh import Edge, EdgeId, Mesh, Triangle, Vertex, VertexId
from mathutil.vector import Vec3D


def test_propagate_window():
    mesh = Mesh(
        vertices=[Vertex(position=Vec3D(0,0,0), d=None), Vertex(position=Vec3D(0,0,1), d=None), Vertex(position=Vec3D(0,1,0), d=None)],
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
    # propagate_window(window=WindowLinear(
    #     edge_id=EdgeId(0),
    #     start_t=0.0,
    #     end_t=1.0,
    #     start_distance=0.0,
    #     source_direction=math.pi / 2,
    # ), mesh=mesh)