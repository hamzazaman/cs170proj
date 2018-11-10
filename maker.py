def generate_output_lsts(bus_num, cap):
    """
    inputs: 
        bus_num: integer number of buses
        cap: inclusive integer capactiy of bus
    return: 
        names inside buses
    """
    max_possible = bus_num * cap
    num_letters = math.ceil(math.log(max_possible, 26)) + 2
    return [[string_maker(num_letters) for _ in range(random.randint(cap/2, cap))] \
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
    if len(labels) == 1:
        print("single node graph")
        return graph
    val = random.uniform(0, 1)
    if val > 8 / 10:
        g = nx.complete_graph(len(labels), graph)
        #print("generated complete graph")
    elif len(labels) > 1:
        while True:
            try:
                #print("generating random tree")
                g = nx.random_powerlaw_tree(len(labels))
                #print("generated random tree")
                break
            except nx.NetworkXException:
                print("did not find tree")
                continue
        randomly_add(g)
        #print("added random edges to tree")
    nx.relabel_nodes(g, {i:labels[i] for i in range(len(labels))}, False)
    return g

def randomly_add(graph):
    """
    Adds a uniformly-determined number of edges with no repeats.
    """
    max_edges = scipy.special.comb(nx.number_of_nodes(graph), 2) \
                        - nx.number_of_edges(graph)
    num_add = numpy.random.randint(0, max_edges + 1)
    for _ in range(num_add):
        v1, v2 = 0, 0
        while v1 == v2:
            v1 = numpy.random.randint(0, nx.number_of_nodes(graph))
            v2 = numpy.random.randint(0, nx.number_of_nodes(graph))
        graph.add_edge(v1,v2)

def add_edges(graph1, graph2, big_graph, cap):
    """
    Add edge between most connected_component of g1 to non-leaf g2
    OR
    Add edge if won't invalidate basic optimality
    inputs:
        graph1: base graph
        graph2: target graph
        big_graph: holds graphs
        cap: max riders on bus
    """
    most_connected, most = None, -1
    g1 = nx.nodes(graph1)
    g2 = nx.nodes(graph2)
    target_nodes = [node for node in g2]

    for node in g1:
        if graph1.degree(node) > most:
            most = graph1.degree(node)
            most_connected = node
    count = 0
    while count < 10 * len(target_nodes):
        print("looking for target edges")          
        node2 = target_nodes[numpy.random.randint(0, len(g2))]
        if graph2.degree(node2) > 1:
            big_graph.add_edge(most_connected, node2)
            print("found")
            return
        if nx.number_of_nodes(graph2) <= 2 and \
                nx.number_of_nodes(graph1) + 1 > cap:
            big_graph.add_edge(most_connected, node2)
            print("found")
            return
        count += 1
    print("not found or adding will decrease optimality")        

def output_file(busses, name):
    file = open(name + ".out", "w") 
    for bus in busses:
        file.write("{}\n".format(bus))

def unnest_lsts(busses):
    lst = []
    for bus in busses:
        for p in bus:
            lst.append(p)
    return lst

def rowdy_crowd(busses, cap, max_constrain=100):
    """
    return:
        2D list where each list is a rowdy group
    """
    people = []
    for b in busses[0:len(busses)//2]:
        if random.randint(0,1) == 1:
            r = b[0: random.randint(len(b)//4, len(b))]
            randBus = busses[len(busses)//2: len(busses)][random.randint(0, len(busses)//2 - 1)]
            r = r + randBus[0: random.randint(1, min(len(randBus) ,  int(cap) - len(r)))]
            people.append(r)

    for b in busses[len(busses)//2: len(busses)]:
        if random.randint(0,1) == 1:
            r = b[0: random.randint(len(b)//4, len(b))]
            randBus = busses[0: len(busses)//2][random.randint(0, len(busses)//2 - 1)]
            r = r + randBus[0: random.randint(1, min(len(randBus) ,  int(cap) - len(r)))]
            people.append(r)
    return people

def input_file(busses, bus_num, cap, name):
    file = open(name + ".txt", "w")
    file.write(f"{bus_num}\n")
    file.write(f"{cap}\n")
    for bus in rowdy_crowd(busses, cap):
        file.write("{}\n".format(bus))

def output_graph(graph, name):
    nx.write_gml(graph, name + ".gml")

def print_usage():
    print("USAGE")
    print("python maker.py <save> <display> <name>")
    print("     <save>: True", "to save file, otherwise not kept")
    print("     <display>: True", "to visualize graph, otherwise no draw")
    print("     <name>: test", "file name output")

def main(program, bus_num, cap, save=False, display=False, name="test"):
    big_graph = nx.Graph()
    try:
        busses = generate_output_lsts(int(bus_num), int(cap))
        components = []
        for bus in busses:
            sub_graph = nx.Graph()
            sub_graph.add_nodes_from(bus)
            sub_graph = basic_connect(sub_graph, bus)
            big_graph = nx.union(big_graph, sub_graph)
            components.append(sub_graph)
        size = len(components)
        seen = {}
        for comp in components:
            num_connects = numpy.random.randint(1, size + 1)
            for _ in range(num_connects):
                g2 = components[numpy.random.randint(0, size)]
                if (comp, g2) not in seen or seen[(comp, g2)] < 3:
                    add_edges(comp, g2, big_graph, int(cap))
                    if (comp, g2) in seen:
                        seen[(comp, g2)] += 1
                        seen[(g2, comp)] += 1
                    else:
                        seen[(comp, g2)] = 0
                        seen[(g2, comp)] = 0
        
        print(f"Busses: {busses}")
        print(f"Number of vertices: {nx.number_of_nodes(big_graph)}")

        if save == "True":
            output_graph(big_graph, name)
            output_file(busses, name)
            input_file(busses, bus_num, cap, name)

        if display == "True":
            nx.draw(big_graph, with_labels=True)
            plt.show()
        
    except nx.NetworkXException:
        print("node names identical encountered", "trying again...")
        main("", bus_num, cap, save, display)

if __name__ == '__main__':
    import networkx as nx
    import numpy
    import string, random, math, sys, os, time, scipy
    import matplotlib.pyplot as plt
    if len(sys.argv) < 3:
        raise SystemExit(print_usage())
    raise SystemExit(main(*sys.argv))