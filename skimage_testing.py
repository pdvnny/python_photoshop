"""
    Parker Dunn (parker_dunn@outlook.com OR pgdunn@bu.edu)

    Created on May 29, 2022

    About this project:

    I am planning to use content from my Advanced Data Structs and Algos course and a tutorial from online to create
    a sort of "photoshop" with Python.

    This particular script is my effort to learn and use scikit-image from https://scikit-image.org/


"""

from skimage import data, io
import numpy as np
from MinCut import edmonds_karp

img1 = data.binary_blobs(length=32, blob_size_fraction=0.1, n_dim=2)  # each blob is smaller
img2 = data.binary_blobs(length=32, blob_size_fraction=0.2, n_dim=2)
img3 = data.binary_blobs(length=32, blob_size_fraction=0.3, n_dim=2)  # each block is larger

io.imshow(img2)
io.show()

# io.imsave("blob_test_1.png", img1)
# io.imsave("blob_test_2.png", img2)
# io.imsave("blob_test_3.png", img3)


def adjacent_nodes(node, dim):
    # I'm assuming nodes are labeled by row!
    left_edge = [i for i in range(0, dim[0] * dim[1], dim[1])]
    right_edge = [j+(dim[1]-1) for j in left_edge]

    if node in left_edge:
        left = -1
        right = node+1
    elif node in right_edge:
        right = -1
        left = node-1
    else:
        left = node-1
        right = node+1

    up = node-dim[0]
    down = node+dim[0]
    return [up, down, left, right]


def convert_linear_to_2d(lin_idx, dim):
    row = lin_idx // dim[1]
    col = lin_idx % dim[1]
    return row, col


def convert_blob_to_graph(img):
    """
    :param img: a numpy ndarray
    :return: graph: a graph of a blob image

    How to do it...
    (1) get dimensions of image
    (2) copy the image to graph
    """
    img_dim = img.shape
    dim = img_dim[:2]

    graph = []

    num_pixels = dim[0]*dim[1]

    " **********  Deal with all normal pixels first ************ "
    for k in range(0, num_pixels):
        # Get 2D indices
        idx_2d = convert_linear_to_2d(k, dim)

        # Get adjacent nodes
        neighbors = adjacent_nodes(k, dim)
        # neighbors.append(num_pixels)
        # neighbors.append(num_pixels+1)

        # Add edges for all adjacent nodes (including source and sink)
        arcs = []
        for neighbor in neighbors:
            if neighbor >= 0 and neighbor < num_pixels:
                arcs.append(neighbor)
        caps = []  # to be appended to arcs

        # Add "capacities" for neighboring pixels
        neighbor_idx_2d = [convert_linear_to_2d(i, dim) for i in arcs]
        for idx in neighbor_idx_2d:
            if img[idx] == img[idx_2d]:  # If this is true, then the value in each position of the image is the same
                caps.append(10)
            else:
                caps.append(1)

        # Add source and sink
        # arcs.append(num_pixels) # NO EDGES TO SOURCE
        arcs.append(num_pixels+1)  # the extra +1 is added later
        "Here, I decide that 'False' means background and 'True' means foreground"
        if img[idx_2d]:
            "FOREGROUND PIXEL"
            # caps.append(10)  # high capacity to foreground
            caps.append(1)  # low capacity to background
        else:
            "BACKGROUND PIXEL"
            # caps.append(1)      # low capacity to foreground
            caps.append(10)     # high capacity to background

        # FINISHING UP
        arcs = [dst+1 for dst in arcs]
        # For edmonds-karp algo...
        # vertex numbers are all one greater than their indices
        graph.append([arcs, caps])

    " ************ Add the source (num_pixels) and sink (num_pixels+1) ********** "

    """
        *** NOTE ***
        
        The structure of the image segmentation problem calls for...
        * Only OUTGOING edges from the SOURCE
        * Only INCOMING edges from the SINK
    """

    src = num_pixels
    # dst = num_pixels+1
    graph.append([[], []])  # adding source
    graph.append([[], []])  # adding sink

    # adding edges from the source to all nodes
    for i in range(num_pixels):
        graph[src][0].append(i)
        # graph[dst][0].append(i)
        idx_2d = convert_linear_to_2d(i, dim)
        if img[idx_2d]:
            graph[src][1].append(10)
            # graph[dst][1].append(1)
        else:
            graph[src][1].append(1)
            # graph[dst][1].append(10)

    return graph

    # END OF FUNCTION THAT CONVERTS A BLOB IMAGE TO A GRAPH


blob2_g = convert_blob_to_graph(img2)
# for i in range(10):
#     print(blob2_g[i])
# for i in range(10):
#     print(blob2_g[-i-3])

"""
    *************** WARNING **************
    
    You have to be careful with the indexing numbers for the graph vertices here!
    
    For the most part, I was using the direct indices as the "ID/#" of the vertex in this script.
    HOWEVER, the edmonds-karp & BFS algo actually use the 1-indexed values of the nodes.
    
    This means...
    -> When calling the edmonds-karp algo, my current setup requires using
        Source = number_of_pixels + 1
        Sink   = number_of_pixels + 2
    -> The s-cut and t-cut have the SAME "source" and "sink" index values!
        Source = number_of_pixels + 1
        Sink   = number_of_pixels + 2
"""

max_flow, s_cut, t_cut = edmonds_karp(blob2_g, 1025, 1026)  # these numbers could be automated but I was feeling lazy

foreground_lst = [False for i in range(1024)]
background_lst = [False for j in range(1024)]

for v in s_cut:
    if v < 1025:  # if v is not the source
        foreground_lst[v-1] = True
for v in t_cut:
    if v < 1025:  # if v is not the sink
        background_lst[v-1] = True

segmented_image_lsts = [foreground_lst, background_lst]
segmented_image = []
for lst in segmented_image_lsts:
    pic = np.array(lst)
    pic2 = np.reshape(pic, (32, 32))
    segmented_image.append(pic2)

foreground, background = segmented_image[:]

io.imshow(foreground)
io.show()
io.imshow(background)
io.show()

# END OF FILE
