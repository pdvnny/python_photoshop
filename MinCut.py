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

from BFS import bfs
from queue import Queue
from copy import deepcopy

""" **************** FUNCTION OUTLINES ***********************

    *** EDMONDS-KARP ***
INPUTS: (1) graph, (2) source, (3) destination
OUTPUTS: (1) max-flow, (2) source side of min-cut, (3) sink side of min-cut

********************************************************** """


def gen_residual_graph(g, g_f):
    g_r = deepcopy(g)
    for node in range(1,len(g_r)+1):  # address each node one at a time

        # update existing edges ... change capacities and remove any edges if necessary
        for j in range(len(g_f[node-1][0])):
            remaining_cap = g_r[node-1][1][j] - g_f[node-1][1][j]

            # update capacity in g_r
            if remaining_cap == 0:    # remove edge in residual graph
                g_r[node-1][0].pop(j)
                g_r[node-1][1].pop(j)
            else:                      # decrease capacity
                g_r[node-1][1][j] = remaining_cap

            # Create reverse edge based on the flow in g_f
            flow = g_f[node-1][1][j]
            if flow > 0:
                dst = node
                src = g_f[node-1][0][j]
                g_r[src-1][0].append(dst)
                g_r[src-1][1].append(flow)
    # END OF FOR LOOP THROUGH ALL NODES

    return g_r


def edmonds_karp(g, s, t):
    # Initialize residual graph (g_r) as original graph
    g_r = deepcopy(g)

    # Create flow graph, f
    f = deepcopy(g)
    for node in f:  # these loops are meant to set the flow on each edge to 0
        for i in range(len(node[1])):
            node[1][i] = 0

    # Additional initialization
    max_flow = 0

    # Find an initial path
    pred, depth, st_path = bfs(g_r, s, t)

    # Starting while loop to repeatedly look for s-->t paths
    while (s in st_path) and (t in st_path):
        print("Current s->t path is:", st_path)

        # (1) find capacity of st-path & updating the flow graph
        cap = 999999
        for i in range(len(st_path)-1):
            src_node = st_path[i]
            dst_node = st_path[i+1]

            # finding the edge from the st_path & checking the capacity
            nbrs = g_r[src_node-1][0]   # g_r[src_node-1][0] => list of all neighbor vertices
            for j in range(len(nbrs)):
                if nbrs[j] == dst_node:
                    nbr_cap = g_r[src_node-1][1][j]
                    if nbr_cap < cap:
                        cap = nbr_cap
                    break
        # "cap" should be equal to the capacity of the s-t path at the end

        for i in range(len(st_path)-1):
            src_node = st_path[i]
            dst_node = st_path[i+1]

            # finding the edge from the st_path & updating the flow graph (a.k.a. update f with s-t path)
            nbrs = f[src_node-1][0]
            sub = False  # using this to control whether flow is added or subtacted
            if dst_node not in nbrs:  # accounting for possibility of a reverse edge
                nbrs = f[dst_node-1][0]
                src_node = st_path[i+1]
                dst_node = st_path[i]
                sub = True
            for j in range(len(nbrs)):
                if nbrs[j] == dst_node:
                    if sub:  # reverse edge -> decrease flow on this edge
                        f[src_node-1][1][j] -= cap
                    else:
                        f[src_node-1][1][j] += cap

        # END OF MAKING UPDATES BASED ON ST-PATH

        max_flow += cap

        # (2) Update the residual graph (a.k.a. update g_r with s-t path and flow graph)
        g_r = gen_residual_graph(g, f)

        # (3) Find another augmenting path before restarting the while loop
        pred, depth, st_path = bfs(g_r, s, t)
        # back to the top

    # END OF WHILE LOOP - no more augmenting paths

    # FINALLY!!! - Generate "source_cut" and "sink_cut"
    # "sink_cut" first
    myQ = Queue(maxsize=len(g_r)+1)
    sink_cut = []
    found = [False for i in range(len(pred))]
    myQ.put(t)
    found[t] = True
    while not myQ.empty():
        current = myQ.get(block=False)
        sink_cut.append(current)
        for i, v in enumerate(pred):
            if (v == current) and (not found[i]):
                myQ.put(v)
                found[i] = True
    # at the end, "sink_cut" should have all nodes from one half of the min-cut graph

    source_cut = []
    for n in range(1, len(g)+1):
        if not (n in sink_cut):
            source_cut.append(n)

    return max_flow, source_cut, sink_cut
