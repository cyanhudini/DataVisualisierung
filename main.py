from tkinter import * 
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import random
from tkinter import filedialog
import csv
import mpldatacursor
import mplcursors
import pandas as pd

class DataVisualisation:
    def __init__(self):
        self.to_export_data = []
        self.canvas = None
        self.window = Tk() 
        self.window.title('Data Visualisierung')
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.imported_headers = []
        self.plot_data = []
        self.window_width = 2500
        self.window_height = 1300
        self.window.geometry("2500x1300") 
        self.coloumn_counter=0
        self.internal_y_counter = 0
        
        
        self.tooltip = mplcursors.cursor(hover=True)
        # top und bottom frame
        self.top_frame = Frame(self.window, width=self.window_width, height=100)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame = Frame(self.window, width=self.window_width, height=1200 )
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        
        # frames für buttons und graph in top und bottom frame
        self.button_bar_frame = Frame(self.top_frame, name="button_bar_frame")
        self.button_bar_frame.grid(row=0, column=0, )
        self.graph_frame = Frame(self.bottom_frame, bg="grey", name="graph_frame")
        self.graph_frame.grid(row=0, column=0, sticky="nsew")
        
        # buttons
        self.plot_button = Button(master = self.button_bar_frame,command = self.plot,height = 2,width = 10,text = "Plot").grid(row=0, column=0)
        self.upload_button = Button(master = self.button_bar_frame,command = self.upload_dataset, height = 2, width = 10, text = "Upload").grid(row=0, column=1)
        self.clear_button = Button(master = self.button_bar_frame, command = self.clear, height = 2, width = 10, text = "clear").grid(row=0, column=2)
        self.clear_all_button = Button(master = self.button_bar_frame, command = self.clear_all, height = 2, width = 10, text = "clear all", background = "red").grid(row=0, column=3)
        #self.add_sec_x_axis_button = Button(master = self.button_bar_frame, command = self.add_sec_x_axis, height = 2, width = 10, text = "2. X Axis").grid(row=0, column=4)
        #self.add_sec_y_axis_button = Button(master = self.button_bar_frame, command = self.add_sec_y_axis, height = 2, width = 10, text = "2. Y Axis").grid(row=0, column=5)
        self.add_sec_axis_button = Button(master = self.button_bar_frame, command = self.add_sec_axis, height = 2, width = 10, text = "2. Achse").grid(row=0, column=5)
        #self.add_sec_y_axis_button = Button(master = self.button_bar_frame, command = self.add_more_y_against_x1, height = 2, width = 10, text = "X(Y)").grid(row=0, column=5)
        
        self.selected_x = StringVar()
        self.selected_y1 = StringVar()
        self.selected_y2 = StringVar()
        self.selected_x2 = StringVar()
        
    
    
    def generate_data_and_plot(self):
        
        clear()
        for _ in range(50):
            to_export_data.append((random.randint(0,100) ,random.randint(0, 100)))
        plot(to_export_data)
    
    def add_sec_axis(self):
        self.dropdown_x2 = OptionMenu(self.button_bar_frame, self.selected_x2, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        self.coloumn_counter+=1
        
        self.x2_label = Label(master = self.button_bar_frame, text = "2nd X-Achse").grid(row=1, column=self.coloumn_counter)
        self.coloumn_counter+=1
        
        self.dropdown_y2 = OptionMenu(self.button_bar_frame, self.selected_y2, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        self.coloumn_counter+=1
        
        self.y2_label = Label(master = self.button_bar_frame, text = "2nd Y-Achse").grid(row=1, column=self.coloumn_counter)
        self.coloumn_counter+=1
        
    # eigentlich nur eine Abkürzung für add_sec_axis
    def add_more_y_against_x1(self):
        
        self.internal_y_counter+=1
        self.dropdown_y = OptionMenu(self.button_bar_frame, (lambda: self.selected_add_y), *self.imported_headers).grid(row=1, column=self.coloumn_counter)


    def plot(self): 
        self.clear()
        if not self.selected_x or not self.selected_y1:
            print("Bitte wählen Sie die Achsen")
            return
        
        
        #x_index = self.imported_headers.index(self.selected_x.get())
        #y1_index = self.imported_headers.index(self.selected_y1.get())
        #sorted_plot_data = sorted(self.plot_data, key = lambda x1: x[x_index])
        #self.figure = Figure(figsize = (5, 5), dpi = 100)
        #self.x1 = [point[x_index] for point in sorted_plot_data]
        self.x1 = (self.csv_df[self.selected_x.get()])
        
        y1 = (self.csv_df[self.selected_y1.get()])
        #y1 = [point[y1_index] for point in sorted_plot_data]
        
        self.fig, self.ax1 = plt.subplots()
        self.ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
        
        plt.xticks(rotation=35, ha='right')  
        self.ax1.plot(self.x1, y1,"-r", label="ax1")
        
        if len(self.selected_y2.get()) > 0:
            y2 = (self.csv_df[self.selected_y2.get()])
            self.ax2 = self.ax1.twinx()
            self.ax2.plot(self.x1, y2,"-b" ,label="ax2")
        if len(self.selected_x2.get()) > 0:
            x2 = (self.csv_df[self.selected_x2.get()])
            plt.xticks(self.x1, x2, rotation=45, ha='right')
        
        
        plt.legend()
        self.fig.set_size_inches(115,80)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)   
        self.canvas.draw() 
        tk_widget = self.canvas.get_tk_widget()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        print("plot")
        

    def upload_dataset(self):
        self.clear_all()
        print("upload")
        
        csv_file = filedialog.askopenfilename(
            title = "Wähle eine hochzuladene CSV Datei",
            filetypes = (("CSV Files", "*.csv"),)
        )
        if csv_file:
            with(open(csv_file, "r")) as file:
                
                csv_reader = csv.reader(file)
                self.imported_headers = next(csv_reader) 
                
                for row in csv_reader:
                    int_row = [(item) for item in row]
                    self.plot_data.append(row)
                # print(self.plot_data)
        self.csv_df = pd.read_csv(csv_file)
                
        self.dropdown_x1 = OptionMenu(self.button_bar_frame, self.selected_x, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        #internal_x1_coloumn_counter = self.coloumn_counter +1
        
        self.x1_label = Label(master = self.button_bar_frame, text = "X-Achse").grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        
        self.dropdown_y1 = OptionMenu(self.button_bar_frame, self.selected_y1, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        
        self.y1_label = Label(master = self.button_bar_frame, text = "X(Y1)-Achse").grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1



    def export_plot(self):
        
        if len(to_export_data) == 0:
            print("Nichts zu exportieren")
        else:
            with open('export.csv', 'w', newline='') as csvfile:
        
                writer = csv.writer(csvfile)

                writer.writerow(['x', 'y'])
                
                for row in to_export_data:
                    writer.writerow(row)
        
    def clear(self):
        print("clear")

        if self.canvas:
            for child in self.graph_frame.winfo_children():
                if isinstance(child, Canvas):
                    child.destroy()
                    print("deleted")
        
        # also clear selected_x and selected_y
        #self.selected_x.set("")
        #self.selected_y1.set("")
        #if hasattr(self, 'dropdown_y2'):
        #    self.selected_y2.set("")
        #    self.dropdown_y2.destroy()
        #if hasattr(self, 'dropdown_x2'):
        #    self.selected_x2.set("")
        #    self.dropdown_x2.destroy()
            
    def clear_all(self):

        self.clear()
        
        self.imported_headers = []
        self.plot_data = []
        for child in self.button_bar_frame.winfo_children():
            if isinstance(child, OptionMenu):
                child.destroy()
            if isinstance(child, Label):
                child.destroy()
        self.coloumn_counter = 0
        

if __name__ == "__main__":
    vis = DataVisualisation()
    vis.window.mainloop()