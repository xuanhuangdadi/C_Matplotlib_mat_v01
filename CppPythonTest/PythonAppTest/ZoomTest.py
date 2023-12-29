

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.io as sio
import os
from matplotlib import cycler
from matplotlib.text import Text, Annotation
from matplotlib.patches import Polygon, Rectangle, Circle, Arrow, ConnectionPatch,Ellipse,FancyBboxPatch
from matplotlib.widgets import Button, Slider, Widget


def call_move(event, fig): # event mouse press/release
    global mPress # whether mouse button press or not
    global startx
    global starty
    if event.name=='button_press_event':
        axtemp=event.inaxes 
        # Whether mouse in a coordinate system or not, yes is the figure in the mouse location, no is None
        if axtemp and event.button==1: 
            print(event)
            mPress=True
            startx=event.xdata
            starty=event.ydata
    elif event.name=='button_release_event':
        axtemp=event.inaxes
        if axtemp and event.button==1:
            mPress=False 
    elif event.name=='motion_notify_event':
        axtemp=event.inaxes
        if axtemp and event.button==1 and mPress: # the mouse continuing press
            x_min, x_max = axtemp.get_xlim()
            y_min, y_max = axtemp.get_ylim()
            w=x_max-x_min
            h=y_max-y_min
            # mouse movement
            mx=event.xdata-startx
            my=event.ydata-starty
            axtemp.set(xlim=(x_min-mx, x_min-mx+w))
            axtemp.set(ylim=(y_min-my, y_min-my+h))
            fig.canvas.draw_idle()  # Delay drawing
    return
 
 
def call_scroll(event, fig):
    print(event.name)
    axtemp=event.inaxes
    print('event:',event)
    print(event.xdata,event.ydata)
    # caculate the xlim and ylim after zooming
    if axtemp:
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        w = x_max - x_min
        h = y_max - y_min
        curx=event.xdata
        cury=event.ydata
        curXposition=(curx - x_min) / w
        curYposition=(cury - y_min) / h
        # Zoom the figure for x times
        zoom_times = 1.5
        if event.button == 'down':
            print('befor:',w,h)
            w = w*zoom_times
            h = h*zoom_times
            print('down',w,h)
        elif event.button == 'up':
            print('befor:',w,h)
            w = w/zoom_times
            h = h/zoom_times
            print('up',w,h)
        print(curXposition,curYposition)
        newx=curx - w*curXposition
        newy=cury - h*curYposition
        axtemp.set(xlim=(newx, newx+w))
        axtemp.set(ylim=(newy, newy+h))
        fig.canvas.draw_idle()  # drawing



