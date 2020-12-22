import re
import networkx as nx
import copy


def rule_to_regex_string(rule_number, rule_map):
    regex_string = r''
    rule_value = rule_map[rule_number]
    if rule_value == 'a' or rule_value == 'b':
        regex_string = rule_value
    else:
        regex_string += '(?:'
        # print(rule_number)
        # input('...')
        for g in rule_value:
            for other_rule_index in g:
                regex_string += rule_to_regex_string(other_rule_index, rule_map)
            if g != rule_value[-1]:
                regex_string += '|'
        regex_string += ')'
    return regex_string


if __name__ == "__main__":
    with open("input.txt") as f:
        message_notes = f.read()
    
    message_notes = re.split(r'\r?\n\r?\n', message_notes)

    rules = message_notes[0].splitlines()
    rule_map ={}
    for e in rules:
        rule_key = int(e.split(": ")[0])
        rule_value = e.split(": ")[1]
        if rule_value == '\"a\"':
            rule_value = 'a'
        elif rule_value == '\"b\"':
            rule_value = 'b'
        else:
            rule_value = rule_value.split(" | ")
            rule_value = [list(map(int, i.split(' '))) for i in rule_value]
        rule_map[rule_key] = rule_value


    rule_0_regex = re.compile(rule_to_regex_string(0, rule_map))

    recived_messages = message_notes[1].splitlines()
    rule_zero_count = 0
    for message in recived_messages:
        if rule_0_regex.match(message) and rule_0_regex.match(message).group(0) == message:
            rule_zero_count += 1
    print(f"Part 1: {rule_zero_count}")


    rule_map_modified = copy.copy(rule_map)
    rule_map_modified[8] = [[42],[42,42],[42,42,42],[42,42,42,42],[42,42,42,42,42],[42,42,42,42,42,42]]
    rule_map_modified[11] = [[42,31],[42,42,31,31],[42,42,42,31,31,31],[42,42,42,42,31,31,31,31],[42,42,42,42,42,31,31,31,31,31],[42,42,42,42,42,42,31,31,31,31,31,31]]
    rule_0_regex_modified = re.compile(rule_to_regex_string(0, rule_map_modified))
    rule_zero_count_modified = 0
    for message in recived_messages:
        if rule_0_regex_modified.match(message) and rule_0_regex_modified.match(message).group(0) == message:
            rule_zero_count_modified += 1
    print(f"Part 2: {rule_zero_count_modified}")
