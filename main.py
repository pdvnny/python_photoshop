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
from MinCut import edmonds_karp

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(sys.version)
    filename = "samplegraph1.txt"
    graph, s, t = read_graph_txt_to_arc(filename)
    # preds, depths, st_path = bfs(graph, s, t)
    max_flow, s_cut, t_cut = edmonds_karp(graph, s, t)
    print(f"Max flow for {filename} is {max_flow}")
    print(f"The two graph cuts are...\n{s_cut}\n{t_cut}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
