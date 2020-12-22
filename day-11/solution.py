from pprint import pprint
from copy import deepcopy
import itertools


def in_array_bounds(i, j, array):
    rows = len(array)
    cols = len(array[0])
    in_bounds = 0 <= i <= rows - 1 and 0 <= j <= cols - 1
    return in_bounds


def get_neighbours(i, j, array):
    neighbours_indexes = list(
        itertools.product(range(i - 1, i + 2), range(j - 1, j + 2))
    )
    neighbours_indexes.remove((i, j))
    rows = len(array)
    cols = len(array[0])
    neighbours_indexes_in_bounds = list(
        filter(
            lambda x: 0 <= x[0] <= rows - 1 and 0 <= x[1] <= cols - 1,
            neighbours_indexes,
        )
    )
    neighbours = [array[a][b] for a, b in neighbours_indexes_in_bounds]
    return neighbours


def get_visible_neighbours(i, j, array):
    slopes = list(itertools.product(range(-1, 2), range(-1, 2)))
    slopes.remove((0, 0))
    neighbours = []

    for s in slopes:
        search_i = i + s[0]
        search_j = j + s[1]
        searching = True
        while in_array_bounds(search_i, search_j, array) and searching:
            if array[search_i][search_j] != ".":
                neighbours.append(array[search_i][search_j])
                searching = False
            search_i += s[0]
            search_j += s[1]

    return neighbours


def run_simulation(initial_state, visible_method=False):
    current_state = deepcopy(initial_state)
    next_state = None
    simluation_running = True
    while simluation_running:
        next_state = deepcopy(current_state)

        for row in range(len(current_state)):
            for col in range(len(current_state[0])):
                occupied_threshold = 0
                nbs = []
                if visible_method:
                    nbs = get_visible_neighbours(row, col, current_state)
                    occupied_threshold = 5
                else:
                    nbs = get_neighbours(row, col, current_state)
                    occupied_threshold = 4

                
                if current_state[row][col] == "L" and nbs.count("#") == 0:
                    next_state[row][col] = "#"
                if current_state[row][col] == "#" and nbs.count("#") >= occupied_threshold:
                    next_state[row][col] = "L"

        if current_state == next_state:
            simluation_running = False

        current_state = deepcopy(next_state)
        # pprint(current_state)

    final_occupied_seats_count = list(itertools.chain(*current_state)).count("#")
    return current_state, final_occupied_seats_count


if __name__ == "__main__":
    with open("input.txt") as f:
        waiting_area_starting = [i.rstrip() for i in f.readlines()]
        waiting_area_starting = [list(line) for line in waiting_area_starting]

    # pprint(waiting_area_starting)

    final_sim_state, final_count = run_simulation(waiting_area_starting, visible_method=False)
    print(f"Part 1: {final_count}")
    final_sim_state_visible_method, final_count_visible_method = run_simulation(waiting_area_starting, visible_method=True)
    print(f"Part 2: {final_count_visible_method}")

