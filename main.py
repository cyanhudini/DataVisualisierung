from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
        self.coloumn_counter=1     
        self.row_counter_data_table = 0
        # label text comapre button
        self.compare_button_text = StringVar(value="Compare")
        # flag to indicate which text to display
        self.compare_flag = 1
        
        self.var_list_menu_button_x = {}
        self.var_list_menu_button_y = {}
        self.var_list_menu_button_y_plot_grouped = {}
        self.var_list_menu_button_id = {}
        self.selected_options_menu_x = []
        self.selected_options_menu_y = []
        self.selected_options_menu_y_plot_grouped = []
        self.selected_options_menu_ids = []
        
        self.identical_coloumns_to_display = []
        
        self.tooltip = mplcursors.cursor(hover=True)
        # top und bottom frame
        self.top_frame = Frame(self.window, width=self.window_width)
        self.top_frame.grid(row=0, column=0, )
        self.middle_frame = Frame(self.window,bg="grey", width=self.window_width)
        self.middle_frame.grid(row=1, column=0, )
        self.bottom_frame = Frame(self.window, width=self.window_width)
        self.bottom_frame.grid(row=2, column=0)
        
        self.top_frame.grid_rowconfigure(0, weight=0)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        
        # frames für buttons und graph in top und bottom frame
        self.button_bar_frame = Frame(self.top_frame, name="button_bar_frame")
        self.button_bar_frame.grid(row=0, column=0)
        self.graph_frame = Frame(self.middle_frame, name="graph_frame")
        self.graph_frame.grid(row=0, column=0)
        self.data_table_frame = Frame(self.bottom_frame, name="data_table_frame")
        self.data_table_frame.grid(row=0, column=0)
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
        
        
    
    def add_menu_buttons(self):
        
        ### Run Ids
        self.menu_button_ids = Menubutton(self.button_bar_frame, text="X ", relief=RAISED)
        
        self.menu_ids = Menu(self.menu_button_ids, tearoff=0)
        
        self.menu_button_ids.config(menu=self.menu_ids)
        
        for option in self.grouped_run_trace_ids:
            variable = BooleanVar()
            self.var_list_menu_button_x[option] = variable
            
            self.menu_ids.add_checkbutton(label=option, variable=variable, command = lambda value=option, variable=variable : self.update_selection("menu_x", value, variable))
        self.menu_button_ids.grid(row=0, column=8)
        
        
        ### Y
        self.menu_button_y = Menubutton(self.button_bar_frame, text="Y  ", relief=RAISED)
        
        self.menu_y = Menu(self.menu_button_y, tearoff=0)
        
        self.menu_button_y.config(menu=self.menu_y)
        
        for option in self.global_compare_headers:
            variable = BooleanVar()
            self.var_list_menu_button_y[option] = variable
            self.menu_y.add_checkbutton(label=option, variable=variable, command = lambda value=option, variable=variable : self.update_selection("menu_y", value, variable))
        self.menu_button_y.grid(row=0, column=9)
        
        
        ### Y die zusammen geplotted werden sollen
        self.menu_button_y_plot_grouped = Menubutton(self.button_bar_frame, text="Grouped Y ", relief=RAISED)
        
        self.menu_y_plot_grouped = Menu(self.menu_button_y_plot_grouped, tearoff=0)
        
        self.menu_button_y_plot_grouped.config(menu=self.menu_y_plot_grouped)
        
        for option in self.global_compare_headers:
            variable = BooleanVar()
            print(variable.get())
            self.var_list_menu_button_y_plot_grouped[option] = variable
            self.menu_y_plot_grouped.add_checkbutton(label=option, variable=variable, command = lambda value=option, variable=variable : self.update_selection("menu_y_plot_grouped", value, variable))
        self.menu_button_y_plot_grouped.grid(row=0, column=10)
        
        
    def update_selection(self, which_menu, value, variable):
    
        # hier versuche ich mutual exclusivity herzustellen
        # 1 . wenn ich in x mehr als eine Option auswähle, kann ich nur eine Option in y wählen
         
        if which_menu == "menu_x":
            
            selected_x = self.change_selected_options(self.selected_options_menu_x, self.selected_options_menu_y, variable, self.var_list_menu_button_x, value)
            selected_x = self.change_selected_options(self.selected_options_menu_x, self.selected_options_menu_y_plot_grouped, variable, self.var_list_menu_button_x, value)
            if (selected_x):
                self.selected_options_menu_x.append(selected_x)
                    #self.var_list_menu_button_x[value] = False
                
        elif which_menu == "menu_y_plot_grouped":
            self.change_selected_options(self.selected_options_menu_y_plot_grouped, self.selected_options_menu_x, variable, self.var_list_menu_button_y_plot_grouped, value)

        else:
            self.change_selected_options(self.selected_options_menu_y, self.selected_options_menu_x, variable, self.var_list_menu_button_y, value)
        print(self.selected_options_menu_x)
    
 
    
    def change_selected_options(self, selected_list_1, selected_list_2, bool_variable, var_list, value):
        if len(selected_list_1) >= len(selected_list_2) and len(selected_list_1) - len(selected_list_2) >= 0:
                selected_list_1 = [option for option, var in var_list.items() if var.get()]
                print(selected_list_1)
        else:
            for option in var_list:
                var_list[option].set(False)
            bool_variable.set(True)
            selected_list_1.clear()
            selected_list_1.append(value)
    
    def group_coloumn_data_by_identical_values(self, df, header_name):
        # gruppiere daten nach identischen werten in einer spalte
        grouped_data = []
        for i in df[header_name]:
                #if i not in grouped_data and i not null
                if i not in grouped_data and i == i:
                    grouped_data.append(i)
        return grouped_data
    
    def group_coloumn_where_values_identical(self, filtered_data):
        #print(filteregrouped_datad_data)
        identical_coloumns_to_display = []
        for coloumn in filtered_data:
            # packe alle header namen dessen spalten werte sich untereinander nicht unterscheiden in eine liste
            if len(filtered_data[coloumn].value_counts()) <= 1 and not filtered_data[coloumn].isnull().sum() > 0:
                identical_coloumns_to_display.append(coloumn)
        return identical_coloumns_to_display

        
    def display_identical_coloumns(self, filtered_data):
        # zeige die identischen spalten an
        print("display")
        coloumn_data = []
        coloumn_header = []
        identical_coloumns_to_display = self.group_coloumn_where_values_identical(filtered_data)
        
        for coloumn in identical_coloumns_to_display:
            print(coloumn)
            coloumn_data.append(self.group_coloumn_data_by_identical_values(filtered_data, coloumn))
            coloumn_header.append(coloumn)
        data_table = ttk.Treeview(self.data_table_frame, columns=identical_coloumns_to_display, show="headings", height=1)
        # insert coloumn_header as header
        for coloumn in coloumn_header:
            data_table.heading(coloumn, text=coloumn)
        data_table.insert("", "end", values=coloumn_data)
        
        data_table.grid(row=self.row_counter_data_table, column=0)
        self.row_counter_data_table =+ 1
    
    def check_for_numeric_data(self, coloumn_headers):

        for coloumn in coloumn_headers:
            if pd.to_numeric(self.csv_df[coloumn], errors="coerce").notnull().all():
                self.global_compare_headers.append(coloumn)
            else:
                pass
                
    
    def plot(self): 
        self.clear()
        if not self.grouped_run_trace_ids or not self.global_compare_headers:
            print("Bitte wählen Sie die Achsen")
            return
 
        self.fig, self.ax1 = plt.subplots(figsize=(12, 6))
        self.ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
        axis_counter=0
        
        for x in self.selected_options_menu_x:
            filtered_data = self.csv_df[self.csv_df['name'] == x]
            self.display_identical_coloumns(filtered_data)
            #filtered_data = self.group_coloumn_data_by_identical_values(self.csv_df, x)
            # da wir immer mit der run_id arbeiten, ist die run_id die x achse
            x_data = filtered_data['id']
            if self.selected_options_menu_y:
                for y in self.selected_options_menu_y:
                    # plot individual
                    print(y)
                    y_data = pd.to_numeric(filtered_data[y])
                
                    ax_y = self.ax1.twinx()
                    ax_y.spines['right'].set_position(('outward',50*axis_counter))
                    ax_y.spines['left'].set_visible(False)
                    ax_y.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
                    #ax_y.yaxis.set_major_locator(ticker.MultipleLocator(base=len(self.selected_options_menu_x*10)))
                    ax_y.set_ylabel(y)
                    axis_counter += 1
                    ax_y.plot(range(len(x_data)), y_data, label=y) 
                
            for y in self.selected_options_menu_y_plot_grouped:
                # plot grouped
                
                y_data = pd.to_numeric(filtered_data[y])
                self.ax1.plot(range(len(x_data)), y_data, label=x)
        
                
        self.bottom_frame.grid(pady=len(self.selected_options_menu_x)*15)       
        if not self.selected_options_menu_y_plot_grouped:
            self.ax1 = self.ax1.set_yticks([])
        
        mplcursors.cursor()
        plt.subplots_adjust(left=0.2, right=0.8, bottom=0.2, top=0.8)
        plt.xticks(rotation=35, ha='right')    
        plt.autoscale()
        plt.legend()
        #self.fig.set_size_inches(20,8)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
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
                #self.global_compare_headers = next(csv_reader)
                self.check_for_numeric_data(next(csv_reader))
                print(self.global_compare_headers)
                 # beim upload sind die ersten options die globalen headers
                for row in csv_reader:
                    int_row = [(item) for item in row]
                    self.plot_data.append(row)
        
        #to_group = self.csv_df["name"] # name ist hier die run_id, in der spalte "name"
        self.grouped_run_trace_ids = self.group_coloumn_data_by_identical_values(self.csv_df, "name")
        
        self.add_menu_buttons()
        
    def clear(self):
        print("clear")

        if self.canvas:
            for child in self.graph_frame.winfo_children():
                if isinstance(child, Canvas):
                    child.destroy()
            for child in self.data_table_frame.winfo_children():
                if isinstance(child, ttk.Treeview):
                    child.destroy()
    def clear_graph(self):
        if self.canvas:
            for child in self.graph_frame.winfo_children():
                if isinstance(child, Canvas):
                    child.destroy()
            
    def clear_all(self):
        self.identical_coloumns_to_display = []
        self.clear()
        self.plot_data = []
        self.var_list_menu_button_x = {}
        self.var_list_menu_button_y = {}
        self.var_list_menu_button_y_plot_grouped = {}
        self.var_list_menu_button_id = {}
        self.selected_options_menu_x = []
        self.selected_options_menu_y = []
        self.selected_options_menu_y_plot_grouped = []
        self.selected_options_menu_ids = []
        self.global_compare_headers = []
        for child in self.button_bar_frame.winfo_children():
            if isinstance(child, OptionMenu):
                child.destroy()
            if isinstance(child, Label):
                child.destroy()
            if isinstance(child, Menubutton):
                    child.destroy()
        
        self.coloumn_counter = 0
        

if __name__ == "__main__":
    vis = DataVisualisation()
    vis.window.mainloop()