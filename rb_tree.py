#!/usr/bin/env python
#from manimlib.imports import *
from manim import *


from mylibrary.trees import Node, Tree, RedBlackTree

RAD = 0.4
RUN_TIME_1 = 3
#https://algorithmtutor.com/Data-Structures/Tree/Red-Black-Trees/

#base scene for all tree scenes
class firstTreeScenes(Scene):

    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)

    def construct(self):
        pass


    def createArrow(self, fromPoint, toPoint):
            curvedArrow=CurvedArrow(start_point=(fromPoint), end_point=(toPoint), color = YELLOW)
            #curvedArrow.flip(RIGHT)
            self.play(Create(curvedArrow))
            self.wait(1)
            self.play(FadeOut(curvedArrow))
        
    def createLinearArrow(self, fromPoint, toPoint):
            arrow=Arrow(start_point=(fromPoint), end_point=(toPoint), color = YELLOW)
            #curvedArrow.flip(RIGHT)
            self.play(Create(arrow))
            self.wait(1)
            self.play(FadeOut(arrow))
             
    #print nodes
    def printNode(self, node, albero):
        if node is not None:
            if node == albero.getRoot():
                node.center()
                node.to_edge(UP)
                node.pos = node.get_center() 
                self.play(Create((node).move_to(node.pos)),
                        run_time=RUN_TIME_1,
                        )
            else:
                node.lne = always_redraw(lambda: Line((node.p).get_center(), node.pos, buff=RAD))
                self.play(Create((node).move_to(node.pos)), 
                        Create(node.lne),
                        run_time=RUN_TIME_1,
                        )
                
            albero.returnTree(node) #for Nill nodes
            tmp = node    
            right = node.r
            left = node.l
            if left is not None:
                self.printNode(left, albero)
            node = tmp
            if right is not None:
                self.printNode(right, albero)
    
    #print nodes one shot
    def printNodeOneShot(self, node, albero):
        if node is not None:
            if node == albero.getRoot():
                node.center()
                node.to_edge(UP)
                node.pos = node.get_center() 
                self.add((node).move_to(node.pos))
            else:
                self.add((node).move_to(node.pos), node.lne)
            albero.returnTree(node) #for Nill nodes
            tmp = node    
            right = node.r
            left = node.l
            if left is not None:
                self.printNodeOneShot(left, albero)
            node = tmp
            if right is not None:
                self.printNodeOneShot(right, albero)
    
    #print tree and evidence value in the vector (to modify)
    def printNodeVect(self, tmp, i, node, albero):
        if node == albero.getRoot() and i==0:
            self.play(Create(node))
            box[i] = Rectangle(height=1, width=1, color = YELLOW)
            box[i].move_to(3*DOWN+5*LEFT)
            text[i].move_to(3*DOWN+5*LEFT)
            self.add((text[i]).shift(RIGHT*i), (box[i]).shift(RIGHT*i))
            i = i + 1
        albero.returnTree(node)
        tmpn = albero.getRoot()   
        right = node.r
        left = node.l
        if i<10:
            if tmpl is not None:
                if tmpl.v == tmp[i]:
                    self.play(Create((left).move_to(left_pos)),
                        run_time=RUN_TIME_1,
                        )
                    box[i] = Rectangle(height=1, width=1, color = YELLOW)
                    box[i].move_to(3*DOWN+5*LEFT)
                    text[i].move_to(3*DOWN+5*LEFT)
                    self.add((text[i]).shift(RIGHT*i), (box[i]).shift(RIGHT*i))
                    i = i+1
                    self.printNodeVect(tmp, i, tmpn, albero)
                else:
                    self.printNodeVect(tmp, i, tmpl, albero)        

            node = tmpn
            if right is not None:
                if right.v == tmp[i]:
                    self.play(Create((right).move_to(right_pos)),
                        run_time=RUN_TIME_1,
                        )
                    box[i] = Rectangle(height=1, width=1, color = YELLOW)
                    box[i].move_to(3*DOWN+5*LEFT)
                    text[i].move_to(3*DOWN+5*LEFT)
                    self.add((text[i]).shift(RIGHT*i), (box[i]).shift(RIGHT*i))
                    i = i+1
                    self.printNodeVect(tmp, i, tmpn, albero)
                else:
                    self.printNodeVect(tmp, i, right, albero)

    #scroll nodes (from leef to root) (to modify)
    def scrollNode(self, node, albero):
        if node is not None:
            albero.returnTree(node)        
            
            if node == albero.getRoot():
                self.play(Create(node))
            tmp = node    
            tmpr = node.r
            tmpl = node.l
            if tmpl is not None:
                self.play(Create((node.l).move_to((node.l).pos)),
                        run_time=RUN_TIME_1,
                        )
                while node is not None:
                    self.play(GrowFromCenter(node))
                    node = node.p
                self.scrollNode(tmpl, albero)
            node = tmp
            if tmpr is not None:
                self.play(Create((node.r).move_to((node.r).pos)),
                        run_time=RUN_TIME_1,
                        )
                while node is not None:
                    self.play(GrowFromCenter(node))
                    node = node.p
                self.scrollNode(tmpr, albero)

    def highlightsNode(self, node):
        if node is not None:
            self.play(GrowFromCenter(node))

    def colorNode(self, node, colorn):
        if node is not None:
            node.set_fill(color = colorn)
            node.set_stroke(color = colorn)
            self.play(GrowFromCenter(node))
    
    #clear the scene
    def clearScene (self):
        self.clear()
    
    #print vector of nodes
    def printVect(self, tmp, node):
        global text 
        text = [0 for i in range(len(tmp))]
        global box
        box = [0 for i in range(len(tmp))]
        for i in range(len(tmp)):
            text[i]= Text(str(tmp[i]), font = 'Open Sans')
            box[i] = Rectangle(height=1, width=1)
            box[i].move_to(3*DOWN+5*LEFT)
            text[i].move_to(3*DOWN+5*LEFT)
            self.play(Write((text[i]).shift(RIGHT*i)))
            self.add(((box[i]).shift(RIGHT*i)))

    def highlightsPath(self, node, root):
        if node.v == root.v:
            node.set_fill(color = YELLOW)
            node.set_stroke(color = YELLOW)
        else:
            if node.v < root.v:
                root.set_fill(color = GREEN)
                root.set_stroke(color = GREEN)
                self.highlightsPath(node, root.l)
            else:
                root.set_fill(color = RED)
                root.set_stroke(color = RED)
                self.highlightsPath(node, root.r)

    #delete node from the subtree node
    def deleteNodeProva(self, val, node, albero):
        tmp = node
        if tmp == None:
            return tmp
        else:
            if val == tmp.v:
                #case 0: leaf
                if tmp.l == None and tmp.r == None:
                    self.remove(tmp.lne)
                    tmp = None
                    print("0")
                #case 1: left soon is none but there is a right subtree (UP+LEFT)
                elif tmp.l == None:
                    parent = tmp.p
                    #delete the subtree of the node to be deleted
                    subtree = []
                    subtree = albero.subTree(tmp, subtree)
                    subtreeGroup = Group(*subtree)
                    self.play(FadeOut(subtreeGroup))
                    tmp = tmp.r
                    # modify nodes dependencies
                    (tmp).p = parent
                    if parent.val > tmp.val:
                        parent.l = tmp
                    else:
                        parent.r = tmp
                    albero.reduceLevel(tmp)
                    self.printNode(parent, albero)
                    print("1")
                #case 2: right soon is none but there is a left subtree (UP+RIGHT)
                elif tmp.r == None:
                    parent = tmp.p
                    #delete the subtree of the node to be deleted
                    subtree = []
                    subtree = albero.subTree(tmp, subtree)
                    subtreeGroup = Group(*subtree)
                    self.play(FadeOut(subtreeGroup))
                    tmp = tmp.l
                    # modify nodes dependencies
                    (tmp).p = parent
                    if parent.val > tmp.val:
                        parent.l = tmp
                    else:
                        parent.r = tmp
                    albero.reduceLevel(tmp)
                    self.printNode(parent, albero)
                    print("2")
                #case 3: find successor and replace
                else:
                    tmp2 = albero.findSucc(tmp)
                    if (tmp2.v) == (tmp.r).v:
                        parent = tmp.p
                        left = tmp.l
                        #delete the subtree of the node to be deleted
                        subtree = []
                        subtree = albero.subTree(tmp, subtree)
                        subtreeGroup = Group(*subtree)
                        self.play(FadeOut(subtreeGroup))
                        tmp = tmp.r
                        # modify nodes dependencies
                        tmp.p = parent
                        tmp.l = left
                        if parent is not None:
                            if tmp.v < parent.v:
                                parent.l = tmp
                            else:
                                parent.r = tmp
                        albero.reduceLevel(tmp)
                        self.printNode(parent, albero)
                        print("3.1")
                    else:
                        subtree = []
                        subtree = albero.subTree(tmp2, subtree)
                        subtreeGroup = Group(*subtree)
                        self.play(FadeOut(subtreeGroup))
                        tmp.v = tmp2.v
                        # modify nodes dependencies
                        (tmp2.p).l = None
                        print("3.2")

            elif val < tmp.v:
                tmp.l = self.deleteNodeProva(val, tmp.l, albero)
            else:
                tmp.r = self.deleteNodeProva(val, tmp.r, albero)
            return tmp
    
    # rotate left at node x 
    def left_rotate_visua(self, x, albero):
        print("left_rotate")
        y = x.r # y is x's right soon
        parent = x.p #support for the print function
        x.r = y.l #subtree B (y.left) becomes x's right soon
        if (y.l).v != (albero.TNULL).v:
            (y.l).p = x
        y.p = x.p   # y becomes soon of x's parent
        if x.p == None:
            albero.root = y
        elif x == (x.p).l:
            (x.p).l = y # y is left soon
        else:
            (x.p).r = y # y is right soon
        y.l = x     # x is left soon of y
        x.p = y     # y is x parent
        self.printNode(parent, albero)
    
    # rotate right at node x 
    def right_rotate_visua(self, x, albero):
        print("right_rotate")
        y = x.l
        parent = x.p
        x.l = y.r
        if y.r != albero.TNULL:
            (y.r).p = x
        y.p = x.p
        if x.p == None:
            albero.root = y
        elif x == (x.p).r:
            (x.p).r = y
        else:
            (x.p).l = y
        y.r = x
        x.p = y
        self.printNode(parent, albero)


    # rotate left at node x (visualization)
    def left_rotate_step(self, x, albero):
        self.clearScene()
        root = albero.getRoot()
        self.printNodeOneShot(root, albero)
        print("left_rotate")
        t1 = Tex('Left rotation')
        t1.scale(1).to_edge(DOWN)
        self.play(Create(t1))
        
        y = x.r # y is x's right soon
        
        # Turn y's left subtree into x's right subtree
        self.remove (y.lne, x.lne, (y.l).lne)
        
        if (y.l).v != (albero.TNULL).v:
            (y.l).p = x
        y.p = x.p   # y becomes soon of x's parent

        if x.p == None:

            (y.lne).suspend_updating()

            albero.root = y
            y.p = x.p
            x.p = y
            x.lne = always_redraw(lambda: Line(x.get_center(), (x.p).get_center(), buff=RAD))
            self.add(x.lne, (y.l).lne)

            position_x = x.pos

            self.play((x).animate.move_to((x.l).pos),
                        run_time=RUN_TIME_1,
                        )
            x.pos = x.get_center()
            x.d = x.d + 1
            albero.returnTree(x)

            self.play((x.l).animate.move_to((x.l).pos),
                        run_time=RUN_TIME_1,
                        )

            self.remove((y.l).lne)
            x.r = y.l
            y.l = x
            (x.r).p = x
            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)
            albero.returnTree(x)
            self.play((x.r).animate.move_to((x.r).pos),
                        run_time=RUN_TIME_1,
                        )
            
            self.play((y).animate.move_to(position_x),
                        run_time=RUN_TIME_1,
                        )
            y.pos = y.get_center()
            y.d = y.d - 1
            albero.returnTree(y)

            self.play((y.r).animate.move_to((y.r).pos),
                        run_time=RUN_TIME_1,
                        )
            albero.returnTree(y.r)
            self.play(((y.r).l).animate.move_to(((y.r).l).pos),
                        run_time=RUN_TIME_1,
                        )
            self.play(((y.r).r).animate.move_to(((y.r).r).pos),
                        run_time=RUN_TIME_1,
                        )
        else:
            
            albero.returnTree(x.p)
            (y).lne = always_redraw(lambda: Line(y.get_center(), (y.p).get_center(), buff=RAD))
            self.add(y.lne)
            self.play((y).animate.move_to(x.pos),
                        run_time=RUN_TIME_1,
                        )
            y.pos = y.get_center()
            y.d = y.d - 1
            albero.returnTree(y)
            
            self.play((y.r).animate.move_to((y.r).pos),
                        run_time=RUN_TIME_1,
                        )
            (y.r).pos = (y.r).get_center()
            
            # move y and right subtree
            if x == ((x.p).l):
                ((y.p).l) = y # y is left soon
            else:
                ((y.p).r) = y # y is right soon
            
            self.remove((x.l).lne) #this is a problem!!!
            
            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), (x).get_center(), buff=RAD))
            self.add((x.l).lne)
            
            # move x and subtrees
            x.p = y     # y is x parent
            (x).lne = always_redraw(lambda: Line(x.get_center(), (x.p).get_center(), buff=RAD))
            self.add(x.lne)
            self.play((x).animate.move_to((x.l).pos),
                        run_time=RUN_TIME_1,
                        )
            x.pos = x.get_center()
            x.d = x.d + 1
            (x.l).p = x
            albero.returnTree(x)
            
            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)
            self.play((x.l).animate.move_to((x.l).pos),
                        run_time=RUN_TIME_1,
                        )
            (x.l).pos = (x.l).get_center()
            self.wait(1)

            self.remove((x.r).lne)
            
            (y.l).lne = always_redraw(lambda: Line((y.l).get_center(), (x).get_center(), buff=RAD))
            (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
            self.add((y.l).lne, y.lne)
            self.play((y.l).animate.move_to((x.r).pos),
                        run_time=RUN_TIME_1,
                        )
            (y.l).pos = (y.l).get_center()

            ((y.r).lne).suspend_updating()
            x.r = y.l #subtree B (y.left) becomes x's right soon
            (y.l).p = x

            y.l = x     # x is left soon of y

            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)
            
        
        self.wait(3)

        self.play(FadeOut(t1))
        self.clearScene()
        root = albero.getRoot()
        print(root.v)
        albero.returnTree(root)
        self.printNodeOneShot(root, albero)

        self.wait(3)
        
        
    # rotate right at node x
    def right_rotate_step(self, x, albero):
        self.clearScene()
        root = albero.getRoot()
        self.printNodeOneShot(root, albero)
        print("right_rotate")
        t1 = Tex('Right rotation')
        t1.scale(1).to_edge(DOWN)
        self.play(Create(t1))
        
        y = x.l # y is x's left soon
        
        # Turn y's right subtree into x's left subtree
        self.remove(y.lne, x.lne, (y.r).lne)

        if (y.r).v != (albero.TNULL).v:
            (y.r).p = x
        y.p = x.p

        if x.p == None:

            (y.lne).suspend_updating()
            
            albero.root = y
            y.p = x.p
            x.p = y
            x.lne = always_redraw(lambda: Line(x.get_center(), (x.p).get_center(), buff=RAD))
            self.add(x.lne, (y.r).lne)

            position_x = x.pos

            self.play((x).animate.move_to((x.r).pos),
                        run_time=RUN_TIME_1,
                        )
            x.pos = x.get_center()
            x.d = x.d + 1
            albero.returnTree(x)

            self.play((x.r).animate.move_to((x.r).pos),
                        run_time=RUN_TIME_1,
                        )

            self.remove((y.r).lne)
            x.l = y.r
            y.r = x
            (x.l).p = x
            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)
            albero.returnTree(x)
            self.play((x.l).animate.move_to((x.l).pos),
                        run_time=RUN_TIME_1,
                        )
            
            self.play((y).animate.move_to(position_x),
                        run_time=RUN_TIME_1,
                        )
            y.pos = y.get_center()
            y.d = y.d - 1
            albero.returnTree(y)

            self.play((y.l).animate.move_to((y.l).pos),
                        run_time=RUN_TIME_1,
                        )
            albero.returnTree(y.l)
            self.play(((y.l).l).animate.move_to(((y.l).l).pos),
                        run_time=RUN_TIME_1,
                        )
            self.play(((y.l).r).animate.move_to(((y.l).r).pos),
                        run_time=RUN_TIME_1,
                        )

        else:
            
            albero.returnTree(x.p)
            (y).lne = always_redraw(lambda: Line(y.get_center(), (y.p).get_center(), buff=RAD))
            self.add(y.lne)
            self.play((y).animate.move_to(x.pos),
                        run_time=RUN_TIME_1,
                        )
            y.pos = y.get_center()
            y.d = y.d - 1
            albero.returnTree(y)
            
            #self.play((y.l).animate.move_to((y.l).pos),
                        #run_time=RUN_TIME_1,
                        #)
            #(y.l).pos = (y.l).get_center()
            #------------HERE---------------
            self.updateTree(y.l)
            
            # move y and right subtree
            if x == ((x.p).r):
                ((y.p).r) = y # y is left soon
            else:
                ((y.p).l) = y # y is right soon
            
            self.remove((x.r).lne) #this is a problem!!!
            
            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), (x).get_center(), buff=RAD))
            self.add((x.r).lne)
            
            # move x and subtrees
            x.p = y     # y is x parent
            (x).lne = always_redraw(lambda: Line(x.get_center(), (x.p).get_center(), buff=RAD))
            self.add(x.lne)
            self.play((x).animate.move_to((x.r).pos),
                        run_time=RUN_TIME_1,
                        )
            x.pos = x.get_center()
            x.d = x.d + 1
            (x.r).p = x
            albero.returnTree(x)
            
            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)
            self.play((x.r).animate.move_to((x.r).pos),
                        run_time=RUN_TIME_1,
                        )
            (x.r).pos = (x.r).get_center()
            self.wait(1)

            self.remove((x.l).lne)
            
            (y.r).lne = always_redraw(lambda: Line((y.r).get_center(), (x).get_center(), buff=RAD))
            (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
            self.add((y.r).lne, y.lne)
            self.play((y.r).animate.move_to((x.l).pos),
                        run_time=RUN_TIME_1,
                        )
            (y.r).pos = (y.r).get_center()

            ((y.l).lne).suspend_updating()
            x.l = y.r #subtree B (y.left) becomes x's right soon
            (y.r).p = x

            y.r = x     # x is left soon of y

            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)
        
        
        self.wait(3)

        self.play(FadeOut(t1))
        self.clearScene()
        root = albero.getRoot()
        print(root.v)
        albero.returnTree(root)
        self.printNodeOneShot(root, albero)

        self.wait(3)


    def insert(self, val, albero):
        # Ordinary Binary Search Insertion
        node = Node(val)
        node.p = None
        node.v = val

        node.color = 1 # new node must be red
        node = albero.setColor(node)
        y = None
        x = albero.root

        t1 = Tex('\\textbf{Insertion:} the new node is ' + str(val))
        t1.scale(0.5).to_edge(RIGHT)
        self.play(Create(t1))
        self.wait(duration=2.5)
        node.next_to(t1, DOWN)
        self.play(Create(node))
        NodeIns = (node)
        
        root = albero.getRoot()
        self.play(
            NodeIns.animate.move_to((root).pos).to_edge(UP),
                        run_time=RUN_TIME_1,
                        )
        NodeIns.pos = NodeIns.get_center()
        self.play(FadeOut(t1))
        
        # node search
        while x.v != "Nil":
            y = x
            if node.v < x.v:
                x = x.l
                albero.returnTree(x)
                if x.l is not None:
                    self.play(
                        NodeIns.animate.move_to((y.l).pos),
                        run_time=RUN_TIME_1,            
                    )  
            else:
                x = x.r
                albero.returnTree(x)
                if x.r is not None:
                    self.play(
                        NodeIns.animate.move_to((y.r).pos),
                        run_time=RUN_TIME_1,            
                    ) 
        
        # y is parent of x, x is the node
        # establish if x is left or right child of y
        node.p = y
        if y == None:
            # new node is a root node
            albero.root = node
            (node).l = Node("Nil")
            ((node).l).color = 0
            (node).r = Node("Nil")
            ((node).r).color = 0
            ((node).l).lne = always_redraw(lambda: Line(node.get_center(), (node.l).get_center(), buff=RAD))
            ((node).r).lne = always_redraw(lambda: Line(node.get_center(), (node.r).get_center(), buff=RAD))
            
            albero.returnTree(node)
            self.play(((node).r).animate.move_to(((node).r).pos),
                        #Create(((node).r).lne),
                        run_time=RUN_TIME_1,
                        )
            self.play(((node).l).animate.move_to(((node).l).pos),
                        #Create(((node).l).lne),
                        run_time=RUN_TIME_1,
                        )
            self.add(((node.l).lne), ((node.r).lne))
            
            # case 1
            print("case 1")
            node.color = 0
            t1 = Tex('\\begin{flushleft}\\textbf{Case 1:}\\\\the new node is a root node\\\\it is a black node\\end{flushleft}')
            t1.scale(0.5).to_edge(RIGHT)
            self.play(Create(t1))
            self.wait(duration=2.5)
            node = albero.setColor(node)
            self.play(FadeOut(t1))
            return
            
        elif node.v < y.v:
            # new node is the left child
            self.remove(y.l)
            y.l = node
            (y.l).lne = always_redraw(lambda: Line(node.get_center(), (y).get_center(), buff=RAD))
            (y.l).l = Node("Nil")
            ((y.l).l).color = 0
            (y.l).r = Node("Nil")
            ((y.l).r).color = 0
            ((y.l).l).lne = always_redraw(lambda: Line((y.l).get_center(), ((y.l).l).get_center(), buff=RAD))
            ((y.l).r).lne = always_redraw(lambda: Line((y.l).get_center(), ((y.l).r).get_center(), buff=RAD))
            albero.returnTree(y)
            self.play((y.l).animate.move_to((y.l).pos),
                        run_time=RUN_TIME_1,
                        )
            albero.returnTree(y.l)
            ((y.l).r).move_to((y.l).pos)
            self.play(((y.l).r).animate.move_to(((y.l).r).pos),
                        #Create(((y.l).r).lne),
                        run_time=RUN_TIME_1,
                        )
            ((y.l).l).move_to((y.l).pos)
            self.play(((y.l).l).animate.move_to(((y.l).l).pos),
                        #Create(((y.l).l).lne),
                        run_time=RUN_TIME_1,
                        )
            self.add((((y.l).l).lne), (((y.l).r).lne))
        else:
            #new node is the right child
            self.remove(y.r)
            y.r = node
            (y.r).lne = always_redraw(lambda: Line(node.get_center(), (y).get_center(), buff=RAD))
            (y.r).l = Node("Nil")
            ((y.r).l).color = 0
            (y.r).r = Node("Nil")
            ((y.r).r).color = 0
            ((y.r).l).lne = always_redraw(lambda: Line((y.r).get_center(), ((y.r).l).get_center(), buff=RAD))
            ((y.r).r).lne = always_redraw(lambda: Line((y.r).get_center(), ((y.r).r).get_center(), buff=RAD))
            albero.returnTree(y)
            self.play((y.r).animate.move_to((y.r).pos),
                        run_time=RUN_TIME_1,
                        )
            albero.returnTree(y.r)
            ((y.r).r).move_to((y.r).pos)
            self.play(((y.r).r).animate.move_to(((y.r).r).pos),
                        #Create(((y.r).r).lne),
                        run_time=RUN_TIME_1,
                        )
            ((y.r).l).move_to((y.r).pos)
            self.play(((y.r).l).animate.move_to(((y.r).l).pos),
                        #Create(((y.r).l).lne),
                        run_time=RUN_TIME_1,
                        )
            self.add((((y.r).l).lne), (((y.r).r).lne))

        # if the grandparent is None, simply return
        if (node.p).p == None:
            return
        
        # Fix the tree
        self.__fix_insert(node, albero)

    def  __fix_insert(self, k, albero):
        while (k.p).color == 1: # parent is red
            if k.p == ((k.p).p).r:  # if parent is right child
                u = ((k.p).p).l # uncle
                #Case 3: P is red.
                if u.color == 1:    # uncle is red
                    # case 3.1: P is red and U is red too.
                    print("case 3.1 (a)")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.1:}\\\\Parent is red\\\\and x is red too\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('If the parent node P is red, this violates the property 4.\\\\P  and K are now both red.\\\\The grandparent node G must be black node because the tree before insertion must be a valid red-black tree.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('In this case, we flip the color of nodes P,U, and G.\\\\That means, P becomes black, U becomes black and, G becomes red.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    u.color = 0
                    u = albero.setColor(u)
                    (k.p).color = 0
                    (k.p) = albero.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = albero.setColor(((k.p).p))
                    k = (k.p).p
                    self.play(FadeOut(t1))
                else:   # uncle is black
                    #Case 3.2: P is red and U is black (or NULL)
                    if k == (k.p).l:
                        # case 3.2.2: P is right child of G and K is left child of P.
                        print("case 3.2.2")
                        t1 = Tex('\\begin{flushleft}\\textbf{Case 3.2.2:}\\\\P is right child of G and\\\\K is left child of P\\end{flushleft}')
                        t1.scale(0.5).to_edge(UR)
                        self.play(Create(t1))
                        self.wait(duration=2.5)
                        t2 = Tex('In this case, we first do the right-rotation at P.\\\\This reduces it to the case 3.2.1.')
                        t2.scale(0.5).to_edge(DOWN)
                        self.play(Create(t2))
                        self.wait(duration=3)
                        t3 = Tex('Next, we perform the left-rotation at G that makes G the new sibling S of K.\\\\Next, we change the color of S to red and P to black.')
                        t3.scale(0.5).to_edge(DOWN)
                        self.play(ReplacementTransform(t2, t3))
                        self.wait(duration=3)
                        self.play(FadeOut(t3))
                        k = k.p
                        self.right_rotate_step(k, albero)
                    # case 3.2.1: P is right child of G and K is right child of P.
                    print("case 3.2.1")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.2.1:}\\\\P is right child of G and\\\\K is right child of P\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('We first perform the left-rotation at G that makes G the new sibling S of K.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('Next, we change the color of S to red and P to black.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    k.p.color = 0
                    (k.p) = albero.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = albero.setColor(((k.p).p))
                    self.left_rotate_step((k.p).p, albero)
            else:   # if parent is left child
                u = ((k.p).p).r # uncle
                if u.color == 1:
                    # mirror case 3.1
                    print("case 3.1 (b)")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.1:}\\\\Parent is red\\\\and x is red too\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('If the parent node P is red, this violates the property 4.\\\\P  and K are now both red.\\\\The grandparent node G must be black node because the tree before insertion must be a valid red-black tree.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('In this case, we flip the color of nodes P,U, and G.\\\\That means, P becomes black, U becomes black and, G becomes red.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    u.color = 0
                    u = albero.setColor(u)
                    (k.p).color = 0
                    (k.p) = albero.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = albero.setColor(((k.p).p))
                    k = (k.p).p 
                    self.play(FadeOut(t1))
                else:
                    if k == (k.p).r:
                        # mirror case 3.2.2: P is left child of G and K is right child of P.
                        print("case 3.2.4")
                        t1 = Tex('\\begin{flushleft}\\textbf{Case 3.2.4:}\\\\P is left child of G and\\\\K is right child of P\\end{flushleft}')
                        t1.scale(0.5).to_edge(UR)
                        self.play(Create(t1))
                        self.wait(duration=2.5)
                        t2 = Tex('In this case, we first do the left-rotation at P.\\\\This reduces it to the case 3.2.1.')
                        t2.scale(0.5).to_edge(DOWN)
                        self.play(Create(t2))
                        self.wait(duration=3)
                        t3 = Tex('We perform the right-rotation at G that makes G the new sibling S of K.\\\\Next, we change the color of S to red and P to black.')
                        t3.scale(0.5).to_edge(DOWN)
                        self.play(ReplacementTransform(t2, t3))
                        self.wait(duration=3)
                        self.play(FadeOut(t3))
                        k = k.p
                        self.left_rotate_step(k, albero)
                    # mirror case 3.2.1: P is left child of G and K is left child of P.
                    print("case 3.2.3")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.2.3:}\\\\P is left child of G and\\\\K is left child of P\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('We change the color of S to red and P to black.')
                    t3 = Tex('We perform the right-rotation at G that makes G the new sibling S of K.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    (k.p).color = 0
                    (k.p) = albero.setColor((k.p))
                    if (k.p).p is not None:
                        ((k.p).p).color = 1
                        ((k.p).p) = albero.setColor(((k.p).p))
                    self.right_rotate_step((k.p).p, albero)
            if k == albero.root:
                break
        (albero.root).color = 0
        (albero.root) = albero.setColor(albero.root)
    
    # fix the rb tree modified by the delete operation
    def __fix_delete(self, x, albero):
        while x != albero.root and x.color == 0:
            # x is left soon
            if x == (x.p).l:
                # s is the right brother
                s = (x.p).r
                if s.color == 1:
                    # case 3.1
                    print("case 3.1")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.1:}\\\\x ’s sibling S is red\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('In this case, we switch the colors of S and x.parent\\\\and then perform the left rotation on x.parent.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('This reduces case 3.1 to case 3.2, 3.3 or 3.4.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    s.color = 0
                    s = albero.setColor(s)
                    (x.p).color = 1
                    x.p = albero.setColor(x.p)
                    self.left_rotate_step(x.p, albero)
                    s = (x.p).r

                if (s.l).color == 0 and (s.r).color == 0:
                    # case 3.2
                    print("case 3.2")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.2:}\\\\x’s sibling S is black,\\\\and both of S’s children are black.\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('The color of x’s parent can be red or black.\\\\We switch the color of S to red.\\\\If the color of x’ parent is red, we change its color to black.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('Otherwise, we make x’s parent a new x and repeat the process from case 3.1.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    s.color = 1
                    s = albero.setColor(s)
                    x = x.p
                else:
                    if (s.r).color == 0:
                        # case 3.3
                        print("case 3.3")
                        t1 = Tex('\\begin{flushleft}\\textbf{Case 3.3:}\\\\x’s sibling S is black, S’s left child is red,\\\\and S’s right child is black.\\end{flushleft}')
                        t1.scale(0.5).to_edge(UR)
                        self.play(Create(t1))
                        self.wait(duration=2.5)
                        t2 = Tex('We can switch the colors of S and its left child and then perform\\\\a right rotation on w without violating any of the properties.')
                        t2.scale(0.5).to_edge(DOWN)
                        self.play(Create(t2))
                        self.wait(duration=3)
                        t3 = Tex('This transforms the tree into case 3.4.')
                        t3.scale(0.5).to_edge(DOWN)
                        self.play(ReplacementTransform(t2, t3))
                        self.wait(duration=3)
                        self.play(FadeOut(t3))
                        (s.l).color = 0
                        s.l = albero.setColor(s.l)
                        s.color = 1
                        s = albero.setColor(s)
                        self.right_rotate_step(s, albero)
                        s = (x.p).r

                    # case 3.4
                    print("case 3.4")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.4:}\\\\x ’s sibling S is black,\\\\and S’s right child is red.\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('We change the color of S’s right child to black, x’s parent to black\\\\and perform the left rotation x’ parent node.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('This way we remove the extra black node on x.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    s.color = (x.p).color
                    s = albero.setColor(s)
                    (x.p).color = 0
                    x.p = albero.setColor(x.p)
                    (s.r).color = 0
                    s.r = albero.setColor(s.r)
                    self.left_rotate_step(x.p, albero)
                    x = albero.root
            #x is right soon
            else:
                s = (x.p).l
                if s.color == 1:
                    # case 3.1
                    print("case 3.1")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.1:}\\\\x ’s sibling S is red.\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('In this case, we switch the colors of S and x.parent\\\\and then perform the left rotation on x.parent.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('This reduces case 3.1 to case 3.2, 3.3 or 3.4.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    s.color = 0
                    s = albero.setColor(s)
                    (x.p).color = 1
                    x.p = albero.setColor(x.p)
                    self.right_rotate_step(x.p, albero)
                    s = (x.p).l

                if (s.l).color == 0 and (s.r).color == 0:
                    # case 3.2
                    print("case 3.2")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.2:}\\\\x’s sibling S is black,\\\\and both of S’s children are black.\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('The color of x’s parent can be red or black.\\\\We switch the color of S to red.\\\\If the color of x’ parent is red, we change its color to black.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('Otherwise, we make x’s parent a new x and repeat the process from case 3.1.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    s.color = 1
                    s = albero.setColor(s)
                    x = x.p
                else:
                    if (s.l).color == 0:
                        # case 3.3
                        print("case 3.3")
                        t1 = Tex('\\begin{flushleft}\\textbf{Case 3.3:}\\\\x’s sibling S is black, S’s left child is red,\\\\and S’s right child is black.\\end{flushleft}')
                        t1.scale(0.5).to_edge(UR)
                        self.play(Create(t1))
                        self.wait(duration=2.5)
                        t2 = Tex('We can switch the colors of S and its left child and then perform\\\\a right rotation on w without violating any of the properties.')
                        t2.scale(0.5).to_edge(DOWN)
                        self.play(Create(t2))
                        self.wait(duration=3)
                        t3 = Tex('This transforms the tree into case 3.4.')
                        t3.scale(0.5).to_edge(DOWN)
                        self.play(ReplacementTransform(t2, t3))
                        self.wait(duration=3)
                        self.play(FadeOut(t3))
                        (s.r).color = 0
                        s.r = albero.setColor(s.r)
                        s.color = 1
                        s = albero.setColor(s)
                        self.left_rotate_step(s, albero)
                        s = (x.p).l 

                    # case 3.4
                    print("case 3.4")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.4:}\\\\x ’s sibling S is black,\\\\and S’s right child is red.\\end{flushleft}')
                    t1.scale(0.5).to_edge(UR)
                    self.play(Create(t1))
                    self.wait(duration=2.5)
                    t2 = Tex('We change the color of S’s right child to black, x’s parent to black\\\\and perform the left rotation x’ parent node.')
                    t2.scale(0.5).to_edge(DOWN)
                    self.play(Create(t2))
                    self.wait(duration=3)
                    t3 = Tex('This way we remove the extra black node on x.')
                    t3.scale(0.5).to_edge(DOWN)
                    self.play(ReplacementTransform(t2, t3))
                    self.wait(duration=3)
                    self.play(FadeOut(t3))
                    s.color = (x.p).color
                    s = albero.setColor(s)
                    (x.p).color = 0
                    x.p = albero.setColor(x.p)
                    (s.l).color = 0
                    s.l = albero.setColor(s.l)
                    self.right_rotate_step(x.p, albero)
                    x = albero.root
        #print(x.p.v)
        if x is not None:
            x.color = 0    
        elif x.v == (albero.TNULL).v:
            x.color = 0
        x = albero.setColor(x)

    # substitute u with v
    def __rb_transplant(self, u, v, albero):
        if v is not None and u is not None:
            if u.p == None:
                albero.root = v
            #u is left soon
            elif u == (u.p).l:
                (u.p).l = v
                #if (v) is not None:
                v.p = u.p
            #u is right soon
            else:
                (u.p).r = v
                #if (v) is not None:
                v.p = u.p
        
    # delete node in a RB tree
    def delete_node(self, val, node, albero):
        
        # find the node containing val
        z = albero.find(val, node)
        
        # node not in the tree
        if z.v == (albero.TNULL).v:
            print ("Couldn't find value in the tree")
            t1 = Tex('Couldn\' t find value in the tree.')
            t1.scale(0.5).to_edge(RIGHT)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            return
        
        t1 = Tex('\\textbf{Deletion:} node ' + str(val))
        t1.scale(0.5).to_edge(RIGHT)
        self.play(Create(t1))
        self.wait(duration=2.5)
        self.play(FadeOut(t1))
        
        y = z
        y_original_color = y.color
        # the node is a leaf (left and right children are nil)
        if ((z.l).v == "Nil") and ((z.r).v == "Nil"):
            print("entra qui 1")
            t1 = Tex('The node is a leaf.')
            t1.scale(0.5).to_edge(RIGHT)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            position_z = z.pos
            parent = z.p
            ((z.l).lne).suspend_updating()
            ((z.r).lne).suspend_updating()
            ((z).lne).suspend_updating()
            self.play(FadeOut(z.l), FadeOut(z.r), FadeOut(z), FadeOut((z.l).lne), FadeOut((z.r).lne), FadeOut(z.lne))
            
            z = Node("Nil")
            if ((parent.l).v == val):
                parent.l = z
            else:
                parent.r = z
            z.p = parent 
            z.lne = always_redraw(lambda: Line(z.get_center(), (z.p).get_center(), buff=RAD))
            self.play(Create(z.move_to(position_z)), Create(z.lne))
            x = z
        # left child is nil
        elif ((z.l).v == "Nil"):
            print("entra qui 2")
            t1 = Tex('Node\'s left child is Nil.')
            t1.scale(0.5).to_edge(RIGHT)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            ((z.l).lne).suspend_updating()
            self.play(FadeOut(z.l), FadeOut((z.l).lne))

            position_z = z.pos
            ((z).lne).suspend_updating()
            self.play(FadeOut(z), FadeOut((z).lne))

            ((z.r).lne).suspend_updating()
            self.play(((z.r).animate.move_to(position_z)))
            (z.r).pos = (z.r).get_center()
            (z.r).d = (z.r).d - 1
            albero.returnTree(z.r)
            self.updateTree(z.r)

            x = z.r
            self.__rb_transplant(z, z.r, albero)
        # right child is nil
        elif ((z.r).v == "Nil"):
            print("entra qui 3")
            t1 = Tex('Node\'s right child is Nil.')
            t1.scale(0.5).to_edge(RIGHT)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            ((z.r).lne).suspend_updating()
            self.play(FadeOut(z.r), FadeOut((z.r).lne))

            position_z = z.pos
            ((z).lne).suspend_updating()
            self.play(FadeOut(z), FadeOut((z).lne))

            ((z.l).lne).suspend_updating()
            self.play(((z.l).animate.move_to(position_z)))
            (z.l).pos = (z.l).get_center()
            (z.l).d = (z.l).d - 1
            albero.returnTree(z.l)
            self.updateTree(z.l)

            x = z.l
            self.__rb_transplant(z, z.left, albero)
        # no nil children
        else:
            print("entra qui 4")
            t1 = Tex('Node\'s children are not Nil.')
            t1.scale(0.5).to_edge(RIGHT)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            y = albero.findSucc(z)
            y_original_color = y.color
            x = y.r
            if y.p == z:
                print("entra qui 4.1")
                t1 = Tex('Node\'s successor is node\'s son.')
                t1.scale(0.5).to_edge(RIGHT)
                self.play(Create(t1))
                self.wait(duration=2.5)
                self.play(FadeOut(t1))
                position_z = z.pos
                ((z.l).lne).suspend_updating()
                ((z.r).lne).suspend_updating()
                self.play(FadeOut(z), FadeOut((z.l).lne), FadeOut((z.r).lne))
                self.play(((y).animate.move_to(position_z)))
                (y).pos = (y).get_center()
                (y).d = (y).d - 1
                ((y.l).lne).suspend_updating()
                self.play(FadeOut(y.l), FadeOut((y.l).lne))
                albero.returnTree(y)
                self.updateTree(y.r)
                x.p = y
                #(z.l).p = y
                #y.l = z.l
            else:
                print("entra qui 4.2")
                position_z = z.pos
                position_y = y.pos
                ((y).lne).suspend_updating()
                self.play(((y).animate.move_to(position_z)))
                ((y.l).lne).suspend_updating()
                self.play(FadeOut(y.l), FadeOut((y.l).lne))
                (y.p).l = y.r
                self.play(((y.r).animate.move_to(position_y)))
                self.__rb_transplant(y, y.r, albero)
                y.r = z.r
                (y.r).p = y

            self.__rb_transplant(z, y, albero)
            y.p = z.p
            y.l = z.l
            (y.l).p = y
            y.color = z.color
            y = albero.setColor(y)
        
        if y_original_color == 0:
            if x is not None:
                t1 = Tex('\\begin{flushleft}\\textbf{Case 3:}\\\\the node is a black node.\\\\The property is violated.\\end{flushleft}')
                t1.scale(0.5).to_edge(RIGHT)
                self.play(Create(t1))
                self.wait(duration=2.5)
                self.play(FadeOut(t1))
                self.__fix_delete(x, albero)
        else:
            t1 = Tex('\\begin{flushleft}\\textbf{Case 1:}\\\\the node is a red node.\\\\Delete x since deleting a red node doesn’t violate any property.\\end{flushleft}')
            t1.scale(0.5).to_edge(RIGHT)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
        
        self.wait(3)
        self.clearScene()
        self.wait(3)
        root = albero.getRoot()
        print (root.v)
        self.printNodeOneShot(root, albero)
        self.wait(3)

    # delete the node from the tree
    #def delete_node(self, data, albero):
        #self.__delete_node_helper(self.root, data, albero)

    # move nodes to the new position in a recursive way
    def updateTree(self, node):
        self.play((node).animate.move_to(node.pos))
        if node.l is not None:
            self.updateTree(node.l)
        if node.r is not None:
            self.updateTree(node.r)

            

    # RULES
    def baseRules(self):
        f1 = Tex("A red-black tree T is a binary search tree\\\\having following five additional properties:")
        f1.to_edge(UP).scale(0.8).set_color(RED)
        bl = BulletedList('{\\small 1) Every node in T is either red or black.}',
                          '{\\small 2) The root node of T is black.}',
                          '{\\small 3) Every Nill node is black.} \\tiny{(NULL nodes are the leaf nodes. They do not contain any keys.)}',
                          '{\\small 4) If a node is red, both of its children are black. This means no two nodes on a path can be red nodes.}',
                          '{\\small 5) Every path from a root node to a Nill node has the same number of black nodes.}',
                          buff=MED_SMALL_BUFF)
        bl.next_to(f1, DOWN, aligned_edge=LEFT).scale(0.7).to_edge(LEFT)
        f2 = Tex("Failure to preserve any of the above five properties\\\\makes T a non-red-black tree.")
        f2.next_to(bl, DOWN).scale(0.5).set_color(BLUE_A)
        self.play(FadeIn(f1))
        self.wait()
        self.play(Write(bl[0]))
        self.wait()
        self.play(Write(bl[1]))
        self.wait()
        self.play(Write(bl[2]))
        self.wait()
        self.play(Write(bl[3]))
        self.wait()
        self.play(Write(bl[4]))
        self.wait()
        self.play(FadeIn(f2))
        self.wait(duration=2)
        elements = VGroup(f1, bl, f2)
        self.play(FadeOut(elements))

    def insertionRules(self):
        f1 = Tex("To insert a node K into a red-black tree T:")
        
        f1.to_edge(UP).set_color(TEAL_B)
        bl = BulletedList('Insert K using an ordinary BST insertion operation.',
                          'Color K red.',
                          'Check if the insertion violated the red-black tree properties\\\\and fix it.',
                          buff=MED_SMALL_BUFF)
        bl.next_to(f1, DOWN, aligned_edge=LEFT).scale(0.8).move_to(LEFT)
        self.play(FadeIn(f1))
        self.wait()
        self.play(FadeIn(bl[0]))
        self.wait()
        
        self.play(FadeIn(bl[1]))
        self.wait()
        self.play(FadeIn(bl[2]))
        self.wait(duration=3)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

        f1 = Tex("\\begin{flushleft}To re-structure the tree\\\\in order to not violate the insertion we can use:\\end{flushleft}")
        f1.to_edge(UP).set_color(TEAL_B)
        bl = BulletedList('\\textbf{Left-Rotation:}\\\\The left rotation at node x makes x goes down\\\\in the left direction and as a result,\\\\its right child goes up. ',
                          '\\textbf{Right-Rotation:}\\\\The right rotation at node x makes x goes down\\\\in the right direction and as a result,\\\\its left child goes up.',
                          '\\textbf{Recolor:}\\\\Recolor flips the color of a node.\\\\If it is red, it becomes black and vice-versa.',
                          buff=MED_SMALL_BUFF)
        bl.next_to(f1, DOWN, aligned_edge=LEFT).scale(0.5).move_to(LEFT)
        self.play(FadeIn(f1))
        self.wait()
        self.play(FadeIn(bl[0]))
        self.wait()
        self.play(FadeIn(bl[1]))
        self.wait()
        self.play(FadeIn(bl[2]))
        self.wait(duration=3)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

    def deletionRules(self):
        f1 = Tex("To delete a node K into a red-black tree T:")
        
        f1.to_edge(UP).set_color(TEAL_B)
        bl = BulletedList('Find the node in the tree.',
                          'Delete K and re-establish connections between nodes.',
                          'Check if the deletion violated the red-black tree properties\\\\and fix it.',
                          buff=MED_SMALL_BUFF)
        bl.next_to(f1, DOWN, aligned_edge=LEFT).scale(0.5).move_to(LEFT)
        self.play(FadeInFromDown(f1))
        self.wait()
        self.play(FadeInFromDown(bl[0]))
        self.wait()
        
        self.play(FadeInFromDown(bl[1]))
        self.wait()
        self.play(FadeInFromDown(bl[2]))
        self.wait(duration=3)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

        f1 = Tex("\\begin{flushleft}To re-structure the tree\\\\in order to not violate the RB properties we can use:\\end{flushleft}")
        f1.to_edge(UP).set_color(TEAL_B)
        bl = BulletedList('\\textbf{Left-Rotation:}\\\\The left rotation at node x makes x goes down\\\\in the left direction and as a result,\\\\its right child goes up. ',
                          '\\textbf{Right-Rotation:}\\\\The right rotation at node x makes x goes down\\\\in the right direction and as a result,\\\\its left child goes up.',
                          '\\textbf{Recolor:}\\\\Recolor flips the color of a node.\\\\If it is red, it becomes black and vice-versa.',
                          buff=MED_SMALL_BUFF)
        bl.next_to(f1, DOWN, aligned_edge=LEFT).scale(0.5).move_to(LEFT)
        self.play(FadeInFromDown(f1))
        self.wait()
        self.play(FadeInFromDown(bl[0]))
        self.wait()
        self.play(FadeInFromDown(bl[1]))
        self.wait()
        self.play(FadeInFromDown(bl[2]))
        self.wait(duration=3)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# HERE START THE SCENES
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------


        

