from copy import deepcopy
import math


def rotate_origin_clockwise(direction_vector, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    x, y = direction_vector[0], direction_vector[1]
    xx = x * math.cos(angle_radians) + y * math.sin(angle_radians)
    yy = -x * math.sin(angle_radians) + y * math.cos(angle_radians)
    rotated_direction_vector = [xx, yy]
    return rotated_direction_vector





def execute_commands(commands, starting_state):
    current_state = deepcopy(starting_state)

    for c in commands:
        c_command = c[0]
        c_arg = int(c[1:])

        if c_command == 'N':
            current_state['position'][1] += c_arg
        if c_command == 'S':
            current_state['position'][1] -= c_arg
        if c_command == 'E':
            current_state['position'][0] += c_arg
        if c_command == 'W':
            current_state['position'][0] -= c_arg
        if c_command == 'L':
            current_state['direction'] = rotate_origin_clockwise(current_state['direction'], -c_arg)
        if c_command == 'R':
            current_state['direction'] = rotate_origin_clockwise(current_state['direction'], c_arg)
        if c_command == 'F':
            current_state['position'][0] += current_state['direction'][0]*c_arg
            current_state['position'][1] += current_state['direction'][1]*c_arg
    
    return current_state

def execute_commands_waypoint_method(commands, starting_state_ship, starting_state_waypoint):
    current_state_ship = deepcopy(starting_state_ship)
    current_state_waypoint = deepcopy(starting_state_waypoint)
    for c in commands:
        c_command = c[0]
        c_arg = int(c[1:])

        if c_command == 'N':
            current_state_waypoint['position'][1] += c_arg
        if c_command == 'S':
            current_state_waypoint['position'][1] -= c_arg
        if c_command == 'E':
            current_state_waypoint['position'][0] += c_arg
        if c_command == 'W':
            current_state_waypoint['position'][0] -= c_arg
        if c_command == 'L':
            current_state_waypoint['position'] = rotate_origin_clockwise(current_state_waypoint['position'], -c_arg)
        if c_command == 'R':
            current_state_waypoint['position'] = rotate_origin_clockwise(current_state_waypoint['position'], c_arg)
        if c_command == 'F':
            current_state_ship['position'][0] += current_state_waypoint['position'][0]*c_arg
            current_state_ship['position'][1] += current_state_waypoint['position'][1]*c_arg

    return current_state_ship, current_state_waypoint

if __name__ == "__main__":
    with open('input.txt') as f:
        command_list = [line.rstrip() for line in f]
    
    
    start_state_ship = {'position':[0,0], 'direction': [1,0]}
    start_state_waypoint = {'position':[10,1]}


    end_state = execute_commands(command_list, start_state_ship)
    manhattan_distance = abs(int(end_state['position'][0])) + abs(int(end_state['position'][1]))
    print(f"Part 1: {manhattan_distance}")

    end_state_ship, end_state_waypoint = execute_commands_waypoint_method(command_list, start_state_ship, start_state_waypoint)
    manhattan_distance_waypoint_method = abs(int(end_state_ship['position'][0])) + abs(int(end_state_ship['position'][1]))
    print(f"Part 2: {manhattan_distance_waypoint_method}")