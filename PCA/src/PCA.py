import os
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

class MYPCA(object):
    def __init__(self):
        """The PCA initialization function
        """
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.data = np.load(os.path.join(data_dir, 'sampled_image.npy')) #self.N * 28 * 28
        self.labels = np.load(os.path.join(data_dir, 'sampled_label.npy')).astype(np.int32) #self.N
        self.N = self.data.shape[0]
        self.size = np.array([1280, 960], dtype=np.int32)
        self.colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'black', 'grey', 'darkgreen']

        
    def get_result_sklearn(self):
        """The sklearn PCA
        """
        self.input = self.data.reshape(self.N, -1) #self.N * 784
        pca = PCA(n_components=2)
        self.result = pca.fit_transform(self.input).T #2 * self.N

    def get_result(self):
        """The main function of PCA
        """
        self.input = self.data.reshape(self.N, -1).T #784 * self.N
        mean = np.mean(self.input, axis=1, keepdims=True).repeat(self.N, axis=1) #784 * self.N
        self.input = self.input - mean #784 * self.N
        self.covariance = np.matmul(self.input, self.input.T) / self.N #784 * 784
        U, sigma, VT = np.linalg.svd(self.covariance)
        P = U[:, 0:2].T #2 * 784
        self.result = np.matmul(P, self.input) #2 * self.N
        

        
    def normalize(self):
        """Normalize the results
        """
        min_result = self.result.min(1) #2
        max_result = self.result.max(1) #2
        dist_result = max_result - min_result #2
        min_result = min_result.reshape(2, 1).repeat(self.N, axis=1)
        dist_result = dist_result.reshape(2, 1).repeat(self.N, axis=1)
        self.show_result = (self.result - min_result) / dist_result #2 * self.N
        size = self.size.reshape(2, 1).repeat(self.N, axis=1)
        self.show_result = (self.show_result * size).astype(np.int32).T #self.N * 2 

    def visualize(self):
        """Visualize the data
        """
        for i in range(10):
            color = self.colors[i]
            mask = (self.labels == i)
            points = self.show_result[mask]
            plt.scatter(points[:, 0], points[:, 1], label=str(i), color=color)
            plt.legend()
        plt.show()
        
    def run(self):
        """The main process of PCA
        """
        self.get_result()
        self.normalize()
        
if __name__ == '__main__':
    a = MYPCA()
    a.run()
    a.visualize()




    

        

        