class RBTree(firstTreeScenes):
    def construct(self):

        bst = RedBlackTree()

        #self.baseRules()

        #self.insertionRules()

        self.insert(15, bst)
        #self.insert(5, bst)
        self.insert(6, bst)
        self.insert(20, bst)
        #self.insert(10, bst)
        
        node = bst.getRoot()

        self.delete_node(15, node, bst)
        
        

        self.wait(3)

class RBTree2(firstTreeScenes):
    def construct(self):

        bst = RedBlackTree()
        code = Tex(r"RED", r"BLACK", r"TREES", 
            background_stroke_width=1, 
            background_stroke_color=WHITE)
        code.set_color_by_tex('RED', RED)
        code.set_color_by_tex('BLACK', BLACK)
        self.play(Create(code))
        self.wait(3)
        self.play(FadeOut(code))
        f1 = Tex("To introduce red-black trees is important\\\\to know the rules of binary search trees:")
        f1.to_edge(UP).scale(0.8).set_color(PURPLE_C)
        bl = BulletedList('{\\small Every node can have only two subtrees. (Two sons)}',
                          '{\\small The tree is ordered.\\\\ Left nodes are smaller, right nodes are larger.}',
                          buff=MED_SMALL_BUFF)
        bl.scale(0.7)
        self.play(FadeIn(f1))
        self.wait()
        self.play(Write(bl[0]))
        self.wait()
        self.play(Write(bl[1]))
        self.wait()
        self.play(bl.animate.next_to(f1, DOWN))
        elements = VGroup(f1, bl)
        self.play(elements.animate.scale(0.9).to_edge(LEFT).to_edge(DOWN))

        

        albero = Tree()
        albero.addd(13)
        albero.addd(3)
        albero.addd(23)
        albero.addd(16)
        node = albero.getRoot()
        self.printNode(node, albero)
        
        #self.play((elements.scale(0.9).to_edge(LEFT)))
        self.wait(3)
        self.clearScene()
        self.add(elements)

        albero2 = Tree()
        albero2.addd(1)
        albero2.addd(3)
        albero2.addd(10)
        albero2.addd(26)
        albero2.addd(15)
        node2 = albero2.getRoot()
        self.printNode(node2, albero2)

        f2 = Tex("If the tree is unbalanced, as in the example, the complexity is greater.")
        f3 = Tex("For this reason we introduce the concept of balanced search trees,\\\\among the variants we will illustrate the red and black trees.")
        f2.to_edge(LEFT).scale(0.5)
        f3.to_edge(LEFT).scale(0.5)
        self.play(FadeIn(f2))
        self.wait(3)
        self.play(Transform(f2, f3))
        self.wait(4)
        self.clearScene()
        #self.play(FadeOut(elements))
        self.baseRules()
        

        self.wait(3)

