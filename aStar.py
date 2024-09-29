import numpy as np
import heapq

# class AstarPlanner1:
#     class Node:
#         def __init__(self, point, g_cost, h_cost):
#             self.point = point
#             self.g_cost = g_cost
#             self.h_cost = h_cost
#             self.f_cost = g_cost + h_cost
#             self.parents = []

#         def __lt__(self, other):
#             return self.f_cost < other.f_cost
        
            

#     def __init__(self, grid):
#         self.grid = grid

#     def a_star(self, start, goal):
#         start_node = self.Node(np.array(start), 0, self.heuristic(start, goal))
#         open_list = []
#         heapq.heappush(open_list, start_node)
#         closed_set = set()

#         path_find = False
#         path_mix_length = 0
#         goal_node = self.Node(np.array(goal),self.heuristic(start, goal),0)
#         while open_list:

#             current_node = heapq.heappop(open_list)

#             if path_find and current_node.f_cost > path_mix_length:
#                 continue

#             if np.array_equal(current_node.point, goal):
#                 # return self.reconstruct_paths(current_node)
#                 goal_node.parents.append(current_node)
#                 path_mix_length = current_node.f_cost
#                 path_find = True

#             closed_set.add(tuple(current_node.point))

#             for neighbor in self.explore_neighbors(current_node.point):

#                 if tuple(neighbor) in closed_set:
#                     continue

#                 g_cost = current_node.g_cost + 1
#                 h_cost = self.heuristic(neighbor, goal)
#                 neighbor_node = self.Node(neighbor, g_cost, h_cost)
#                 neighbor_node.parents.append(current_node)

#                 if not self.node_in_open(open_list, neighbor_node):
#                     heapq.heappush(open_list, neighbor_node)
#                 else:
#                     self.update_open_node(open_list, neighbor_node,current_node)
        
#         return  self.reconstruct_paths(goal_node)
#         # return []  

#     def explore_neighbors(self, point):
#         directions = [
#             [1, 0, 0], [-1, 0, 0],
#             [0, 1, 0], [0, -1, 0],
#             [0, 0, 1], [0, 0, -1]
#         ]
#         neighbors = []
#         x_max, y_max, z_max = self.grid.shape

#         for direction in directions:
#             neighborPoint = point + np.array(direction)
#             if (0 <= neighborPoint[0] < x_max and
#                 0 <= neighborPoint[1] < y_max and
#                 0 <= neighborPoint[2] < z_max and
#                 self.is_valid(neighborPoint)):
#                     neighbors.append(neighborPoint)

#         return neighbors

#     def heuristic(self, point, goal):
#         return np.sum(np.abs(np.array(point) - np.array(goal)))


#     def is_valid(self, point):
#         return self.grid[tuple(point)] == 0



#     def node_in_open(self, open_list, node):
#         return any(np.array_equal(existing.point, node.point) for existing in open_list)

#     def update_open_node(self, open_list, new_node,current_node):
#         for i, existing_node in enumerate(open_list):
#             if np.array_equal(existing_node.point, new_node.point):
#                 if new_node.f_cost < existing_node.f_cost:
#                     open_list[i] = new_node
#                     heapq.heapify(open_list)
#                 elif new_node.f_cost == existing_node.f_cost:
#                     if current_node not in open_list[i].parents:
#                         open_list[i].parents.append(current_node)
                

                                

#                 break

#     def reconstruct_paths(self, node):
#         if not node:
#             return []

#         if not node.parents:
#             return [[node.point.tolist()]]

#         paths = []
#         for parent in node.parents:
#             for path in self.reconstruct_paths(parent):
#                 if path not in paths:  
#                     paths.append(path + [node.point.tolist()])

#         return sorted(paths, key=len)





class AstarPlanner2:
    class Node:
        def __init__(self, point, g_cost, h_cost, previous_direction=None, num_turns = 0):
            self.point = point
            self.g_cost = g_cost  
            self.h_cost = h_cost  
            self.f_cost = g_cost + h_cost  
            self.num_turns = num_turns  
            self.previous_direction = previous_direction  
            self.parents = []

        def __lt__(self, other):
            if self.num_turns != other.num_turns:
                return self.num_turns < other.num_turns
            elif self.f_cost != other.f_cost:
                return self.f_cost < other.f_cost
            else:
                return self.g_cost < other.g_cost

    def __init__(self, grid):
        self.grid = grid

    def a_star(self, start, goal):
        start_node = self.Node(np.array(start), 0, self.heuristic(start, goal), previous_direction=None, num_turns=0)
        open_list = []
        heapq.heappush(open_list, start_node)
        closed_set = {}

        path_find = False
        path_mix_length = 0
        goal_node = self.Node(np.array(goal), self.heuristic(start, goal), 0)
        while open_list:

            current_node = heapq.heappop(open_list)

            if path_find and current_node.g_cost > path_mix_length :
                continue

            if np.array_equal(current_node.point, goal):
                goal_node.parents.append(current_node)
                if not path_find:
                    path_mix_length = current_node.g_cost
                path_find = True

            closed_set[tuple(current_node.point)] = current_node.num_turns

            for neighbor_point in self.explore_neighbors(current_node.point):

                direction = neighbor_point - current_node.point

                num_turns = current_node.num_turns
                if current_node.previous_direction is not None and not np.array_equal(direction, current_node.previous_direction):
                    num_turns += 1

                if tuple(neighbor_point) in closed_set and num_turns >= closed_set[tuple(neighbor_point)]:
                    continue

                g_cost = current_node.g_cost + 1
                h_cost = self.heuristic(neighbor_point, goal)

                if path_find and g_cost + h_cost > path_mix_length :
                    continue

                neighbor_node = self.Node(neighbor_point, g_cost, h_cost, previous_direction=direction, num_turns=num_turns)
                neighbor_node.parents.append(current_node)

                heapq.heappush(open_list, neighbor_node)

        return self.reconstruct_paths(goal_node)

    def explore_neighbors(self, point):
        directions = [
            [1, 0, 0], [-1, 0, 0],
            [0, 1, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ]
        neighbors = []
        x_max, y_max, z_max = self.grid.shape

        for direction in directions:
            neighborPoint = point + np.array(direction)
            if (0 <= neighborPoint[0] < x_max and
                0 <= neighborPoint[1] < y_max and
                0 <= neighborPoint[2] < z_max and
                self.is_valid(neighborPoint)):
                    neighbors.append(neighborPoint)

        return neighbors

    def heuristic(self, point, goal):
        return np.sum(np.abs(np.array(point) - np.array(goal)))

    def is_valid(self, point):
        return self.grid[tuple(point)] == 0

    def reconstruct_paths(self, node):
        if not node:
            return []

        if not node.parents:
            return [[node.point.tolist()]]

        paths = []
        for parent in node.parents:
            for path in self.reconstruct_paths(parent):
                if path not in paths:
                    paths.append(path + [node.point.tolist()])

        return sorted(paths, key=len)
    

