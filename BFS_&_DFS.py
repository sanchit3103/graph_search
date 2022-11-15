'''
ECE 172A, Homework 2 Maze Pathfinding
Author: regreer@ucsd.edu
Maze generator adapted from code by Łukasz Nojek
For use by UCSD ECE 172A students only.
'''

import matplotlib.pyplot as plt
import numpy as np
import pickle

def draw_path(final_path_points, other_path_points):
	'''
	final_path_points: the list of points (as tuples or lists) comprising your final maze path.
	other_path_points: the list of points (as tuples or lists) comprising all other explored maze points.
	(0,0) is the start, and (49,49) is the goal.
	Note: the maze template must be in the same folder as this script.
	'''
	im = plt.imread('172maze2021.png')
	x_interval = (686-133)/49
	y_interval = (671-122)/49
	plt.imshow(im)
	fig = plt.gcf()
	ax = fig.gca()
	circle_start = plt.Circle((133,800-122), radius=4, color='lime')
	circle_end = plt.Circle((686, 800-671), radius=4, color='red')
	ax.add_patch(circle_start)
	ax.add_patch(circle_end)
	for point in other_path_points:
		if not (point[0]==0 and point[1]==0) and not (point[0]==49 and point[1]==49):
			circle_temp = plt.Circle((133+point[0]*x_interval, 800-(122+point[1]*y_interval)), radius=4, color='blue')
			ax.add_patch(circle_temp)
	for point in final_path_points:
		if not (point[0]==0 and point[1]==0) and not (point[0]==49 and point[1]==49):
			circle_temp = plt.Circle((133+point[0]*x_interval, 800-(122+point[1]*y_interval)), radius=4, color='yellow')
			ax.add_patch(circle_temp)
	plt.show()

### Your Work Below:

# Function to obtain neighbors of any node
def get_neighbors(node , i, j):
	neighbors = []
	if node[0]:
		a = i
		b = j + 1
		neighbors.append([a,b])

	if node[1]:
		a = i + 1
		b = j
		neighbors.append([a,b])

	if node[2]:
		a = i
		b = j - 1
		neighbors.append([a,b])

	if node[3]:
		a = i - 1
		b = j
		neighbors.append([a,b])

	return neighbors

# Load Maze from the Pickle file
maze = pickle.load( open("172maze2021.p", "rb") )

# Depth First Search Algorithm

# Variable Definitions
stack 				= []
neighbors 			= []
visited_Nodes 		= []
final_Path 			= []
bool_Final_Path 	= False
x_Index 			= 0
y_Index 			= 0
iterations			= 0

# Initialize stack with the starting [0,0] Node
stack.append([0,0])

# Loop to run DFS Algorithm until all the nodes are covered
while len(stack) != 0:
	if stack[ len(stack) - 1 ] not in visited_Nodes:
		visited_Nodes.append( stack[ len(stack) - 1 ] )

		# Steps to obtain neighbors of a node
		x_Index = stack[ len(stack) - 1 ][0]
		y_Index = stack[ len(stack) - 1 ][1]
		neighbors = get_neighbors( maze[x_Index, y_Index], x_Index , y_Index )

		i = 0 # General counter

		# Condition to check if neighbors are present in stack and visited_Nodes arrays
		if len(neighbors) != 0:
			for i in range( len(neighbors) ):
				#if neighbors[i] not in visited_Nodes:
				if neighbors[i] not in stack:
					stack.append( neighbors[i] )

		# Condition to check if a node is reached which has no further neighbors. If so, remove such node from the stack
		if ( all( item in visited_Nodes for item in neighbors ) ):
			stack.pop()

		# Condition to check if the end point is reached
		if x_Index == 49 and y_Index == 49:
			bool_Final_Path = True

	# Condition to remove visited nodes from the Stack. Further, store the final path nodes in final_Path array
	else:
		if bool_Final_Path:
			final_Path.append( stack[ len(stack) - 1 ] )
		stack.pop()

	iterations = iterations + 1

print('Number of Iterations for DFS:', iterations)
draw_path(final_Path, visited_Nodes)

# Breadth First Search Algorithm

# Variable Definitions
queue 				= []
neighbors 			= []
visited_Nodes 		= []
final_Path 			= []
x_Index 			= 0
y_Index 			= 0
end_Point_Index		= 0
iterations			= 0
temp_Counter		= 1

# Initialize stack with the starting [0,0] Node
queue.append([0,0])

# Loop to run BFS Algorithm until all the nodes are covered
#while len(stack) != 0:
while x_Index != 49 or y_Index != 49:
	if queue[0] not in visited_Nodes:
		visited_Nodes.append( queue[0] )

		# Steps to obtain neighbors of a node
		x_Index = queue[0][0]
		y_Index = queue[0][1]
		neighbors = get_neighbors( maze[x_Index, y_Index], x_Index , y_Index )

		i = 0 # General counter

		# Condition to check if neighbors are present in stack and visited_Nodes arrays. Add the nodes in stack accordingly
		if len(neighbors) != 0:
			for i in range( len(neighbors) ):
				if neighbors[i] not in queue and neighbors[i] not in visited_Nodes:
					queue.append( neighbors[i] )

					# Condition to build the final path array
					if queue[0] not in final_Path:
						final_Path.append( queue[0] )

		# Remove the first node from the stack
		queue.pop(0)

		# Condition to check if the end point is reached
		if x_Index == 49 and y_Index == 49:
			final_Path.append( [x_Index, y_Index] )
			end_Point_Index = len(final_Path)

	# If a particular node is already visited, remove it from stack directly
	else:
		queue.pop(0)

	iterations = iterations + 1

# Loop to backtrack and determine the path from start point to end point

while temp_Counter < len(final_Path) + 2:

	# Get neighbors starting from the end point and then, for every node traversing reverse in the final_Path array
	x_Index = final_Path[ len(final_Path) - temp_Counter ][0]
	y_Index = final_Path[ len(final_Path) - temp_Counter ][1]
	neighbors = get_neighbors( maze[x_Index, y_Index], x_Index , y_Index )

	# Starting from the final point, backtrack and check if a particular node is a neighbor to the next node in final_Path array. Update the counter if it is a neighbor
	if final_Path[ len(final_Path) - temp_Counter - 1 ] in neighbors:
		temp_Counter = temp_Counter + 1

	# Remove the node from the final_Path array if a node is not a neighbor to the next node
	else:
		final_Path.pop( len(final_Path) - temp_Counter - 1 )

print('Number of Iterations for BFS:', iterations)
draw_path(final_Path, visited_Nodes)