class RBTree3(firstTreeScenes):
    def construct(self):

        bst = RedBlackTree()
        txt1 = Text("let's see an example")
        txt1.scale(0.8)
        txt2 = Text("we insert the nodes inside the red black tree")
        txt2.scale(0.8)
        self.play(Create(txt1))
        self.wait(3)
        self.play(Transform(txt1, txt2))
        self.wait(3)
        self.play(FadeOut(txt1))
        #self.baseRules()
        self.insertionRules()
        self.wait(3)

class RBTree4(firstTreeScenes):
    def construct(self):

        bst = RedBlackTree()
        self.insert(20, bst)
        self.insert(7, bst)
        self.insert(3, bst)
        self.insert(16, bst)
        self.insert(18, bst)
        self.wait(3)

class deleteTree(firstTreeScenes):
    def construct(self):
    
        global n
        n = 10
        albero = Tree()
        
        albero.addd(13)
        albero.addd(3)
        albero.addd(23)
        albero.addd(16)
        albero.addd(5)
        albero.addd(1)
        albero.addd(8)
        albero.addd(15)
        albero.addd(0)
        albero.addd(9)
        albero.addd(6)


        #caso 1: elimino una foglia 0, 6, 9, 15                 OK
        #caso 2: elimino un nodo con un figlio 1, 5, 8, 16      1, 5, 8, 16
        #caso 3: elimino un nodo con due figli 3, 23, 13        3, 13, 23
        # 1, 16
        
        node = albero.getRoot()
        valdel = [1, 0, 3, 23, 13]
        vaaldeln = albero.find(valdel[0], node)

        self.printVect(valdel, node)
        self.printNode(node, albero)
        
        if vaaldeln is not None:
            self.deleteNodeProva(valdel[0], node, albero)
            self.deleteNodeProva(valdel[1], node, albero)
            self.deleteNodeProva(valdel[2], node, albero)
            self.deleteNodeProva(valdel[3], node, albero)
            self.deleteNodeProva(valdel[4], node, albero)
            self.wait(3)
            
        self.clearScene()
        self.printNode(node, albero)

        self.wait(5)

