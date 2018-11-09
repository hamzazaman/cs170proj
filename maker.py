def generate_output_lsts(bus_num, cap):
    """
    inputs:
        bus_num: integer number of buses
        cap: inclusive integer capactiy of bus
    return: 
        names inside buses
    """
    max_possible = bus_num * cap
    num_letters = math.ceil(math.log(max_possible, 26)) + 1
    return [[string_maker(num_letters) for _ in range(random.randint(1, cap))] \
        for _ in range(bus_num)]

def string_maker(length):
    """
    return: random character string size length
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def basic_connect(graph, labels, control=123):
    """ 
    Adds edges randomly in graph but maintains
    connectivity.
    inputs:
        graph: networkx graph
        labels: vertex labels
        control: seed for erdos-renyi
    return: None
    """
    val = random.uniform(0, 1)
    print(val)
    if val > 1 / 2:
        g = nx.complete_graph(len(labels), graph)
    else:
        g = None
        while g is None or not nx.is_connected(g): 
            val = random.uniform(0, 1)
            g = nx.erdos_renyi_graph(len(labels), val, seed=control, directed=False)
    nx.relabel_nodes(g, {i:labels[i] for i in range(len(labels))}, False)
    return g

def add_edges(graph):
    pass

def output_file(busses, name="test"):
    file = open(name + ".out", "w") 
    for bus in busses:
        file.write("{}\n".format(bus))

def unnest_lsts(busses):
    lst = []
    for bus in busses:
        for p in bus:
            lst.append(p)
    return lst

def rowdy_crowd(busses, max_constrain=100):
    people = unnest_lsts(busses)
    #implement rowdy crowds filling
    return people

def input_file(busses, bus_num, cap, name="test"):
    file = open(name + ".txt", "w")
    file.write(f"{bus_num}\n")
    file.write(f"{cap}\n")
    for bus in rowdy_crowd(busses):
        file.write("{}\n".format(bus))

def output_graph(graph, name="test"):
    nx.write_gml(graph, name + ".gml")

def main(program, bus_num, cap, save=False, display=False, folder="output"):
    big_graph = nx.Graph()
    try:
        busses = generate_output_lsts(int(bus_num), int(cap))
        for bus in busses:
            sub_graph = nx.Graph()
            sub_graph.add_nodes_from(bus)
            sub_graph = basic_connect(sub_graph, bus)
            big_graph = nx.union(big_graph, sub_graph)
        if display:
            nx.draw(big_graph)
            plt.show()
        if save:
            output_graph(big_graph)
            output_file(busses)
            input_file(busses, bus_num, cap)

    except nx.NetworkXException:
        print("node names identical encountered", "trying again...")
        main("", bus_num, cap, display)

if __name__ == '__main__':
    import networkx as nx
    import string, random, math, sys, os
    import matplotlib.pyplot as plt
    raise SystemExit(main(*sys.argv))