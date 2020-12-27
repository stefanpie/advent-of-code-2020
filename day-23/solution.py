import copy
import time


def play_2(cup_list_starting, moves=100):
    cup_list=copy.copy(cup_list_starting)
    min_cup_value = min(cup_list)
    max_cup_value = max(cup_list)

    # janky linked list using a dict
    d = {}
    for i in range(len(cup_list)):
        if i == len(cup_list)-1:
            d[cup_list[i]] = cup_list[0]
        else:
            d[cup_list[i]] = cup_list[i+1]
        
    start = cup_list[0]
    for i in range(moves):
        a = d[start]
        b = d[a]
        c = d[b]
        d[start] = d[c]
        put = start-1
        if put in [a,b,c] or put < 1:
            while put in [a,b,c] or put < 1:
                put -=1
                if put < 1:
                    put = max_cup_value
        d[c] = d[put]
        d[put] = a
        start = d[start]
    
    return d



def play(cup_list_starting, moves=100):
    cup_list=copy.copy(cup_list_starting)
    current_cup = cup_list[0]
    min_cup_value = min(cup_list)
    max_cup_value = max(cup_list)



    m = 1
    for i in range(moves):
        # print(f"-- move {m} --")
        # print(f"cups: {cup_list}")
        # print(f"current cup: {current_cup}")
        # print(f"current cup index: {cup_list.index(current_cup)}")
        

        picked_up_cups = []
        pick_up_count = 3
        for j in range(pick_up_count):
            picked_up_cups.append(cup_list.pop((cup_list.index(current_cup)+1) % len(cup_list)))
        # print(f"pick up: {picked_up_cups}")

        destination_cup = current_cup-1
        if destination_cup < min_cup_value:
                    destination_cup = max_cup_value
        destination_cup_found = False
        while not destination_cup_found:
            if destination_cup not in picked_up_cups:
                destination_cup_found = True
            else:
                destination_cup -= 1
                if destination_cup < min_cup_value:
                    destination_cup = max_cup_value
        # print(f"destination: {destination_cup}")

        left_part = cup_list[:cup_list.index(destination_cup)+1]
        right_part = cup_list[cup_list.index(destination_cup)+1:]
        cup_list = left_part + picked_up_cups + right_part
    
        current_cup = cup_list[(cup_list.index(current_cup)+1 )% len(cup_list)]
        # print()
        m+=1
    
    # print("-- final --")
    # print(f"cups: {cup_list}")
    return cup_list



if __name__ == "__main__":
    with open("input.txt") as f:
        data = [line.rstrip() for line in f]
    
    cup_list = list(map(int, list(data[0])))

    final_cup_list = play(cup_list, moves=100)
    left_part = final_cup_list[:final_cup_list.index(1)]
    right_part = final_cup_list[final_cup_list.index(1)+1:]
    final_pattern = "".join(map(str, right_part+left_part))
    print(f"Part 1: {final_pattern}")

    million_cups = cup_list + list(range(len(cup_list) + 1, 1000000 + 1))
    after_10m = play_2(million_cups, moves=10000000)
    cup_product = after_10m[1] * after_10m[after_10m[1]]
    print(cup_product)
    print(f"Part 2: {cup_product}")