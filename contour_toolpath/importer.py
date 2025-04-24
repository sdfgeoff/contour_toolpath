from typing import DefaultDict
import trimesh
from contour_toolpath.mesh import EdgeId, FaceId, Mesh, Vec3D, Vertex, Edge, Triangle, VertexId
from collections import defaultdict

def build_mesh_from_trimesh(tm: trimesh.Trimesh) -> Mesh:
    vertex_objs = [Vertex(position=Vec3D(x=v[0], y=v[1], z=v[2]), d=None) for v in tm.vertices]

    edge_map: dict[tuple[VertexId, VertexId], EdgeId] = {}  # (min_idx, max_idx) -> edge_id
    edge_list: list[Edge] = []
    edge_faces: DefaultDict[EdgeId, list[FaceId]] = defaultdict(list)

    triangles: list[Triangle] = []

    for face_id, face in enumerate(tm.faces):
        face_id = FaceId(face_id)
        tri_edges: list[EdgeId] = []
        for i in range(3):
            a, b = VertexId(face[i]), VertexId(face[(i + 1) % 3])
            key = (a, b) if a < b else (b, a)

            if key not in edge_map:
                edge_id = EdgeId(len(edge_list))
                edge_map[key] = edge_id
                edge_list.append(Edge(start=key[0], end=key[1]))

            edge_id = edge_map[key]
            edge_faces[edge_id].append(face_id)
            tri_edges.append(edge_id)

        assert len(tri_edges) == 3
        edges = (tri_edges[0], tri_edges[1], tri_edges[2])
        triangles.append(Triangle(edges=edges))

    return Mesh(vertices=vertex_objs, edges=edge_list, faces=triangles)