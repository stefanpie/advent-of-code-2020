import copy
from pprint import pprint

def step(acc, pc, pc_history, boot_code):
    pc_history.append(pc)
    current_op = boot_code[pc]
    if current_op['op'] == 'nop':
        pc += 1
    if current_op['op'] == 'acc':
        acc += current_op['arg']
        pc += 1
    if current_op['op'] == 'jmp':
        pc += current_op['arg']
    
    return acc, pc, pc_history

def execute_boot_code(boot_code):
    acc = 0
    pc = 0
    pc_history = []
    running = True
    halt_case = None
    while(running):
        acc, pc, pc_history = step(acc, pc, pc_history, boot_code)
        if pc in pc_history:
            running = False
            halt_case = 'loop detected'
        if pc == len(boot_code):
            running = False
            halt_case = 'end of boot'
    return acc, pc, pc_history, halt_case


def load_boot_code(code):
    boot_code = code.splitlines()
    boot_code = [s.split(' ') for s in boot_code]
    boot_code = [{'op': s[0], 'arg': int(s[1]), 'idx': i} for i, s in enumerate(boot_code)]
    return boot_code

if __name__ == "__main__":
    with open("input.txt") as f:
        boot_code_raw = f.read()


    original_boot_code = load_boot_code(boot_code_raw)
    original_run_results = execute_boot_code(original_boot_code)
    print(f"Part 1: {original_run_results[0]}")

    # print(original_boot_code)

    possible_boot_codes = []
    for idx in range(len(original_boot_code)):

        if original_boot_code[idx]['op'] == 'nop':
            modified_boot_code = copy.deepcopy(original_boot_code)
            modified_boot_code[idx]['op'] = 'jmp'
            possible_boot_codes.append(modified_boot_code)

        if original_boot_code[idx]['op'] == 'jmp':
            modified_boot_code = copy.deepcopy(original_boot_code)
            modified_boot_code[idx]['op'] = 'nop'
            possible_boot_codes.append(modified_boot_code)
    
    test_run_result = None
    for c in possible_boot_codes:
        test_run_result = execute_boot_code(c)
        if test_run_result[3] == 'end of boot':
            break
    
    print(f"Part 2: {test_run_result[0]}")
     