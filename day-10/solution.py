import networkx as nx
from collections import Counter
import numpy as np

def find_valid_adapter_connections(a,l):
    result = list(filter(lambda x: 1 <= x-a <= 3, l))
    return result

if __name__ == "__main__":

    with open('input.txt') as f:
        adapter_list = [int(line.rstrip()) for line in f]

    device_joltage =  max(adapter_list) + 3
    adapter_list_sorted = sorted(adapter_list)
    adapter_list_with_ends = [0] + adapter_list_sorted + [device_joltage]
    joltage_deltas = [adapter_list_with_ends[n]-adapter_list_with_ends[n-1] for n in range(1,len(adapter_list_with_ends))]
    joltage_distribution = dict(Counter(joltage_deltas))
    distribution_number = joltage_distribution[1] * joltage_distribution[3]
    print(f"Part 1: {distribution_number}")


    adapter_graph = nx.DiGraph()
    for a in adapter_list_with_ends:
        adapter_graph.add_node(a)
    for a in adapter_list_with_ends:
        valid_adapter_connections = find_valid_adapter_connections(a,adapter_list_with_ends)
        for c in valid_adapter_connections:
            adapter_graph.add_edge(a, c)

    # Use some graph theory and linear algebra 

    adapter_graph_adjacency_matrix = nx.to_numpy_array(adapter_graph)
    identity_matrix = np.identity(adapter_graph_adjacency_matrix.shape[0])
    count_matrix = np.linalg.inv(identity_matrix - adapter_graph_adjacency_matrix)
    combination_count = int(count_matrix[0][-1])
    print(f"Part 2: {combination_count}")