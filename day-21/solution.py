import networkx as nx
from networkx.readwrite.json_graph import adjacency
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import copy

def parse_food_line(food_line):
    line_data = {"ingredients": [], "allergens": []}
    l = food_line.split(" (contains ")
    l[0] = l[0].split(" ")
    l[1] = l[1].replace(")", "").split(", ")
    line_data["ingredients"] += l[0]
    line_data["allergens"] += l[1]
    line_data["ingredients"] = set(line_data["ingredients"])
    line_data["allergens"] = set(line_data["allergens"])
    return line_data


if __name__ == "__main__":
    with open("input.txt") as f:
        food_list = [line.rstrip() for line in f]

    food_list = list(map(parse_food_line, food_list))

    all_ingredients = set()
    all_ingredients_repeated = []
    all_allergens = set()
    for f in food_list:
        for i in f["ingredients"]:
            all_ingredients.add(i)
            all_ingredients_repeated.append(i)
        for a in f["allergens"]:
            all_allergens.add(a)

    allergen_map = {}
    for a in all_allergens:
        possible_ingredients = []
        for f in food_list:
            if a in f["allergens"]:
                possible_ingredients.append(f["ingredients"])
        allergen_map[a] = set.intersection(*possible_ingredients)

    ingredients_with_allergens = set.union(*allergen_map.values())
    ingredients_without_allergens = all_ingredients-ingredients_with_allergens
    ingredients_without_allergens_count = 0
    for i in ingredients_without_allergens:
        ingredients_without_allergens_count += all_ingredients_repeated.count(i)
    print(f"Part 1: {ingredients_without_allergens_count}")


    def all_sets_are_len_one(mapping):
        return all([len(v) == 1 for v in mapping.values()])
    
    allergen_map_unique = copy.deepcopy(allergen_map)
    uniquely_mapped = set()

    while(not all_sets_are_len_one(allergen_map_unique)):
        for k, v in allergen_map_unique.items():
            if k not in uniquely_mapped and len(v) == 1:
                keys_to_remove_from = [key_to_remove_from for key_to_remove_from in allergen_map_unique if key_to_remove_from != k]
                for key_to_remove_from in keys_to_remove_from:
                    allergen_map_unique[key_to_remove_from] -= v
                uniquely_mapped.add(k)
                break


    canonical_dangerous_ingredient_list = [(k, list(v)[0]) for k, v in allergen_map_unique.items()]
    canonical_dangerous_ingredient_list.sort(key=lambda i: i[0])
    canonical_dangerous_ingredient_list = ",".join([i[1] for i in canonical_dangerous_ingredient_list])

    print(f"Part 2: {canonical_dangerous_ingredient_list}")



            
