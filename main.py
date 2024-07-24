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
        self.global_compare_headers = []
        self.grouped_run_trace_ids = [] # gruppierte daten von von traces in jeweils einem run zum vergleichen
        self.used_headers_x = []
        self.plot_data = []
        self.window_width = 2500
        self.window_height = 1300
        self.window.geometry("2500x1300") 
        self.coloumn_counter=0        
            
        self.selected_x1 = StringVar()
        self.selected_x2 = StringVar()
        self.selected_y1 = StringVar()
        self.selected_ys = []
        # label text comapre button
        self.compare_button_text = StringVar(value="Compare")
        # flag to indicate which text to display
        self.compare_flag = 1
        
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
        self.plot_button = Button(master = self.button_bar_frame,command = self.plot,height = 2,width = 10,text = "Plot")
        self.plot_button.grid(row=0, column=0)
        self.upload_button = Button(master = self.button_bar_frame,command = self.upload_dataset, height = 2, width = 10, text = "Upload")
        self.upload_button.grid(row=0, column=1)
        self.clear_button = Button(master = self.button_bar_frame, command = self.clear, height = 2, width = 10, text = "clear")
        self.clear_button.grid(row=0, column=2)
        self.clear_all_button = Button(master = self.button_bar_frame, command = self.clear_all, height = 2, width = 10, text = "clear all", background = "red")
        self.clear_all_button.grid(row=0, column=3)
        #self.add_sec_axis_button = Button(master = self.button_bar_frame, command = self.add_sec_axis, height = 2, width = 10, text = "2. Achse").grid(row=0, column=5)
        self.add_more_axis_button = Button(master = self.button_bar_frame, command = self.add_more_axis, height = 2, width = 10, text = "Add Axis").grid(row=0, column=5)
        self.to_compare_runs_button = Button(master = self.button_bar_frame, command = self.switch_compare_scope, height = 2, width = 10, text = self.compare_button_text.get())
        self.to_compare_runs_button.grid(row=0, column=6)
        
        
        
        
    # TODO: switch_between_global_compare_and_single_runs, re-import headers von csv_df/csv file
    
    
    def switch_compare_scope(self):
        
        print("compare")
        self.clear()
        if self.compare_flag == 0:
            self.used_headers_x = []
            self.used_headers_x = self.global_compare_headers
            self.change_optionsmenu_options()
            self.compare_button_text.set("Compare")
            self.to_compare_runs_button.config(text=self.compare_button_text.get())
            self.compare_flag = 1

        else:
            self.used_headers_x = []
            self.used_headers_x = self.grouped_run_trace_ids
            self.change_optionsmenu_options()
            self.compare_button_text.set("Global")
            self.to_compare_runs_button.config(text=self.compare_button_text.get())
            self.x1_label.config(text="Run ID")
            self.dropdown_x2_for_run_compare = OptionMenu(self.button_bar_frame, self.selected_x2, *self.global_compare_headers)
            self.dropdown_x2_for_run_compare.grid(row=1, column=self.coloumn_counter)
            self.coloumn_counter+=1
            self.dropdown_x2_label = Label(master = self.button_bar_frame, text = "X-Achse")
            self.dropdown_x2_label.grid(row=1, column=self.coloumn_counter+1)
            self.coloumn_counter+=1
            self.compare_flag = 0
            
            
    def change_optionsmenu_options(self):
        menu = self.dropdown_x1["menu"]
        menu.delete(0, "end")
        for child in self.button_bar_frame.winfo_children():
            if isinstance(child, OptionMenu):
                for options in self.used_headers_x:
                    menu.add_command(label=options, command=lambda value=options: self.selected_x1.set(value))
    
    def add_more_axis(self):
        selected_y = StringVar()
        selected_x1 = StringVar()
        
        dropdown_x = OptionMenu(self.button_bar_frame, selected_x1 , *self.used_headers_x)
        dropdown_x.grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        
        dropdown_y = OptionMenu(self.button_bar_frame, selected_y , *self.global_compare_headers)
        dropdown_y.grid(row=1, column=self.coloumn_counter)
        self.selected_ys.append(selected_y)
        self.coloumn_counter+=1
    
    def plot(self): 
        self.clear()
        if not self.selected_x1 or not self.selected_y1:
            print("Bitte wählen Sie die Achsen")
            return
        
       
        
        self.fig, self.ax1 = plt.subplots()
        self.ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
        
        if self.compare_flag == 1:
            filtered_data = self.csv_df[self.csv_df['name'] == self.selected_x1.get()]
            x = (filtered_data[self.selected_x2.get()])
            print(x.to_list())
            print(self.selected_x1.get())
            
            y = pd.to_numeric(filtered_data[self.selected_y1.get()])
            self.ax1.plot(x, y,"-r", label="ax1")
        
        else:
            x1 = (self.csv_df[self.selected_x1.get()])
            #y1 = (self.csv_df[self.selected_y1.get()])
            for y in self.selected_ys:
                y = (self.csv_df[y.get()])
                self.ax1.plot(x1, y,"-r", label="ax1")
        plt.xticks(rotation=35, ha='right') 
       
        
        plt.legend()
        self.fig.set_size_inches(20,9.5)
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
                self.global_compare_headers = next(csv_reader)
                self.used_headers_x = self.global_compare_headers
                for row in csv_reader:
                    int_row = [(item) for item in row]
                    self.plot_data.append(row)
        
        to_group = self.csv_df["name"]
        for i in to_group:
                if i not in self.grouped_run_trace_ids:
                    print(i)
                    self.grouped_run_trace_ids.append(i)
        
        #self.compare_runs()
        self.dropdown_x1 = OptionMenu(self.button_bar_frame, self.selected_x1, *self.used_headers_x)
        self.dropdown_x1.grid(row=1, column=self.coloumn_counter)
        self.coloumn_counter+=1
        #internal_x1_coloumn_counter = self.coloumn_counter +1
        
        self.x1_label = Label(master = self.button_bar_frame, text = "X-Achse")
        self.x1_label.grid(row=1, column=self.coloumn_counter)
        self.coloumn_counter+=1
        
        self.dropdown_y1 = OptionMenu(self.button_bar_frame, self.selected_y1, *self.used_headers_x)
        self.dropdown_y1.grid(row=1, column=self.coloumn_counter)
        
        self.selected_ys.append(self.selected_y1)
        
        self.coloumn_counter+=1
        
        self.y1_label = Label(master = self.button_bar_frame, text = "Y-Achse")
        self.y1_label.grid(row=1, column=self.coloumn_counter)
        
        self.coloumn_counter+=1
        
    def clear(self):
        print("clear")
        self.compare_flag = 1
        self.selected_ys = []
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