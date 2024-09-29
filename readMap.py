
import numpy as np
from typing import List, Tuple

def load_map(file_path: str) -> Tuple[List[Tuple[int, int, int]], np.ndarray, int, int, int, int]:
    space_array = None
    space_interval = 0
    x0, y0, z0 = 0, 0, 0
    x_len, y_len, z_len = 50, 50, 50
    
    try:
        # 读取文本文件内容
        with open(file_path, 'r', encoding='gb2312') as file:
            content = file.read()
            space_desc = content.split('\n')

            for space_line in space_desc:
                if not space_line:
                    continue
                space_line = space_line.split(' ')
                space_line = [item for item in space_line if item != '']

                if '网格划分精度' in space_line[-1]:
                    grid_resolution = int(space_line[2])
                elif '格划分起始点' in space_line[-1]:
                    x0, y0, z0 = int(space_line[1]), int(space_line[2]), int(space_line[3])
                elif '网格数量' in space_line[-1]:
                    x_len, y_len, z_len = int(space_line[1]), int(space_line[2]), int(space_line[3])
                elif any('这是Z向输出第' in item for item in space_line):
                    space_layer_info = space_line[1].split('\t')
                    space_layer_info = [s for s in space_layer_info if s.isdigit()]
                    space_layer_int = [int(item) for item in space_layer_info]
                    space_layer_array = np.array(space_layer_int).reshape((y_len, x_len))

                    if space_array is None:
                        space_array = space_layer_array
                    else:
                        space_array = np.dstack((space_array, space_layer_array))

            # 转换数据为三维数组
            if space_array is None:
                raise ValueError("未找到任何有效的体素数据")
            
            voxel_grid_data = space_array
            indices = np.nonzero(voxel_grid_data)
            x_indices, y_indices, z_indices = indices
            occupied_voxel_coords = list(zip(x_indices, y_indices, z_indices))
            occupied_voxel_coords = [(x, y, z) for y, x, z in occupied_voxel_coords]
            voxel_grid_data = np.transpose(voxel_grid_data, (1, 0, 2))
        return occupied_voxel_coords, voxel_grid_data, x0, y0, z0, grid_resolution

    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到。")
        return [], np.array([]), 0, 0, 0, 0
    except UnicodeDecodeError:
        print(f"错误: 文件 '{file_path}' 的编码格式不正确。请使用 'gb2312' 编码。")
        return [], np.array([]), 0, 0, 0, 0
    except Exception as e:
        print(f"解析数据文件时发生错误: {e}")
        return [], np.array([]), 0, 0, 0, 0
