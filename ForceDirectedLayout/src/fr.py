import os 
import csv
from math import *
import numpy as np 

    

class FruchtermanReingold(object):
    """The Fruchterman-Reingold algorithm
    """
    
    class Node(object):
        """One node
        """
        def __init__(self, name, size):
            """Initialize the node

            Args:
                name [string]: [the person name represented by the node]
                size [array]: [the width and height of the screen]
            """
            self.name = name 
            self.size = size
            self.x = 0.0
            self.y = 0.0
            self.dx = 0.0
            self.dy = 0.0
            
        def update_place(self, t):
            """Update the place 

            Args:
                t [float]: [the learning rate]
            """
            dx = self.dx - self.x 
            dy = self.dy - self.y
            dist = sqrt(dx ** 2 + dy ** 2)
            dx = dx / dist * min(dist, t)
            dy = dy / dist * min(dist, t)
            
            self.x += dx
            self.y += dy
            if self.x < 0.0:
                self.x = 0.0
            if self.x > self.size[0] - 1:
                self.x = float(self.size[0] - 1)
            if self.y < 0.0:
                self.y = 0.0
            if self.y > self.size[1] - 1:
                self.y = float(self.size[1] - 1)
            self.dx = 0.0 
            self.dy = 0.0
    
    def __init__(self):
        """Load the data and initialize the map
        """
        self.size = [1280, 960]
        self.node_list = []
        self.link_list = []
        self.nodes = 0
        self.links = 0
        self.total_num = 100
        self.q = 0.0
        self.k = 30
        node_hash = {}
        
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        data_place_1 = os.path.join(data_dir, 'scopus_visual_analytics_part1.csv')
        data_place_2 = os.path.join(data_dir, 'scopus_visual_analytics_part2.csv')
        csvfile_1 = open(data_place_1, 'r', encoding="utf-8-sig")
        data_reader_1 = csv.reader(csvfile_1)
        csvfile_2 = open(data_place_2, 'r', encoding="utf-8-sig")
        data_reader_2 = csv.reader(csvfile_2)
        current_num = 0
        
        for row in data_reader_1:
            if self.total_num >= 0 and current_num >= self.total_num:
                break
            authors = row[0].split(',')
            nodes = []
            for author in authors:
                if author in node_hash.keys():
                    node = self.node_list[node_hash[author]]
                    nodes.append(node)
                else:
                    node = self.Node(author, self.size)
                    self.node_list.append(node)
                    node_hash[author] = len(self.node_list) - 1
            for i in range(len(nodes) - 1):
                for j in range(i + 1, len(nodes)):
                    self.link_list.append((nodes[i], nodes[j]))
            current_num += 1
        
        for row in data_reader_2:
            if self.total_num >= 0 and current_num >= self.total_num:
                break
            authors = row[0].split(',')
            nodes = []
            for author in authors:
                if author in node_hash.keys():
                    node = self.node_list[node_hash[author]]
                    nodes.append(node)
                else:
                    node = self.Node(author, self.size)
                    self.node_list.append(node)
                    node_hash[author] = len(self.node_list) - 1
            for i in range(len(nodes) - 1):
                for j in range(i + 1, len(nodes)):
                    self.link_list.append((nodes[i], nodes[j]))
            current_num += 1
        
        
        self.nodes = len(self.node_list)
        self.links = len(self.link_list)
        self.q = sqrt(self.size[0] * self.size[1] / self.nodes)
            
    def set_initial_place(self):
        """Set the initial places of the nodes
        """
        item_per_dim = ceil(sqrt(self.nodes))
        dist_x = self.x / item_per_dim
        dist_y = self.y / item_per_dim
        for i in range(self.nodes):
            ix = i // item_per_dim
            iy = i % item_per_dim
            self.node_list[i].x = dist_x * ix 
            self.link_list[i].y = dist_y * iy 
            self.node_list[i].dx = 0.0
            self.node_list[i].dy = 0.0 
    
    def get_repulsive_force(self):
        """Get the repulsive forces between links
        """
        for i in range(self.nodes - 1):
            for j in range(i + 1, self.nodes):
                dx = self.node_list[i].x - self.node_list[j].x
                dy = self.node_list[i].y - self.node_list[j].y
                d = sqrt(dx ** 2 + dy ** 2)
                dx = dx / d
                dy = dy / d
                self.node_list[i].dx += self.k * self.k / d  * dx 
                self.node_list[i].dy += self.k * self.k / d  * dy

    def get_attractive_force(self):
        """Get the attractive forces between links
        """
        for link in range(self.links):
            left, right = link 
            dx = left.x - right.x 
            dy = left.y - right.y 
            d = sqrt(dx ** 2 + dy ** 2)
            move_x = d * d / self.k * dx 
            move_y = d * d / self.k * dy
            self.right.dx += move_x
            self.right.dy += move_y
            self.left.dx -= move_x 
            self.left_dy -= move_y
            
    def update_place(self, t):
        """Update the places of the nodes

        Args:
            t [float]: [the learning rate]
        """
        for node in self.node_list:
            node.update_place(t)

        
           
        
    def run(self):
        """The main function of Fruchterman-Reingold algorithm
        """
        self.set_initial_place()
        t = 1.0
        for i in range(100):
            self.get_repulsive_force()
            self.get_attractive_force()
            self.update_place(t)
            t = t - t / (i + 1)
            
                
                
                
a = FruchtermanReingold()
a.run()