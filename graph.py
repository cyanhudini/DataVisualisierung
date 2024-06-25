import tkinter
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import random
from tkinter import filedialog
import csv
import numpy as np
import mpldatacursor
import mplcursors

root = tkinter.Tk()
root.title('Data Visualisierung')
random_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18]
more = [5,3,2,1,7,86,43,22,6,4,2334,56,3,2,453,65,234,346]
no = [2,512,7,1,78,3,92,2,6,53, 12,89,45,28,10,15,31,33]
x1 = np.linspace(0, 10, 100)
x2 = np.linspace(0, 20, 100)
y = np.cos(x1)

t = np.arange(0, 3, .01)
s = np.arange(0, 3, .01)
u = np.arange(0, 3, .01)
second = ["a", "b", "c", "d", "e", "f", "g"]
f = np.arange(7)
y = np.arange(7)

fig, ax = plt.subplots()
#l, = ax1.plot(x, y, label="")
plt.xticks(second, f)
ax.plot(f, y, label="cos")
ax.xaxis.set_major_locator(plt.MaxNLocator(100))
#ax2 = ax1.twinx()
#ax2.plot(x, z)
#mplcursors.cursor(hover=True)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)



def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.