import numpy as np
from pprint import pprint
import math

with open("input.txt") as f:
    sled_map = [i.rstrip() for i in f.readlines()]
    sled_map = [list(line) for line in sled_map]

pprint(sled_map)

slope_x = 3
slope_y = 1

slopes = [[1, 1], [3, 1], [5, 1], [7,1],[1,2]]

sled_map = np.array(sled_map)
print(sled_map)


def count_trees(sled_map, slope_x, slope_y):
    sled_map_width = sled_map.shape[1]
    sled_map_height = sled_map.shape[0]
    location = [0, 0]
    sled_map_location = [0, 0]

    is_sledding = True
    tree_intersection_count = 0

    while is_sledding:
        if sled_map[sled_map_location[0], sled_map_location[1]] == "#":
            tree_intersection_count += 1

        location[0] += slope_y
        location[1] += slope_x

        sled_map_location[0] = location[0]
        # print(location[1])
        # print(sled_map.shape[1])
        sled_map_location[1] = location[1] % sled_map.shape[1]

        is_sledding = sled_map_location[0] < sled_map.shape[0]

    return tree_intersection_count



part_1_solution = count_trees(sled_map, slope_x, slope_y)
print(f"Part 1 Solution: {part_1_solution}")


counts = [count_trees(sled_map, s[0], s[1]) for s in slopes]
part_2_solution = math.prod(counts)
print(f"Part 2 Solution: {part_2_solution}")
