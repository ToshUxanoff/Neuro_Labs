from tkinter import *
from itertools import chain
from lab9 import *
from copy import deepcopy
from processor import process
#---GUI init---
root = Tk()
root.geometry("800x500")

canv = Canvas(root, width=800, height=500, bg='white')
canv.pack(side=LEFT)
#---Constants---
points = []
clusters = []
old_clusters = [] 
colors = ['green','blue','cyan',
          'gold', 'violet', 'pink',
          'khaki', 'aquamarine','red',
         'orange','black','purple']
step = 5
#---
Mode = IntVar()
Mode.set(0)
def run_main():
    global clusters
    mode = Mode.get()
    new_clusters, new_point = process(points, clusters, mode)
    clear_cluster()

    new_clusters = [new_clusters[i] for i in range(len(new_clusters))]
    clusters = deepcopy(new_clusters)
    draw_result(clusters, new_point)
    print("Mode:", mode)
    print("Clusters coords:", clusters)

#---Utility funcs---
def write_point(event):
    x, y = event.x, event.y
    canv.create_oval(x-step, y-step, x+step, y+step, fill="black")
    points.append((x,y))

def write_cluster(event):
    x,y = event.x, event.y
    canv.create_rectangle(x-step, y-step, x+step, y+step, fill="black")
    clusters.append((x,y))

def clear():
    while points:
        elem = points.pop()
        x, y = elem
        canv.create_oval(x-step, y-step, x+step, y+step, fill="white", outline="white")
    
    while clusters:
        elem = clusters.pop()
        x, y = elem
        canv.create_rectangle(x-step, y-step, x+step, y+step, fill="white", outline="white")

def clear_cluster():
    while clusters:
        elem = clusters.pop()
        x, y = elem
        canv.create_rectangle(x-step, y-step, x+step, y+step, fill="white", outline="white")

def get_color(num_cluster):
    return colors[num_cluster%len(colors)]

def draw_result(clusters, new_points):
    for ind in range(len(clusters)):
        color = get_color(ind)
        
        cluster = clusters[ind]
        x,y = cluster
        canv.create_rectangle(x-step, y-step, x+step, y+step, fill=color, outline=color)
        
        arr_points = new_points[ind]
        for point in arr_points:
            x,y = point
            canv.create_oval(x-step, y-step, x+step, y+step, fill=color, outline=color)

#---Events
root.bind("<Button-2>", write_point)
root.bind("<Shift-Button-1>", write_cluster)

#---Buttons
clear_button = Button(root, text="Clear", width=15, height=2, command=clear)
clear_button.place(x=0, y=100)

run_button = Button(root, text="Start", width=15, height=2, command=run_main)
run_button.place(x=0, y=150)

Euclid_mode_button = Radiobutton(root, text="Euclid", width=15, height=2, variable=Mode, value=0)
Euclid_mode_button.place(x=0, y=200)

Chebyshev_mode_button = Radiobutton(root, text="Chebyshev", width=15, height=2, variable=Mode, value=1)
Chebyshev_mode_button.place(x=0, y=250)
#----run
root.mainloop()
