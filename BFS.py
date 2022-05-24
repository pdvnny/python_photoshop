"""

	Parker Dunn (parker_dunn@outlook.com)

	Created 6 May 2022

	Task: Implement the Breadth First Search (BFS) algorithm
	** I'll stick to using a module implementation of a Queue **

	Notes for using queue.Queue:
	- Some info on this queue: https://www.geeksforgeeks.org/queue-in-python/
	- "Queue" is a built-in module of Python
	- Syntax for creating an object --> "queue.Queue(maxsize)" OR "Queue(maxsize)"
		- maxsize = 0 creates an infinitely large queue
	- Functions!
		(1) maxsize 	-> returns number of items allowed
		(2) empty() 	-> boolean operation; True if queue is empty
		(3) get()		-> Remove and return an item from the queue. If queue is empty, wait until an item is available
		(4) put() 		-> put an item into the queue; if the queue is full, wiat until a free slot is available before adding the item

	- WARNING: unlike c++ implementations, this implementation of a queue seems to use a buffer that automatically manages
		overloading the queue or pulling too many elements from the queue. IT MAY BE EASY TO LOSE TRACK OF CALLS TO THE QUEUE
		BECAUSE ERRORS MAY NOT ALWAYS RAISE WHEN MY CODE MAKES A MISTAKE

"""

from queue import Queue


""" ASSUMED STRUCTURE OF THE GRAPH

	Each node is a tuple: (id/key, list of neighbors, list of weights/capacities)

"""

# *************** A FUNCTION TO PRINT BFS SPANNING TREE **********


def bfs_print(p_array, depth_array):
	print("Starting from the source(s)...\n")
	for i in range(1, len(p_array)):
		to_print = f"Node {i} - Depth {depth_array[i]} \t\t visited from {p_array[i]}"
		print(to_print)


# ******************** BFS FUNCTION ******************************


def bfs(G, s, t):
	# SETUP - create a queue
	myQ = Queue(maxsize=len(G)+1)

	# SETUP - create output arrays that are modified by the algo
	predecessors = [-1 for i in range(len(G)+1)]  # predecessors[0] not used
	depth = [-1 for i in range(len(G)+1)]
	visited = [False for i in range(len(G)+1)]
	st_path = []

	# SETUP - select node s to start from
	myQ.put(s)
	depth[s] = 0
	visited[s] = True

	# CORE BFS algo
	while True:
		while not myQ.empty():
			c = myQ.get(block=False)  # current node being processed
			nbrs = G[c-1][0]
			if nbrs:
				for nbr in nbrs:  # G[c-1][1] should refer to the list of neighbors
					if not visited[nbr]:
						myQ.put(nbr)
						predecessors[nbr] = c
						depth[nbr] = depth[c] + 1
						visited[nbr] = True
		unvisited = False
		for i in range(1, len(visited)):
			if not visited[i]:
				myQ.put(i)  # "i" should match a node number that was not visited
				unvisited = True
				break
		if not unvisited:
			break

	# PRINT BFS TREE(S)
	bfs_print(predecessors, depth)

	# GENERATE S-T Path
	st_path.append(t)
	pred = predecessors[t]
	while pred != -1:
		st_path.append(pred)
		pred = predecessors[pred]
	st_path.reverse()

	return predecessors, depth, st_path


"""
	For identifying the shortest st_path, while working through the Queue use some code like this	
	
	if (!st_path):   <-- Python lists are implicitly "False" when empty
		st_path.append(t)
		st_path.append(current element pulled from the queue)


	Using this approach, I will have to reverse the elements of "st_path" before returning them

"""


# *************** USING BFS **********************

# qSize = 10000  # can be adjusted, picked a random number that seemed large enough for now - NVM, DON'T NEED THIS


