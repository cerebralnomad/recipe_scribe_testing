#! /usr/bin/env python3

# Code to search recipe files based on a keyword
# and whether to search filenames or ingredients
# 
# This is sandbox code for eventual inclusion 
# into the GUI recipe creator program Recipe Scribe
#
# This code is currently being developed to send 
# the search results to the left pane of the 
# main window

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Listbox
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import filedialog
import re
import configparser
from os import path
import glob

root = tk.Tk()
width = int(root.winfo_screenwidth() / 1.9) # To start scaled based on display width
height = int(root.winfo_screenheight() / 1.2) # To start based on display height
#width = int(root.winfo_screenwidth())   # To start fullscreen
#height = int(root.winfo_screenheight()) # To Start fullscreen
root.geometry('%sx%s' % (width, height))
root.configure(background = 'gray0')
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 1)
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 3)
style = ttk.Style()

background = '#d4d4d4'
text_color = 'black'
entry_bg = '#f2f2f2'
entry_text = 'black'
label_bg = '#d4d4d4'
label_text = 'black'
scroll_color = '#bababa'
scroll_bg = '#cccccc'
scrollbar_color = '#858585'
insert_bg = 'black'

style.configure('TLabelframe', background = background)
style.configure('TLabelframe.Label', background = background)

search_path = '/home/clay/Documents/recipes/**/*'

