"""
    Parker Dunn (parker_dunn@outook.com OR pgdunn@bu.edu)

    Created on May 25th, 2022

    PROJECT: Python Photoshop - image segmentation application with a user interface

    TASK: Create a function (and all helper functions) to find the MAX-FLOW and MIN-CUT
    in a graph given the graph as an input.

    I will need to...
    (1) create the residual network
    (2) run the Edmonds-Karp algo (using BFS.py)
    (3) return the max-flow and min-cut (MIN-CUT as two sets of nodes)

"""

""" **************** FUNCTION OUTLINES ***********************

    *** EDMONDS-KARP ***
INPUTS: (1) graph, (2) source, (3) destination
OUTPUTS: (1) max-flow, (2) source side of min-cut, (3) sink side of min-cut

********************************************************** """

from BFS import bfs

def gen_residual_graph(g, g_f):

    return g_r

def edmonds_karp(g, s, t):
    # Initialize residual graph (g_r) as original graph
    g_r = g

    # Create flow graph, f
    f = g
    for node in f: # these loops are meant to set the flow on each edge to 0
        for i in range(len(node[1])):
            node[1][i] = 0

    # Additional initialization
    max_flow = 0

    # Find an initial path
    pred, depth, st_path = bfs(g_r, s, t)

    # Starting while loop to repeatedly look for s-->t paths
    while (s in st_path) and (t in st_path):
        # (1) find capacity of st-path
        cap = 99999
        for i in range(len(st_path)-1):
            src_node = st_path[i]
            dst_node = st_path[i+1]
            nbrs = g_r[src_node-1][0]   # g_r[src_node-1][0] => list of all neighbor vertices

            # finding the edge from the st_path and checking it's capacity
            for j in range(len(nbrs)):
                if nbrs[j] == dst_node:
                    nbr_cap = g_r[src_node-1][1][j]
                    if nbr_cap < cap:
                        cap = nbr_cap
                    break
        # NOW, "cap" should be equal to the capacity of the s-t path

        # (2) Update the flow graph (a.k.a. update f with s-t path)


        # (3) Update the residual graph (a.k.a. update g_r with s-t path and flow graph)


        # (4) Find another augmenting path before resarting the while loop
        pred, depth, st_path = bfs(g_r, s, t)
    # END OF WHILE LOOP


    return max_flow, source_cut, sink_cut