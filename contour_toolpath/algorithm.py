from collections import defaultdict
import heapq
import math
from typing import Dict, List, Tuple

from contour_toolpath.mesh import EdgeId, Mesh, TriangleId
from contour_toolpath.window import Window, WindowLinear
from contour_toolpath.window_propagation import propagate_window
from mathutil.vector import Vec2D



def create_windows_at_boundaries(mesh: Mesh) -> set[WindowLinear]:
    triangles_by_edge_id: Dict[EdgeId, list[TriangleId]] = defaultdict(list)
    for face_id, face in enumerate(mesh.faces):
        for edge_id in face.edges:
            triangles_by_edge_id[edge_id].append(TriangleId(face_id))

    windows: set[WindowLinear] = set()
    for edge_id, _edge in enumerate(mesh.edges):
        edge_id = EdgeId(edge_id)
        if len(triangles_by_edge_id[edge_id]) == 1:
            window = WindowLinear(
                edge_id=edge_id,
                start_t=0.0,
                end_t=1.0,
                start_distance=0.0,
                source_direction=math.pi / 2
            )
            windows.add(window)
    return windows

def refine_mesh(mesh: Mesh, windows: set[Window]):
    raise NotImplementedError("Refinement not implemented yet")

def merge_windows(new_windows: List[Window], window_set: set[Window]) -> set[Window]:
    raise NotImplementedError("Merging not implemented yet")


def propagate_distance_field(mesh: Mesh, initial_windows: set[Window]) -> set[Window]:
    queue = PropagationQueue()
    for w in initial_windows:
        queue.push(w)

    window_set = set(initial_windows)

    while not queue.empty():
        window = queue.pop()

        new_windows = propagate_window(window, mesh)
        new_window_set = merge_windows(new_windows, window_set)
        changed_windows = new_window_set - window_set
        for w in changed_windows:
            queue.push(w)
        window_set = new_window_set


    return window_set




class PropagationQueue:
    def __init__(self):
        self.heap: List[Tuple[float, Window]] = []

    def push(self, window: Window):
        min_d = min(window.start_distance, window.end_distance)
        priority = window.cumulative_distance + min_d
        heapq.heappush(self.heap, (priority, window))

    def pop(self) -> Window:
        return heapq.heappop(self.heap)[1]

    def empty(self) -> bool:
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)