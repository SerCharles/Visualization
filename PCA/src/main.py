from tkinter import *
import numpy as np 
from PCA import MYPCA

mypca = MYPCA()
mypca.run()
result = mypca.result
labels = mypca.labels
N = labels.shape[0]


app = Tk()

#通过event形参来获取对应事件描述
def callback(event): 
    click_place = np.array([event.x - 4, event.y - 4]).reshape(1, 2).repeat(N, axis=0) #N * 2
    distance = np.sqrt(np.sum((result - click_place) ** 2, axis=1)) #N
    min_distance = np.min(distance)
    min_item = np.argmin(distance)
    if(min_distance < 4):
        print("当前元素id:", min_item, "当前元素标签:", labels[min_item])

#创建框架，窗口尺寸
#frame = Frame(app, width = 800, height = 800)
# 创建一个Canvas，设置其背景色为白色
cv = Canvas(app, bg = 'white', width = 808, height = 808)
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'black', 'grey', 'darkgreen']
for i in range(N):
    label = labels[i]
    color = colors[label]
    cv.create_oval(result[i, 0], result[i, 1], result[i, 0] + 8, result[i, 1] + 8, fill=color)
# 创建一个矩形，坐标为(10,10,110,110)
#frame.bind("<Motion>",callback)
cv.bind("<Button-1>",callback)
cv.bind("<Button-2>",callback)
cv.bind("<Button-3>",callback)
cv.pack()
#<Button-1>Button：表示鼠标的点击事件 “—”左边是事件本身，右边是事件描述
#1：表示左键 2：中间键的滚轮点击 3：右键

mainloop()