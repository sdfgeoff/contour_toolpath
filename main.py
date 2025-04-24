from contour_toolpath.algorithm import create_windows_at_boundaries, propagate_distance_field, refine_mesh
from contour_toolpath.importer import build_mesh_from_trimesh
from contour_toolpath.mesh import Window
from contour_toolpath.visualization import visualize_mesh
import trimesh




def main():
    mesh_in = trimesh.load_mesh("test_objects/Simple.stl")  # type: ignore
    mesh = build_mesh_from_trimesh(mesh_in)

    windows: set[Window] = create_windows_at_boundaries(mesh)

    windows = propagate_distance_field(mesh, windows)
    refine_mesh(mesh, windows)

    

    visualize_mesh(mesh)
    


if __name__ == "__main__":
    main()
