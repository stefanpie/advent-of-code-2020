

def run_sequence(starting_sequence, length):
    last_index_lookup = {}
    for i, n in enumerate(starting_sequence):
        last_index_lookup[n]=i

    sequence = [] + starting_sequence
    for i in range(len(sequence), length):
        last_number = sequence[i-1]
        # print(f'sequence: {sequence}')
        # print(f'filling index: {i}')
        # print(f'last number: {last_number}')
        if last_number not in last_index_lookup:
            # print(f'{last_number} not seen before')
            sequence.append(0)
        else:
            # print(f'{last_number} seen before ')
            new_number = (i-1)-last_index_lookup[last_number]
            # print(f'new number: {new_number}')
            sequence.append(new_number)
        
        last_index_lookup[last_number] = i-1
    last_value = sequence[-1]
    return last_value


if __name__ == "__main__":
    with open("input.txt") as f:
        starting_sequence = [line.rstrip() for line in f][0].split(',')
        starting_sequence = list(map(int, starting_sequence))
    
    
    value_2020 = run_sequence(starting_sequence, 2020)
    print(f'Part 1: {value_2020}')
    value_30000000 = run_sequence(starting_sequence, 30000000)
    print(f'Part 2: {value_30000000}')
