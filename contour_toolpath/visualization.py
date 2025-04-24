from contour_toolpath.mesh import Mesh
import plotly.graph_objects as go  # type: ignore
import numpy as np



def visualize_mesh(mesh: Mesh, show_edges: bool=True):

    # Vertex positions
    verts = np.array([v.position for v in mesh.vertices])
    
    # Treat None as -1.0 for visualization
    d_values = np.array([
        v.d if v.d is not None else -1.0
        for v in mesh.vertices
    ])

    # Normalize to [0, 1] using full range
    d_max = np.max(d_values)

    # Faces (as sets of 3 vertex indices)
    faces: list[list[int]] = []
    for tri in mesh.faces:
        e1, e2, e3 = mesh.edges[tri.edges[0]], mesh.edges[tri.edges[1]], mesh.edges[tri.edges[2]]
        v_ids = set([e1.start, e1.end, e2.start, e2.end, e3.start, e3.end])
        if len(v_ids) != 3:
            raise ValueError(f"Face has incorrect number of unique vertices: {v_ids}")
        faces.append(list(v_ids))

    x, y, z = verts[:, 0], verts[:, 1], verts[:, 2]
    i, j, k = zip(*faces)

    mesh3d = go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        intensity=d_values,  # original values, not normalized
        colorscale='Viridis',
        cmin=-1.0,
        cmax=d_max,
        showscale=True,
        colorbar=dict(title="Distance (d)"),
        opacity=1.0,
        name="mesh"
    )

    fig = go.Figure(data=[mesh3d])

    if show_edges:
        edge_lines: list[go.Scatter3d] = []
        for edge in mesh.edges:
            v0 = mesh.vertices[edge.start].position
            v1 = mesh.vertices[edge.end].position
            edge_lines.append(go.Scatter3d(
                x=[v0[0], v1[0]],
                y=[v0[1], v1[1]],
                z=[v0[2], v1[2]],
                mode='lines',
                line=dict(color='black', width=1),
                showlegend=False
            ))
        fig.add_traces(edge_lines)  # type: ignore

    fig.update_layout(  # type: ignore
        scene=dict(aspectmode='data'),
        title="3D Mesh Visualization (Distance Field)",
    )
    fig.show()  # type: ignore