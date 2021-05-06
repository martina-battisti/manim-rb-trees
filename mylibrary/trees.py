#from manimlib.imports import *
from manim import *

#import igraph #????

RAD: float = 0.4
OP: float = 1.0
COL = WHITE
LEAFRAD: float = 0.1
LEAFCOL = BLACK
VARIABLE = "Nil"


class Node(VGroup):

    def __init__(self, val, **kwargs):
        #digest_config(self, kwargs, locals())
        super().__init__(**kwargs)
        #draw the node
        self.circle = Circle(radius = RAD, color = BLACK, stroke_color = WHITE)
        #self.text = Tex(str(val), color = WHITE) #the label
        self.text = Text(str(val)).scale(0.3) #the label
        #if val is not None:
            #self.text = Text(str(val)) #the label
        #else:
            #self.text = Tex("None")
        self.pos = self.get_center() #position of the node
        self.lne = Line(self.pos, self.pos, buff = RAD) #line from this node and the parent
        #self.lne = Line(buff = RAD) #line from this node and the parent
        node = self.add(self.circle, self.text, self.lne)
        node.set_fill(opacity=OP)
        node.to_edge(UP)
        #define tree structure
        self.l = None #left soon
        self.r = None #right soon
        self.p = None #parent
        self.v = val #value of the node
        self.d = 1 #level in the tree
        self.color = 1 # 1 . Red, 0 . Black
        #self.visit = None #is the node visited? not used yet
        #self.dele = 0 #is the node deleted? not used yet
        #self.vgroupL = None  #this node,left children and their lines (to move subtrees)
        #self.vgroupR = None  #this node,right children and their lines (to move subtrees)

    '''
    #Returns a boolean indicating if the node has children
    def has_children(self) -> bool: 
        return bool(self.get_children_count())

    #Returns the number of NOT NIL children the node has
    def get_children_count(self) -> int:
        if self.color == NIL:
            return 0
        return sum([int(self.l.color != NIL), int(self.r.color != NIL)])
    '''
#not used yet
class LeafNode(Node):
    
    def __init__(self):
        #super().__init__(**kwargs)
        #draw the node
        #global circle
        #circle = Circle(radius = RAD)
        #node = self.add(circle)
        #node.set_fill(opacity=OP, color = LEAFCOL)
        #node.to_edge(UP)
        #define tree structure
        #self.l = None #left soon
        #self.r = None #right soon
        #self.p = None #parent
        val = "Nil"
        self.v = val #value of the node
        #self.txt = Tex(str()) #the label
        #self.txt = Tex(str(node.v)) #the label
        #self.d = 1 #level in the tree
        #self.lne = None #line from this node and the parent
        #self.pos = self.get_center() #position of the node
        self.color = 0 # 1 . Red, 0 . Black

