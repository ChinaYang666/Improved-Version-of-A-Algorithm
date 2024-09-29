# main.py
from readMap import load_map
from aStar import AstarPlanner2
from visualize import visualizeMapWithStartGoal
import commonUtils as cUtils
import evaluePath as eP
import time

def main():
    # Load the map
    file_path = "/home/yang/兼职/aStarTest/map.txt"
    occupied_voxel_coords, voxel_grid_data, grid_origin_x, grid_origin_y, grid_origin_z, grid_resolution = load_map(file_path)

    if voxel_grid_data is None:
        print("Failed to load the map.")
        return

    startNode = (25, 40, 25)
    targetNode = (200, 85, 50)

    ratioFactor = 5
    downsampled_voxel_grid_data = cUtils.downsample_3d(voxel_grid_data, ratioFactor)

    startNode = cUtils.originalIndex2DownsampledIndex(startNode, ratioFactor)
    targetNode = cUtils.originalIndex2DownsampledIndex(targetNode, ratioFactor)

    print(f"startNode: {startNode}, targetNode: {targetNode}")

    planner = AstarPlanner2(downsampled_voxel_grid_data)


    start_time = time.perf_counter()
    
    paths = planner.a_star(startNode, targetNode)

    end_time = time.perf_counter()
    print(f"执行时间: {end_time - start_time} 秒")
    filtered_paths = []
    if paths:
        print(f"paths num: {len(paths)}")
        
        startNode = (25, 40, 25)
        targetNode = (200, 85, 50)

        for path in paths:
            visualizeMapWithStartGoal(voxel_grid_data,startNode, targetNode,cUtils.convert_path(path,ratioFactor))

        
        # sorted_indices = eP.evaluate_and_score_paths(paths)
        # for idx in sorted_indices:
        #     realPath = cUtils.convert_path(paths[idx],ratioFactor)
        #     k = 10
        #     filtered_path = cUtils.filter_path_by_kDistance(realPath,k)
        #     if filtered_path == []:
        #         continue
        #     visualizeMapWithStartGoal(voxel_grid_data,startNode, targetNode,filtered_path)
        #     filtered_paths.append(filtered_path)

        # print(f"k: {k}\nfiltered path num: {len(filtered_paths)}")




    else:
        print("No path found.")

if __name__ == '__main__':
    main()
