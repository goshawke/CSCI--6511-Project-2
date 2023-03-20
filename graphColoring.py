"""
Author: Connor Norton
Date: 03/01/2023
Last Updated: N/A

CS-6511 Artificial Intelligence
Project II

Description: You are given a graph in the form of a text file, that you are supposed to color. 
The proper vertex coloring is such that each vertex is assigned a color and no two adjacent vertices are assigned the same color.

Write a CSP algorithm to solve this coloring problem. The CSP algorithm should have the following components:
• Search algorithm to solve the CSP
• Heuristics (min remaining values, least constraining value)
• Constraint propagation using AC3.

Variables: n vertices, where n equals the number of vertices referenced in text file
Domain Values: m colors, where m equals the colors value in the first line of the text file
Constraints: 
    1. Each vertex must be assigned a color to be considered a solution
        - coloring[n] != null
        - if not, cannot be a goal state
    2. No 2 adjacent vertices can be assigned the same color
        - If vertex x and vertex y have an edge between them, they must be different colors
        - check the coloring of the adjacent nodes before giving coloring assignment

"""

"""
The vertices parameter is a list of vertex names (e.g. ["A", "B", "C"]), 
and the edges parameter is a list of tuples representing edges (e.g. [("A", "B"), ("B", "C")]).
"""
class Graph:
    def __init__(self, vertices, edges, colors):
        self.vertices = vertices
        self.edges = {vertex: [] for vertex in vertices}
        for edge in edges:
            self.edges[edge[0]].append(edge[1])
            self.edges[edge[1]].append(edge[0])
        self.num_colors = colors

    def __str__(self): 
        string = "Colors = % sNumber of Vertices = % s \nVertices:\n" % (self.num_colors, len(self.vertices) )
        for v in self.vertices:
            string += str(v) + "\n"
        string += "Edges:\n"
        for edge in self.edges:
            string += str(edge) + "\n"
        return string


"""
reads a graph in from a text file in the following format

colors = #
#,#
#,#
#,#
.
.
.

creates a graph object based on the input
"""
def read_graph(filename):
    with open(filename, 'r') as f:
        
        lines = f.readlines()
        num_colors = int(lines[0].strip("colors = "))
        # print('num colors is ' + num_colors)
        edges = [tuple(map(int, line.split(','))) for line in lines[1:]]
        vertices = []
        for edge in edges:
            # print(edge)
            v1,v2 = edge
            if vertices.count(v1) == 0:
                vertices.append(v1)
            if vertices.count(v2) == 0:
                vertices.append(v2)
        #for v in vertices:
            # print(v)
        graph = Graph(vertices, edges, num_colors)
        return graph


'''
This intitalizes the coloring list with the names of each vertex and a None value
Moreover, it begins the call to the recursive backtracking search function
'''
def graphColoring(graph):
    coloring = {}
    for v in graph.vertices:
        coloring[v] = None
    return backtracking_search(graph, coloring)

# implementation of the backtracting search pseudocode found in lecture 4
def backtracking_search(graph, coloring):
   
   # enforces constraint 1 - every vertex must be assigned a color
    if all(coloring[vertex] is not None for vertex in graph.vertices):
        return coloring

    # pick an unassigned (uncolored) vertex based on MRV    
    unassigned_vertex = select_vertex_MRV(graph, coloring)

    """
    1.  Order the possible colorings of that vertex by LCV
    2.  Loop through those possible colorings
    2a. Check if the graph would be consistent if assigned the coloring. If yes, assign that coloring to the unassigned vertex. If no, move on to next possible coloring
    2b. Runs the AC3 algorithm, returning a possible coloring solution
    2c. If the solution is valid, assigns the coloring and returns true. Else returns false and graphColoring also returns false

    """
    for coloring_value in order_LCV(unassigned_vertex, graph, coloring):
        if is_consistent(unassigned_vertex, coloring_value, coloring):
            coloring[unassigned_vertex] = coloring_value
            solutions = ac_3(graph, unassigned_vertex, coloring_value, coloring)
            if solutions is not False:
                for key, val in solutions.items():
                    coloring[key] = val
                result = backtracking_search(graph, coloring)
                if result is not False:
                    return result
                for key in solutions.keys():
                    coloring[key] = None
            coloring[unassigned_vertex] = None
    return False


# Implementation of AC3 algorithm from lecture 4. Used to enforce Arc Consistency
def ac_3(graph, unassigned_vertex, coloring_value, coloring):
    # a queue of arcs, initially just those neighboring the unassigned vertex
    queue = [(neighbor, unassigned_vertex) for neighbor in graph.edges[unassigned_vertex] if coloring[neighbor] is None]
    solutions = {}
    while queue:
        (a, b) = queue.pop(0)
        
        # returns true if all inconsistent coloring values have been removed from the graph, else false
        if remove_inconsistent_values(a, b, graph, coloring):
            if len(possible_colorings(a, graph, coloring)) == 1:

                color = possible_colorings(a, graph, coloring)[0]

                # checks if vertex a can be assigned this color, if not returns false and breaks if statement
                if not is_consistent(a, color, coloring):
                    return False
                # adds vertex a and the coloring to the list of solutions/inferences
                solutions[a] = color

                # removes vertex b from the queue
                queue += [(neighbor, a) for neighbor in graph.edges[a] if neighbor != b and coloring[neighbor] is None]
    return solutions


# returns all of the possible coloring values for any given vertex
def possible_colorings(vertex, graph, coloring):
    # find the colors that the vertex cannot use
    used_colors = set(coloring[neighbor] for neighbor in graph.edges[vertex] if coloring[neighbor] is not None)
    # return the colors that are not in used_colors
    return [color for color in range(graph.num_colors) if color not in used_colors]


# Selects an unassigned (uncolored) vertex using the minimum remaining values (MRV) heuristic
def select_vertex_MRV(graph, coloring):
    unassigned_vertex = [vertex for vertex in graph.vertices if coloring[vertex] is None]

    return min(unassigned_vertex, key=lambda vertex: len(possible_colorings(vertex, graph, coloring)))



# Looking at the vertex selected through the MRV heurisitic, this function orders possible coloring for the vertex using the least constraining value (LCV) heurisitic 
def order_LCV(vertex, graph, coloring):
    colors_LCV = possible_colorings(vertex, graph, coloring)
    return sorted(colors_LCV, key=lambda color: count_conflicts(vertex, coloring, graph, coloring))


# checks constraint 2 for one vertex and its neigghbors, that no adjacent vertices can have the same color value
def is_consistent(vertex, color, coloring):
    # returns True if coloring is consistent, False if it is inconsistent
    return all(coloring[neighbor] != color for neighbor in graph.edges[vertex])

# returns the number
def count_conflicts(vertex, color, graph, coloring):
    return sum(coloring[neighbor] == color for neighbor in graph.edges[vertex])


# Function to remove inconsistent coloring values from graph for arc consistency
def remove_inconsistent_values(a, b, graph, coloring):
    # returns false if not all inconsistent values are removed
    removed = False
    for color in possible_colorings(a, graph, coloring):
        if all(not is_consistent(b, color2, coloring) for color2 in possible_colorings(b, graph, coloring) if color2 != color):
            coloring[a] = color
            # assigned value of True when all inconsistent value are removed
            removed = True
    # returns T or F
    return removed



# This is where the graph is being read from the input file
graph = read_graph("CS6511 P2 Graph Coloring/input.txt")

# This function call runs the graph coloring algorithm and returns a list of the vertices and their assigned colors
coloring = graphColoring(graph)

# print colorin solution
for color in coloring:
    print("Vertex " + str(color) + " = " + str(coloring[color]))
