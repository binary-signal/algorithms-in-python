import networkx as nx  # graph library
import random
import math
import os
import argparse


def min_quadratic_root(a, b, c):
    """
    find the min root of second order polynomial
    :param 3rd p : 
    :return: return min (root1,root2)
    """
    a = float(a)
    b = float(b)
    c = float(c)

    d = math.sqrt((b * b) - 4 * a * c)
    root1 = (-b + d) / (2 * a)
    root2 = (-b - d) / (2 * a)

    # print("The solutions are:{:f} {:f}".format(root1, root2))
    if 0 <= root1 <= 1:
        return root1
    elif 0 <= root2 <= 1:
        return root2


def find_pq(n):
    """
    find suitable p, q values for hamiltonian cycle randomised algorithm
    :param: number of nodes in graph
    :rtype: a tuple with suitable p and q values
    """
    while True:
        p = random.random()
        # print ("*loop p={:f} con={:f}".format(p, (40 * math.log(n) / n)))

        if p >= (40 * math.log(n) / n):  # condition
            break

    q = min_quadratic_root(1, -2, p)

    return p, q


def graph_add_nodes(G, n):
    """
    add n vertices to a graph object 
    :param G: the graph
    :param n: number of vertices
    :return: the updated graph object G
    """
    for v in range(0, n):  # generate vertices
        G.add_node(v, name='node_' + str(v))
    return G


def graph_connect_edges(G, q):
    """
    iterate over all vertices in graph G and connect edges with prob q
    :param G: Graph to connect
    :param q: probability to connect two edges
    :return: the connected graph
    """
    for v in G.nodes():
        nodes = G.nodes()
        for n in nodes:
            if v == n:
                continue
            if random.random() < q:
                G.add_edge(v, n)
    return G


def find_unused_edges(G):
    """
    find and store unused edges of every vertex in the graph G,
    for every vertex store unused edges in a dictionary of lists  
    an example of key value pairs for each vertex are below
    {vertex: [unused edges list]}
    for example
    {n1 : [(n1, n2) , (n1, n3)]}
    ...
    {n10 : [(n10, n1), (n10, n5)]}
    :param G: a Graph
    :return : return a dictionary with lists of unused edges 
    """
    unused_edges = {}

    for v in G.nodes():
        unused_edges_of_v = []
        for u in G.nodes():
            if v == u:
                continue
            if nx.Graph.has_edge(G, v, u):
                unused_edges_of_v.append((v, u))
        unused_edges.update({v: unused_edges_of_v})

    return unused_edges


def print_path(path):
    print ("current path: "),
    for vertex in path:
        print(str(vertex) + ' -> '),
    print ('\n')


def is_hamiltonian(path, v, n):
    """
    :param path: a list  nodes in path
    :param v: current head
    :param n: total number of nodes in the graph 
    :return: True if it's a hamiltonian path False otherwise
    """
    if path[0] == v and len(path) == n:
        return True
    else:
        return False


def is_unused_list_empty(unused_edges, vertex):
    """
    given a dictionary of {vertex : list of unused edges} and
    a vertex , check if the unused edges list of the vertex is empty 
    a.k.a if the vertex has unused edges left
    :param vertex: the vertex to check 
    :param unused_edges: dictionary with unused_edges of all nodes
    :return: 
    """
    if len(unused_edges[vertex]) == 0:
        return True
    else:
        return False


def rotate(path, j):
    """
    rotate list of vertices at vertex j
    :param path: a list of nodes
    :param j: vertex to perform rotation at
    :return: rotated path 
    """
    if j in path:
        i = path.index(j)
        newpath = path[:i + 1]
        return newpath + list(reversed((path[i + 1:])))
    else:
        print("error vertex {} not in path".format(j))
        return None


