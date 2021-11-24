from math import *
import os 
import json 


class NodeLinkTree(object):
    """The Reingold-Tilford Algorithm to visualize a node-link tree 
    """
    
    class Node(object):
        """A node of a tree
        """
        def __init__(self, name, index, depth, father, sons_visible):
            """Init the node

            Args:
                name [string]: [the name of the node]
                index [int]: [the index of the subtree in its father's sons]
                depth [int]: [the depth of the root of the subtree]
                father [Node]: [the father of the node, None if empty]
                sons_visible [bool]: [whether the node's sons are visible]
            """
            #basic information of the subtree
            self.name = name 
            self.index = index
            self.depth = depth
            self.father = father
            self.left = None 
            self.right = None
            self.sons_visible = sons_visible
            self.sons = []
            self.childrens = 0
            
            #the variables used in Reingold-Tilford Algorithm
            self.x = 0.0
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
            self.childrens += 1

        def assign_brothers(self):
            """Assign the brothers of the sons
            """
            for i in range(self.childrens):
                if i == 0:
                    left = None 
                else:
                    left = self.sons[i - 1]
                if i == self.childrens - 1:
                    right = None 
                else:
                    right = self.sons[i + 1]
                self.sons[i].left = left 
                self.sons[i].right = right


            
    
    def __init__(self, data_name):
        """Initialize the Algorithm by loading and parsing the data

        Args:
            data_name [string]: [the name of the dataset]
        """
        #load data
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        data_place = os.path.join(data_dir, data_name)
        with open(data_place, encoding='utf-8') as fin:
            self.data = json.load(fin)
        
        #build the tree and set the initial x, mod values
        self.tree = self.build_tree(self.data, 0, 0, None)
    
    def build_tree(self, data, index, depth, father):
        """Recursive function, build the tree based on the data dictionary loaded from json

        Args:
            data [dictionary]: [the data used to build the subtree]
            index [int]: [the index of the subtree in its father's sons]
            depth [int]: [the depth of the root of the subtree]
            father [Node]: [the father of the node, None if empty]
            
        Returns:
            root [Node]: [return the root node of the tree]
        """
        name = data['name']
        sons_visible = True 
        root = self.Node(name, index, depth, father, sons_visible)
        try:
            sons = data['sons']
        except:
            sons = []
        for i in range(len(sons)):                 
            son = self.build_tree(sons[i], i, depth + 1, root)
            root.add_son(son)
        root.assign_brothers()
        return root
    
    #TODO
            private static void GetLeftContour(TreeNodeModel<T> node, float modSum, ref Dictionary<int, float> values)
        {
            if (!values.ContainsKey(node.Y))
                values.Add(node.Y, node.X + modSum);
            else
                values[node.Y] = Math.Min(values[node.Y], node.X + modSum);
 
            modSum += node.Mod;
            foreach (var child in node.Children)
            {
                GetLeftContour(child, modSum, ref values);
            }
        }
 
        private static void GetRightContour(TreeNodeModel<T> node, float modSum, ref Dictionary<int, float> values)
        {
            if (!values.ContainsKey(node.Y))
                values.Add(node.Y, node.X + modSum);
            else
                values[node.Y] = Math.Max(values[node.Y], node.X + modSum);
 
            modSum += node.Mod;
            foreach (var child in node.Children)
            {
                GetRightContour(child, modSum, ref values);
            }
        }
    
    
    def check_subtree_conflicts(self, root):
        """Check the conflicts of current root to the subtrees of its left brothers

        Args:
            root [Node]: [the root of the tree]
        """
        root.get_contours()#TODO

        brothers = root.father.sons
        for i in range(root.index):
            brother = brothers[i]
            max_shift = 0.0
            len_left = len(root.left_contour)
            len_right = len(brother.right_contour)
            length = min(len_left, len_right)
            for j in range(length):
                shift = brother.right_contour[j] + 1.0 - root.left_contour[j]
                max_shift = max(max_shift, shift)
            if max_shift > 0:
                root.x += max_shift
                root.mod += max_shift
                if root.index - i > 1:
                    self.center_nodes_between(brothers, i, root.index)
                
    def center_nodes_between(self, brothers, left_index, right_index):
        """Center the nodes between two conflict nodes, in which the right one is the root to be processed

        Args:
            brothers [Node array]: [the brothers]
            left_index ([type]): [description]
            right_index ([type]): [description]
        """
        brother = brothers[left_index]
        root = brothers[right_index]
        fractions = right_index - left_index
        distance = root.x - brother.x
        length_per_fraction = distance / fractions
        for i in range(1, fractions):
            middle_node = brothers[left_index + i]
            desired_x = brother.x + length_per_fraction * i 
            offset = desired_x - middle_node.x 
            middle_node.x += offset
            middle_node.mod += offset
        self.check_subtree_conflicts(root)
    
    def first_traversal(self, root):
        """Traverse the tree for the first time, getting the x and mod values to satisfy the six criterions
        
        Args:
            root [Node]: [the root of the tree]
        """
        whether_sons = root.sons_visible and (root.childrens > 0)
        
        #post traversal
        if whether_sons:
            for son in root.sons:
                self.first_traversal(son)
        
        #positioning child nodes under parents
        root.x = float(root.index)
        desired_x = root.x
        if not whether_sons:
            if root.index == 0:
                root_x = 0.0
            else:
                root_x = root.left.x + 1.0
        else:
            desired_x = (root.sons[0].x + root.sons[-1].x) / 2
            if root.index == 0:
                root.x = desired_x 
            else: 
                root.x = root.left.x + 1.0
                root.mod = root.x - desired_x
        
        #checking for node conflicts
        if root.father != None and root.index > 0 and whether_sons:
            self.check_subtree_conflicts(root)
        kebab = 0         
        
        
        
    def run(self):
        """The main process of Reingold-Tilford Algorithm
        """
        self.first_traversal(self.tree) 
        kebab = 0
        

a = NodeLinkTree('test.json')
a.run()