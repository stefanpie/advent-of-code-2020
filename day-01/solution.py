from itertools import combinations 
from operator import mul
from functools import reduce

input_list = []
with open("./input.txt") as f:
    input_list = [int(x) for x in f.read().split()]

combination_pairs = list(combinations(input_list, 3))
sums = list(map(sum, combination_pairs))
index_of_2020 = sums.index(2020)

pair_2020 = combination_pairs[index_of_2020]
pair_mult_2020 = reduce(mul, pair_2020, 1)

print(pair_mult_2020)