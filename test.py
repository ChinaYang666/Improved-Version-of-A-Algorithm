import heapq

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start to current Node
        self.h = 0  # Heuristic based estimated cost from current to end
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def astar(grid, start, end):
    start_node = Node(None, start)
    end_node = Node(None, end)
    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start_node)

    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure walkable terrain
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) - 1) or node_position[1] < 0:
                continue

            if grid[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            # Append if not in closed list
            if new_node in closed_list:
                continue

            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if add_to_open_list(open_list, child):
                heapq.heappush(open_list, child)

    return None  # Return None if no path is found

def add_to_open_list(open_list, child):
    for node in open_list:
        if child == node and child.g > node.g:
            return False
    return True

# Example grid, 0 is walkable, non-zero is not walkable
grid = [[0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]]

start = (0, 0)
end = (4, 4)

path = astar(grid, start, end)
print(path)