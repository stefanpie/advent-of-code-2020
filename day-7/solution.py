import re
import networkx as nx
import matplotlib.pyplot as plt


def parse_rule(rule):
    rule = rule.replace('.', '')
    rule = rule.replace(' bags', '').replace(' bag', '')
    rule = rule.split(' contain ')

    if rule[1] == 'no other':
        rule[1] = []
    else:
        rule[1] = rule[1].split(', ')

    rule[1] = [( s[2:], int(s[0]) ) for s in rule[1]]
    rule = tuple(rule)
    return rule

def total_bag_count(graph, bag_node):
    # print()
    # print(f'Looking at {bag_node}')
    if graph[bag_node] == {}:
        # print("bag is empty")
        return 1
    else:
        bag_sum = 0
        for key, value in graph[bag_node].items():
            bags_under = total_bag_count(graph, key) * value['weight']
            bag_sum += bags_under
            # print(f'for {key} : {bags_under} bags under')
        bag_sum += 1
        return bag_sum


if __name__ == "__main__":
    with open('input.txt') as f:
        rules = [line.rstrip() for line in f]
    
    rules_parsed = list(map(parse_rule, rules))
    rules_graph = nx.DiGraph()

    for rule in rules_parsed:
        from_bag = rule[0]
        for to_bag in rule[1]:
            rules_graph.add_edge(from_bag, to_bag[0], weight=to_bag[1])

    ancestors = nx.ancestors(rules_graph, 'shiny gold')
    number_of_gold_bag_ancestors = len(ancestors)
    print(f"Part 1: {number_of_gold_bag_ancestors}")

    decendents_set = nx.descendants(rules_graph, 'shiny gold')
    decendents_set.add('shiny gold')
    gold_bag_graph = rules_graph.subgraph(decendents_set)

    bags_inside_gold_bags = total_bag_count(gold_bag_graph, 'shiny gold')-1
    print(f"Part 2: {bags_inside_gold_bags}")


    # plt.subplot(111)
    # pos = nx.random_layout(rules_graph)
    # nx.draw_networkx(rules_graph, pos=pos, with_labels=True)
    # labels = nx.get_edge_attributes(rules_graph,'weight')
    # nx.draw_networkx_edge_labels(rules_graph,pos,edge_labels=labels)
    # plt.show()

    # plt.subplot(111)
    # pos = nx.random_layout(gold_bag_graph)
    # nx.draw_networkx(gold_bag_graph, pos=pos, with_labels=True)
    # labels = nx.get_edge_attributes(gold_bag_graph,'weight')
    # nx.draw_networkx_edge_labels(gold_bag_graph,pos,edge_labels=labels)
    # plt.show()