class MAIN():

    '''
    The main window where the recipe information is entered
    '''
    def __init__(self, master):
        '''
        Create the root window, call the methods to create
        key bindings and all the widgets
        '''
        self.frame = tk.Frame(root)
        self.frame.pack(fill = 'both', expand = True, side = 'top')
        self.frame.configure(background = background)
        self.frame.rowconfigure(1, weight = 1)
        self.frame.columnconfigure(0, weight = 1)
        self.frame.columnconfigure(1, weight = 3)
        master.title('Recipe Search')
        self.create_widgets()

    

    def ingSearch(self):
            rec_files = glob.glob(search_path, recursive = True)
            search_str = self.search_entered.get()
            self.search_results = {}
            self.results.delete(0, 'end')
            self.display.delete(1.0, 'end')

            # use try loop to avoid trying to open directories in the file list

            for file in rec_files:
                try:
                        with open(file, 'r') as f:
                                contents = f.read()
                        # use re.findall to make search case insensitive
                        if re.findall(search_str, contents, flags=re.IGNORECASE):
                                self.search_results[file]=path.basename(file)
                                file.close()

                except:
                        pass
            for i in self.search_results.values():
                    self.results.insert(0, i)
                    #self.results.insert(n, i)

    # Code to perform a search of the recipe titles

    def titleSearch(self):
            rec_files = glob.glob(search_path, recursive = True) # gather list to search
            search_str = self.search_entered.get()  # get the term to be searched for
            self.search_results = {}
            self.results.delete(0, 'end') # Clear results box to keep multiple searches from appending
            self.display.delete(1.0, 'end') # Clear the display box of any previous search results
            for file in rec_files:
                    # use re.findall to make search case insensitive
                    if re.findall(search_str, file, flags=re.IGNORECASE):
                            self.search_results[file]=path.basename(file) # set key as full path, value as filename
            for i in self.search_results.values():
                    self.results.insert(0, i)

    # Code to display the selected recipe in the display box

    def viewRec(self, event):
            # separate the file names and their full paths into lists
            key_list = list(self.search_results.keys()) # full paths to files
            val_list = list(self.search_results.values()) # filenames from search results
            for i in self.results.curselection():
                    file = self.results.get(i) # get the currently selected filename
                    position = val_list.index(file)
                    self.cur_path = key_list[position] # Save full path of selected recipe
                    self.display.delete(1.0, 'end') # clear recipe display box
                    with open(key_list[position], 'r') as f: # Display selected recipe in right hand pane
                            contents = f.read()
                            self.display.insert(1.0, contents)

    def saveEdit(self):
            edited_file = self.display.get(1.0, 'end-1c') # copy contents of recipe display box
            # Write the edits to the original file
            with open(self.cur_path, "w") as file:
                    file.write(edited_file)
                    file.close()
            self.savebutton.config(state='disabled') # Disable save button after saving file

    # Function to enable the save button when the mouse is clicked in the recipe display box

    def saveEnable(self, arg):
            self.savebutton.config(state='normal')

    def create_widgets(self):
        '''
        Long method to create all widgets on the root window
        '''

        # Creating a Menu Bar

        menu_bar = Menu(root)
        root.config(menu=menu_bar)
        menu_bar.config(background = background, foreground = text_color)
        # Code for the cascading File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New   Ctrl+n')
        file_menu.add_separator()
        file_menu.add_command(label='Save  Ctrl+s')
        file_menu.add_separator()
        file_menu.add_command(label='Quit  Ctrl+q')
        file_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='File', menu=file_menu)

        # Code for cascading config menu

        config_menu = Menu(menu_bar, tearoff=0)
        config_menu.add_command(label='Set Default Save Path')
        config_menu.add_separator()
        config_menu.add_command(label='Use Bullet Points')
        config_menu.add_separator()
        config_menu.add_command(label='Format Filename')
        config_menu.configure(background = background, foreground = text_color)
        config_menu.add_separator()
        config_menu.add_command(label='Use Dark Mode')
        config_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='Config', menu=config_menu)

        # Code for the cascading Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Program Help  Ctrl+h')
        help_menu.add_separator()
        help_menu.add_command(label='About')
        help_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='Help', menu=help_menu)

        # Top frame for search entry
        nameLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Enter Search Term')
        self.search_frame = ttk.LabelFrame(self.frame, labelwidget=nameLabel)
        self.search_frame.grid(column=0, row=0, columnspan=1, padx=8, pady=4, sticky='W')

        # Frame for the search buttons
        searchLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Click to Perform Search')
        self.sbutton_frame = ttk.LabelFrame(self.frame, labelwidget=searchLabel)
        self.sbutton_frame.grid(column=1, row=0, padx=8, sticky='W')
        self.sbutton_frame.columnconfigure(0, weight = 1)

        # Frame for the save button
        saveLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Click to Save Changes')
        self.svbutton_frame = ttk.LabelFrame(self.frame, labelwidget=saveLabel)
        self.svbutton_frame.grid(column=2, row=0, padx=8, sticky='W')
        self.svbutton_frame.columnconfigure(0, weight = 1)

        # Left frame for search results
        ingLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Search Results')
        self.result_frame = ttk.LabelFrame(self.frame, labelwidget=ingLabel)
        self.result_frame.grid(column=0, row=1, padx=8, pady=4, sticky = 'news')
        self.result_frame.rowconfigure(0, weight = 1)
        self.result_frame.columnconfigure(0, weight = 1)

        # Right frame for recipe display
        dirLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Recipe Selected')
        self.display_frame = ttk.LabelFrame(self.frame, labelwidget=dirLabel)
        self.display_frame.grid(column=1, row=1, columnspan=2, padx=8, pady=4, sticky='nwes')
        self.display_frame.rowconfigure(0, weight = 1)
        self.display_frame.columnconfigure(0, weight = 1)

        # Search box
        self.search = tk.StringVar()
        self.search_entered = tk.Entry(self.search_frame, width=30, textvariable=self.search,
                                      bd=5, relief=tk.RIDGE)
        self.search_entered.configure(background = entry_bg, foreground = entry_text, insertbackground = insert_bg)
        self.search_entered.grid(column=0, row=0, padx=8, pady=(3, 8), sticky='W')
        self.search_entered.focus()

        # Add button for Title search
        self.tsbutton = tk.Button(self.sbutton_frame, text='Title Search', relief='raised', command = self.titleSearch)
        self.tsbutton.grid(column=0, row=1, padx=8, pady=(3, 8), sticky='W')

        # Add button for Ingredient search
        self.ingbutton = tk.Button(self.sbutton_frame, text='Ingredient Search', relief='raised', command = self.ingSearch)
        self.ingbutton.grid(column=1, row=1, padx=8, pady=(3, 8))

        # Add button to save edits
        self.savebutton = tk.Button(self.svbutton_frame, text='Save Edits', relief='raised', command = self.saveEdit)
        self.savebutton.grid(column=0, row=1, padx=8, pady=(3, 8))
        self.savebutton.config(state='disabled')

        # Search results box
        self.results = tk.Listbox(self.result_frame, width = 30, bd=5, selectmode=tk.SINGLE,\
                 relief=tk.RIDGE)
        self.results.configure(background = entry_bg, foreground = entry_text)
        self.results.grid(column=0, row=0, padx=8, pady=(0, 20), sticky=tk.N+tk.S+tk.E+tk.W)
        self.results.bind('<<ListboxSelect>>', self.viewRec)

        # recipe display box
        self.display = scrolledtext.ScrolledText(self.display_frame, bd=5,\
                wrap=tk.WORD, relief=tk.RIDGE)
        self.display.configure(background = entry_bg, foreground = entry_text, insertbackground = insert_bg)
        self.display.vbar.configure(troughcolor = scroll_color, background = scroll_bg, activebackground = scrollbar_color)
        self.display.grid(column=0, row=0, padx=8, pady=(0, 20), sticky=tk.N+tk.S+tk.E+tk.W)
        self.display.bind("<Button-1>", self.saveEnable) # left click enables save button
        self.display.bind("<Button-3>", self.saveEnable) # right click enables save button



#=============
#Start GUI
#=============

if __name__ == "__main__":
        main = MAIN(root)
        root.mainloop()