class firstTree(firstTreeScenes):

    def construct(self):

        t1 = Tex('First Tree')
        t1.scale(1.5).to_edge(TOP)
        self.play(Create(t1))
        self.wait(duration=1.5)

        self.play((t1).animate.shift(UP * 1.5))

        albero = Tree()
        albero.addd(13)
        albero.addd(3)
        albero.addd(23)
        albero.addd(16)
        albero.addd(5)
        albero.addd(1)
        albero.addd(8)
        albero.addd(15)
        albero.addd(0)
                    
        node = albero.getRoot()

        self.scrollNode(node, albero)

        self.clearScene()

        #albero.delete(23, node)
        #albero.delete(0, node)
        #albero.delete(1, node)
        #albero.delete(3, node)
        #albero.delete(5, node)
        #albero.delete(8, node)
        #albero.delete(13, node)
        #albero.delete(16, node)
        #albero.delete(15, node)
        self.printNode(node, albero)

        #self.highlightsNode(albero.find(10, node))
        #self.highlightsNode(albero.findMin(node))
        #self.colorNode(albero.findMax(node), YELLOW)
        #self.highlightsNode(albero.findPred(node))
        #self.highlightsNode(albero.findSucc(node))
        
        self.wait(5)

class addTree(firstTreeScenes):
    def construct(self):
        
        global n
        n = 10
        albero = Tree()
        random.seed(0)
        tmp = [0 for i in range(n)]
        tmp = random.sample(range(1, 100), n)
        for i in range(n):
            albero.addd(tmp[i])
             
        node = albero.getRoot() 
        self.printVect(tmp, node)  
        i = 0
        self.printNodeVect(tmp, i, node, albero)

        print(tmp)
        self.wait(5)

