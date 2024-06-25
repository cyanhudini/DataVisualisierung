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
        self.imported_headers = []
        self.plot_data = []
        self.window.geometry("2500x1300") 
        self.coloumn_counter=1
        # self.export_button = Button(master = self.window,command = self.export_plot,height = 2,width = 10,text = "Export")
        self.plot_button = Button(master = self.window,command = self.plot,height = 2,width = 10,text = "Plot").grid(row=0, column=1)
        self.upload_button = Button(master = self.window,command = self.upload_dataset, height = 2, width = 10, text = "Upload").grid(row=0, column=2)
        self.clear_button = Button(master = self.window, command = self.clear, height = 2, width = 10, text = "clear").grid(row=0, column=3)
        self.clear_all_button = Button(master = self.window, command = self.clear_all, height = 2, width = 10, text = "clear all", background = "red").grid(row=0, column=4)
        self.add_sec_y_axis_button = Button(master = self.window, command = self.add_sec_y_axis, height = 2, width = 10, text = "Add 2nd Y Axis").grid(row=0, column=self.coloumn_counter)
        self.add_sec_x_axis_button = Button(master = self.window, command = self.add_sec_x_axis, height = 2, width = 10, text = "X Axis").grid(row=0, column=self.coloumn_counter)
        #self.dropdown_x1 = []
        #self.dropdown_y1 = []
        self.selected_x = StringVar()
        self.selected_y1 = StringVar()
        self.selected_y2 = StringVar()
        self.selected_x2 = StringVar()
        
        #self.plot_button.pack() 
        #self.upload_button.pack()
        #self.clear_all_button.pack()
        #self.clear_button.pack()
        #self.add_sec_y_axis_button.pack()
        #self.add_sec_x_axis_button.pack()
        #self.export_button.pack(   )
        
        
    
    
    def generate_data_and_plot(self):
        
        clear()
        for _ in range(50):
            to_export_data.append((random.randint(0,100) ,random.randint(0, 100)))
        plot(to_export_data)

    def add_sec_y_axis(self):
        self.coloumn_counter+=1
        self.dropdown_y2 = OptionMenu(self.window, self.selected_y2, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        #self.dropdown_y2.pack()
        
    def add_sec_x_axis(self):
        self.coloumn_counter+=1
        self.dropdown_x2 = OptionMenu(self.window, self.selected_x2, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        #self.dropdown_x2.pack()


    def plot(self): 
        self.clear()
        if not self.selected_x or not self.selected_y1:
            print("Bitte wählen Sie die Achsen")
            return
        
        mplcursors.cursor(hover=True)
        #x_index = self.imported_headers.index(self.selected_x.get())
        #y1_index = self.imported_headers.index(self.selected_y1.get())
        #sorted_plot_data = sorted(self.plot_data, key = lambda x1: x[x_index])
        #self.figure = Figure(figsize = (5, 5), dpi = 100)
        #self.x1 = [point[x_index] for point in sorted_plot_data]
        self.x1 = (self.csv_df[self.selected_x.get()]).sort_values()
        
        y1 = (self.csv_df[self.selected_y1.get()]).sort_values()
        #y1 = [point[y1_index] for point in sorted_plot_data]
        
        self.fig, self.ax1 = plt.subplots()
        self.ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
        
        plt.xticks(rotation=35, ha='right')  
        self.ax1.plot(self.x1, y1)
        
        if len(self.selected_y2.get()) > 0:
            y2 = (self.csv_df[self.selected_y2.get()]).sort_values()
            self.ax2 = self.ax1.twinx()
            self.ax2.plot(self.x1, y2)
        if len(self.selected_x2.get()) > 0:
            x2 = (self.csv_df[self.selected_x2.get()]).sort_values()
            plt.xticks(self.x1, x2, rotation=45, ha='right')
        
        
        
        self.fig.set_size_inches(115,80)
        self.canvas = FigureCanvasTkAgg(self.fig,master = self.window)   
        self.canvas.draw() 
        tk_widget = self.canvas.get_tk_widget()
        self.canvas.get_tk_widget().pack() 
        

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
                print(self.plot_data)
        self.csv_df = pd.read_csv(csv_file)
                
        self.dropdown_x1 = OptionMenu(self.window, self.selected_x, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        self.dropdown_y1 = OptionMenu(self.window, self.selected_y1, *self.imported_headers).grid(row=1, column=self.coloumn_counter)
        #self.dropdown_x1.pack()
        #self.dropdown_y1.pack()


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
        
        if self.canvas:
            self.canvas.get_tk_widget().forget()
            canvas = None
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
        
        if hasattr(self, 'dropdown_x1'):
            self.dropdown_x1.destroy()
        if hasattr(self, 'dropdown_y1'):
            self.dropdown_y1.destroy()
        
        # if dropdown_y2 exists, destroy it
        if hasattr(self, 'dropdown_y2'):
            self.dropdown_y2.destroy()
        if hasattr(self, 'dropdown_x2'):
            self.dropdown_x2.destroy()
        

if __name__ == "__main__":
    vis = DataVisualisation()
    vis.window.mainloop()