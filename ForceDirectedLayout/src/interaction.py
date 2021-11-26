import os
import time
from tkinter import *
import tkinter.messagebox
import numpy as np 
from fr import FruchtermanReingold

class Interaction(object):
    """The class of Interaction
    """
    
    def __init__(self):
        """The function of data initialization
        """
        self.fr = FruchtermanReingold()
        self.radius = 4.0
        

    def run(self):
        """The main function of the interaction program
        """
        app = Tk()
        app.title('Fruchterman-Reingold visualization')
        cv = Canvas(app, bg='white', width=self.fr.size[0] + 2 * self.radius, height=self.fr.size[1] + 2 * self.radius)
        cv.pack()
        
        for i in range(self.fr.max_iters):
            self.fr.run_one_iter()
            
            for j in range(self.fr.links):
                index_0 = self.fr.link_list[j][0]
                index_1 = self.fr.link_list[j][1]
                x0 = int(self.fr.position[index_0, 0] + self.radius)
                y0 = int(self.fr.position[index_0, 1] + self.radius)
                x1 = int(self.fr.position[index_1, 0] + self.radius)
                y1 = int(self.fr.position[index_1, 1] + self.radius)
                cv.create_line(x0, y0, x1, y1, fill='grey')
            
            for j in range(self.fr.nodes):
                x = int(self.fr.position[j, 0])
                y = int(self.fr.position[j, 1])
                #if x < 0 or x >= self.fr.size[0] or y < 0 or y >= self.fr.size[1]:
                #    continue 
                cv.create_oval(x, y, x + 2 * self.radius, y + 2 * self.radius, fill="red", outline="red")
            cv.update()

            if i < self.fr.max_iters - 1:
                time.sleep(0.05)
                cv.delete(ALL)        
        mainloop()
        
        
if __name__ == '__main__':
    a = Interaction()
    a.run()