from tkinter import * 
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import random
from tkinter import filedialog
import csv

imported_headers = []


def generate_data_and_plot():
    global to_export_data
    clear()
    for _ in range(50):
        to_export_data.append((random.randint(0,100) ,random.randint(0, 100)))
    plot(to_export_data)

def plot(plot_data): 
    global canvas
    
    x = [point[0] for point in plot_data]
    y = [point[1] for point in plot_data]
    fig, ax = plt.subplots() 
    ax.plot(x, y, 'o')

    canvas = FigureCanvasTkAgg(fig,master = window)   
    print(to_export_data)
    canvas.draw() 
    tk_widget = canvas.get_tk_widget()
    canvas.get_tk_widget().pack() 

def upload_dataset():
    clear()
    print("upload")
    
    csv_file = filedialog.askopenfilename(
        title = "Wähle eine hochzuladene CSV Datei",
        filetypes = (("CSV Files", "*.csv"),)
    )
    if csv_file:
        with(open(csv_file, "r")) as file:
            
            csv_reader = csv.reader(file)
            header = []
            header = next(csv_reader) 
            plot_data = []
            for row in csv_reader:
                int_row = [int(item) for item in row]
                plot_data.append(row)
            print(plot_data)
            
    plot(plot_data)


def export_plot():
    global to_export_data
    if len(to_export_data) == 0:
        print("Nichts zu exportieren")
    else:
        with open('export.csv', 'w', newline='') as csvfile:
    
            writer = csv.writer(csvfile)

            writer.writerow(['x', 'y'])
            
            for row in to_export_data:
                writer.writerow(row)
    
    
def clear():
    global canvas, to_export_data
    if canvas:
        canvas.get_tk_widget().forget()
    to_export_data.clear() 
    canvas = None

to_export_data = []
canvas = None

window = Tk() 
window.title('Data Visualisierung') 

window.geometry("500x500") 
export_button = Button(master = window,command = export_plot,height = 2,width = 10,text = "Export")
plot_button = Button(master = window,command = generate_data_and_plot,height = 2,width = 10,text = "Plot") 
upload_button = Button(master = window,command = upload_dataset, height = 2, width = 10, text = "Upload")
clear_button = Button(master = window, command = clear, height = 2, width = 10, text = "clear", background = "red")


plot_button.pack() 
upload_button.pack()
clear_button.pack()
export_button.pack()


window.mainloop() 