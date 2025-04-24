from typing import NamedTuple, NewType
from mathutil.vector import Vec3D


EdgeId = NewType("EdgeId", int)
FaceId = NewType("FaceId", int)
VertexId = NewType("VertexId", int)
TriangleId = NewType("TriangleId", int)


class Vertex(NamedTuple):
    """A class representing a vertex in 3D space."""
    position: Vec3D

    d: float | None
    """ distance from boundary """


class Edge(NamedTuple):
    start: VertexId
    end: VertexId


class Triangle(NamedTuple):
    edges: tuple[EdgeId, EdgeId, EdgeId]


class Mesh(NamedTuple):
    """A class representing a 3D mesh."""
    vertices: list[Vertex]
    edges: list[Edge]
    faces: list[Triangle]



def get_edge_length(edge: EdgeId, mesh: Mesh) -> float:
    """
    Get the length of an edge
    """
    edge_obj = mesh.edges[edge]
    v1 = mesh.vertices[edge_obj.start]
    v2 = mesh.vertices[edge_obj.end]
    return (v1.position - v2.position).length()
