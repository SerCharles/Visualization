import os
from tkinter import *
import tkinter.messagebox
import numpy as np 
from PIL import Image, ImageTk
from PCA import MYPCA

class Interaction(object):
    """The class of Interaction
    """
    
    def __init__(self):
        """The function of data initialization
        """
        mypca = MYPCA()
        mypca.run()
        self.data = mypca.data #N * 28 * 28
        self.result = mypca.result #2 * N
        self.show_result = mypca.show_result #N * 2
        self.labels = mypca.labels #N
        self.N = self.labels.shape[0]
        self.radius = 4.0
        self.window_size = mypca.size
        self.colors = mypca.colors


    def mouse_callback(self, event): 
        """The callback function of mouse interaction

        Args:
            event [tkinter event]: [the mouse click event]
        """
        click_place = np.array([event.x - self.radius, event.y - self.radius]).reshape(1, 2).repeat(self.N, axis=0) #N * 2
        distance = np.sqrt(np.sum((self.show_result - click_place) ** 2, axis=1)) #N
        min_distance = np.min(distance)
        click_id = int(np.argmin(distance))
        label = int(self.labels[click_id])
        x_weight = float(self.result[0, click_id])
        y_weight = float(self.result[1, click_id])
        show_text = 'The id of selected item: {}\nThe label of selected item: {}\
            \nThe PCA result of selected item: ({:.4f}, {:.4f})'.format(click_id, label, x_weight, y_weight)
        if(min_distance <= self.radius):
            if tkinter.messagebox.showinfo('Selected Information', show_text):
                if tkinter.messagebox.askyesno('View the picture or not?', 'View the picture or not?'):
                    current_picture = self.data[click_id]
                    current_picture = Image.fromarray(current_picture)
                    current_picture.show()

    def run(self):
        """The main function of the interaction program
        """
        app = Tk()
        app.title('PCA visualization')
        cv = Canvas(app, bg='white', width=self.window_size[0] + 2 * self.radius, height=self.window_size[1] + 2 * self.radius)
        cv.bind("<Button-1>", self.mouse_callback)
        for i in range(self.N):
            label = self.labels[i]
            color = self.colors[label]
            cv.create_oval(self.show_result[i, 0], self.show_result[i, 1], self.show_result[i, 0] + 2 * self.radius, self.show_result[i, 1] + 2 * self.radius, fill=color, outline=color)
        
        legend_place = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'), 'legend.png')
        legend = Image.open(legend_place)  
        legend = ImageTk.PhotoImage(legend)  
        cv.create_image(self.window_size[0] - 20, 120, image=legend)  
        
        cv.pack()
        mainloop()
        
        
if __name__ == '__main__':
    a = Interaction()
    a.run()