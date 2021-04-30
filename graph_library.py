import matplotlib.pyplot as plt
import networkx as nx

from manim import *

#reference: https://github.com/nipunramk/Reducible	

class GraphNode:
    def __init__(self, name, position, radius=0.5, font_size=1):
        #geometric properties
        self.center = position
        self.radius = radius
        self.circle = Circle(radius=radius)
        self.circle.move_to(position)

        #node label 
        self.name_key = name
        self.name = Text(str(name))
        self.name.scale(font_size) #text size
        self.name.move_to(position)

        #list of neighbours 
        self.neighbours = []

        #useful for visit (TODO: move out to make this class more general)
        self.visited = False
        self.from_where = ''		
        

    def connect(self, other, arrow=False):
        #line between the current node and its neighbour ('other')
        line_center = Line(self.center, other.center)

        #now the problem is that the line connects the centers of the nodes
        
        #here we get the direction of the line and the point 'start' and 'end'
        direction = line_center.get_unit_vector()
        start, end = line_center.get_start_and_end()		
        #now we move 'start' and 'end' by the value of the radius along this direction		
        new_start = start + direction * self.radius
        new_end = end - direction * self.radius

        line = Line(new_start, new_end)	

        if arrow:
            line.add_tip()            

        #add 'other' node to the list of neighbours of the current node
        self.neighbours.append(other)

        return line


def node_layout(edges_input, layout = 'kamada_kawai_layout'):

    #we use the library NETWORKX, we create a graph and add the edges
    #https://networkx.org/documentation/stable/reference/drawing.html?highlight=layout#module-networkx.drawing.layout
    G = nx.DiGraph()				
    G.add_edges_from(edges_input) 

    try:
        layout_function = eval(f'nx.{layout}') #f-string 
        #in 'pos' we have each node label with (x,y) coordinates
        pos = layout_function(G)
        labels = list(pos.keys())
  
        #we want to give as output something in the form
        # {'0': array([-1.6,  0.1,  0. ]), '1': array([ 0.4, -1.8 ,  0. ])}
        
        #we use (x,y) coordinates from 'pos' and edit them in order to fit the space properly
        #the following coefficient indicates how much we want the nodes to be spaced out			
        #we compute the ratio between the available space and the space taken by the graph in order to scale it
        
        x = [x for x, y in pos.values()]
        y = [y for x, y in pos.values()]

        coeff_x = config.frame_x_radius/(abs(max(x)-min(x)))
        coeff_y = config.frame_y_radius/(abs(max(y)-min(y)))

        #here we save the scaled positions
        positions = []

        for label in labels:
            positions.append( np.array([pos.get(label)[0]*coeff_x, pos.get(label)[1]*coeff_y, 0]) )

        #the following is the output in the desired shape
        nodes_and_positions = dict(zip(labels, positions))

        return nodes_and_positions

    except:
        print('Layout not available')



def make_graph_given_positions(nodes_pos_input, edges_input, undirected=True, arrow=False, radius=0.5, font_size=1):
    nodes = {}
    edges = {}

    #from the input we read the label and the position, then we create a 'GraphNode'
    for node_label in nodes_pos_input.keys():
        pos = nodes_pos_input[node_label]
        nodes[node_label] = GraphNode(node_label, position=pos, radius=radius, font_size=font_size)

    #now we add edges to the dictionary 'edges', where the key is the pair (u, v)
    #first we create the pair (first, second) reading from the input 'edges_input'
    #then we call the function 'connect' on each edge    
    for edge in edges_input:
        first, second = edge
        edges[edge] = nodes[ first ].connect(nodes[ second ], arrow=arrow)
        
        #if the graph is undirected we add also the pair (v, u)
        if undirected:
            first, second = edge
            edge = second, first
            edges[edge] = nodes[ second ].connect(nodes[ first ], arrow=arrow)

    return nodes, edges       


def set_graph_visual_properites(nodes, edges, 
        node_color=LIGHT_GREY, stroke_color=WHITE, data_color=WHITE, edge_color=LIGHT_GREY, 
        scale_factor=1):

        n = []
        e = []

        #here we set visual properties of each node
        for node in nodes.values():
            node.circle.set_fill(color=node_color, opacity=0.5)
            node.circle.set_stroke(color=stroke_color)
            node.name.set_color(color=data_color)
            
            #add node to the list
            n.append(VGroup(node.circle, node.name))
            
        #here we set visual properties of each edge
        for edge in edges.values():
            edge.set_stroke(width=7*scale_factor)
            edge.set_color(color=edge_color)
            
            if edge.has_tip():
                edge.get_tip().set_stroke(width=1)

            e.append(edge)
        
        #this function returns a graph with all the colors/opacity/distances defined
        return VGroup( VGroup(*n), VGroup(*e) )		


def highlight_node(node, color=RED, scale_factor=1):

    #here we create a (red) circle with the same radius and opacity 0 
    highlighted_node = Circle(radius=node.circle.radius * scale_factor)
    highlighted_node.move_to(node.circle.get_center())
    highlighted_node.set_stroke(width=8 * scale_factor)
    highlighted_node.set_color(color)
    highlighted_node.set_fill(opacity=0)
    
    return highlighted_node	


def highlight_edge(edges, u, v, color=RED, scale_factor=1, arrow=False):
    #edge that we want to highlight
    
    edge = edges[(u, v)]
    
    #new line, same as the one already in the graph

    highlighted_edge = Line(edge.get_start(), edge.get_end())	
    highlighted_edge.set_stroke(width=16*scale_factor)
    highlighted_edge.set_color(color)

    if arrow:
        highlighted_edge.add_tip()    
        highlighted_edge.get_tip().set_color(color)   

    
    return highlighted_edge	


def dfs(nodes, start):
        #we want this function to return the order in which the nodes are visited: 'dfs_order'
        dfs_order = []

        #when visiting a node we also want to keep track of from which node we are coming from
        #this in necessary for the animation, because we need to know which edge to highlight

        #we add the first node to the stack
        stack = [ nodes[start] ]
        while len(stack) > 0:
            node = stack.pop()
            if not node.visited:
                node.visited = True
                #when a node is visited, we add its name to 'dfs_order'
                dfs_order.append( node.name_key ) 

                #now we check its neighbours
                for neighbour in node.neighbours: 
                    if not neighbour.visited:
                        #if a neighbour has never been visited we save that we are coming from the current node
                        neighbour.from_where = node.name_key
                        
                        #then we add it to the stack for it to be visited
                        stack.append(neighbour)

        return dfs_order 

