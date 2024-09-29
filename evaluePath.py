import numpy as np

def evaluate_and_score_paths(paths):
    def is_turning_point(path, index):
        if index == 0 or index == len(path) - 1:
            return True  # 起点和终点都是转折点

        # 计算前后两段的方向向量
        prev_vector = np.array(path[index]) - np.array(path[index - 1])
        next_vector = np.array(path[index + 1]) - np.array(path[index])

        # 判断是否为拐点（前后向量垂直）
        return np.isclose(np.dot(prev_vector, next_vector), 0)  # 点积接近于零表示垂直

    turning_points_counts = []

    for index, path in enumerate(paths):
        # 计算转折点
        num_turns = sum(1 for i in range(1, len(path) - 1) if is_turning_point(path, i))
        
        # 存储拐点数量和路径索引
        turning_points_counts.append((num_turns, index))

    # 根据拐点数量排序，返回排序后的数组
    turning_points_counts.sort()  # 按拐点数量从小到大排序

    # 返回仅包含路径索引的数组
    return [index for count, index in turning_points_counts]
