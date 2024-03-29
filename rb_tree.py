#!/usr/bin/env python
#from manimlib.imports import *
from manim import *


from mylibrary.trees import Node, Tree, RedBlackTree

RAD = 0.4
RUN_TIME_1 = 2
#https://algorithmtutor.com/Data-Structures/Tree/Red-Black-Trees/

#base scene for all tree scenes
class firstTreeScene(Scene):

    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)

    def construct(self):
        pass
             
    #print nodes
    def printNode(self, node, albero):
        if node is not None:
            if node == albero.root:
                node.center()
                node.to_edge(UP)
                node.pos = node.get_center() 
                self.play(Create((node).move_to(node.pos)),
                        run_time=RUN_TIME_1,
                        )
            else:
                self.play(Create((node).move_to(node.pos)), 
                        run_time=RUN_TIME_1,
                        )
                node.lne = always_redraw(lambda: Line((node.p).get_center(), node.get_center(), buff=RAD))
                self.play(Create(node.lne))
                
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
            if node == albero.root:
                node.center()
                node.to_edge(UP)
                node.pos = node.get_center() 
                self.add((node).move_to(node.pos))
            else:
                if node.p is not None:
                    node.lne = always_redraw(lambda: Line((node.p).get_center(), node.get_center(), buff=RAD))
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
        if node == albero.root and i==0:
            self.play(Create(node))
            box[i] = Rectangle(height=1, width=1, color = YELLOW)
            box[i].move_to(3*DOWN+5*LEFT)
            text[i].move_to(3*DOWN+5*LEFT)
            self.add((text[i]).shift(RIGHT*i), (box[i]).shift(RIGHT*i))
            i = i + 1
        albero.returnTree(node)
        tmpn = albero.root   
        right = node.r
        left = node.l
        if i<10:
            if left is not None:
                if left.v == tmp[i]:
                    self.play(Create((left).move_to(left.pos)),
                        run_time=RUN_TIME_1,
                        )
                    left.lne = always_redraw(lambda: Line((left.p).get_center(), (left).get_center(), buff=RAD))
                    self.play(Create(left.lne))
                    box[i] = Rectangle(height=1, width=1, color = YELLOW)
                    box[i].move_to(3*DOWN+5*LEFT)
                    text[i].move_to(3*DOWN+5*LEFT)
                    self.add((text[i]).shift(RIGHT*i), (box[i]).shift(RIGHT*i))
                    i = i+1
                    self.printNodeVect(tmp, i, tmpn, albero)
                else:
                    self.printNodeVect(tmp, i, left, albero)        

            node = tmpn
            if right is not None:
                if right.v == tmp[i]:
                    self.play(Create((right).move_to(right.pos)),
                        run_time=RUN_TIME_1,
                        )
                    right.lne = always_redraw(lambda: Line((right.p).get_center(), (right).get_center(), buff=RAD))
                    self.play(Create(right.lne))
                    box[i] = Rectangle(height=1, width=1, color = YELLOW)
                    box[i].move_to(3*DOWN+5*LEFT)
                    text[i].move_to(3*DOWN+5*LEFT)
                    self.add((text[i]).shift(RIGHT*i), (box[i]).shift(RIGHT*i))
                    i = i+1
                    self.printNodeVect(tmp, i, tmpn, albero)
                else:
                    self.printNodeVect(tmp, i, right, albero)

    def highlightsNode(self, node):
        if node is not None:
            self.play(GrowFromCenter(node))

    def colorNode(self, node, colorn):
        if node is not None:
            node.set_fill(color = colorn, opacity = 0.5)
            self.play(GrowFromCenter(node))
    
    def recolorNode_rbt(self, node):
        if node is not None:
            if node.color == 1:
                (node.circle).set_fill(color = NEW_RED, opacity = 1)
            else:
                (node.circle).set_fill(color = BLACK, opacity = 1)
            self.add((node))

    #clear the scene
    def clearScene(self):
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
    '''
    #delete node from the subtree node (review)
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
                    if parent.v > tmp.v:
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
                    if parent.v > tmp.v:
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
    '''

    # rotate left at node x (visualization)
    def left_rotate_step(self, x, albero):
        self.clearScene()
        root = albero.root
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
            x.pos = (x.l).pos
            self.play((x).animate.move_to(x.pos),
                        (x.l).animate.shift(DL),
                        run_time=RUN_TIME_1,
                        )

            self.remove((y.l).lne)
            x.r = y.l
            y.l = x
            (x.r).p = x
            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)
            x.d = x.d + 1
            albero.returnTree(x)

            self.play((x.l).animate.move_to((x.l).pos),
                        run_time=RUN_TIME_1,
                        )
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
            self.updateTree(y.r, albero)

            
        else:
            
            albero.returnTree(x.p)
            (y).lne = always_redraw(lambda: Line(y.get_center(), (y.p).get_center(), buff=RAD))
            (x).lne = always_redraw(lambda: Line(x.get_center(), (y).get_center(), buff=RAD))
            self.add(y.lne, x.lne)
            self.play((y).animate.move_to(x.pos),
                        (x).animate.move_to((x.l).pos),
                        (x.l).animate.shift(DL),
                        run_time=RUN_TIME_1,
                        )
            y.pos = y.get_center()
            y.d = y.d - 1
            albero.returnTree(y)
            #self.updateTree(y.r, albero)

            x.pos = x.get_center()
            x.d = x.d + 1
            (x.l).p = x
            albero.returnTree(x)
            
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
            (y.r).p = y

            y.l = x     # x is left soon of y

            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)
            
            albero.returnTree(y.p)
            self.remove((y.r).lne)
            (y.r).lne = always_redraw(lambda: Line((y.r).get_center(), ((y.r).p).get_center(), buff=RAD))
            self.add((y.r).lne)
            self.updateTree(y.r, albero)
            
        
        self.wait(3)

        self.play(FadeOut(t1))
        self.clearScene()
        root = albero.root
        print(root.v)
        albero.returnTree(root)
        self.printNodeOneShot(root, albero)

        self.wait(3)
        
        
    # rotate right at node x
    def right_rotate_step(self, x, albero):
        self.clearScene()
        root = albero.root
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
            x.pos = (x.r).pos
            self.play((x).animate.move_to(x.pos),
                        (x.r).animate.shift(DR),
                        run_time=RUN_TIME_1,
                        )

            self.remove((y.r).lne)
            x.l = y.r
            y.r = x
            (x.l).p = x
            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)
            x.d = x.d + 1
            albero.returnTree(x)

            self.play((x.r).animate.move_to((x.r).pos),
                        run_time=RUN_TIME_1,
                        )
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
            self.updateTree(y.l, albero)
            
        else:
            
            albero.returnTree(x.p)
            (y).lne = always_redraw(lambda: Line(y.get_center(), (y.p).get_center(), buff=RAD))
            (x).lne = always_redraw(lambda: Line(x.get_center(), (y).get_center(), buff=RAD))
            self.add(y.lne, x.lne)
            self.play((y).animate.move_to(x.pos),
                        (x).animate.move_to((x.r).pos),
                        (x.r).animate.shift(DR),
                        run_time=RUN_TIME_1,
                        )
            y.pos = y.get_center()
            y.d = y.d - 1
            albero.returnTree(y)
            #self.updateTree(y.l, albero)

            x.pos = x.get_center()
            x.d = x.d + 1
            (x.r).p = x
            albero.returnTree(x)            
            
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
            x.l = y.r #subtree B (y.right) becomes x's left soon
            (y.r).p = x
            (y.l).p = y

            y.r = x     # x is right soon of y

            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)

            albero.returnTree(y.p)
            self.remove((y.l).lne)
            (y.l).lne = always_redraw(lambda: Line((y.l).get_center(), ((y.l).p).get_center(), buff=RAD))
            self.add((y.l).lne)
            self.updateTree(y.l, albero)
        
        
        self.wait(3)

        self.play(FadeOut(t1))
        self.clearScene()
        root = albero.root
        print(root.v)
        albero.returnTree(root)
        self.printNodeOneShot(root, albero)

        self.wait(3)

    # rotate left at node x (visualization)
    def left_rotate(self, x, albero):
        self.clearScene()
        root = albero.root
        self.printNodeOneShot(root, albero)
        print("left_rotate")
        
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
            x.pos = (x.l).pos
            
            self.remove((y.l).lne)
            x.r = y.l
            y.l = x
            (x.r).p = x
            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)
            x.d = x.d + 1
            albero.returnTree(x)

            y.pos = position_x
            y.d = y.d - 1
            albero.returnTree(y)

            albero.returnTree(y.r)
            #self.updateTree(y.r)
            
        else:
            
            albero.returnTree(x.p)
            (y).lne = always_redraw(lambda: Line(y.get_center(), (y.p).get_center(), buff=RAD))
            (x).lne = always_redraw(lambda: Line(x.get_center(), (y).get_center(), buff=RAD))
            self.add(y.lne, x.lne)

            y.pos = x.pos
            y.d = y.d - 1
            albero.returnTree(y)
            #self.updateTree(y.r)

            x.pos = (x.l).pos
            x.d = x.d + 1
            (x.l).p = x
            albero.returnTree(x)
            
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
            
            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)

            self.remove((x.r).lne)
            
            (y.l).lne = always_redraw(lambda: Line((y.l).get_center(), (x).get_center(), buff=RAD))
            (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
            self.add((y.l).lne, y.lne)
            
            (y.l).pos = (x.r).pos

            ((y.r).lne).suspend_updating()
            x.r = y.l #subtree B (y.left) becomes x's right soon
            (y.l).p = x

            y.l = x     # x is left soon of y

            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)

    # rotate right at node x
    def right_rotate(self, x, albero):
        self.clearScene()
        root = albero.root
        self.printNodeOneShot(root, albero)
        print("right_rotate")
        
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
            x.pos = (x.r).pos

            self.remove((y.r).lne)
            x.l = y.r
            y.r = x
            (x.l).p = x
            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)
            x.d = x.d + 1
            albero.returnTree(x)

            y.pos = position_x
            y.d = y.d - 1
            albero.returnTree(y)
            
            albero.returnTree(y.l) 
            #self.updateTree(y.l)
            
        else:
            
            albero.returnTree(x.p)
            (y).lne = always_redraw(lambda: Line(y.get_center(), (y.p).get_center(), buff=RAD))
            (x).lne = always_redraw(lambda: Line(x.get_center(), (y).get_center(), buff=RAD))
            self.add(y.lne, x.lne)
            
            y.pos = x.pos
            y.d = y.d - 1
            albero.returnTree(y)
            #self.updateTree(y.l)

            x.pos = (x.l).pos
            x.d = x.d + 1
            (x.r).p = x
            albero.returnTree(x)            
            
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
            
            (x.r).lne = always_redraw(lambda: Line((x.r).get_center(), ((x.r).p).get_center(), buff=RAD))
            self.add((x.r).lne)

            self.remove((x.l).lne)
            
            (y.r).lne = always_redraw(lambda: Line((y.r).get_center(), (x).get_center(), buff=RAD))
            (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
            self.add((y.r).lne, y.lne)
            (y.r).pos = (x.l).pos

            ((y.l).lne).suspend_updating()
            x.l = y.r #subtree B (y.left) becomes x's right soon
            (y.r).p = x

            y.r = x     # x is left soon of y

            (x.l).lne = always_redraw(lambda: Line((x.l).get_center(), ((x.l).p).get_center(), buff=RAD))
            self.add((x.l).lne)
    
    def insert(self, val, albero):
        # Ordinary Binary Search Insertion
        node = Node(val)
        node.p = None
        node.v = val

        node.color = 1 # new node must be red
        node = albero.setColor(node)
        y = None
        x = albero.root

        root = albero.root
        
        # node search
        while x.v != "Nil":
            y = x
            if node.v < x.v:
                x = x.l
            else:
                x = x.r
        
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
            
            # case 1
            print("case 1")
            node.color = 0
            node = albero.setColor(node)
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
            albero.returnTree(y.l)
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
            albero.returnTree(y.r)

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
                    u.color = 0
                    u = albero.setColor(u)
                    (k.p).color = 0
                    (k.p) = albero.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = albero.setColor(((k.p).p))
                    k = (k.p).p
                else:   # uncle is black
                    #Case 3.2: P is red and U is black (or NULL)
                    if k == (k.p).l:
                        # case 3.2.2: P is right child of G and K is left child of P.
                        print("case 3.2.2")
                        k = k.p
                        self.right_rotate(k, albero)
                    # case 3.2.1: P is right child of G and K is right child of P.
                    print("case 3.2.1")
                    k.p.color = 0
                    (k.p) = albero.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = albero.setColor(((k.p).p))
                    self.left_rotate((k.p).p, albero)
            else:   # if parent is left child
                u = ((k.p).p).r # uncle
                if u.color == 1:
                    # mirror case 3.1
                    print("case 3.1 (b)")
                    u.color = 0
                    u = albero.setColor(u)
                    (k.p).color = 0
                    (k.p) = albero.setColor((k.p))
                    ((k.p).p).color = 1
                    ((k.p).p) = albero.setColor(((k.p).p))
                    k = (k.p).p 
                else:
                    if k == (k.p).r:
                        # mirror case 3.2.2: P is left child of G and K is right child of P.
                        print("case 3.2.4")
                        k = k.p
                        self.left_rotate(k, albero)
                    # mirror case 3.2.1: P is left child of G and K is left child of P.
                    print("case 3.2.3")
                    (k.p).color = 0
                    (k.p) = albero.setColor((k.p))
                    if (k.p).p is not None:
                        ((k.p).p).color = 1
                        ((k.p).p) = albero.setColor(((k.p).p))
                    self.right_rotate((k.p).p, albero)
            if k == albero.root:
                break
        (albero.root).color = 0
        (albero.root) = albero.setColor(albero.root)

    def insert_step(self, val, albero):
        # Ordinary Binary Search Insertion
        node = Node(val)
        node.p = None
        node.v = val

        node.color = 1 # new node must be red
        node = albero.setColor(node)
        y = None
        x = albero.root

        t1 = Tex('\\textbf{Insertion:}\\\\the new node is ' + str(val))
        t1.scale(0.5).to_edge(RIGHT)
        self.play(Create(t1))
        self.wait(duration=2.5)
        node.next_to(t1, DOWN)
        self.play(Create(node))
        NodeIns = (node)
        
        root = albero.root
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
                        ((node).l).animate.move_to(((node).l).pos),
                        run_time=RUN_TIME_1,
                        )
            self.add(((node.l).lne), ((node.r).lne))
            
            # case 1
            print("case 1")
            node.color = 0
            t1 = Tex('\\begin{flushleft}\\textbf{Case 1:}\\\\the new node is a root node\\\\it is a black node\\end{flushleft}')
            t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
            ((y.l).l).move_to((y.l).pos)
            self.play(((y.l).r).animate.move_to(((y.l).r).pos),
                        ((y.l).l).animate.move_to(((y.l).l).pos),
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
            ((y.r).l).move_to((y.r).pos)
            self.play(((y.r).r).animate.move_to(((y.r).r).pos),
                        ((y.r).l).animate.move_to(((y.r).l).pos),
                        run_time=RUN_TIME_1,
                        )
            
            self.add((((y.r).l).lne), (((y.r).r).lne))

        # if the grandparent is None, simply return
        if (node.p).p == None:
            return
        
        # Fix the tree
        self.__fix_insert_step(node, albero)

    def  __fix_insert_step(self, k, albero):
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
                    t3 = Tex('We change the color of S to red and P to black.')
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
                        t2 = Tex('In this case, we first do the left-rotation at P.\\\\This reduces it to the case 3.2.3.')
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
                    s.color = 0
                    s = albero.setColor(s)
                    (x.p).color = 1
                    x.p = albero.setColor(x.p)
                    self.left_rotate(x.p, albero)
                    s = (x.p).r

                if (s.l).color == 0 and (s.r).color == 0:
                    # case 3.2
                    print("case 3.2")
                    s.color = 1
                    s = albero.setColor(s)
                    x = x.p
                else:
                    if (s.r).color == 0:
                        # case 3.3
                        print("case 3.3")
                        (s.l).color = 0
                        s.l = albero.setColor(s.l)
                        s.color = 1
                        s = albero.setColor(s)
                        self.right_rotate(s, albero)
                        s = (x.p).r

                    # case 3.4
                    print("case 3.4")
                    s.color = (x.p).color
                    s = albero.setColor(s)
                    (x.p).color = 0
                    x.p = albero.setColor(x.p)
                    (s.r).color = 0
                    s.r = albero.setColor(s.r)
                    self.left_rotate(x.p, albero)
                    x = albero.root
            #x is right soon
            else:
                s = (x.p).l
                if s.color == 1:
                    # case 3.1
                    print("case 3.1")
                    s.color = 0
                    s = albero.setColor(s)
                    (x.p).color = 1
                    x.p = albero.setColor(x.p)
                    self.right_rotate(x.p, albero)
                    s = (x.p).l

                if (s.l).color == 0 and (s.r).color == 0:
                    # case 3.2
                    print("case 3.2")
                    s.color = 1
                    s = albero.setColor(s)
                    x = x.p
                else:
                    if (s.l).color == 0:
                        # case 3.3
                        print("case 3.3")
                        (s.r).color = 0
                        s.r = albero.setColor(s.r)
                        s.color = 1
                        s = albero.setColor(s)
                        self.left_rotate(s, albero)
                        s = (x.p).l 

                    # case 3.4
                    print("case 3.4")
                    s.color = (x.p).color
                    s = albero.setColor(s)
                    (x.p).color = 0
                    x.p = albero.setColor(x.p)
                    (s.l).color = 0
                    s.l = albero.setColor(s.l)
                    self.right_rotate(x.p, albero)
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
    def delete(self, val, node, albero):
        
        # find the node containing val
        z = albero.find(val, node)
        
        # node not in the tree
        if z.v == (albero.TNULL).v:
            print ("Couldn't find value in the tree")
            return
        
        y = z
        y_original_color = y.color
        # the node is a leaf (left and right children are nil)
        if ((z.l).v == "Nil") and ((z.r).v == "Nil"):
            print("entra qui 1")
            position_z = z.pos
            parent = z.p
            ((z.l).lne).suspend_updating()
            ((z.r).lne).suspend_updating()
            (z.lne).suspend_updating()
            #self.play(FadeOut(z.l), FadeOut(z.r), FadeOut(z), FadeOut((z.l).lne), FadeOut((z.r).lne), FadeOut(z.lne))
            
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
            ((z.l).lne).suspend_updating()
            #self.play(FadeOut(z.l), FadeOut((z.l).lne))

            position_z = z.pos
            (z.lne).suspend_updating()
            #self.play(FadeOut(z), FadeOut(z.lne))

            ((z.r).lne).suspend_updating()
            #self.play(FadeOut((z.r).lne))
            self.play((z.r).animate.move_to(position_z))
            (z.r).pos = (z.r).get_center()
            (z.r).d = (z.r).d - 1
            albero.returnTree(z.r)
            #self.updateTree(z.r, albero)

            x = z.r
            self.__rb_transplant(z, z.r, albero)
            (z.r).lne = always_redraw(lambda: Line((z.r).get_center(), ((z.r).p).get_center(), buff=RAD))
            self.add((z.r).lne)
        # right child is nil
        elif ((z.r).v == "Nil"):
            print("entra qui 3")
            ((z.r).lne).suspend_updating()
            #self.play(FadeOut(z.r), FadeOut((z.r).lne))

            position_z = z.pos
            (z.lne).suspend_updating()
            #self.play(FadeOut(z), FadeOut(z.lne))

            ((z.l).lne).suspend_updating()
            #self.play(FadeOut((z.l).lne))
            self.play(((z.l).animate.move_to(position_z)))
            (z.l).pos = (z.l).get_center()
            (z.l).d = (z.l).d - 1
            albero.returnTree(z.l)
            #self.updateTree(z.l, albero)

            x = z.l
            self.__rb_transplant(z, z.l, albero)
            (z.l).lne = always_redraw(lambda: Line((z.l).get_center(), ((z.l).p).get_center(), buff=RAD))
            self.add((z.l).lne)
        # no nil children
        else:
            print("entra qui 4")
            y = albero.findSucc(z)
            y_original_color = y.color
            x = y.r
            if y.p == z:
                print("entra qui 4.1")
                position_z = z.pos
                ((z).lne).suspend_updating()
                ((z.l).lne).suspend_updating()
                ((z.r).lne).suspend_updating()
                #self.play(FadeOut(z), FadeOut(z.lne), FadeOut((z.l).lne), FadeOut((z.r).lne))
                self.play(((y).animate.move_to(position_z)))
                (y).pos = (y).get_center()
                (y).d = (y).d - 1
                ((y.l).lne).suspend_updating()
                #self.play(FadeOut(y.l), FadeOut((y.l).lne))
                albero.returnTree(y)
                #self.updateTree(y.r, albero)
                x.p = y

                self.__rb_transplant(z, y, albero)
                y.p = z.p
                y.l = z.l
                y.r = z.r
                (y.l).p = y
                y.color = z.color
                y = albero.setColor(y)
                (y.l).lne = always_redraw(lambda: Line((y.l).get_center(), ((y.l).p).get_center(), buff=RAD))
                if y.p is not None:
                    (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
                    self.add(y.lne)
                self.add((y.l).lne)
            else:
                print("entra qui 4.2")
                position_z = z.pos
                position_y = y.pos
                (y.lne).suspend_updating()
                ((y.l).lne).suspend_updating()
                ((y.r).lne).suspend_updating()
                self.play((y).animate.move_to(position_z))
                #self.play(FadeOut(y.l), FadeOut((y.l).lne), FadeOut((y.r).lne))
                z.v = y.v
                ((y.p.l).lne).suspend_updating()
                self.__rb_transplant(y, y.r, albero)
                self.play((y.r).animate.move_to(position_y))
                (y.r).p = y.p

                self.__rb_transplant(z, y, albero)

                y.p = z.p
                y.l = z.l
                y.r = z.r
                (y.l).p = y
                y.color = z.color
                y = albero.setColor(y)
                (y.l).lne = always_redraw(lambda: Line((y.l).get_center(), ((y.l).p).get_center(), buff=RAD))
                if y.p is not None:
                    (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
                    self.add(y.lne)
                self.add((y.l).lne)

        
        if y_original_color == 0:
            if x is not None:
                self.__fix_delete(x, albero)
      
        
     

    # fix the rb tree modified by the delete operation
    def __fix_delete_step(self, x, albero):
        while x != albero.root and x.color == 0:
            # x is left soon
            if x == (x.p).l:
                # s is the right brother
                s = (x.p).r
                if s.color == 1:
                    # case 3.1
                    print("case 3.1")
                    t1 = Tex('\\begin{flushleft}\\textbf{Case 3.1:}\\\\x ’s sibling S is red\\end{flushleft}')
                    t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
                    t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
                        t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
                    t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
                    t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
                    t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
                        t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
                    t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
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
        
    # delete node in a RB tree
    def delete_step(self, val, node, albero):
        
        # find the node containing val
        z = albero.find(val, node)
        
        # node not in the tree
        if z.v == (albero.TNULL).v:
            print ("Couldn't find value in the tree")
            t1 = Tex('Couldn\' t find value in the tree.')
            t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            return
        
        t1 = Tex('\\textbf{Deletion:} node ' + str(val))
        t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
        self.play(Create(t1))
        self.wait(duration=2.5)
        self.play(FadeOut(t1))
        
        y = z
        y_original_color = y.color
        # the node is a leaf (left and right children are nil)
        if ((z.l).v == "Nil") and ((z.r).v == "Nil"):
            print("entra qui 1")
            t1 = Tex('The node is a leaf.')
            t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            position_z = z.pos
            parent = z.p
            ((z.l).lne).suspend_updating()
            ((z.r).lne).suspend_updating()
            (z.lne).suspend_updating()
            self.play(FadeOut(z.l), FadeOut(z.r), FadeOut(z), FadeOut((z.l).lne), FadeOut((z.r).lne), FadeOut(z.lne))
            
            z = Node("Nil")
            if ((parent.l).v == val):
                parent.l = z
            else:
                parent.r = z
            z.p = parent
            self.play(Create(z.move_to(position_z)))
            z.lne = always_redraw(lambda: Line(z.get_center(), (z.p).get_center(), buff=RAD))
            
            self.play(Create(z.lne))
            x = z 
            
            
        # left child is nil
        elif ((z.l).v == "Nil"):
            print("entra qui 2")
            t1 = Tex('Node\'s left child is Nil.')
            t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            ((z.l).lne).suspend_updating()
            self.play(FadeOut(z.l), FadeOut((z.l).lne))

            position_z = z.pos
            (z.lne).suspend_updating()
            self.play(FadeOut(z), FadeOut(z.lne))

            ((z.r).lne).suspend_updating()
            self.play(FadeOut((z.r).lne))
            self.play((z.r).animate.move_to(position_z))
            (z.r).pos = (z.r).get_center()
            (z.r).d = (z.r).d - 1
            albero.returnTree(z.r)
            self.updateTree(z.r, albero)

            x = z.r
            self.__rb_transplant(z, z.r, albero)
            (z.r).lne = always_redraw(lambda: Line((z.r).get_center(), ((z.r).p).get_center(), buff=RAD))
            self.add((z.r).lne)
        # right child is nil
        elif ((z.r).v == "Nil"):
            print("entra qui 3")
            t1 = Tex('Node\'s right child is Nil.')
            t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            ((z.r).lne).suspend_updating()
            self.play(FadeOut(z.r), FadeOut((z.r).lne))

            position_z = z.pos
            (z.lne).suspend_updating()
            self.play(FadeOut(z), FadeOut(z.lne))

            ((z.l).lne).suspend_updating()
            self.play(FadeOut((z.l).lne))
            self.play(((z.l).animate.move_to(position_z)))
            (z.l).pos = (z.l).get_center()
            (z.l).d = (z.l).d - 1
            albero.returnTree(z.l)
            self.updateTree(z.l, albero)

            x = z.l
            self.__rb_transplant(z, z.l, albero)
            (z.l).lne = always_redraw(lambda: Line((z.l).get_center(), ((z.l).p).get_center(), buff=RAD))
            self.add((z.l).lne)
        # no nil children
        else:
            print("entra qui 4")
            t1 = Tex('Node\'s children are not Nil.')
            t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
            self.play(Create(t1))
            self.wait(duration=2.5)
            self.play(FadeOut(t1))
            y = albero.findSucc(z)
            y_original_color = y.color
            x = y.r
            if y.p == z:
                print("entra qui 4.1")
                t1 = Tex('Node\'s successor is node\'s son.')
                t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
                self.play(Create(t1))
                self.wait(duration=2.5)
                self.play(FadeOut(t1))
                position_z = z.pos
                ((z).lne).suspend_updating()
                ((z.l).lne).suspend_updating()
                ((z.r).lne).suspend_updating()
                self.play(FadeOut(z), FadeOut(z.lne), FadeOut((z.l).lne), FadeOut((z.r).lne))
                self.play(((y).animate.move_to(position_z)))
                (y).pos = (y).get_center()
                (y).d = (y).d - 1
                ((y.l).lne).suspend_updating()
                self.play(FadeOut(y.l), FadeOut((y.l).lne))
                albero.returnTree(y)
                self.updateTree(y.r, albero)
                x.p = y

                self.__rb_transplant(z, y, albero)
                y.p = z.p
                y.l = z.l
                y.r = z.r
                (y.l).p = y
                y.color = z.color
                y = albero.setColor(y)
                (y.l).lne = always_redraw(lambda: Line((y.l).get_center(), ((y.l).p).get_center(), buff=RAD))
                if y.p is not None:
                    (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
                    self.add(y.lne)
                self.add((y.l).lne)
                #(z.l).p = y
                #y.l = z.l
            else:
                print("entra qui 4.2")
                position_z = z.pos
                position_y = y.pos
                (y.lne).suspend_updating()
                ((y.l).lne).suspend_updating()
                ((y.r).lne).suspend_updating()
                self.play((y).animate.move_to(position_z))
                self.play(FadeOut(y.l), FadeOut((y.l).lne), FadeOut((y.r).lne))
                z.v = y.v
                #z.text = Text(str(z.v)).scale(0.5)
                #self.play(FadeOut(y), FadeIn(z))
                ((y.p.l).lne).suspend_updating()
                self.__rb_transplant(y, y.r, albero)
                self.play((y.r).animate.move_to(position_y))
                (y.r).p = y.p
                

                self.__rb_transplant(z, y, albero)

                print(y.r.v)
                print(y.r.p.v)

                y.p = z.p
                y.l = z.l
                y.r = z.r
                (y.l).p = y
                y.color = z.color
                y = albero.setColor(y)
                (y.l).lne = always_redraw(lambda: Line((y.l).get_center(), ((y.l).p).get_center(), buff=RAD))
                if y.p is not None:
                    (y).lne = always_redraw(lambda: Line((y).get_center(), (y.p).get_center(), buff=RAD))
                    self.add(y.lne)
                self.add((y.l).lne)

                print(y.r.v)
                print(y.r.p.v)
                #((y.r).l).p = y.r
        
        if y_original_color == 0:
            if x is not None:
                t1 = Tex('\\begin{flushleft}\\textbf{Case 3:}\\\\the node is a black node.\\end{flushleft}')
                t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
                self.play(Create(t1))
                self.wait(duration=2.5)
                t2 = Tex('The property is violated.')
                t2.scale(0.5).to_edge(DOWN)
                self.play(Create(t2))
                self.wait(duration=3)
                self.play(FadeOut(t1), FadeOut(t2))
                self.__fix_delete_step(x, albero)
        else:
            t1 = Tex('\\begin{flushleft}\\textbf{Case 1:}\\\\the node is a red node.\\end{flushleft}')
            t1.scale(0.5).to_edge(RIGHT).to_edge(UP)
            self.play(Create(t1))
            self.wait(duration=2.5)
            t2 = Tex('Delete x since deleting a red node doesn’t violate any property.')
            t2.scale(0.5).to_edge(DOWN)
            self.play(Create(t2))
            self.wait(duration=3)
            self.play(FadeOut(t1), FadeOut(t2))
        
        self.wait(3)
        self.clearScene()
        self.wait(3)
        root = albero.root
        print (root.v)
        self.printNodeOneShot(root, albero)
        self.wait(3)

    # delete the node from the tree
    #def delete_node(self, data, albero):
        #self.__delete_node_helper(self.root, data, albero)

    # move nodes to the new position in a recursive way
    def updateTree(self, node, albero):
        self.play((node).animate.move_to(node.pos))
        albero.returnTree(node)
        if node.l is not None:
            self.updateTree(node.l, albero)
        if node.r is not None:
            self.updateTree(node.r, albero)
            

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
        self.wait(5)
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
        self.wait(5)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

        f1 = Tex("To re-structure the tree\\\\in order to not violate the insertion we can use:")
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
        self.wait(6)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

    def deletionRules(self):
        f1 = Tex("To delete a node K into a red-black tree T:")
        
        f1.to_edge(UP).set_color(TEAL_B)
        bl = BulletedList('Find the node in the tree.',
                          'Delete K and re-establish connections between nodes.',
                          'Check if the deletion violated the red-black tree properties\\\\and fix it.',
                          buff=MED_SMALL_BUFF)
        bl.next_to(f1, DOWN, aligned_edge=LEFT).scale(0.7).move_to(LEFT)
        self.play(FadeIn(f1))
        self.wait()
        self.play(FadeIn(bl[0]))
        self.wait()
        
        self.play(FadeIn(bl[1]))
        self.wait()
        self.play(FadeIn(bl[2]))
        self.wait(5)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

        f1 = Tex("\\begin{flushleft}To re-structure the tree in order to not violate\\\\the RB properties we can use:\\end{flushleft}")
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
        self.wait(7)
        elements = VGroup(f1, bl)
        self.play(FadeOut(elements))

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# HERE START THE SCENES
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------


class RBTree2(firstTreeScene):
    def construct(self):

        title = Tex(r"RED", r"BLACK", r"TREES", 
            background_stroke_width=1, 
            background_stroke_color=WHITE)
        title.set_color_by_tex('RED', RED)
        title.set_color_by_tex('BLACK', BLACK)
        self.play(Create(title))
        self.wait(5)
        self.play(FadeOut(title))
        bst = Tex("To introduce red-black trees it is important\\\\to know the rules of binary search trees:")
        bst.to_edge(UP).scale(0.8).set_color(PURPLE_C)
        bst_bl = BulletedList('{\\small Every node can have only two subtrees. (Two sons)}',
                          '{\\small The tree is ordered.\\\\ Left nodes are smaller, right nodes are larger.}',
                          buff=MED_SMALL_BUFF)
        bst_bl.scale(0.7)
        self.play(FadeIn(bst))
        self.wait()
        self.play(Write(bst_bl[0]))
        self.wait()
        self.play(Write(bst_bl[1]))
        self.wait(4)
        self.play(bst_bl.animate.next_to(bst, DOWN))
        bst_group = VGroup(bst, bst_bl)
        self.play(bst_group.animate.scale(0.9).to_edge(LEFT).to_edge(DOWN))
        rect_bst_group = SurroundingRectangle(bst_group, color = WHITE)
        self.add(rect_bst_group)

        albero = Tree()
        albero.addd(13)
        albero.addd(3)
        albero.addd(23)
        albero.addd(16)
        albero.addd(1)
        albero.addd(5)
        node = albero.root
        self.printNode(node, albero)
        
        self.wait(4)
        self.clearScene()
        self.add(bst_group, rect_bst_group)

        albero2_txt = Tex("Let's see another example:")
        albero2_txt.scale(0.8).to_edge(UP)
        self.play(Write(albero2_txt))
        self.wait(2)
        self.play(FadeOut(albero2_txt))

        albero2 = Tree()
        albero2.addd(1)
        albero2.addd(3)
        albero2.addd(10)
        albero2.addd(26)
        albero2.addd(15)
        node2 = albero2.root
        self.printNode(node2, albero2)

        f2 = Tex("If the tree is unbalanced, as in the example, the complexity is greater.")
        f3 = Tex("For this reason we introduce the concept of balanced search trees,\\\\among the variants we will illustrate the red and black trees.")
        f2.to_edge(LEFT).scale(0.5)
        f3.to_edge(LEFT).scale(0.5)
        self.play(FadeIn(f2))
        self.wait(4)
        self.play(Transform(f2, f3))
        self.wait(5)
        self.clearScene()
        self.baseRules()
        self.clearScene()
        txt1 = Text("Let's see an example.")
        txt1.scale(0.6)
        txt2 = Text("We insert step by step the nodes inside the red black tree.")
        txt2.scale(0.6)
        self.play(Create(txt1))
        self.wait(3)
        self.play(Transform(txt1, txt2))
        self.wait(3)
        self.play(FadeOut(txt1))
        self.insertionRules()
        self.wait(2)
        case1 = Text("CASE: the tree is balanced")
        case1.scale(0.6).to_edge(UP).to_edge(LEFT)
        case1bis = Text("In this example we use only Recolor function")
        case1bis.scale(0.4).next_to(case1, DOWN)
        self.play(Write(case1), Write(case1bis))
        bl = BulletedList('{\\small 1) Every node in T is either red or black.}',
                          '{\\small 2) The root node of T is black.}',
                          '{\\small 3) Every Nill node is black.} \\tiny{(NULL nodes are the leaf nodes. They do not contain any keys.)}',
                          '{\\small 4) If a node is red, both of its children are black. This means no two nodes on a path can be red nodes.}',
                          '{\\small 5) Every path from a root node to a Nill node has the same number of black nodes.}',
                          buff=MED_SMALL_BUFF)
        bl.to_edge(DOWN).scale(0.5).shift(UP)
        rect = SurroundingRectangle(bl, color = WHITE)
        self.add(bl, rect)
        
        bst1 = RedBlackTree()
        self.insert_step(10, bst1)
        self.insert_step(7, bst1)
        self.insert_step(16, bst1)
        self.insert_step(3, bst1)
        self.insert_step(18, bst1)
        
        self.wait(3)
        self.clearScene()
        
        case2 = Text("CASE: the tree is unbalanced")
        case2.scale(0.6).to_edge(UP).to_edge(LEFT)
        case2bis = Text("Recolor and Rotation functions")
        case2bis.scale(0.4).next_to(case2, DOWN)
        self.play(Write(case2), Write(case2bis))
        bst2 = RedBlackTree()
        self.insert(20, bst2)
        self.insert(7, bst2)
        self.insert(10, bst2)
        node2 = bst2.root
        self.printNodeOneShot(node2, bst2)
        self.add(case2, case2bis)
        self.insert_step(13, bst2)
        self.insert_step(15, bst2)
        self.wait(3)
        finish = Text("Now the tree is balanced.")
        finish.scale(0.6).to_edge(DOWN)
        self.add(case2, case2bis)
        self.play(Write(finish))
        bl.next_to(finish, UP)
        rect = SurroundingRectangle(bl, color = WHITE)
        self.add(bl, rect)
        self.wait(3)
        self.clearScene()

        bst3 = RedBlackTree()
        self.insert(20, bst3)
        self.insert(7, bst3)
        self.insert(10, bst3)
        node2 = bst3.root
        self.printNodeOneShot(node2, bst3)
        self.add(case2, case2bis)
        self.insert_step(9, bst3)
        self.insert_step(8, bst3)
        self.wait(3)
        finish = Text("Now the tree is balanced.")
        finish.scale(0.6).to_edge(DOWN)
        self.play(Write(finish))
        self.add(bl, rect)
        self.wait(4)
        self.clearScene()

class pp(firstTreeScene):
    def construct(self):
        bst3 = RedBlackTree()
        self.insert(20, bst3)
        self.insert(7, bst3)
        self.insert(10, bst3)
        node2 = bst3.root
        self.printNodeOneShot(node2, bst3)
        #self.insert_step(9, bst3)
        #self.insert_step(8, bst3)
        self.insert_step(15, bst3)
        self.insert_step(17, bst3)
        self.wait(3)

class RBTree3(firstTreeScene):
    def construct(self):

        title = Tex(r"RED", r"BLACK", r"TREES", 
            background_stroke_width=1, 
            background_stroke_color=WHITE)
        title.set_color_by_tex('RED', RED)
        title.set_color_by_tex('BLACK', BLACK)
        self.play(Create(title))
        self.wait(5)
        self.play(FadeOut(title))

        self.deletionRules()
        
        txt1 = Text("Let's review RB Tree rules.")
        txt1.scale(0.6)
        self.play(Create(txt1))
        self.wait(3)
        
        bl = BulletedList('{\\small 1) Every node in T is either red or black.}',
                          '{\\small 2) The root node of T is black.}',
                          '{\\small 3) Every Nill node is black.} \\tiny{(NULL nodes are the leaf nodes. They do not contain any keys.)}',
                          '{\\small 4) If a node is red, both of its children are black. This means no two nodes on a path can be red nodes.}',
                          '{\\small 5) Every path from a root node to a Nill node has the same number of black nodes.}',
                          buff=MED_SMALL_BUFF)
        bl.to_edge(DOWN).scale(0.7).shift(UP)
        rect = SurroundingRectangle(bl, color = WHITE)
        
        self.play(Transform(txt1, bl))
        self.add(rect)
        self.wait(10)
        
        self.clearScene()

        bst1 = RedBlackTree()
        self.insert(5, bst1)
        self.insert(2, bst1)
        self.insert(8, bst1)
        self.insert(1, bst1)
        self.insert(9, bst1)
        self.insert(4, bst1)
        self.insert(7, bst1)

        node1 = bst1.root
        self.printNodeOneShot(node1, bst1)
        
        case1 = Text("CASE: delete a leaf")
        case1.scale(0.6).to_edge(UP).to_edge(LEFT)
        case1bis = Text("Simple deletion")
        case1bis.scale(0.4).next_to(case1, DOWN)
        self.play(Write(case1), Write(case1bis))

        self.delete_node(4, node1, bst1)

        #self.wait(6)
        self.clearScene()

        #self.insert(1, bst1)
        self.printNodeOneShot(node1, bst1)

        case2 = Text("CASE: delete a node with a Nil children")
        case2.scale(0.6).to_edge(UP).to_edge(LEFT)
        case2bis = Text("Deletion with shift of a son")
        case2bis.scale(0.4).next_to(case2, DOWN)
        self.play(Write(case2), Write(case2bis))

        self.delete_node(2, node1, bst1)

        #self.wait(6)
        self.clearScene()

        self.printNodeOneShot(node1, bst1)

        case3 = Text("CASE: delete a node with a two children")
        case3.scale(0.6).to_edge(UP).to_edge(LEFT)
        case3bis = Text("Deletion with shift of successor's node")
        case3bis.scale(0.4).next_to(case3, DOWN)
        self.play(Write(case3), Write(case3bis))

        self.delete_node(5, node1, bst1)

        self.wait(8)


        '''  
        case2 = Text("CASE: the tree is unbalanced")
        case2.scale(0.6).to_edge(UP).to_edge(LEFT)
        case2bis = Text("Recolor and Rotation functions")
        case2bis.scale(0.4).next_to(case2, DOWN)
        self.play(Write(case2), Write(case2bis))
        bst2 = RedBlackTree()
        self.insert(20, bst2)
        self.insert(7, bst2)
        self.insert(10, bst2)
        node2 = bst2.root
        self.printNodeOneShot(node2, bst2)
        self.add(case2, case2bis)
        self.insert_step(13, bst2)
        self.insert_step(15, bst2)
        self.wait(3)
        finish = Text("Now the tree is balanced.")
        finish.scale(0.6).to_edge(DOWN)
        self.add(case2, case2bis)
        self.play(Write(finish))
        bl.next_to(finish, UP)
        rect = SurroundingRectangle(bl, color = WHITE)
        self.add(bl, rect)
        self.wait(3)
        self.clearScene()

        bst3 = RedBlackTree()
        self.insert(20, bst3)
        self.insert(7, bst3)
        self.insert(10, bst3)
        node2 = bst3.root
        self.printNodeOneShot(node2, bst3)
        self.add(case2, case2bis)
        self.insert_step(9, bst3)
        self.insert_step(8, bst3)
        self.wait(3)
        finish = Text("Now the tree is balanced.")
        finish.scale(0.6).to_edge(DOWN)
        self.play(Write(finish))
        self.add(bl, rect)
        self.wait(4)
        self.clearScene()
        '''


class RBTree4(firstTreeScene):
    def construct(self):

        bst1 = RedBlackTree()
        self.insert(5, bst1)
        self.insert(2, bst1)
        self.insert(8, bst1)
        self.insert(1, bst1)
        self.insert(10, bst1)
        self.insert(4, bst1)
        self.insert(7, bst1)
        self.insert(9, bst1)

        node1 = bst1.root
        self.printNodeOneShot(node1, bst1)
        self.wait(3)

        self.delete_step(9, node1, bst1)

        #node1 = bst1.root
        #self.printNodeOneShot(node1, bst1)

        self.wait(8)

class RBTree5(firstTreeScene):
    def construct(self):

        bst1 = RedBlackTree()
        self.insert(5, bst1)
        self.insert(2, bst1)
        self.insert(8, bst1)
        self.insert(1, bst1)
        self.insert(10, bst1)
        self.insert(4, bst1)
        self.insert(7, bst1)
        self.insert(9, bst1)

        node1 = bst1.root
        self.printNodeOneShot(node1, bst1)

        inorder = bst1.inorderTraversal(node1)
        for i in range (len(inorder)):
            self.colorNode(inorder[i], YELLOW)
        
        for i in range (len(inorder)):
            self.recolorNode_bst(inorder[i])


        self.wait(8)


class deleteTree(firstTreeScene):
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
        albero.addd(4)


        #caso 1: elimino una foglia 0, 6, 9, 15                 OK
        #caso 2: elimino un nodo con un figlio 1, 5, 8, 16      1, 5, 8, 16
        #caso 3: elimino un nodo con due figli 3, 23, 13        3, 13, 23
        # 1, 16
        
        node = albero.root
        valdel = [1, 0, 3, 23, 13]
        vaaldeln = albero.find(valdel[0], node)

        #self.printVect(valdel, node)
        self.printNodeOneShot(node, albero)
        self.wait(3)
        self.clearScene()

        #albero.deleteNode(0, node, albero)
        #albero.deleteNode(6, node, albero)
        #albero.deleteNode(9, node, albero)
        #albero.deleteNode(15, node, albero)

        #albero.deleteNode(1, node, albero)
        #albero.deleteNode(5, node, albero)
        #albero.deleteNode(8, node, albero)
        #albero.deleteNode(16, node, albero)

        #albero.deleteNode(3, node, albero)
        #albero.deleteNode(23, node, albero)
        albero.deleteNode(13, node, albero)

        #3, 8, 13
        self.wait(3)
        node = albero.root
        
        self.printNodeOneShot(node, albero)
        

        self.wait(5)

class firstTree(firstTreeScene):

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
                    
        node = albero.root

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

class addTree(firstTreeScene):
    def construct(self):
        
        global n
        n = 10
        albero = Tree()
        random.seed(1)
        #tmp = [0 for i in range(n)]
        #tmp = random.sample(range(1, 100), n)
        tmp = [50, 95, 54, 6, 34, 66, 63, 52, 39, 99]
        for i in range(n):
            albero.addd(tmp[i])
             
        node = albero.root 
        self.printVect(tmp, node)  
        i = 0
        self.printNodeVect(tmp, i, node, albero)

        print(tmp)
        self.wait(5)

class addTree2(firstTreeScene):
    def construct(self):
        
        global n
        n = 10
        albero = RedBlackTree()
        random.seed(0)
        tmp = [0 for i in range(n)]
        tmp = random.sample(range(1, 100), n)
        for i in range(n):
            self.insert(tmp[i], albero)
             
        node = albero.root 
        self.printVect(tmp, node)  
        i = 0
        self.printNodeVect(tmp, i, node, albero)

        print(tmp)
        self.wait(5)

class findTree(firstTreeScene):
    def construct(self):
        
        global n
        n = 10
        albero = Tree()
        random.seed(0)
        tmp = [0 for i in range(n)]
        tmp = random.sample(range(1, 100), n)
        for i in range(n):
            albero.addd(tmp[i])
        node = albero.root

        valdel = [34]
        valdeln = albero.find(valdel[0], node)
        
        self.printVect(valdel, valdeln)
        self.printNode(node, albero)

        nodefind = albero.find(valdel[0], node)

        if nodefind is not None:
            self.highlightsPath(nodefind, node)

        self.wait(5)

class visitTree(firstTreeScene):
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

        node = albero.root
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
         








        