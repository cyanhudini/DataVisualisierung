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
            
        # label text comapre button
        self.compare_button_text = StringVar(value="Compare")
        # flag to indicate which text to display
        self.compare_flag = 1
        
        self.var_list_menu_button_x = {}
        self.var_list_menu_button_y = {}
        self.var_list_menu_button_id = {}
        self.selected_options_menu_x = []
        self.selected_options_menu_y = []
        self.selected_options_menu_ids = []
        
        self.identical_coloumns_to_display = []
        
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
        #self.add_more_axis_button = Button(master = self.button_bar_frame, command = self.add_more_axis, height = 2, width = 10, text = "Add Axis").grid(row=0, column=5)
        
    
        self.to_compare_runs_button = Button(master = self.button_bar_frame, command = self.switch_compare_scope, height = 2, width = 10, text = self.compare_button_text.get())
        self.to_compare_runs_button.grid(row=0, column=7)
        
    
    def add_menu_buttons(self):
        
        ### Run Ids
        self.menu_button_ids = Menubutton(self.button_bar_frame, text="Run IDs  ", relief=RAISED)
        
        self.menu_ids = Menu(self.menu_button_ids, tearoff=0)
        
        self.menu_button_ids.config(menu=self.menu_ids)
        
        for option in self.used_headers_x:
            variable = BooleanVar()
            self.var_list_menu_button_id[option] = variable
            
            self.menu_ids.add_checkbutton(label=option, variable=variable ,command = lambda  value=option: self.update_selection("menu_ids", value))
        self.menu_button_ids.grid(row=0, column=8)
        
        #### X
        self.menu_button_x = Menubutton(self.button_bar_frame, text="X  ", relief=RAISED)
        
        self.menu_x = Menu(self.menu_button_x, tearoff=0)
        
        self.menu_button_x.config(menu=self.menu_x)
        
        for option in self.global_compare_headers:
            variable = BooleanVar()
            self.var_list_menu_button_x[option] = variable
            
            self.menu_x.add_checkbutton(label=option, variable=variable, command = lambda  value=option: self.update_selection("menu_x", value))
        self.menu_button_x.grid(row=0, column=9)
        
        
        ### Y
        self.menu_button_y = Menubutton(self.button_bar_frame, text="Y  ", relief=RAISED)
        
        self.menu_y = Menu(self.menu_button_y, tearoff=0)
        
        self.menu_button_y.config(menu=self.menu_y)
        
        for option in self.global_compare_headers:
            variable = BooleanVar()
            self.var_list_menu_button_y[option] = variable
            
            self.menu_y.add_checkbutton(label=option, variable=variable, command = lambda value=option : self.update_selection("menu_y", value))
        self.menu_button_y.grid(row=0, column=10)
        
        
    def update_selection(self, which_menu, value):
    
        # hier versuche ich mutual exclusivity herzustellen
        # 1 . wenn ich in x mehr als eine Option auswähle, kann ich nur eine Option in y wählen
        if which_menu == "menu_ids":
            self.selected_options_menu_ids = [option for option, var in self.var_list_menu_button_id.items() if var.get()]
            
        if which_menu == "menu_x":
            if len(self.selected_options_menu_x) >= len(self.selected_options_menu_y) and len(self.selected_options_menu_x) >= 1:
                self.selected_options_menu_x = [option for option, var in self.var_list_menu_button_x.items() if var.get()]
            else:
                self.selected_options_menu_x.clear()
                self.selected_options_menu_x.append(value)
        else:
            if len(self.selected_options_menu_y) >= len(self.selected_options_menu_x) and len(self.selected_options_menu_y) >= 1:
                self.selected_options_menu_y = [option for option, var in self.var_list_menu_button_y.items() if var.get()]
            else:
                print("clear y")
                self.selected_options_menu_y.clear()
                self.selected_options_menu_y.append(value)
        print(self.selected_options_menu_x)
        print(self.selected_options_menu_y)
     
     
    def switch_compare_scope(self):
        if self.compare_flag == 0:
            self.compare_flag = 1
            self.compare_button_text.set("Compare")
        else:
            self.used_headers_x = []
            self.used_headers_x = self.grouped_run_trace_ids
            self.change_optionsmenu_options()
            self.insert_options()
            
    def insert_options(self):
        for options in self.used_headers_x:
            self.multiple_selection_button_x.insert(END, options)
            
            
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
    
    def group_coloumn_data_by_identical_values(self, df):
        for coloumn in filtered_data:
            # iterate over all coloumns
            # then check whether the values in the rwos are each identical or not
            # if yes, put the name of the coloumn in the list of grouped_data
            
            if len(filtered_data[coloumn].value_counts()) <= 1:
                self.identical_coloumns_to_display.append(coloumn)
    
    def group_generic_data(self, filtered_data):
        print(filteregrouped_datad_data)
        for coloumn in filtered_data:
            # iterate over all coloumns
            # then check whether the values in the rwos are each identical or not
            # if yes, put the name of the coloumn in the list of grouped_data
            
            if len(filtered_data[coloumn].value_counts()) <= 1:
                self.identical_coloumns_to_display.append(coloumn)
        print(self.identical_coloumns_to_display)
        
    
    def plot(self): 
        self.clear()
        if not self.selected_options_menu_x or not self.selected_options_menu_y or not self.selected_options_menu_ids:
            print("Bitte wählen Sie die Achsen")
            return
        self.fig, self.ax1 = plt.subplots()
        self.ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
        for run_id in self.selected_options_menu_ids:
            filtered_data = self.csv_df[self.csv_df['name'] == run_id]
            self.group_generic_data(filtered_data)
            for x in self.selected_options_menu_x:
                x_data = (filtered_data[x])
                x_sorted = x_data.sort_values()
                print(x_data)
                for y in self.selected_options_menu_y:
                    y_data = (filtered_data[y])
                    y_sorted = y_data.sort_values()
                    
                    print(y_data)
                    self.ax1.plot(range(len(x_data)), y_data, "-r", label=run_id)

        mplcursors.cursor(hover=True)
        
        '''
        for x 
        '''
        
        
        plt.xticks(rotation=35, ha='right') 

        #plt.autoscale()
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
                 # beim upload sind die ersten options die globalen headers
                for row in csv_reader:
                    int_row = [(item) for item in row]
                    self.plot_data.append(row)
        
        to_group = self.csv_df["name"] # name ist hier die run_id, in der spalte "name"
        # self.group_coloumn_data_by_identical_values(self.csv_df, "name")
        for i in to_group:
                if i not in self.grouped_run_trace_ids:
                    print(i)
                    self.grouped_run_trace_ids.append(i)
        self.used_headers_x = self.grouped_run_trace_ids
        self.add_menu_buttons()
        
    def clear(self):
        print("clear")
        self.compare_flag = 1

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