def update_annot(ind, l1, annot, x_str, y_str, fig):
    posx = np.array(l1.get_data())[0][ind["ind"][0]] #get the x in the line
    posy = np.array(l1.get_data())[1][ind["ind"][0]] #get the y in the line
    annot.xy = ([posx, posy])
    text = "{}, {}".format(" ".join([x_str[n] for n in ind["ind"]]),
                           " ".join([y_str[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor('green') # set facecolor green
    annot.get_bbox_patch().set_alpha(0.4) # transparency


    """
    # set face Gradualcolor if needed
    cmap = plt.cm.RdYlGn
    norm = plt.Normalize(1,4)
    c = np.random.randint(1,10,size=200000) # the upper colour
    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]]))) # set facecolor
    """


    
def hover(event, l1, annot, ax, x_str, y_str, fig):

    vis = annot.get_visible()
    if event.inaxes == ax: # the mouse in the figure
        cont, ind = l1.contains(event)
        if cont: # the mouse in the point
            update_annot(ind, l1, annot, x_str, y_str, fig)
            annot.set_visible(True)
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


def set_colors(color_nums):
    num_plots = color_nums # the number of colour types 
    colormap = plt.cm.gist_ncar
    c = [colormap(i) for i in np.linspace(0, 1, num_plots)]
    myCycler = cycler(color = c)
    plt.gca().set_prop_cycle(myCycler) # set the colour change


def SetFigSize(ax, x, y):
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
   
    ax.set_xlim(x_min, x_max) # xlabel start limition
    ax.set_ylim(y_min, y_max) # ylabel start limition
    

def get_path(Array):
    up_dir_path = os.path.abspath(os.path.join(os.getcwd(), "..")) # get the up directory
    demo_path = os.path.join(up_dir_path, "CppPythonTest/mattest.mat") # the mat file path
    data = sio.loadmat(demo_path)


def main(cell, X_axis, Y_axis):  # the second parameter means cell position, the third parameter means X-axis, the forth parameter means Y-axis
    
    up_dir_path = os.path.abspath(os.path.join(os.getcwd(), "..")) # get the up directory
    demo_path = os.path.join(up_dir_path, "CppPythonTest/mattest.mat") # the mat file path
    data = sio.loadmat(demo_path)

    list_Array_key = list(data.keys())
    Array = data[list_Array_key[3]] # As a matter of fact is 2 demensions array
    Array = Array.squeeze()
    fig = plt.figure() # Set up Canvas
    ax = fig.add_subplot(111) # set the Canvas 1 * 1， and the figure will show at the first figure

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->")) # set annot
    list_Array_key = list(data.keys()) # get the matrix key
    Array = data[list_Array_key[3]] #get the matrix data
    Array = Array.squeeze() # Dimensionality reduction to get a 2 Matrix of demension 
    # the Array types
    """ defined by the file format, if you choose this file format, you need to exegesis next my_data
    if Array[0][0].ndim != 0:
        Array = Array[cell].T # Matrix transpose  
    else:
        Array = Array.T
    Array = Array[Array[:,X_axis].argsort()] # Array ordered by X_axis
    set_colors(len(Array)) # set line color types
    x = np.array([])
    y = np.array([])
    for i in Y_axis: # from y_axis
        x = np.hstack((x, Array[X_axis])) 
        y = np.hstack((y, Array[i]))
        l = plt.plot(Array[X_axis], Array[i])
    """ 

    # my_data
    Array = Array.T # Matrix transpose  
    Array = Array[Array[:,len(Array) - X_axis].argsort()] # Array ordered by X_axis
    Tag = str(data[list_Array_key[4]])   
    Tag = Tag[2 : len(Tag) - 2].split(', ') # get the matrix tag, use split function split string


    set_colors(len(Array)) # set line color types
    x = np.array([])
    y = np.array([])
    for i in Y_axis: # from y_axis
        x = np.hstack((x, Array[len(Array) - X_axis - 1]))
        y = np.hstack((y, Array[len(Array) - i - 1]))
        l = plt.plot(Array[len(Array) - X_axis - 1], Array[len(Array) - i - 1], label = Tag[i])
    # if you choose first file format, exegesis my_data 
    plt.legend(loc='upper right') # the tag show position
    x = np.around(x, decimals=2) # Keep 2 decimal places
    y = np.around(y, decimals=2)
    x_str = np.array(x).astype(str)
    y_str = np.array(y).astype(str)
    l1, = plt.plot(x, y) # l1 show the x_ticks, y_ticks
    l1.remove() #hide the l1
    #l2, = plt.plot(x, y2,color='red',linewidth=1.0,linestyle='--',label='square line')
    #plt.legend(handles=[l1, l2], labels=['up', 'down'], loc='upper right')
    annot.set_visible(False) # mouse not display the information when not pointing
    plt.grid()

    startx=0
    starty=0
    mPress=False
    fig.canvas.mpl_connect('scroll_event', lambda event: call_scroll(event, fig)) # Event mouse wheel
    fig.canvas.mpl_connect('button_press_event', lambda event: call_move(event, fig)) # Event mouse button press
    fig.canvas.mpl_connect('button_release_event', lambda event: call_move(event, fig)) # Event mouse button release
    #fig.canvas.mpl_connect('draw_event', call_move) # Event draw figure
    fig.canvas.mpl_connect('motion_notify_event', lambda event: call_move(event, fig)) # Event mouse move
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, l1, annot, ax, x_str, y_str, fig))
    SetFigSize(ax, x, y) # Set the starting figsize，ax is the canvas
    plt.show()
    



if __name__ == "__main__":
    print("Hello Python")
 





   




