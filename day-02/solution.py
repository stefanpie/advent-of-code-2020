import re
entries = []

with open('input.txt') as f:
    entries = [line.rstrip() for line in f]

def parse_entry(entry_text):
    entry = {}
    
    result = re.search(r'(\d*)-(\d*) ([a-z]): ([a-z]*)', entry_text)
    entry['lower'] = int(result.group(1))
    entry['upper'] = int(result.group(2))
    entry['letter'] = result.group(3)
    entry['password'] = result.group(4)
    return entry


entries_parsed = list(map(parse_entry, entries))

def is_valid_entry(entry):
    letter_count = entry['password'].count(entry['letter'])
    valid = (letter_count >= entry['lower'] and letter_count <= entry['upper'])
    return valid

entries_valid = list(map(is_valid_entry, entries_parsed))
valid_count = entries_valid.count(True)


def is_valid_entry_modified(entry):
    print(entry)
    lower_match = entry['password'][entry['lower']-1] == entry['letter']
    upper_match = entry['password'][entry['upper']-1] == entry['letter']
    valid = lower_match ^ upper_match
    print(valid)
    return valid

entries_valid_modified = list(map(is_valid_entry_modified, entries_parsed))
valid_count_modified = entries_valid_modified.count(True)
print(valid_count_modified)