class findTree(firstTreeScenes):
    def construct(self):
        
        global n
        n = 10
        albero = Tree()
        random.seed(0)
        tmp = [0 for i in range(n)]
        tmp = random.sample(range(1, 100), n)
        for i in range(n):
            albero.addd(tmp[i])
        node = albero.getRoot()

        valdel = [34]
        valdeln = albero.find(valdel[0], node)
        
        self.printVect(valdel, valdeln)
        self.printNode(node, albero)

        nodefind = albero.find(valdel[0], node)

        if nodefind is not None:
            self.highlightsPath(nodefind, node)

        self.wait(5)

class visitTree(firstTreeScenes):
    def construct(self):

        global n
        n = 10
        albero = Tree()
        albero.addd(13)
        albero.addd(3)
        albero.addd(23)
        albero.addd(16)
        albero.addd(5)
        albero.addd(1)
        albero.addd(8)
        albero.addd(15)
        albero.addd(0)
        albero.addd(9)
        albero.addd(6)

        node = albero.getRoot()
        self.printNode(node, albero)

        inorder = []
        preorder = []
        postorder = []

        inorder = albero.inorderTraversal(node)
        preorder = albero.preorderTraversal(node)
        postorder = albero.postorderTraversal(node)
        bfsvect = albero.bfs(node)


        for i in range (len(inorder)):
            self.colorNode(inorder[i], YELLOW)

        for i in range (len(inorder)):
            self.colorNode(preorder[i], GREEN)

        for i in range (len(inorder)):
            self.colorNode(postorder[i], RED)

        for i in range (len(bfsvect)):
            self.colorNode(bfsvect[i], BLUE)
         








        