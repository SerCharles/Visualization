import os 
import csv
import time
from math import *
import numpy as np 
import collections

    

class FruchtermanReingold(object):
    """The Fruchterman-Reingold algorithm
    """
        
    def __init__(self):
        """Load the data and initialize the map
        """
        #init basic
        self.iter = 0
        self.max_iters = 1000
        self.size = [1280, 960]
        self.threshold_repulsive = 50.0
        self.total_num = 100
        self.name_list = []
        self.paper_list = []
        self.coauthor_list = []
        self.link_list = []
        self.nodes = 0
        self.links = 0
        self.t = 1.0
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        data_place_1 = os.path.join(data_dir, 'scopus_visual_analytics_part1.csv')
        data_place_2 = os.path.join(data_dir, 'scopus_visual_analytics_part2.csv')
        csvfile_1 = open(data_place_1, 'r', encoding="utf-8-sig")
        data_reader_1 = csv.reader(csvfile_1)
        csvfile_2 = open(data_place_2, 'r', encoding="utf-8-sig")
        data_reader_2 = csv.reader(csvfile_2)
        current_num = 0
        papers = []
        author_arrays = []
        node_hash = {}

        #init points
        for row in data_reader_1:
            if self.total_num >= 0 and current_num >= self.total_num:
                break
            authors = row[0].split(',')
            nodes = []
            for author in authors:
                if author == 'Authors' or author == '[No author name available]':
                    continue
                if not author in node_hash.keys():
                    self.name_list.append(author)
                    node_hash[author] = len(self.name_list) - 1
                    nodes.append(len(self.name_list) - 1)
                else:
                    nodes.append(node_hash[author])
            author_arrays.append(nodes)
            papers.append(row[1])
            current_num += 1
        
        for row in data_reader_2:
            if self.total_num >= 0 and current_num >= self.total_num:
                break
            authors = row[0].split(',')
            nodes = []
            for author in authors:
                if author == 'Authors' or author == '[No author name available]':
                    continue
                if not author in node_hash.keys():
                    self.name_list.append(author)
                    node_hash[author] = len(self.name_list) - 1
                    nodes.append(len(self.name_list) - 1)
                else:
                    nodes.append(node_hash[author])
            author_arrays.append(nodes)
            papers.append(row[1])
            current_num += 1
        
        #init links
        self.nodes = len(self.name_list)
        self.k = sqrt(self.size[0] * self.size[1] / self.nodes)
        self.adjacency = np.zeros((self.nodes, self.nodes), dtype=np.int32)
        self.position = np.zeros((self.nodes, 2), dtype=np.float64)
        self.move = np.zeros((self.nodes, 2), dtype=np.float64)
        for coauthors in author_arrays:
            for i in range(len(coauthors) - 1):
                for j in range(i + 1, len(coauthors)):
                    self.adjacency[coauthors[i], coauthors[j]] += 1 
                    self.adjacency[coauthors[j], coauthors[i]] += 1 
                    self.link_list.append([coauthors[i], coauthors[j]])
                    self.links += 1
                    
        #init coauthor and paper
        for i in range(self.nodes):
            self.paper_list.append([])
            self.coauthor_list.append({})
            
        for i in range(len(papers)):
            authors = author_arrays[i]
            title = papers[i]
            for j in range(len(authors)):
                self.paper_list[authors[j]].append(title)
    
            for j in range(len(authors) - 1):
                for k in range(j + 1, len(authors)):
                    if authors[k] in self.coauthor_list[authors[j]].keys():
                        self.coauthor_list[authors[j]][authors[k]] += 1
                    else:
                        self.coauthor_list[authors[j]][authors[k]] = 1
                        
                    if authors[j] in self.coauthor_list[authors[k]].keys():
                        self.coauthor_list[authors[k]][authors[j]] += 1
                    else:
                        self.coauthor_list[authors[k]][authors[j]] = 1
                    
        self.sorted_coauthor_list = []
        for i in range(self.nodes):
            sorted_dict = sorted(self.coauthor_list[i].items(), key=lambda obj: obj[1], reverse=True)
            self.sorted_coauthor_list.append(collections.OrderedDict(sorted_dict))

        
        print(self.nodes, self.links)
        self.set_initial_place()
            
    def set_initial_place(self):
        """Set the initial places of the nodes
        """
        item_per_dim = ceil(sqrt(self.nodes)) + 1
        dist_x = self.size[0] / item_per_dim
        dist_y = self.size[1] / item_per_dim
        index = np.arange(0, self.nodes)
        ix = index // item_per_dim + 1
        iy = index % item_per_dim + 1
        self.position[:, 0] = ix * dist_x
        self.position[:, 1] = iy * dist_y
    
    def get_distance_matrix(self):
        """Get the distance matrix between the nodes
        """
        self.dist_x = []
        self.dist_y = []
        self.dist = []
        for i in range(self.nodes):
            x = self.position[i, 0]
            y = self.position[i, 1]
            dist_x = -(self.position[:, 0] - x) #N * 1
            dist_y = -(self.position[:, 1] - y) #N * 1
            dist = np.sqrt(dist_x ** 2 + dist_y ** 2) #N * 1
            dist[i] = 1.0
            dist_x = dist_x / dist #N * 1
            dist_y = dist_y / dist #N * 1
            dist[i] = 0.0 
            self.dist_x.append(dist_x.reshape(1, self.nodes)) #1 * N
            self.dist_y.append(dist_y.reshape(1, self.nodes)) #1 * N
            self.dist.append(dist.reshape(1, self.nodes)) #1 * N
        
        self.dist_x = np.concatenate(self.dist_x, axis=0) #N * N
        self.dist_y = np.concatenate(self.dist_y, axis=0) #N * N
        self.dist = np.concatenate(self.dist, axis=0) #N * N

    def get_repulsive_force(self):
        """Get the repulsive forces between nodes
        """
        self.repulsive = []
        mask = self.dist <= self.threshold_repulsive 
        dist_x = self.dist_x * mask 
        dist_y = self.dist_y * mask 
        
        for i in range(self.nodes):
            self.dist[i, i] = 1.0 #avoid / 0
            repulsive_x = np.sum(dist_x[i] / self.dist[i] * self.k * self.k)
            repulsive_y = np.sum(dist_y[i] / self.dist[i] * self.k * self.k)
            repulsive = np.array([repulsive_x, repulsive_y], dtype=np.float32).reshape(1, 2)
            self.dist[i, i] = 0.0
            self.repulsive.append(repulsive)
        self.repulsive = np.concatenate(self.repulsive, axis=0) #N * 2


    def get_attractive_force(self):
        """Get the attractive forces between nodes that have links
        """
        self.attractive = []
        mask = self.adjacency
        dist_x = self.dist_x * mask 
        dist_y = self.dist_y * mask         
        
        for i in range(self.nodes):
            attractive_x = np.sum(-dist_x[i] * self.dist[i] * self.dist[i] / self.k)
            attractive_y = np.sum(-dist_y[i] * self.dist[i] * self.dist[i] / self.k)
            attractive = np.array([attractive_x, attractive_y], dtype=np.float32).reshape(1, 2)
            self.attractive.append(attractive)
        self.attractive = np.concatenate(self.attractive, axis=0) #N * 2
            
    def update_place(self, t):
        """Update the places of the nodes

        Args:
            t [float]: [the learning rate]
        """
        delta = self.attractive + self.repulsive #N * 2
        delta_length = np.sqrt(np.sum(delta ** 2, axis=1)) #N
        mask = (delta_length < t)
        learning_rate = (mask * delta_length + (~mask) * t).reshape(self.nodes, 1).repeat(2, axis=1)
        length = delta_length.reshape(self.nodes, 1).repeat(2, axis=1)
        length = length + (delta <= 0)
        move = delta / length * learning_rate #N * 2
        #print(np.sqrt(np.sum(move[:, 0] ** 2)))
        self.position = self.position + move


        
    def run_one_iter(self):
        """The main function of Fruchterman-Reingold algorithm
        """
        start = time.time()
        t = 1.0 - (self.iter / self.max_iters)
        self.get_distance_matrix()
        self.get_repulsive_force()
        self.get_attractive_force()
        self.update_place(t)
        end = time.time()
        #print('Iteration: {}, Total time: {:.4f}s'.format(self.iter + 1, end - start))                
                