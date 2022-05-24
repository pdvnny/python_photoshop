"""
    Parker Dunn (parker_dunn@outlook.com OR pgdunn@bu.edu)

    Created on May 19, 2022

    About this project:

    I am planning to use content from my Advanced Data Structs and Algos course and a tutorial from online to create
    a sort of "photoshop" with Python.


"""

# Using this script to test functions... I guess

import sys
from read_graphs import read_graph_txt_to_arc
from BFS import bfs

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(sys.version)
    graph, s, t = read_graph_txt_to_arc("samplegraph1.txt")
    preds, depths, st_path = bfs(graph, s, t)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
