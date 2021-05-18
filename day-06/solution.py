import re
# import math
from pprint import pprint

if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        group_answers = f.read()

    group_answers = re.split(r'\r?\n\r?\n', group_answers)
    group_answers_combined = [s.replace('\n','').replace('\n','') for s in group_answers]


    group_answers_counts = [len(set(s)) for s in group_answers_combined]
    total_count = sum(group_answers_counts)
    print(f'Part 1: {total_count}')


    group_answers_per_person = [s.split('\n') for s in group_answers]
    group_answers_sets = [list(map(set, s)) for s in group_answers_per_person]
    group_answers_intersection = [set.intersection(*s) for s in group_answers_sets]
    group_answers_intersection_counts = [len(s) for s in group_answers_intersection]
    total_count_intersection = sum(group_answers_intersection_counts)
    print(f'Part 2: {total_count_intersection}')
