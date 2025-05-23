import numpy as np
import random

g_diameters = [1, 3, 4]
g_costs_a = {1: 16, 3: 24, 4: 27}
g_costs_b = {1: 45, 3: 62, 4: 68}
g_capacities = {1: 353, 3: 1414, 4: 2036}

g_ranges = {
    'small': {
        'plants': (1, 2),
        'pipes': (5, 10),
        'transbord_client': (5, 10),
        'final_client': (10, 20),
    },
    'medium': {
        'plants': (3, 4),
        'pipes': (10, 20),
        'transbord_client': (10, 20),
        'final_client': (20, 50),
    },
    'large': {
        'plants': (5, 7),
        'pipes': (20, 50),
        'transbord_client': (25, 50),
        'final_client': (50, 100),
    }
}

def generate_nodes(type, count) -> list:
    return [f"{type}{i+1}" for i in range(count)]

def generate_edges(start, final) -> list:
    edges = {}
    for i in start:
        for j in final:
            if i not in edges:
                edges[i] = []
            edges[i].append(j)
    return edges

def generate_instance(tamano='small', seed=None) -> dict:
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    print(f"Used seed: {seed}")
    
    n_plants = random.randint(*g_ranges[tamano]['plants'])
    
    plants = generate_nodes('plant', n_plants)
    pipes = generate_nodes('pipe', random.randint(*g_ranges[tamano]['pipes']))
    transbord_client = generate_nodes('transbord_client', random.randint(*g_ranges[tamano]['transbord_client']))
    final_client = generate_nodes('final_client', random.randint(*g_ranges[tamano]['final_client']))
    
    edge_to_plant_pipes = generate_edges(plants, pipes)
    edge_transbord_to_client = generate_edges(pipes, transbord_client)
    edge_transbord_client_to_final_client = generate_edges(transbord_client, final_client)
    
    
    graph = edge_to_plant_pipes | edge_transbord_to_client | edge_transbord_client_to_final_client
    
    requests = {c: round(random.uniform(40, 100), 2) for c in final_client}
    
    prices = {}
    for i,j in graph.items():
        for k in j:
            price_ij = np.random.normal(8, 2)
            if price_ij < 1:
                price_ij = 1.0
            prices[(i,k)] = round(price_ij, 2)
    
    total_price= sum(requests.values())
    supply_per_plant = round(total_price / n_plants, 2)
    supplys = {p: supply_per_plant for p in plants}
    
    instance = {
        'plants': plants,
        'pipes': pipes,
        'transbord_client': transbord_client,
        'final_client': final_client,
        'graph': graph,
        'requests': requests,
        'transport_prices': prices,
        'supplys': supplys,
        'diameters': g_diameters,
        'cost_a': g_costs_a,
        'cost_b': g_costs_b,
        'capacity': g_capacities
    }
    
    return instance

def print_instance(instance):
    print("Plants:", instance['plants'])
    print("Pipes:", instance['pipes'])
    print("Transbord clients:", instance['transbord_client'])
    print("Final clients:", instance['final_client'])
    print("\nGraph origin -> destination:")
    for key, value in instance['graph'].items():
        for i in value:
            print(f"  {key} -> {i}")
    print("\nRequests final clients:")
    for key, value in instance['requests'].items():
        print(f"  {key}: {value} l/min")
    print("\nTransport_prices (per edge):")
    for key, value in instance['transport_prices'].items():
        print(f"  {key[0]}->{key[1]}: {value}")
    print("\nPlants supplys:")
    for key, value in instance['supplys'].items():
        print(f"  {key}: {value} l/min")
    print("\nDiameters availavle:", instance['diameters'])
    print("Cost instalation type A:", instance['cost_a'])
    print("Cost instalation type B:", instance['cost_b'])
    print("Capacity per diameter:", instance['capacity'])

instance = generate_instance('small', seed=123)
print_instance(instance)
