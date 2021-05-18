


def process_boarding_pass(boarding_pass):
    row_pattern = boarding_pass[:7]
    col_pattern = boarding_pass[7:]
    print(f'{row_pattern} : {col_pattern}')


    row_pattern_binary = row_pattern.replace('B', '1').replace('F', '0')
    col_pattern_binary = col_pattern.replace('R', '1').replace('L', '0')

    row_index = int(row_pattern_binary, 2)
    col_index = int(col_pattern_binary, 2)

    print(f'{row_index} : {col_index}')

    seat_id = row_index * 8 + col_index

    print(f'seat_id: {seat_id}')

    return seat_id

def missing_elements(l):
    start, end = l[0], l[-1]
    return sorted(set(range(start, end + 1)).difference(l))[0]

if __name__ == "__main__":
    with open('input.txt') as f:
        boarding_passes = [line.rstrip() for line in f]
    boarding_passes_processed = list(map(process_boarding_pass, boarding_passes))
    largest_seat_id = max(boarding_passes_processed)
    print(f'Part 1: {largest_seat_id}')

    sorted_seat_ids = sorted(boarding_passes_processed)
    missing_seat_id = missing_elements(sorted_seat_ids)
    print(f'Part 2: {missing_seat_id}')