class Tree(VGroup):

    def __init__(self, parent=None):
        # Basic tree members
        #super().__init__(**kwargs)
        self.root = None
        
        # Tracking for using igraph to layout trees (not used)
        #self.igraph_vertex_id = 0
        
        # Manim objects related to the tree
        #self.label = None  # For this node
        #self.line_to_parent = None  # For this node
        #self.vgroup = None  # This node and all children and their lines
    
    def getRoot (self):
        return self.root

    def getLeft (self, node):
        return node.l
    
    def getRight (self, node):
        return node.r
    
    def getParent (self, node):
        return node.p
    
    def getDepth (self, node):
        return node.d

    def addd (self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root) 

    def _add (self, val, node):
        if val == node.v:
            node.v = node.v
        elif val < node.v:
            if node.l is not None:
                self._add(val, node.l)
            else:
                node.l = Node(val)
                (node.l).p = node
        else:
            if node.r is not None:
                self._add(val, node.r)
            else:
                node.r = Node(val)
                (node.r).p = node

    def find(self, val, node):
        if node is not None:
            return self._find(val, node)
        else:
            return None

    def _find(self, val, node):
        if val == node.v:
            return node
        elif (val < node.v and node.l is not None):
            node = node.l
            return self._find(val, node)
        elif (val > node.v and node.r is not None):
            node = node.r
            return self._find(val, node)

    def findMax(self, node):
        if node is not None:
            if node.v == "Nil":
                return node.p
            else:
                if node.r is not None:
                    if (node.r).v == "Nil":
                        return node
                    else:
                        node = node.r
                        return self.findMax(node)
                else: 
                    return node
        else:
            return None

    def findPred(self, node):
        if node is not None:
            if node.v == "Nil":
                return node.p
            else:
                if node.l is not None:
                    if (node.l).v == "Nil":
                        return node
                    else:
                        node = node.l
                    if node.r is not None:
                        if (node.r).v == "Nil":
                                return node
                        else:
                            node = node.r
                        return self.findMax(node)
                    else: 
                        return node
        else:
            return None

    def findMin(self, node):
        if node is not None:
            if node.v == "Nil":
                return node.p
            else:
                if node.l is not None:
                    if (node.l).v == "Nil":
                            return node
                    else:
                        node = node.l
                        return self.findMin(node)
                else: 
                    return node
        else:
            return None

    def findSucc(self, node):
        if node is not None:
            if node.v == "Nil":
                node = node.p
                return node
            else:
                if node.r is not None:
                    if (node.r).v == "Nil":
                        return node
                    else:
                        node = node.r
                    if node.l is not None:
                        if (node.l).v == "Nil":
                            return node
                        else:
                            node = node.l
                            return self.findMin(node)
                    else: 
                        return node
        else:
            return None

    #not used
    def delTree (self):
        # garbage collector will do this for us. 
        self.root = None
    
    def findParent (self, tmp):
            while tmp is not None:
                    tmp = tmp.p
                    return tmp
   
    def returnTree(self, node):
        if node.p is None:
            node.d = 1
        if node is not None:
            left_pos = None
            right_pos = None
            left = node.l
            right = node.r
            if left is not None:
                left.d = node.d + 1
                left_pos = node.get_center()+(1.2*DOWN)+(15*LEFT/(2**left.d))
                left.pos = left_pos
                self.returnTree(left)
    
            if right is not None:
                right.d = node.d + 1
                right_pos = node.get_center()+(1.2*DOWN)+(15*RIGHT/(2**right.d))
                right.pos = right_pos
                self.returnTree(right)
    
    def subTree(self, node, subtree):
        if node:
            if node.l is not None:
                self.subTree(node.l, subtree)

            subtree.append(node)
            subtree.append(node.lne)
            
            if node.r is not None:
                self.subTree(node.r, subtree)
        return subtree

    def reduceLevel(self, node):
        if node:
            if node.l is not None:
                self.reduceLevel(node.l)

            node.d = node.d - 1
            
            if node.r is not None:
                self.reduceLevel(node.r)   

    #DFS
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.l)
            res.append(root)
            res = res + self.inorderTraversal(root.r)
        return res

    #DFS
    def preorderTraversal(self, root):
        res = []
        if root:
            res.append(root)
            res = res + self.preorderTraversal(root.l)
            res = res + self.preorderTraversal(root.r)
        return res

    #DFS
    def postorderTraversal(self, root):
        res = []
        if root:
            res = self.postorderTraversal(root.l)
            res = res + self.postorderTraversal(root.r)
            res.append(root)
        return res 

    #BFS
    def bfs(self, root): 
        queue = Queue()
        queue.put(root)
        res = []

        while not queue.empty():
            root = queue.get()
            res.append(root)
            if root.l:
                queue.put(root.l)
            if root.r:
                queue.put(root.r)
        return res
    
