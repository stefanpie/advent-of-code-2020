import re
import matplotlib.pyplot as plt
import numpy as np
import z3
from itertools import permutations  
import time


rule_pattern = re.compile(r'([\w ]+): ([\d]+)-([\d]+) or ([\d]+)-([\d]+)')

def parse_rule(rule_string):
    rule = {}
    m = rule_pattern.match(rule_string)
    rule['field'] = m.group(1)
    rule['ranges'] = []
    rule['ranges'].append([int(m.group(2)), int(m.group(3))])
    rule['ranges'].append([int(m.group(4)), int(m.group(5))])
    return rule

def check_value(number, rule):
    in_range = []
    for r in rule['ranges']:
        in_range.append(r[0]<=number<=r[1])
    valid = any(in_range)
    return valid
    

def calculate_ticket_scanning_error_rate(nearby_tickets, rules):
    error_values = []
    valid_tickets = []
    for ticket in nearby_tickets:
        valid_ticket = True
        for field_value in ticket:
            in_range_for_rules = []
            for rule in rules:
                in_range_for_rules.append(check_value(field_value, rule))
            if not any(in_range_for_rules):
                error_values.append(field_value)
                valid_ticket = False
        if valid_ticket:
            valid_tickets.append(ticket)
    ticket_scanning_error_rate = sum(error_values)
    return ticket_scanning_error_rate, valid_tickets

if __name__ == "__main__":
    with open("input.txt") as f:
        input_notes = f.read()
    
    input_notes = re.split(r'\r?\n\r?\n', input_notes)

    rules = input_notes[0].splitlines()
    rules = list(map(parse_rule, rules))
    # print(rules)

    my_ticket = input_notes[1].splitlines()[1].split(",")
    my_ticket = list(map(int, my_ticket))
    # print(my_ticket)

    nearby_tickets = input_notes[2].splitlines()[1:]
    nearby_tickets = [list(map(int, t.split(','))) for t in nearby_tickets]
    # print(nearby_tickets)
    
    ticket_scanning_error_rate, valid_tickets = calculate_ticket_scanning_error_rate(nearby_tickets, rules)
    print(f"Part 1: {ticket_scanning_error_rate}")




    ticket_indexes = list(range(len(my_ticket)))
    valid_array = np.ones((len(rules), len(ticket_indexes)))

    all_valid_tickets = [my_ticket] + valid_tickets
    # print(all_valid_tickets)

    for i in range(len(rules)):
        for ticket in all_valid_tickets:
            for field_index, field_value in enumerate(ticket):
                for rule_index, rule in enumerate(rules):
                    if not check_value(field_value,rule):
                        valid_array[rule_index][field_index] = 0
            for field_index, field_value in enumerate(ticket):
                if (valid_array[:, field_index] == 1).sum() == 1:
                    # print(field_index)
                    # print(valid_array[:, field_index])
                    one_rule_index = int(np.where(valid_array[:, field_index] == 1)[0])
                    # print(one_rule_index)
                    for i in  [element for (i,element) in enumerate(list(range(len(ticket)))) if i != field_index]:
                        valid_array[one_rule_index, i] = 0

    field_map={}
    for rule_index, rule in enumerate(rules):
        for index in ticket_indexes:
            if valid_array[rule_index, index] == 1:
                field_map[rule['field']] = index

    departure_product = 1
    for key in field_map:
        if "departure" in key:
            departure_product *= my_ticket[field_map[key]]

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # timgplot = ax.matshow(valid_array)
    # ax.set_xticks(np.arange(len(ticket_indexes)))
    # ax.set_xticklabels(ticket_indexes)
    # ax.set_yticks(np.arange(len([r['field'] for r in rules])))
    # ax.set_yticklabels([r['field'] for r in rules])
    # plt.show()

    print(f"Part 2: {departure_product}")
    