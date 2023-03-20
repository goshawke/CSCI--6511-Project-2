import graphColoring

def test_graph_creation():
    num_colors = 3
    edges = [(1, 3),(2, 18), (3, 19), (2, 19), (1, 19)]
    vertices = [1, 2, 3, 18, 19]
    graph = graphColoring.Graph(vertices, edges, num_colors)

    if (graph != None):
        print(graph)
        return True
    return False

def test_input_graph():
    graph = graphColoring.read_graph("CS6511 P2 Graph Coloring/input.txt")
    if (graph != None):
        print(graph)
        return True
    return False


def test_graphColoring_SHOULD_FAIL():
    num_colors = 1
    edges = [(1, 3),(2, 18), (3, 19), (2, 19), (1, 19)]
    vertices = [1, 2, 3, 18, 19]
    graph = graphColoring.Graph(vertices, edges, num_colors)

    # This function call runs the graph coloring algorithm and returns a list of the vertices and their assigned colors
    coloring = graphColoring.graphColoring(graph)

    if coloring == False:
        return True
    else:
        return False


def test_graphColoring_SHOULD_PASS():
    num_colors = 3
    edges = [(1, 3),(2, 18), (3, 19), (2, 19), (1, 19)]
    vertices = [1, 2, 3, 18, 19]
    graph = graphColoring.Graph(vertices, edges, num_colors)

    # This function call runs the graph coloring algorithm and returns a list of the vertices and their assigned colors
    coloring = graphColoring.graphColoring(graph)

    if coloring != False:
        return True
    else:
        return False