class RedBlackTree(Tree):
    def __init__(self):
        
        #self.TNULL = Node("Nil")
        self.TNULL = Node("Nil")
        self.TNULL.color = 0
        (self.TNULL) = self.setColor((self.TNULL))
        self.TNULL.l = None
        self.TNULL.r = None
        self.root = self.TNULL
        
        #self.root = Node(0)
        #self.root = None
    
    def setColor(self, node):
        if node.color == 1:
            (node.circle).set_fill(color = NEW_RED)
        else:
            (node.circle).set_fill(color = BLACK)
        return node

    '''
    # fix the red-black tree
    def  __fix_insert(self, k):
        while (k.p).color == 1:
            if k.p == ((k.p).p).r:
                u = ((k.p).p).l # uncle
                if u.color == 1:
                    # case 3.1
                    u.color = 0
                    u = self.setColor(u)
                    (k.p).color = 0
                    (k.p) = self.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = self.setColor(((k.p).p))
                    k = (k.p).p
                else:
                    if k == (k.p).l:
                        # case 3.2.2
                        k = k.p
                        self.right_rotate(k)
                    # case 3.2.1
                    k.p.color = 0
                    (k.p) = self.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = self.setColor(((k.p).p))
                    self.left_rotate((k.p).p)
            else:
                u = ((k.p).p).r # uncle

                if u.color == 1:
                    # mirror case 3.1
                    u.color = 0
                    u = self.setColor(u)
                    (k.p).color = 0
                    (k.p) = self.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = self.setColor(((k.p).p))
                    k = (k.p).p 
                else:
                    if k == (k.p).r:
                        # mirror case 3.2.2
                        k = k.p
                        self.left_rotate(k)
                    # mirror case 3.2.1
                    (k.p).color = 0
                    (k.p) = self.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = self.setColor(((k.p).p))
                    self.right_rotate((k.p).p)
            if k == self.root:
                break
        (self.root).color = 0
        (self.root) = self.setColor((self.root))

    # rotate left at node x
    def left_rotate(self, x):
        y = x.r
        x.r = y.l
        if y.l != self.TNULL:
            (y.l).p = x

        y.p = x.p
        if x.p == None:
            self.root = y
        elif x == (x.p).l:
            (x.p).l = y
        else:
            (x.p).r = y
        y.l = x
        x.p = y

    # rotate right at node x
    def right_rotate(self, x):
        y = x.l
        x.l = y.r
        if y.r != self.TNULL:
            (y.r).p = x

        y.p = x.p
        if x.p == None:
            self.root = y
        elif x == (x.p).r:
            (x.p).r = y
        else:
            (x.p).l = y
        y.r = x
        x.p = y
    '''

    '''
    # insert the key into the tree and fix the tree
    def insert(self, key):
        # Ordinary Binary Search Insertion
        node = Node(key)
        node.p = None
        node.v = key
        node.l = (self.TNULL).copy()
        (node.l).txt = ((self.TNULL).txt).copy()
        node.r = (self.TNULL).copy()
        (node.r).txt = ((self.TNULL).txt).copy()
        node.color = 1 # new node must be red
        node = self.setColor(node)

        y = None
        x = self.root

        while x.v != (self.TNULL).v:
            y = x
            if node.v < x.v:
                x = x.l
            else:
                x = x.r

        # y is parent of x, x is the node
        # establish if x is left or right soon of y
        node.p = y
        if y == None:
            self.root = node
        elif node.v < y.v:
            y.l = node
        else:
            y.r = node

        # if new node is a root node, simply return
        if node.p == None:
            node.color = 0
            node = self.setColor(node)
            return

        # if the grandparent is None, simply return
        if (node.p).p == None:
            return

        # Fix the tree
        self.__fix_insert(node)
    
    # fix the rb tree modified by the delete operation
    def __fix_delete(self, x):
        while x != self.root and x.color == 0:
            # x is left soon
            if x == (x.p).l:
                # s is the right brother
                s = (x.p).r
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    (x.p).color = 1
                    self.left_rotate(x.p)
                    s = (x.p).r

                if (s.l).color == 0 and (s.r).color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.p
                else:
                    if (s.r).color == 0:
                        # case 3.3
                        (s.l).color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = (x.p).r

                    # case 3.4
                    s.color = (x.p).color
                    (x.p).color = 0
                    (s.r).color = 0
                    self.left_rotate(x.p)
                    x = self.root
            #x is right soon
            else:
                s = (x.p).l
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    (x.p).color = 1
                    self.right_rotate(x.p)
                    s = (x.p).l

                if (s.l).color == 0 and (s.r).color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.p
                else:
                    if (s.l).color == 0:
                        # case 3.3
                        (s.r).color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = (x.p).l 

                    # case 3.4
                    s.color = (x.p).color
                    (x.p).color = 0
                    (s.l).color = 0
                    self.right_rotate(x.p)
                    x = self.root
        #print(x.p.v)
        if x is not None:
            x.color = 0
    '''
    '''
    # substitute u with v
    def __rb_transplant(self, u, v):
        if u.p == None:
            self.root = v
        #u is left soon
        elif u == (u.p).l:
            (u.p).l = v
            v.p = u.p
        #u is right soon
        else:
            (u.p).r = v
            v.p = u.p
            

    def __delete_node_helper(self, node, key):
        # find the node containing key
        z = self.TNULL
        while node.v != (self.TNULL).v:
            if node.v == key:
                z = node

            if node.v <= key:
                node = node.r
            else:
                node = node.l

        if z == self.TNULL:
            print ("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if ((z.l).v == (self.TNULL).v) and ((z.r).v == (self.TNULL).v):
            z = None
            x = z
        elif ((z.l).v == (self.TNULL).v):
            x = z.r
            self.__rb_transplant(z, z.r)
        elif ((z.r).v == (self.TNULL).v):
            x = z.l
            self.__rb_transplant(z, z.left)
        else:
            y = self.findSucc(z)
            y_original_color = y.color
            x = y.r
            if y.p == z:
                x.p = y
            else:
                self.__rb_transplant(y, y.r)
                y.r = z.r
                (y.r).p = y

            self.__rb_transplant(z, y)
            y.l = z.l
            (y.l).p = y
            y.color = z.color
        if y_original_color == 0:
            self.__fix_delete(x)

    # delete the node from the tree
    def delete_node(self, data):
        self.__delete_node_helper(self.root, data)
    
    '''

    # print the tree structure (secondary function)
    def __print_helper(self, node, indent, last):
        
        #if node != self.TNULL:
        if node.v != "Nil":
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print (str(node.v) + "(" + s_color + ")")
            self.__print_helper(node.l, indent, False)
            self.__print_helper(node.r, indent, True)

    # print the tree structure on the screen
    def pretty_print(self):
        self.__print_helper(self.root, "", True)
    

    '''
    def layout(self, x_scale, y_scale):
        g = igraph.Graph()
        self._to_igraph_graph(g)
        layout = g.layout_reingold_tilford(root=[0])

        # Builtin plotting this for debugging is pretty helpful.
        # igraph.plot(g, layout=layout, bbox=(2000, 1000))

        # Scale the layout, and also convert y to match Manim's coords
        scaled_layout = [[x * x_scale, -y * y_scale] for x, y in layout]
        self._apply_layout(scaled_layout)

    def _to_igraph_graph(self, g, parent_id=None):
        v = g.add_vertex()
        self.igraph_vertex_id = v.index
        if parent_id is not None:
            g.add_edge(parent_id, v.index)
        for c in self.children:
            c._to_igraph_graph(g, v.index)

    def _apply_layout(self, layout):
        self.apply_layout(*layout[self.igraph_vertex_id])
        for c in self.children:
            c._apply_layout(layout)

    # Default is to simply move the label into position and add a line to the
    # parent.
    def apply_layout(self, x, y):
        self.label.move_to(np.array([x, y, 0]))
        if self.parent is not None:
            # It is more straightforward to simply redo the Line
            self.line_to_parent = self.create_line_between()

    # Create a line between a node and its parent. This default is reasonable
    # for a lot of label types.
    def create_line_between(self):
        pl = self.parent.label
        l = self.label
        if pl.get_x() <= l.get_x():
            direction = RIGHT
        else:
            direction = LEFT
        return Line(pl.get_corner(DOWN + direction) + DOWN * SMALL_BUFF,
                    l.get_top() + UP * SMALL_BUFF,
                    stroke_width=2,
                    color=GREY)

    def print_tree(self, level=0):
        print(" " * level + str(self))
        for c in self.children:
            c.print_tree(level + 1)

    # Always overwrites the old group
    def to_vgroup(self):
        self.vgroup = VGroup()
        if self.label is not None:
            self.vgroup.add(self.label)
        if self.line_to_parent is not None:
            self.vgroup.add(self.line_to_parent)
        for c in self.children:
            self.vgroup.add(c.to_vgroup())
        return self.vgroup
    '''