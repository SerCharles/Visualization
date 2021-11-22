import os
import numpy as np 


class TSNE(object):
    def __init__(self, perplexity=30.0):
        """The TSNE initialization function
        """
        self.perplexity = perplexity
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.data = np.load(os.path.join(data_dir, 'sampled_image.npy'))
        self.labels = np.load(os.path.join(data_dir, 'sampled_label.npy'))
        self.N = self.data.shape[0]
        self.data = self.data.reshape(self.N, -1)

    def get_dist_picture(self):
        """Get the distance between the i and j picture data
        """
        #(a - b) ^ 2 = a ^ 2 + b ^ 2 - 2 * a * b
        square = np.sum(self.data ** 2, axis=1) #N
        a2 = square.reshape(1, self.N).repeat(self.N, 1) #N * N
        b2 = square.reshape(self.N, 1).repeat(1, self.N) #N * N
        ab = np.matmul(self.data, self.data.T)
        self.dist = a2 + b2 - ab * 2
    
    def calculate_perplexity(self, i, sigma):
        """Get the perplexity of item i

        Args:
            i [int]: [the ith item]
            sigma [float]: [the current sigma]
        
        Return:
            perplexity [float]: [the predicted perplexity]
            divided_probability [numpy float array], [N]: [the pj|i]
        """
        probability_i = np.exp(-self.dist[i] / (2 * sigma * sigma)) #N
        probability_i[i] = 0.0
        probability_sum = np.sum(probability_i) #1
        divided_probability = probability_i / probability_sum #N
        divided_probability[i] = 1.0 #avoid log 0 
        entropy = divided_probability * np.log2(divided_probability) #N
        perplexity = float(np.exp2(np.sum(entropy)))
        divided_probability[i] = 0.0
        return perplexity, divided_probability
        
    def predict_sigma(self):
        """Predict the sigma of each data and update the P using the binary search
        """
        threshold = 1e-5
        max_iter = 50
        self.sigma = np.zeros((self.N), dtype=np.float32)
        self.P = np.zeros((self.N, self.N), dtype=np.float32)
        for i in range(self.N):
            sigma_down = 0.0
            sigma_up = np.inf 
            sigma = 1.0
            iters = 0
            while True:
                perplexity, _ = self.calculate_perplexity(i, sigma)
                iters += 1
                if iters > max_iter or abs(perplexity - self.perplexity) < threshold:
                    break 
                elif perplexity > self.perplexity:
                    sigma_down = sigma
                    if sigma_up == np.inf:
                        sigma = sigma * 2
                    else:
                        sigma = (sigma + sigma_up) / 2
                else: 
                    sigma_up = sigma 
                    sigma = (sigma + sigma_down) / 2
                    
            self.sigma[i] = sigma 
            _, probability = self.calculate_perplexity(i, sigma)
            self.P[i, :] = probability
        
    def run(self):
        """The main process of TSNE
        """
        self.P = (self.P + self.P.T) / (2 * self.N)
        
                
        

TSNE()
        