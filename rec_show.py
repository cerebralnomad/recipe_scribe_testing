#! /usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import filedialog
import re
import configparser
from os import path
import glob
import ToolTip as tt
from HelpText import help_text
from AboutText import about_text

root = tk.Tk()
width = int(root.winfo_screenwidth() / 1.9)
height = int(root.winfo_screenheight() / 1.2)
root.geometry('%sx%s' % (width, height))
root.configure(background = 'gray0')
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 1)
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 3)
style = ttk.Style()

config = configparser.ConfigParser()

# Set the variables from the config file if it exists
# If not create it with the default values

if path.exists("CONFIG"):
    config.read("CONFIG")
    save_path = config.get('DefaultSavePath', 'save_path')
    search_path = save_path
    use_bp = config.get('UseBulletPoints', 'use_bp')
    fn_format = config.get('FormatFileName', 'fn_format')
    dark_mode = config.get('UseDarkMode', 'dark_mode')
else:
    file = open('CONFIG', 'w+')
    file.write("# The options can be changed from the GUI\n")
    file.write("# If editing this file directly:")
    file.write("# Options for UseBulletPoints are True or False\n")
    file.write("# Options for FormatFileName are True or False\n")
    file.write("# Options for UseDarkMode are True or False\n")
    file.write("\n")
    file.close()
    save_path = "None"
    use_bp = "True"
    fn_format = "True"
    dark_mode = "False"

    config.add_section("DefaultSavePath")
    config.add_section("UseBulletPoints")
    config.add_section("FormatFileName")
    config.add_section("UseDarkMode")
    config.set("DefaultSavePath", "save_path", "None")
    config.set("UseBulletPoints", "use_bp", "True")
    config.set("FormatFileName", "fn_format", "True")
    config.set("UseDarkMode", "dark_mode", "False")
    with open("CONFIG", "a") as configfile:
        config.write(configfile)

# Set the color theme for the GUI to avoid ocnflicts with
# other distros and dark themes
 
if dark_mode == 'False' or dark_mode == 'false':
    background = '#d4d4d4'
    text_color = 'black'
    entry_bg = '#f2f2f2'
    entry_text = 'black'
    label_bg = '#d4d4d4'
    label_text = 'black'
    scroll_color = '#bababa'
    scroll_bg = '#cccccc'
    scrollbar_color = '#858585'
elif dark_mode == 'True' or dark_mode == 'true':
    background = '#343232'
    text_color = 'white'
    entry_bg = '#1e1e1e'
    entry_text = 'white'
    label_bg = '#343232'
    label_text = 'white'
    scroll_color = '#5d5c5c'
    scroll_bg = '#464444'
    scrollbar_color = '#858585'

style.configure('TLabelframe', background = background)
style.configure('TLabelframe.Label', background = background)

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
        master.title('Recipe Scribe')
#        self.bind_keys()
        self.create_widgets()

