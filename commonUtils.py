import numpy as np
from typing import List, Tuple
from scipy.interpolate import CubicSpline

def get_non_zero_coordinates(downsampled_voxel_grid_data: np.ndarray) -> List[Tuple[int, int, int]]:
    
    indices = np.nonzero(downsampled_voxel_grid_data)
    downsampled_occupied_voxel_coords = list(zip(indices[0], indices[1], indices[2]))
    return downsampled_occupied_voxel_coords

def downsample_3d(array, factor):
    if isinstance(factor, int):
        factor = (factor, factor, factor)

    if array.ndim != 3:
        raise ValueError("Input array must be a 3D array")
    
    for f in factor:
        if f < 1:
            raise ValueError("Downsampling factor must be greater than or equal to 1")

    depth, height, width = array.shape
    d_factor, h_factor, w_factor = factor

    new_depth = depth // d_factor
    new_height = height // h_factor
    new_width = width // w_factor

    downsampled_array = array.reshape(new_depth, d_factor, new_height, h_factor, new_width, w_factor).mean(axis=(1, 3, 5))
    
    return downsampled_array


def originalIndex2DownsampledIndex(index, factor):

    d_index, h_index, w_index = index
    downsampled_index = (int(round(d_index / factor)), 
                         int(round(h_index / factor)), 
                         int(round(w_index / factor)))
    return downsampled_index

def downsampledIndex2OriginalIndex(downsampled_index, factor):

    new_d_index, new_h_index, new_w_index = downsampled_index
    original_index = (new_d_index * factor, 
                      new_h_index * factor, 
                      new_w_index * factor)
    return original_index


def convert_path(path, factor):
    original_path = []
    for point in path:
        original_point = downsampledIndex2OriginalIndex(point, factor)
        original_path.append(original_point)
    return original_path



def optimize_path(path, grid):
    """
    Minimize the path length by reducing the number of inflection points.
    """
    def is_straight_line(p1, p2, grid, resolution=0.1):

        direction = p2 - p1
        distance = np.linalg.norm(direction)
        steps = int(distance / resolution)
        step_vector = direction / steps
        
        for i in range(1, steps):
            point = p1 + step_vector * i
            if (point < 0).any() or (point >= np.array(grid.shape)).any():
                return False
            if grid[int(np.round(point[0])), int(np.round(point[1])), int(np.round(point[2]))] != 0:
                return False
        return True
    
    optimized_path = [path[0]]  
    i = 0
    while i < len(path) - 1:
        j = i + 1
    
        while j < len(path) and is_straight_line(np.array(path[i]), np.array(path[j]), grid):
            j += 1
        optimized_path.append(path[j - 1])
        i = j - 1
    
    return optimized_path


def smooth_path(control_points, t_values):

    control_points = np.array(control_points)  
    n = len(control_points)
    smooth_curve = np.zeros((len(t_values), 3))
    for i, t in enumerate(t_values):
        temp_points = control_points.copy()
        for k in range(1, n):
            for j in range(n - k):
                temp_points[j] = (1 - t) * temp_points[j] + t * temp_points[j + 1]
        smooth_curve[i] = temp_points[0]

    return smooth_curve




def filter_path_by_kDistance(path, k):

    class Node:
        def __init__(self,_x,_y,_z):
            self.x = _x
            self.y = _y
            self.z = _z

    len_path = len(path)
    startNode = Node(path[0][0],path[0][1],path[0][2])
    endNode = Node(path[len_path-1][0],path[len_path-1][1],path[len_path-1][2])
    cur_set = []
    cur_set.append(startNode)
    
    v1 = Node(0,0,0)
    v2 = Node(0,0,0)

    for i in range(len_path-2):
        pre_node = Node(path[i+0][0],path[i+0][1],path[i+0][2])
        cur_node = Node(path[i+1][0],path[i+1][1],path[i+1][2])
        atf_node = Node(path[i+2][0],path[i+2][1],path[i+2][2])
        
        v1.x = cur_node.x - pre_node.x
        v1.y = cur_node.y - pre_node.y
        v1.z = cur_node.z - pre_node.z

        v2.x = cur_node.x - atf_node.x
        v2.y = cur_node.y - atf_node.y
        v2.z = cur_node.z - atf_node.z


        if  v1.y*v2.z - v1.z*v2.y != 0 or v1.z*v2.x - v1.x*v2.z != 0 or v1.x*v2.y - v1.y*v2.x != 0:
            cur_set.append(cur_node)

    cur_set.append(endNode)


    for i in range(len(cur_set)-1):
        if  (cur_set[i].x - cur_set[i+1].x)*(cur_set[i].x - cur_set[i+1].x) + (cur_set[i].y - cur_set[i+1].y)*(cur_set[i].y - cur_set[i+1].y) + (cur_set[i].z - cur_set[i+1].z)*(cur_set[i].z - cur_set[i+1].z) < k*k:
            return []

    return path
