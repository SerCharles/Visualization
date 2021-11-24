import os 
import json 


class NodeLinkTree(object):
    """The Reingold-Tilford Algorithm to visualize a node-link tree 
    """
    
    class Node(object):
        """A node of a tree
        """
        def __init__(self, name, index, depth, sons_visible):
            """Init the node

            Args:
                name [string]: [the name of the node]
                index [int]: [the index of the subtree in its father's sons]
                depth [int]: [the depth of the root of the subtree]
                sons_visible [bool]: [whether the node's sons are visible]
            """
            #basic information of the subtree
            self.name = name 
            self.index = index
            self.depth = depth
            self.sons_visible = sons_visible
            self.sons = []
            
            #the variables used in Reingold-Tilford Algorithm
            self.x = float(index)
            self.y = float(depth) 
            self.mod = 0.0 
            
            #the real showing place of the node in the visualization result
            self.show_x = 0
            self.show_y = 0
            
        def switch_son_visible(self):
            """Switch the status of whether the sons of the node is visible
            """
            self.sons_visible = not self.sons_visible
            
        def add_son(self, son):
            """Add a son to the node

            Args:
                son [Node]: [the node of the son]
            """
            self.sons.append(son)
    
    
    def __init__(self, data_name):
        """Initialize the Algorithm by loading and parsing the data

        Args:
            data_name [string]: [the name of the dataset]
        """
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        data_place = os.path.join(data_dir, data_name)
        with open(data_place, encoding='utf-8') as fin:
            self.data = json.load(fin)
        self.tree = self.build_tree(self.data, 0, 0)
        kebab = 0
    
    def build_tree(self, data, index, depth):
        """Recursive function, build the tree based on the data dictionary loaded from json

        Args:
            data [dictionary]: [the data used to build the subtree]
            index [int]: [the index of the subtree in its father's sons]
            depth [int]: [the depth of the root of the subtree]
            
        Returns:
            root [Node]: [return the root node of the tree]
        """
        name = data['name']
        sons_visible = True 
        root = self.Node(name, index, depth, sons_visible)
        try:
            sons = data['sons']
        except:
            sons = []
        for i in range(len(sons)): 
            son = self.build_tree(sons[i], i, depth + 1)
            root.add_son(son)
        return root
    
    

a = NodeLinkTree('test.json')