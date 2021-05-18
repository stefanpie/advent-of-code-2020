import re

class Passport:
    def __init__(self):
        self.byr = None
        self.iyr = None
        self.eyr = None
        self.hgt = None
        self.hcl = None
        self.ecl = None
        self.pid = None
        self.cid = None
    
    def parse_passport(self, passport_string):
        pass

    def is_valid_passport(self):
        pass


def parse_passport(passport_string):
    data = {}
    passport_string = passport_string.split(' ')
    for pair in passport_string:
        key, val = pair.split(':')
        data[key] = val
    return data

def is_valid_passport(passport):
    contains_all = True
    contains_all &= 'byr' in passport
    contains_all &= 'iyr' in passport
    contains_all &= 'eyr' in passport
    contains_all &= 'hgt' in passport
    contains_all &= 'hcl' in passport
    contains_all &= 'ecl' in passport
    contains_all &= 'pid' in passport
    # contains_all &= 'cid' in passport
    return contains_all

def is_valid_passport_part_2(passport):
    is_valid_passport = True
    is_valid_passport &= 'byr' in passport
    is_valid_passport &= 'iyr' in passport
    is_valid_passport &= 'eyr' in passport
    is_valid_passport &= 'hgt' in passport
    is_valid_passport &= 'hcl' in passport
    is_valid_passport &= 'ecl' in passport
    is_valid_passport &= 'pid' in passport
    # contains_all &= 'cid' in passport

    # print(f'has everything: {is_valid_passport}')

    if not is_valid_passport:
        return is_valid_passport

    is_valid_passport &= len(passport['byr']) == 4 and int(passport['byr']) >= 1920 and int(passport['byr']) <= 2002
    is_valid_passport &= len(passport['iyr']) == 4 and int(passport['iyr']) >= 2010 and int(passport['iyr']) <= 2020
    is_valid_passport &= len(passport['eyr']) == 4 and int(passport['eyr']) >= 2020 and int(passport['eyr']) <= 2030
    
    # print(f'good byr, iyr, eyr: {is_valid_passport}')


    if 'cm' in passport['hgt']:
        is_valid_passport &= int(passport['hgt'].replace('cm','')) >= 150
        is_valid_passport &= int(passport['hgt'].replace('cm','')) <= 193
    elif 'in' in passport['hgt']:
        is_valid_passport &= int(passport['hgt'].replace('in','')) >= 59
        is_valid_passport &= int(passport['hgt'].replace('in','')) <= 76
    else:
        is_valid_passport &= False
    
    # print(f'good hgt: {is_valid_passport}')


    is_valid_passport &= bool(re.match(r'#[0-9a-fA-F]{6}', passport['hcl']))
    # print(f'good hcl: {is_valid_passport}')


    valid_ecl_list = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    is_valid_passport &= passport['ecl'] in valid_ecl_list
    # print(f'good ecl: {is_valid_passport}')

    is_valid_passport &= len(passport['pid']) == 9
    # print(f'good pid: {is_valid_passport}')

    
    return is_valid_passport

blank_line_pattern = re.compile(r'\r?\n\r?\n')


if __name__ == "__main__":
    
    with open('input.txt', 'r') as f:
        text_database = f.read()
    
    text_database = blank_line_pattern.split(text_database)
    text_database = [s.replace('\r',' ').replace('\n',' ') for s in text_database]
    # print(text_database)

    passports = list(map(parse_passport, text_database))
    valid_passports = list(map(is_valid_passport, passports))
    valid_passports_count = valid_passports.count(True)
    print(f'Part 1: {valid_passports_count}')

    valid_passports_2 = list(map(is_valid_passport_part_2, passports))
    valid_passports_count_2 = valid_passports_2.count(True)
    print(f'Part 2: {valid_passports_count_2}')
