#from manimlib.imports import *
from manim import *

RAD: float = 0.4
OP: float = 1.0
COL = WHITE
LEAFRAD: float = 0.1
LEAFCOL = BLACK
VARIABLE = "Nil"


class Node(VGroup):

    def __init__(self, val, **kwargs):
        super().__init__(**kwargs)
        #draw the node
        self.circle = Circle(radius = RAD, color = BLACK, stroke_color = WHITE)
        self.text = Text(str(val)).scale(0.5) #the label
        self.pos = self.get_center() #position of the node
        self.lne = Line(self.pos, self.pos, buff = RAD) #line from this node and the parent
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
        
class Tree(VGroup):

    def __init__(self, parent=None):
        # Basic tree members
        self.root = None
        

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

    def deleteTree (self):
        # garbage collector will do this for us. 
        self.root = None

    def deleteNode (self, val, node, tree):
        # Base Case
        if node is None:
            return

        delnode = self.find(val, node)
        if delnode is None:
            return
        elif delnode.p is None:
            # Node with no child
            if delnode.l is None and delnode.r is None:
                delnode = None
                tree.root = None
                return

            # Node with only one child
            elif delnode.l is None:
                tree.root = delnode.r
                (delnode.r).p = delnode.p
                delnode = None
                return
    
            elif delnode.r is None:
                tree.root = delnode.l
                (delnode.l).p = delnode.p
                delnode = None
                return

            else:
                # Node with two children:
                # Get the inorder successor (smallest in the right subtree)
                temp = self.findSucc(delnode)
                parentsucc = temp.p
                if ((parentsucc).l) is not None and temp.v == ((parentsucc).l).v:
                    (parentsucc).l = None
                else:
                    (parentsucc).r = None
                tree.root = temp
                temp.p = delnode.p
                temp.l = delnode.l
                (delnode.l).p = temp
                temp.r = delnode.r
                (delnode.r).p = temp
                delnode = None
                return
        else:
            # Node with no child
            if delnode.l is None and delnode.r is None:
                if delnode.v == ((delnode.p).l).v:
                    (delnode.p).l = None
                else:
                    (delnode.p).r = None
                delnode = None
                return

            # Node with only one child
            elif delnode.l is None:
                (delnode.r).p = delnode.p
                if delnode.v == ((delnode.p).l).v:
                    (delnode.p).l = delnode.r
                else:
                    (delnode.p).r = delnode.r
                delnode = None
                return
    
            elif delnode.r is None:
                (delnode.l).p = delnode.p
                if delnode.v == ((delnode.p).l).v:
                    (delnode.p).l = delnode.l
                else:
                    (delnode.p).r = delnode.l
                delnode = None
                return

            else:
                # Node with two children:
                # Get the inorder successor (smallest in the right subtree)
                temp = self.findSucc(delnode)
        
                # Copy the inorder successor's content to this node
                if ((delnode.p).l) is not None and delnode.v == ((delnode.p).l).v:
                    (delnode.p).l = temp
                else:
                    (delnode.p).r = temp
                parentsucc = temp.p
                if ((parentsucc).l) is not None and temp.v == ((parentsucc).l).v:
                    (parentsucc).l = None
                else:
                    (parentsucc).r = None
                temp.p = delnode.p
                temp.l = delnode.l
                (delnode.l).p = temp
                temp.r = delnode.r
                (delnode.r).p = temp
                delnode = None
                return
    
   
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

    #DFS
    def inorderTraversal(self, node):
        res = []
        if node:
            res = self.inorderTraversal(node.l)
            res.append(node)
            res = res + self.inorderTraversal(node.r)
        return res

    #DFS
    def preorderTraversal(self, node):
        res = []
        if node:
            res.append(node)
            res = res + self.preorderTraversal(node.l)
            res = res + self.preorderTraversal(node.r)
        return res

    #DFS
    def postorderTraversal(self, node):
        res = []
        if node:
            res = self.postorderTraversal(node.l)
            res = res + self.postorderTraversal(node.r)
            res.append(node)
        return res 

    #BFS
    def bfs(self, node): 
        queue = Queue()
        queue.put(node)
        res = []

        while not queue.empty():
            node = queue.get()
            res.append(node)
            if node.l:
                queue.put(node.l)
            if node.r:
                queue.put(node.r)
        return res
    
class RedBlackTree(Tree):
    def __init__(self):
        
        self.TNULL = Node("Nil")
        self.TNULL.color = 0
        (self.TNULL) = self.setColor((self.TNULL))
        self.TNULL.l = None
        self.TNULL.r = None
        self.root = self.TNULL
        
    
    def setColor(self, node):
        if node.color == 1:
            (node.circle).set_fill(color = NEW_RED)
        else:
            (node.circle).set_fill(color = BLACK)
        return node
