import os 
import csv
import numpy as np 

    

class FruchtermanReingold(object):
    """The Fruchterman-Reingold algorithm
    """
    
    class Node(object):
        """One node
        """
        def __init__(self, name, size):
            self.name = name 
            self.size = size
            self.x = 0.0
            self.y = 0.0
            self.vx = 0.0
            self.vy = 0.0
            
    
    def __init__(self):
        """Load the data and initialize the map
        """
        self.size = [1280, 960]
        self.NodeList = []
        self.LinkList = []
        self.total_num = 100
        NodeHash = {}
        
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
                if author in NodeHash.keys():
                    node = self.NodeList[NodeHash[author]]
                    nodes.append(node)
                else:
                    node = self.Node(author, self.size)
                    self.NodeList.append(node)
                    NodeHash[author] = len(self.NodeList) - 1
            for i in range(len(nodes) - 1):
                for j in range(i + 1, len(nodes)):
                    self.LinkList.append((nodes[i], nodes[j]))
            current_num += 1
        
        for row in data_reader_2:
            if self.total_num >= 0 and current_num >= self.total_num:
                break
            authors = row[0].split(',')
            nodes = []
            for author in authors:
                if author in NodeHash.keys():
                    node = self.NodeList[NodeHash[author]]
                    nodes.append(node)
                else:
                    node = self.Node(author, self.size)
                    self.NodeList.append(node)
                    NodeHash[author] = len(self.NodeList) - 1
            for i in range(len(nodes) - 1):
                for j in range(i + 1, len(nodes)):
                    self.LinkList.append((nodes[i], nodes[j]))
            current_num += 1
            
    def run(self):
        """The main function of Fruchterman-Reingold algorithm
        """
        kebab = 0
                
                
                
a = FruchtermanReingold()
a.run()