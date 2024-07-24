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
        self.grouped_run_trace_ids = [] # gruppierte daten von von traces in jeweils einem run zum vergleichen
        self.window_width = 2500
        self.window_height = 1300
        self.window.geometry("2500x1300") 
        self.coloumn_counter=0        
        
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
        #self.add_sec_axis_button = Button(master = self.button_bar_frame, command = self.add_sec_axis, height = 2, width = 10, text = "2. Achse").grid(row=0, column=5)
        self.add_sec_y_axis_button = Button(master = self.button_bar_frame, command = self.add_more_y_against_x1, height = 2, width = 10, text = "X(Y_c)").grid(row=0, column=5)
        self.to_compare_runs = Button(master = self.button_bar_frame, command = self.compare_runs, height = 2, width = 10, text = "Compare").grid(row=0, column=6)
        self.to_switch_comparison_scope = Button(master = self.button_bar_frame, command = self.switch_between_global_compare_and_single_runs, height = 2, width = 10, text = "Switch").grid(row=0, column=7)
        
        self.selected_x = StringVar()
        self.selected_y1 = StringVar()
        self.selected_ys = []
    # TODO: switch_between_global_compare_and_single_runs, re-import headers von csv_df/csv file
    
    
    def compare_runs(self):
        # coloumns werden "gruppiert" indem duplikate entfernt werden
        print("compare" )
        to_group = self.csv_df["name"]
        for i in to_group:
            if i not in self.grouped_run_trace_ids:
                print(i)
                self.grouped_run_trace_ids.append(i)
    
    def switch_between_global_compare_and_single_runs(self):
        self.clear_all()
        pass
    
    def import_headers_from_csv(self):
        
    def add_more_y_against_x1(self):
        selected_y = StringVar()
        self.dropdown_y = OptionMenu(self.button_bar_frame, selected_y , *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        self.selected_ys.append(selected_y)
        self.coloumn_counter+=1
    
    def plot(self): 
        self.clear()
        if not self.selected_x or not self.selected_y1:
            print("Bitte wählen Sie die Achsen")
            return
        
       
        x1 = (self.csv_df[self.selected_x.get()])
        #y1 = (self.csv_df[self.selected_y1.get()])
        self.fig, self.ax1 = plt.subplots()
        self.ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
        
        plt.xticks(rotation=35, ha='right')  
        for y in self.selected_ys:
            y = (self.csv_df[y.get()])
            self.ax1.plot(x1, y,"-r", label="ax1")
       
        
        plt.legend()
        self.fig.set_size_inches(25,11.5)
        self.canvas = FigureCanvasTkAgg(self.fig, master =self.graph_frame)
        self.canvas.draw()
        #self.canvas.get_tk_widget()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        

    def upload_dataset(self):
        self.clear_all()
        print("upload")
        
        csv_file = filedialog.askopenfilename(
            title = "Wähle eine hochzuladene CSV Datei",
            filetypes = (("CSV Files", "*.csv"),)
        )
        self.csv_df = pd.read_csv(csv_file)
        if csv_file:
            with(open(csv_file, "r")) as file:
                
                csv_reader = csv.reader(file)
                self.imported_headers = next(csv_reader) 
                                
                for row in csv_reader:
                    int_row = [(item) for item in row]
                    self.plot_data.append(row)
        
        self.compare_runs()
        self.dropdown_x1 = OptionMenu(self.button_bar_frame, self.selected_x, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        #internal_x1_coloumn_counter = self.coloumn_counter +1
        
        self.x1_label = Label(master = self.button_bar_frame, text = "X-Achse").grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        
        self.dropdown_y1 = OptionMenu(self.button_bar_frame, self.selected_y1, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        self.selected_ys.append(self.selected_y1)
        
        self.coloumn_counter+=1
        
        self.y1_label = Label(master = self.button_bar_frame, text = "X(Y1)-Achse").grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        
    def clear(self):
        print("clear")

        if self.canvas:
            for child in self.graph_frame.winfo_children():
                if isinstance(child, Canvas):
                    child.destroy()
       
            
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