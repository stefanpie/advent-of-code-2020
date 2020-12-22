from pprint import pprint
import itertools
import copy


def get_neigbors_indexes(p, d=3):
    ranges = [range(p[i] - 1, p[i] + 2) for i in range(d)]
    neighbours_indexes = list(
        itertools.product(*ranges)
    )
    neighbours_indexes.remove(p)
    return neighbours_indexes

def get_neigbors(p, pocket_dimension_map, d=3):
    neighbours = []
    neighbours_indexes = get_neigbors_indexes(p, d=d)
    for index in neighbours_indexes:
        if index not in pocket_dimension_map:
            neighbours.append('.')
        else:
            neighbours.append(pocket_dimension_map[index])
    return neighbours

def run_cycles(initial_pocket_dimension_map, n=6, d=3):
    current_pocket_dimension_map = copy.copy(initial_pocket_dimension_map)
    next_pocket_dimension_map = copy.copy(current_pocket_dimension_map)
    for i in range(n):
        print(i)
        valid_indexes = []
        for pos in current_pocket_dimension_map:
            vaild = True
            for val in pos:
                # print(val)
                vaild &= -2-i<=val<=10+i
            if vaild:
                valid_indexes.append(pos)
        # print(valid_indexes)

        for pos in valid_indexes:
            neigbors = get_neigbors(pos, current_pocket_dimension_map, d=d)
            if current_pocket_dimension_map[pos] == '#':
                if not (2 <= neigbors.count('#') <= 3):
                    next_pocket_dimension_map[pos] = '.'
            if current_pocket_dimension_map[pos] == '.':
                if neigbors.count('#') == 3:
                    next_pocket_dimension_map[pos] = '#'
        current_pocket_dimension_map = copy.copy(next_pocket_dimension_map)
    return current_pocket_dimension_map

if __name__ == "__main__":
    
    with open("input.txt") as f:
        pocket_dimension_array = [i.rstrip() for i in f.readlines()]
        pocket_dimension_array = [list(line) for line in pocket_dimension_array]
        pocket_dimension_array = [pocket_dimension_array]
    

    initial_pocket_dimension_map = {}

    for i in itertools.product(range(-25,26), repeat=3):
        initial_pocket_dimension_map[i] = '.'
    
    for i in range(len(pocket_dimension_array)):
        for j in range(len(pocket_dimension_array[0])):
            for k in range(len(pocket_dimension_array[0][0])):
                initial_pocket_dimension_map[(i,j,k)] = pocket_dimension_array[i][j][k]

    final_pocket_dimension_map = run_cycles(initial_pocket_dimension_map)
    final_pocket_dimension_active_count = list(final_pocket_dimension_map.values()).count('#')
    print(f"Part 1: {final_pocket_dimension_active_count}")

    pocket_dimension_array_4d =[pocket_dimension_array]
    initial_pocket_dimension_map_4d = {}
    for i in itertools.product(range(-21,22), repeat=4):
        initial_pocket_dimension_map_4d[i] = '.'

    for i in range(len(pocket_dimension_array_4d)):
        for j in range(len(pocket_dimension_array_4d[0])):
            for k in range(len(pocket_dimension_array_4d[0][0])):
                for l in range(len(pocket_dimension_array_4d[0][0][0])):
                    initial_pocket_dimension_map_4d[(i,j,k,l)] = pocket_dimension_array_4d[i][j][k][l]
    
    final_pocket_dimension_map_4d = run_cycles(initial_pocket_dimension_map_4d, d=4)
    final_pocket_dimension_4d_active_count = list(final_pocket_dimension_map_4d.values()).count('#')
    print(f"Part 2: {final_pocket_dimension_4d_active_count}")

    # # print(initial_pocket_dimension_map_4d)


