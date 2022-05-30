"""
    Parker Dunn (parker_dunn@outlook.com OR pgdunn@bu.edu)

    Created on 19 May 2022

    Part of "python photoshop" project

    GOAL: I want to use this file to read in graphs from files. I am thinking about using this
    file to create multiple functions for reading graphs. I will at least need to read graphs for:
    (1) read a simple graph into an "arc representation"
        -- each node stores neighbor nodes and edge weights
    (2) read an image into a graph
        -- I expect to have to do this in a few ways
        -- I expect to have a function for small images, and...
        -- I expect to have a different function for reading in a full blown image for image segmentation
"""

# **************** READ GRAPH TO ARC REPRESENTATION ************************
"""
INPUTS: (1) Filename
OUTPUTS: (1) Graph, (2) source, (3) destination
"""


def read_graph_txt_to_arc(graph_file):
    # grab graph information from file
    file = open(graph_file, 'r')
    graph_as_txt = file.readlines()
    file.close()

    # Basic Graph information
    graph_dims = graph_as_txt[0]
    sz = int(graph_dims[0])
    # print(f"Size of graph: {sz}")

    st = graph_as_txt[1]
    st_lst = st.split(" ")
    s = int(st_lst[0])
    t = int(st_lst[1])
    # print(f'Source: {s} | Destination: {t}')
    # print(f"Types are {type(s)} and {type(t)}")

    # Building graph
    graph = []
    for i in range(sz):
        graph.append([[], []])

    edges = graph_as_txt[2:]
    for edge in edges:
        src, dst, cap = edge.split(" ")
        graph[int(src)-1][0].append(int(dst))
        graph[int(src)-1][1].append(int(cap))

    # for node in graph:
    #     print(node)

    # print(graph)

    return graph, s, t