#    def bind_keys(self):
#        '''
#        Set the bindings for the keyboard shortcuts to the menu items
#        '''
#        root.bind('<Control-s>', self._save)
#        root.bind('<Control-n>', self._new)
#        root.bind('<Control-q>', self._quit)
#        root.bind('<Control-h>', HelpWindow)
#        root.bind('<Control-c>', DefaultPath)

    def _quit(self, event='q'):
        '''
        Function to exit GUI cleanly
        Bound to the Exit command on the file menu
        '''
        root.quit()
        root.destroy()

    def focus_next_widget(self, event):
        '''
        Allows the use of the TAB key to advance to the next entry field
        '''
        if event.widget == self.title_entered:
            self.ingredients.focus_set()
            return 'break'
        elif event.widget == self.ingredients:
            self.directions.focus_set()
            return 'break'
        elif event.widget == self.directions:
            self.title_entered.focus_set()
            return 'break'

    def _save(self, event='s'):
            pass

    def _new(self, event='e'):
            pass

    def ingSearch(self, term):
            self.rec_files = glob.glob(search_path, recursive = True)
            search_str = term
            results = []
            for file in self.rec_files:
                    try:
                            with open(file, 'r') as f:
                                    contents = f.read()
                            if search_str in contents:
                                    result = file.rsplit('/', 2)
                                    results.append(result)
                    except:
                        pass

            return results


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
        file_menu.add_command(label='New   Ctrl+n', command=self._new)
        file_menu.add_separator()
        file_menu.add_command(label='Save  Ctrl+s', command=self._save)
        file_menu.add_separator()
        file_menu.add_command(label='Quit  Ctrl+q', command=self._quit)
        file_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='File', menu=file_menu)

        # Code for cascading config menu

        config_menu = Menu(menu_bar, tearoff=0)
        config_menu.add_command(label='Set Default Save Path', command=DefaultPath)
        config_menu.add_separator()
        config_menu.add_command(label='Use Bullet Points (' + use_bp + ')', command=SetBulletPoints)
        config_menu.add_separator()
        config_menu.add_command(label='Format Filename (' + fn_format + ')', command=FilenameFormat)
        config_menu.configure(background = background, foreground = text_color)
        config_menu.add_separator()
        config_menu.add_command(label='Use Dark Mode (' + dark_mode + ')', command=UseDarkMode)
        config_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='Config', menu=config_menu)

        # Code for the cascading Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Program Help  Ctrl+h', command=HelpWindow)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=AboutWindow)
        help_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='Help', menu=help_menu)

        '''
        ====================================================================
        Recipe name entry box to be replaced with search term box
        To the right of the box will be two check boxes
        One for Ingredient Search and one for Filename Search
        Filename will be preselected. Selecting ingredient wilet
        deselect filename and vice versa
        Stack the check boxes and place a search button to the right of them
        ====================================================================
        '''

        # Top frame for the recipe name entry
        
        #====================================
        # Edited to be search
        #====================================

        nameLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Enter Search Term')
        self.search_frame = ttk.LabelFrame(self.frame, labelwidget=nameLabel)
        self.search_frame.grid(column=0, row=0, columnspan=1, padx=8, pady=4, sticky='W')

        # Frame for the search buttons

        searchLabel = ttk.Label(foreground=label_text, background=label_bg, text=' CLick to Perform Search')
        self.sbutton_frame = ttk.LabelFrame(self.frame, labelwidget=searchLabel)
        self.sbutton_frame.grid(column=1, row=0, padx=8, sticky='W')
        self.sbutton_frame.columnconfigure(0, weight = 1)

        '''
        ===================================================================
        Ingredients box will be used to display the returned search results
        ===================================================================
        '''

        # Left frame for the search results

        #=====================================
        # Edited to be result frame
        #=====================================

        ingLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Search Results')
        self.result_frame = ttk.LabelFrame(self.frame, labelwidget=ingLabel)
        self.result_frame.grid(column=0, row=1, padx=8, pady=4, sticky = 'news')
        self.result_frame.rowconfigure(0, weight = 1)
        self.result_frame.columnconfigure(0, weight = 1)

        '''
        ====================================================================
        Directions box will be used to display a recipe when clicked on in
        the search results box (hopefully)
        ====================================================================
        '''

        # Right frame for display of selected recipe

        #=====================================
        # Edited to be display box frame
        #=====================================

        dirLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Recipe Selected')
        self.display_frame = ttk.LabelFrame(self.frame, labelwidget=dirLabel)
        self.display_frame.grid(column=1, row=1, padx=8, pady=4, sticky='nwes')
        self.display_frame.rowconfigure(0, weight = 1)
        self.display_frame.columnconfigure(0, weight = 1)

        '''
        =====================================================================
        Change this to say "Enter search term here"
        =====================================================================
        '''

        # Adding a text box entry widget for the recipe search
        
        #=====================================================
        # Edited to be search box
        #=====================================================

        self.search = tk.StringVar()
        self.search_entered = tk.Entry(self.search_frame, width=30, textvariable=self.search,
                                      bd=5, relief=tk.RIDGE)
        self.search_entered.configure(background = entry_bg, foreground = entry_text, insertbackground='white')
        self.search_entered.grid(column=0, row=0, padx=8, pady=(3, 8), sticky='W')
        self.search_entered.bind("<Tab>", self.focus_next_widget)
        tt.create_ToolTip(self.search_entered, 'Enter the term to search for here')

        # Add button for Title search
        search = Search()
        search_term = self.search_entered.get()
        self.tsbutton = tk.Button(self.sbutton_frame, text='Title Search', relief='raised', command=search.titleSearch(search_term))
        self.tsbutton.grid(column=0, row=1, padx=8, pady=(3, 8), sticky='W')
        

        # Add button for Ingredient search
        search_term = self.search_entered.get()
        self.ingbutton = tk.Button(self.sbutton_frame, text='Ingredient Search', relief='raised', command=self.ingSearch(search_term))
        self.ingbutton.grid(column=1, row=1, padx=8, pady=(3, 8))

        # Add a scroll box for search results

        #=====================================
        # Edited to be results box
        #=====================================

        self.results = scrolledtext.ScrolledText(self.result_frame, width = 30, bd=5,\
                wrap=tk.WORD, relief=tk.RIDGE)
        self.results.configure(background = entry_bg, foreground = entry_text, insertbackground='white')
        self.results.vbar.configure(troughcolor = scroll_color, background = scroll_bg, activebackground = scrollbar_color)
        self.results.grid(column=0, row=0, padx=8, pady=(0, 20), sticky=tk.N+tk.S+tk.E+tk.W)
        self.results.bind("<Tab>", self.focus_next_widget)
        #tt.create_ToolTip(self.results, 'Enter ingredients here, one per line\nBegin line with a period to omit bullet point')

        # Add a scroll text box for recipe display

        #======================================
        # Edited to be recipe display box
        #======================================

        self.display = scrolledtext.ScrolledText(self.display_frame, bd=5,\
                wrap=tk.WORD, relief=tk.RIDGE)
        self.display.configure(background = entry_bg, foreground = entry_text, insertbackground='white')
        self.display.vbar.configure(troughcolor = scroll_color, background = scroll_bg, activebackground = scrollbar_color)
        self.display.grid(column=0, row=0, padx=8, pady=(0, 20), sticky=tk.N+tk.S+tk.E+tk.W)
        self.display.bind("<Tab>", self.focus_next_widget)
        #tt.create_ToolTip(self.display, 'Enter the recipe instructions here')

        self.search_entered.focus()  # Place cursor into the search entry box

        def resultDisplay(self, var):
                search_results = var
                self.results.insert(1.0, search_results)

class DefaultPath():
        pass

class SetBulletPoints():
        pass

class FilenameFormat():
        pass

class UseDarkMode():
        pass

class HelpWindow():
        pass

class AboutWindow():
        pass

class Search():

        def __init__(self):
            self.rec_files = glob.glob(search_path, recursive = True)
            self.search_results = []

        def ingredientSearch(self, term):
            self.search_term = term
            for file in self.rec_files:
                try:
                        with open(file, 'r') as f:
                                contents = f.read()
                        if self.search_term in contents:
                                result = file.rsplit('/', 2)
                                self.search_results.append(result)
                                file.close()

                except:
                        pass

            return self.search_results

        def titleSearch(self, term):
                self.search_term = term
                for file in self.rec_files:
                    if self.search_term in file:
                        result = file.rsplit('/', 2)
                        self.search_results.append(result)
                        
                return self.search_results


#=============
#Start GUI
#=============

main = MAIN(root)    # Create an instance of the MAIN class
root.mainloop()
