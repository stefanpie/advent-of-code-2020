from itertools import combinations, islice

def window(seq, n):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def generate_combination_sums(l):
    sums = set()
    pairs = combinations(l, 2)
    for p in pairs:
        sums.add(sum(p))
    return sums


if __name__ == "__main__":

    with open('input.txt') as f:
        message_data = [int(line.rstrip()) for line in f]
    
    message_length = len(message_data)
    preamble_size = 25
    checking_index = preamble_size

    broken_data_number = 0
    broken_data_index = 0

    while checking_index < message_length:
        sub_message = message_data[checking_index-preamble_size:checking_index]
        sub_message_combination_sums = generate_combination_sums(sub_message)
        valid_number = message_data[checking_index] in sub_message_combination_sums
        if not valid_number:
            broken_data_number = message_data[checking_index]
            broken_data_index = checking_index
            break
        checking_index+=1



    print(f"Part 1: {broken_data_number}")

    message_data_filtered = [n for i, n in enumerate(message_data) if i < broken_data_index]
    message_data_filtered_length = len(message_data_filtered)

    contiguous_sequences = []
    for i in range(2, message_data_filtered_length+1):
        contiguous_sequences += list(window(message_data_filtered, i))

    contiguous_sequences_sums = list(map(sum, contiguous_sequences))
    # print(contiguous_sequences_sums)
    matching_sequence = contiguous_sequences[contiguous_sequences_sums.index(broken_data_number)]
    # print(matching_sequence)
    encryption_weakness_number = min(matching_sequence) + max(matching_sequence)
    print(f"Part 2: {encryption_weakness_number}")