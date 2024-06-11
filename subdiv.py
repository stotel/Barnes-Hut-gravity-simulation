import sys
import pygame
import random
import math
from pygame.locals import *

sys.setrecursionlimit(2000)

def main(w=10000,n=1000):
    meteoroids = []
    for i in range(n):
        meteoroids.append(meteoroid(mass = 1000,x=random.randint(0,w),y=random.randint(0,w)))
    
    pygame.init()
    surface = pygame.display.set_mode((w/10, w/10))
    pygame.display.set_caption('`_`')

    Q = QTree(1,meteoroids,w)
    Q.subdivide()
    Q.find_mass_dist()
    update_frame = 0
    while(True):
        update_frame+=1
        surface.fill((0,0,0))
        draw_meteoroids(surface,meteoroids)
        Q = QTree(1,meteoroids,w)
        Q.subdivide()
        Q.find_mass_dist()
        Q.graph(surface)
        for i in meteoroids:
            compute_force(Q.root,i,w,meteoroids.index(i),w)
            i.vx+=i.ax
            i.vy+=i.ay
            i.x+=i.vx
            i.y+=i.vy
            i.x=i.x%w
            i.y=i.y%w
            i.ax = 0
            i.ay = 0
        if update_frame % 1 == 0:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

def draw_meteoroids(surface, meteoroids):
    for i in meteoroids:
        surface.set_at((int(i.x/10),int(i.y/10)),(255,255,255))

def compute_force(Root_node,meteor,w1,ind,w,	θ=1):
    f = 0
    if len(Root_node.points) == 1:
        dx = (-meteor.x+Root_node.mass_cent[0])
        ax = abs(dx)
        if ax!=0:
            adx = dx/ax
        else: adx = 0
        if ax != 0:
            if ax > w/2:
                dx = (w-ax)*adx*-1
        dy = (-meteor.y+Root_node.mass_cent[1])
        ay = abs(dy)
        if ay != 0:
            ady = dy/ay
        else: ady = 0
        if ay != 0:
            if ay > w/2:
                dy = (w-ay)*ady*-1
        r = math.sqrt(((dx)**2)+((dy)**2))
        r = max(r,100)
        f1=find_gravity(meteor.mass,Root_node.mass,r)
        f+=f1
        meteor.ax = (f1*(dx)/r)/meteor.mass
        meteor.ay = (f1*(dy)/r)/meteor.mass
    else:
        dx = (-meteor.x+Root_node.mass_cent[0])
        ax = abs(dx)
        if ax!=0:
            adx = dx/ax
        else: adx = 0
        if ax != 0:
            if ax > w/2:
                dx = (w-ax)*adx*-1
        dy = (-meteor.y+Root_node.mass_cent[1])
        ay = abs(dy)
        if ay != 0:
            ady = dy/ay
        else: ady = 0
        if ay != 0:
            if ay > w/2:
                dy = (w-ay)*ady*-1
        r = math.sqrt(((dx)**2)+((dy)**2))
        r = max(r,100)
        d = w1

        if d/r < θ:
            f1=find_gravity(meteor.mass,Root_node.mass,r)
            f+=find_gravity(meteor.mass,Root_node.mass,r)
            meteor.ax = (f1*(dx)/r)/meteor.mass
            meteor.ay = (f1*(dy)/r)/meteor.mass
        else:
            for n in Root_node.children:
                compute_force(n,meteor,n.w,ind,w)

def find_gravity(m_1, m_2, r):
   G_val = 10
   F_val = (G_val*m_1*m_2)/(r**2)

   return F_val
        
class QTree():
    def __init__(self, k,points,w):
        self.threshold = k
        self.points = points
        self.root = Node(0, 0, w, self.points)

    def add_point(self, x, y):
        self.points.append(Point(x, y))
    
    def get_points(self):
        return self.points
    
    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    def graph(self,surface):
        c = find_children(self.root)
        for n in c:
            pygame.draw.line(surface, (0,255,0),(n.x0/10,n.y0/10), ((n.x0+n.w)/10,n.y0/10) ,  1)
            pygame.draw.line(surface, (0,255,0),(n.x0/10,n.y0/10),(n.x0/10,(n.y0+n.w)/10) ,  1)
            pygame.draw.line(surface, (0,255,0),((n.x0+n.w)/10,n.y0/10),((n.x0+n.w)/10,(n.y0+n.w)/10) ,  1)
            pygame.draw.line(surface, (0,255,0),(n.x0/10,(n.y0+n.w)/10),((n.x0+n.w)/10,(n.y0+n.w)/10) ,  1)

        return
    
    def find_mass_dist(self):
        self.root.find_mass()

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node():
    def __init__(self, x0, y0, w, points):
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.points = points
        self.mass = 0
        self.mass_cent = [0,0]
        self.children = []
        
    def find_mass(self):
        self.mass = 0
        self.mass_cent = [0,0]
        if len(self.points)  == 1 : 
            self.mass_cent = [self.points[0].x,self.points[0].y]
            self.mass = self.points[0].mass
        elif len(self.points)  != 0 :
            for i in self.children: 
                i.find_mass()
                self.mass += i.mass
                self.mass_cent[0] = self.mass_cent[0]+i.mass*i.mass_cent[0]
                self.mass_cent[1] = self.mass_cent[1]+i.mass*i.mass_cent[1]
            self.mass_cent[0] = self.mass_cent[0]/self.mass
            self.mass_cent[1] = self.mass_cent[1]/self.mass

                
                    

class meteoroid:
    def __init__(self, x,y,quater = None,mass=1000,vx=0,vy=0,ax=0,ay=0):
        self.quater = quater
        self.mass = mass
        self.x,self.y = x,y
        self.vx,self.vy = vx,vy
        self.ax,self.ay = ax,ay
    
def recursive_subdivide(node, k):
   if len(node.points)<=k:
       return
   
   w_ = float(node.w/2)

   p = contains(node.x0, node.y0, w_, node.points)
   x1 = Node(node.x0, node.y0, w_, p)
   recursive_subdivide(x1, k)

   p = contains(node.x0, node.y0+w_, w_, node.points)
   x2 = Node(node.x0, node.y0+w_, w_, p)
   recursive_subdivide(x2, k)

   p = contains(node.x0+w_, node.y0, w_, node.points)
   x3 = Node(node.x0 + w_, node.y0, w_, p)
   recursive_subdivide(x3, k)

   p = contains(node.x0+w_, node.y0+w_, w_, node.points)
   x4 = Node(node.x0+w_, node.y0+w_, w_, p)
   recursive_subdivide(x4, k)

   node.children = [x1, x2, x3, x4]
   
   
def contains(x, y, w, points):
   pts = []
   for point in points:
       if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+w:
           pts.append(point)
   return pts


def find_children(node):
   if not node.children:
       return [node]
   else:
       children = []
       for child in node.children:
           children += (find_children(child))
   return children

main(10000,1000)