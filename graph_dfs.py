from manim import *
from graph_library import *

class Graph_DFS(Scene):
    def construct(self):               

        #this is the input        
        #if in 'make_graph_given_position' we set 'undirected=True', now we only need to add the edge (u,v) and not (v,u)  
        edges_input = [('0','1') , ('0','2'), ('0','3'), ('2','3'), ('3','4'), ('1','4')]      

        arrow = False 	
        undirected = True
        
  
        """ Different inputs to try out:

        (best kamada_kawai_layout)
        edges_input = [('0','1') , ('0','2'), ('0','3'), ('2','3'), ('3','4'), ('1','4')] 

        (best spring_layout)
        edges_input = [('0','1') , ('0','2'), ('0','3'), ('0','4'), ('0','5')]		

        (best circular_layout)
        edges_input = [	('0', '1'), ('1', '2'), ('2', '3'), ('3', '4'), ('4', '0')]					

        """	

        #the function 'node_layout' uses the library NETWORKX and returns the position of each node
        nodes_and_positions = node_layout(edges_input, layout = 'kamada_kawai_layout')		


        '''
        One could also decide to manually set the position of each node.
        The input should be as the following:
        nodes_and_positions = { 'a' : LEFT * 4, 
                                'b' : LEFT * 2 + UP * 2, 'c' : LEFT * 2 + DOWN * 2,
                                'd' : RIGHT * 2 + UP * 2, 'e' : RIGHT * 2 + DOWN * 2,
                                'f' : RIGHT * 4} 
        '''
        
        #the function 'make_graph_given_positions' creates 'GraphNode' objects 
        nodes, edges = make_graph_given_positions(nodes_and_positions, edges_input, undirected=undirected, arrow=arrow)    

        #we set visual properties of the graph
        graph = set_graph_visual_properites(nodes, edges, node_color=LIGHT_GREY, stroke_color=WHITE, 
                                            data_color=WHITE, edge_color=LIGHT_GREY, scale_factor=1)


      
        #here we write the title
        title = Tex("Visita in profondità")
        title.scale(1.2)
        title.move_to(UP * 3.5)
        h_line = Line(LEFT, RIGHT)
        h_line.next_to(title, DOWN)

       

        #START OF THE ANIMATION

        #title (underlined)
        self.play(
            Write(title),
            ShowCreation(h_line)
        )
        self.wait()

        #display graph
        self.play(
            ShowCreation(graph),
            run_time=4
        )
        self.wait(1)
        

        #visualization of the visit (in this case dfs)
        #we start from node with key '0'
        start = '0'

        #first we execute the algorithm and get the order of the visit 
        #while visiting, we save from which node we are coming from when visiting a new one
        order = dfs(nodes, start) 
        
        #now we can visualize the visit: for each node saved in 'order' we highlight the edge that arrives to it 
        #then we highlight the actual node
        for current_node_key in order:

            if( current_node_key != start):                
                #'nodes[current_node_key].from_where' and 'current_node_key' are the extremes of the edge           
                highlighted_edge = highlight_edge(edges, nodes[current_node_key].from_where, current_node_key, scale_factor=1, color=RED, arrow=arrow)

                #animation of the edge
                self.play(
                    ShowCreation(highlighted_edge),
                    run_time=1
                )

            highlighted_node = highlight_node(nodes[current_node_key], scale_factor=1, color=RED)
            self.play(
                ShowCreation(highlighted_node),
                run_time=0.7
            )	