def modified_hamiltonian_cycle(G, n):
    # for every vertex v in the graph
    # find unused adjacent vertices of vertex v
    # return a dictionary of {nodes: [unused edges list]}
    unused_edges = find_unused_edges(G)

    # make a dictionary of lists,it holds a list
    # of used edges for every vertex(key) in the
    # dictionary
    used_edges = {}
    for v in G.nodes():  # initially lists are empty
        used_edges.update({v: list()})

    path = list()  # holds the path of nodes
    head = random.choice(nx.nodes(G))  # start with a random vertex in graph G
    path.append(head)  # add to path

    loop = 0
    iteration_path = 0
    iteration_close_cycle = 0

    """ repeat until all adjacent nodes of head were visited from head
    """
    while not is_unused_list_empty(unused_edges, head):

        if len(path) < n:
            iteration_path += 1

        if iteration_path > 2 * n * math.log(n):
            print "Path iterations over 2*n*log(n)={} aborting".format(
                int(2 * n * math.log(n)))
            break
        if iteration_close_cycle > n * math.log(n):
            print "Close cycle iterations over n*log(n)={} aborting".format(
                int(n * math.log(n)))
            break

        x = float(
            len(used_edges[
                    head]))  # number of nodes visited from head before
        r = random.random()

        if r <= 1 / float(n):  # step 2.(b).i

            path = list(reversed(path))
            head = path[-1]  # set v1 as new head
        elif 1 / float(n) < r <= x / float(n):  # step 2.(b).ii

            # choose a random vertex adjacent to vk
            # edge is python tuple (v,u), we can access u
            # with edge[1] and v with edge[0].
            edge = random.choice(used_edges[head])

            if len(path) == n:  # num of iterations to close cycle
                iteration_close_cycle += 1

            if edge[1] not in path:  # extend step
                path.append(edge[1])
                head = edge[1]
            else:  # rotate step
                path = rotate(path, edge[1])
                head = path[-1]

            if is_hamiltonian(path, head, n):
                return (path, iteration_path, iteration_close_cycle)



        elif x / float(n) < r <= (
                        1 - 1 / float(n) - x / float(n)):  # step 2.(b).iii

            # pick a random adjacent edge to head
            edge = random.choice(unused_edges[head])
            random_edge_index = unused_edges[head].index(edge)

            # pop the edge from  the heads unused list of adjacent edges
            edge = unused_edges[head].pop(random_edge_index)

            # add new edge to used list
            used_edges[head].append(edge)

            if len(path) == n:  # num of iterations to close cycle
                iteration_close_cycle += 1

            if edge[1] not in path:  # extend
                path.append(edge[1])
                head = edge[1]
            else:
                path = rotate(path, edge[1])
                head = path[-1]

            if is_hamiltonian(path, edge[1], n):
                return (path, iteration_path, iteration_close_cycle)

    return None, iteration_path, iteration_close_cycle






if __name__ == "__main__":
    n = 1000 # number of nodes
    loops = 5 # number of loops

    """ pick a suitable p,q in [0 1]"""
    tuple_pq = find_pq(n)
    p = tuple_pq[0]  # unpack tuple
    q = tuple_pq[1]

    print ("Running for p{:f} q{:f}".format(p, q))
    print ("\n\nn: {}".format(n))
    print('-' * 80)
    print (
        '{:^10} {:^10}\t\t{:^10} {:^10} {:^10}'.format('loop', 'status',
                                                       'iter path',
                                                       'iter cycle', 'total'))
    print('-' * 80)
    print(
        '\t\t\t limits \t\t{:^10} {:^10} {:^10}'.format(
            int(2 * n * math.log(n)),
            int(n * math.log(n)),
            int(3 * n * math.log(n))))
    print('-' * 80)
    for i in range(0, loops):



        # make an empty directed graph object
        G = nx.DiGraph()

        # add vertices in graph
        G = graph_add_nodes(G, n)

        # connect each vertex in G with the other vertices with prob q
        G = graph_connect_edges(G, q)

        (cycle, iteration_path,
         iteration_close_cycle) = modified_hamiltonian_cycle(
            G, n)

        if cycle is None:

            print (
                '{:^10} {:^10}\t\t{:^10} {:^10} {:^10}'.format(i, 'FAIL',
                                                               iteration_path,
                                                               iteration_close_cycle,
                                                               iteration_path
                                                               + iteration_close_cycle))
        else:

            print (
                '{:^10} {:^10}\t\t{:^10} {:^10} {:^10}'.format(i, 'OK',
                                                               iteration_path,
                                                               iteration_close_cycle,
                                                               iteration_path + iteration_close_cycle))



