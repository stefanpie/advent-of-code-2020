import itertools
import functools
import copy
import time


# import networkx as nx
# import numpy as np
# import matplotlib.pyplot as plt


if __name__ == "__main__":

    with open("input.txt") as f:
        data_lines = [line.rstrip() for line in f]

    data_lines_processed = []
    for l in data_lines:
        line_as_list = []
        i = 0
        while i < len(l):
            if l[i] == "e":
                line_as_list.append("e")
                i += 1
            elif l[i] == "w":
                line_as_list.append("w")
                i += 1
            else:
                line_as_list.append(l[i : i + 2])
                i += 2
        data_lines_processed.append(line_as_list)

    floor = {}
    starting_point = (0, 0, 0)

    def move(p_initial, cmd):
        if cmd == "e":
            return (p_initial[0] + 1, p_initial[1] - 1, p_initial[2])
        elif cmd == "w":
            return (p_initial[0] - 1, p_initial[1] + 1, p_initial[2])
        elif cmd == "se":
            return (p_initial[0], p_initial[1] - 1, p_initial[2] + 1)
        elif cmd == "sw":
            return (p_initial[0] - 1, p_initial[1], p_initial[2] + 1)
        elif cmd == "ne":
            return (p_initial[0] + 1, p_initial[1], p_initial[2] - 1)
        elif cmd == "nw":
            return (p_initial[0], p_initial[1] + 1, p_initial[2] - 1)

    for l in data_lines_processed:
        current_pos = starting_point
        for cmd in l:
            current_pos = move(current_pos, cmd)
        if current_pos not in floor:
            floor[current_pos] = "black"
        else:
            if floor[current_pos] == "black":
                floor[current_pos] = "white"
            elif floor[current_pos] == "white":
                floor[current_pos] = "black"

    black = 0
    for k in floor:
        if floor[k] == "black":
            black += 1

    part_1_number = black
    print(f"Part 1: {part_1_number}")

    def neighbors(p):
        return [
            (p[0] + 1, p[1] - 1, p[2]),
            (p[0] - 1, p[1] + 1, p[2]),
            (p[0], p[1] - 1, p[2] + 1),
            (p[0] - 1, p[1], p[2] + 1),
            (p[0] + 1, p[1], p[2] - 1),
            (p[0], p[1] + 1, p[2] - 1),
        ]

    biggest_index_x = max([p[0] for p in floor])
    biggest_index_y = max([p[1] for p in floor])
    biggest_index_z = max([p[2] for p in floor])

    current_floor = copy.copy(floor)
    next_floor = copy.copy(current_floor)

    for i in range(100):
        biggest_index_x = max([abs(p[0]) for p in current_floor])
        biggest_index_y = max([abs(p[1]) for p in current_floor])
        biggest_index_z = max([abs(p[2]) for p in current_floor])
        biggest_index = max(biggest_index_x, biggest_index_y,biggest_index_z)

        pos_to_check = []
        N = biggest_index+2+i
        for x in range(-N, N+1):
            for y in range(max(-N, -x-N), min(+N, -x+N)+1):
                z = -x-y
                pos_to_check.append((x, y, z))
        
        for pos in pos_to_check:
            pos_ns = neighbors(pos)
            values_ns = {'white':0, 'black':0}
            for p in pos_ns:
                if p not in current_floor:
                    values_ns["white"] += 1
                else:
                    values_ns[current_floor[p]] += 1

            bc = values_ns["black"]
            wc = values_ns["white"]

            if pos not in current_floor:
                if bc == 2:
                    next_floor[pos] = "black"
            else:
                if current_floor[pos] == "black":
                    if bc == 0 or bc > 2:
                        next_floor[pos] = "white"
                if current_floor[pos] == "white":
                    if bc == 2:
                        next_floor[pos] = "black"

        current_floor = copy.copy(next_floor)
        next_floor = copy.copy(current_floor)

    day_100_black = list(current_floor.values()).count("black")
    part_2_number = day_100_black
    print(f"Part 2: {part_2_number}")
