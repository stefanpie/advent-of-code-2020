import copy
import re
from typing import final

mask_command_pattern = re.compile(r'mask = ([X01]+)')
memory_command_pattern = re.compile(r'mem\[([0-9]+)\] = ([0-9]+)')

def to_binary_array(n, bits=36):
    binary_string = format(n, f'0{bits}b')
    binary_array = list(binary_string) 
    return binary_array

def to_value(binary_array):
    binary_string = ''.join(binary_array)
    value = int(binary_string, 2)
    return value

def mask_value(value, mask):
    value_binary_array = to_binary_array(value)
    final_value_array = []
    for v, m in zip(value_binary_array, mask):
        if m == '0' or m =='1':
            final_value_array.append(m)
        if m == 'X':
            final_value_array.append(v)
    final_value = to_value(final_value_array)
    return final_value

def mask_memory_address(address, mask):
    address_binary_array = to_binary_array(address)
    final_address_array = []
    for v, m in zip(address_binary_array, mask):
        if m == '0':
            final_address_array.append(v)
        if m == '1':
            final_address_array.append(m)
        if m == 'X':
            final_address_array.append(m)
    return final_address_array

def generate_address_from_address_array(address_array):
    generated_addresses = []
    floating_indexes = [i for i, b in enumerate(address_array) if b == "X"]
    binary_combinations = [list(to_binary_array(i, bits=len(floating_indexes))) for i in range(2**len(floating_indexes))]
    current_generated_address = None
    current_generated_address_value = 0
    for c in binary_combinations:
        current_generated_address = copy.deepcopy(address_array)
        for i, v in zip(floating_indexes, c):
            current_generated_address[i]=v
        current_generated_address_value = to_value(current_generated_address)
        generated_addresses.append(current_generated_address_value)
    return generated_addresses



def run_initialization_program(initialization_program, memory_initial_state):
    memory_state = copy.deepcopy(memory_initial_state)
    current_mask = None
    current_address = None
    current_value = None
    current_masked_value = None
    for line in initialization_program:
        if bool(mask_command_pattern.match(line)):
            # print('Mask Command:')
            current_mask = mask_command_pattern.search(line).group(1)
            current_mask = list(current_mask)
            # print(f'mask set to {current_mask}')


        if bool(memory_command_pattern.match(line)):
            # print('Memory Command:')
            current_address = memory_command_pattern.search(line).group(1)
            current_value = memory_command_pattern.search(line).group(2)
            current_address = int(current_address)
            current_value = int(current_value)
            # print(f'memory address: {current_address}')
            # print(f'memory value before mask: {current_value}')
            current_masked_value = mask_value(current_value, current_mask)
            # print(f'memory value after mask: {current_masked_value}')
            memory_state[current_address] = current_masked_value
        # print()
    return memory_state

def run_initialization_program_v2(initialization_program, memory_initial_state):
    memory_state = copy.deepcopy(memory_initial_state)
    current_mask = None
    current_address = None
    for line in initialization_program:
        if bool(mask_command_pattern.match(line)):
            # print('Mask Command:')
            current_mask = mask_command_pattern.search(line).group(1)
            current_mask = list(current_mask)
            # print(f'mask set to {current_mask}')


        if bool(memory_command_pattern.match(line)):
            # print('Memory Command:')
            current_address = memory_command_pattern.search(line).group(1)
            current_value = memory_command_pattern.search(line).group(2)
            current_address = int(current_address)
            current_value = int(current_value)
            # print(f'memory address: {current_address}')
            # print(f'memory address before mask: {current_value}')

            masked_memory_address_array = mask_memory_address(current_address, current_mask)
            generated_addresses = generate_address_from_address_array(masked_memory_address_array)
            for a in generated_addresses:
                memory_state[a] = current_value
        # print()
    return memory_state



if __name__ == "__main__":
    
    with open("input.txt") as f:
        initialization_program = [line.rstrip() for line in f]

    memory_initial_state = {}
    memory_final_state = run_initialization_program(initialization_program, memory_initial_state)
    sum_memory_final_state = sum(list(memory_final_state.values()))
    print(f'Part 1: {sum_memory_final_state}')

    memory_initial_state = {}
    memory_final_state_v2 = run_initialization_program_v2(initialization_program, memory_initial_state)
    sum_memory_final_state_v2 = sum(list(memory_final_state_v2.values()))
    print(f'Part 2: {sum_memory_final_state_v2}')    