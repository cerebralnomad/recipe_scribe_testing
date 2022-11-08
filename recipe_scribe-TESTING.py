#!/usr/bin/env python3
'''
Switching frames now works in full screen without the loss
of the menu bar.
Archiving at this point to preserve progress.
Config parser still commented out

Added the check for leading . in directions to escape indent

'''


import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import filedialog
import re
import configparser
import glob
from os import path
import ToolTip as tt
from HelpText import help_text
from AboutText import about_text
import time



'''
ConfigParser options comment prefixes and allow no value
let's me include comments in the config file that will not
be stripped on a write to the file initiated from the GUI

The optionxform setting preserves capitialization in those comments
'''
config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
config.optionxform = str

# Set the variables from the config file if it exists
# If not create it with the default values
'''
if path.exists("CONFIG"):
    config.read("CONFIG")
    save_path = config.get('DefaultSavePath', 'save_path')
    use_bp = config.get('UseBulletPoints', 'use_bp')
    fn_format = config.get('FormatFileName', 'fn_format')
    dark_mode = config.get('UseDarkMode', 'dark_mode')
    fullscreen = config.get('StartFullscreen', 'fullscreen')

    
else:
    save_path = "None"
    use_bp = "True"
    fn_format = "True"
    dark_mode = "False"
    fullscreen = "False"
    
    config.add_section("Comments") # Configparser strips comments on write, this preserves them
    config.add_section("DefaultSavePath")
    config.add_section("UseBulletPoints")
    config.add_section("FormatFileName")
    config.add_section("UseDarkMode")
    config.add_section("StartFullscreen")
    config.set("Comments", "# The options can be changed from the GUI")
    config.set("Comments", "# If editing this file directly:")
    config.set("Comments", "# Options for UseBulletPoints are True or False (default: True)")
    config.set("Comments", "# Options for FormatFileName are True or False (default: True)")
    config.set("Comments", "# Options for UseDarkMode are True or False (default: False)")
    config.set("Comments", "# Options for StartFullscreen are True or False (default: False)")
    config.set("Comments", "# Anything other than true or false will result in the default")
    config.set("DefaultSavePath", "save_path", "None")
    config.set("UseBulletPoints", "use_bp", "True")
    config.set("FormatFileName", "fn_format", "True")
    config.set("UseDarkMode", "dark_mode", "False")
    config.set("StartFullscreen", "fullscreen", "False")
    with open("CONFIG", "a") as configfile:
        config.write(configfile) 

# Set the color theme for the GUI to avoid ocnflicts with
# other distros and dark themes

if dark_mode == 'True' or dark_mode == 'true':
    background = '#343232'
    text_color = 'white'
    entry_bg = '#1e1e1e'
    entry_text = 'white'
    label_bg = '#343232'
    label_text = 'white'
    scroll_color = '#5d5c5c'
    scroll_bg = '#464444'
    scrollbar_color = '#858585'
    insert_bg = 'white'
else:
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
'''
# =================================================
# Remove these variables after enabling the parser
# Their values will be pulled from the CONFIG file

fullscreen = 'False'
background = '#d4d4d4'
text_color = 'black'
entry_bg = '#f2f2f2'
entry_text = 'black'
label_bg = '#d4d4d4'
label_text = 'black'
scroll_color = '#bababa'
scroll_bg = '#cccccc'
scrollbar_color = '#858585'
save_path = "None"
use_bp = "True"
fn_format = "True"
dark_mode = "False"
insert_bg = 'black'
# ===================================================

root = tk.Tk()
if fullscreen == 'True' or fullscreen == 'true':
    root.attributes('-zoomed', True)
    #width = int(root.winfo_screenwidth() / 1.01)
    #height = int(root.winfo_screenheight() / 1.01)
else:
    width = int(root.winfo_screenwidth() / 1.9)
    height = int(root.winfo_screenheight() / 1.2)
    root.geometry('%sx%s' % (width, height))
root.configure(background = 'gray0')
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 1)
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 3)
style = ttk.Style()
root.update_idletasks()

style.configure('TLabelframe', background = background)
style.configure('TLabelframe.Label', background = background)

# Uncomment search_path and remove hard code path after
# Parser is enabled

# search_path = save_path
search_path = '/home/clay/Documents/recipes/**/*'

fs = ''

class MAIN():
    '''
    The main window where the recipe information is entered
    '''
    def __init__(self, master):
        '''
        Hack to prevent the loss of the menu bar when switching
        frames in full screen.
        Instantly resizing the window size down and back to
        full brings the menu back seamlessly.

        The elif is in case launch was not in fullscreen, but the window
        was maximized after switching to the search page.
        '''
        if fullscreen == 'True' or fullscreen == 'true':
            width = int(root.winfo_screenwidth() / 1.9)
            height = int(root.winfo_screenheight() / 1.2)
            root.geometry('%sx%s' % (width, height))
            root.attributes('-zoomed', True)

        elif fs == "F":
            w = (root.winfo_width())
            h = (root.winfo_height())
            root.geometry('%sx%s' % (w-1, h-1))

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
        self.bind_keys()
        self.create_widgets()

    def bind_keys(self):
        '''
        Set the bindings for the keyboard shortcuts to the menu items
        '''
        root.bind('<Control-s>', self._save)
        root.bind('<Control-n>', self._new)
        root.bind('<Control-q>', self._quit)
        root.bind('<Control-h>', HelpWindow)
        #root.bind('<Control-c>', DefaultPath)

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
        '''
        _save opens the save dialog box. Not sure if the code is proper here
        Without the event parameter, there's an error using the keyboard
        shortcut (1 param expected, 2 given)
        Without giving event a default value, there's an error when clicking the
        menu item (2 param expected, 1 given)
        '''

        # Retrieve the name of the recipe from the title box widget
        recipe_name = self.title_entered.get()
        # reformat the recipe name for use as the file name
        if fn_format == "True" or fn_format == "true":
            file_name = recipe_name.lstrip().lower().replace(' ', '_')
        else:
            file_name = recipe_name
        # split the ingredient list based on newline
        ingredients = self.ingredients.get(1.0, 'end-1c').split('\n')
        # split the directions based on newline
        directions = self.directions.get(1.0, 'end-1c').split('\n')

        if save_path is None:
            file = filedialog.asksaveasfile(mode='w', initialfile=file_name,
                                            defaultextension=".txt")
        else:
            file = filedialog.asksaveasfile(mode='w', initialfile=file_name,
                                            defaultextension=".txt", initialdir=save_path)
        if file is None:
            return
        file.write('\n')
        file.write(recipe_name)
        file.write('\n\n')
        file.write('Ingredients')
        file.write('\n\n')
        # Make sure blank lines in ingredients or lines beginning with a . are not bullet pointed
        if use_bp =="True" or use_bp == "true":
            for i in ingredients:
                line = i
                if re.match('\.', line):
                    newline = re.sub(r'\.', '', line)
                    file.write(newline + '\n')
                elif not re.match('\w', line): # using re import for regex search to see if line contains letters or numbers
                    file.write(line +'\n')
                else:
                    file.write('• ' + line + '\n')  # Prepend each ingredient with a bullet point
        else:
            for i in ingredients:
                line = i
                file.write(line + '\n')
        file.write('\n')
        file.write('Directions')
        file.write('\n\n')
        '''
        Code to automatically indent any line not beginning with a number
        Written as:
        	1. First do this thing.
        	Then do this further thing

        Will be saved as:
        	1. First do this thing.
        	   Then do this further thing

        This makes the directions look better without requiring manual
        indentation
        However, step 10 and beyond will result in one space of indentation
        too many.
        Few recipes have more than 9 steps normally.
        This issue may be looked at later.

        Lines in Directions beginning with a period will not be indented.
        This will allow for the inclusion of notes or links without having them
        indented in the saved file.
        '''
        for i in directions:
            line = i
            if re.match('[1-9]', line):
                file.write(line + '\n')
            elif re.match('\.', line): # Do not indent lines beginning with a period
                newline = re.sub(r'\.', '', line) # Remove the . before writing
                file.write(newline + '\n')
            else:
                file.write('   ' + line + '\n')

        file.write("\n\n\n")
        file.close()

    # Function to clear the text for entering another recipe.
    # See comments for _save for explanation of the event parameter

    def _new(self, event='e'):

        self.title_entered.delete(0, 'end')
        self.ingredients.delete(1.0, 'end')
        self.directions.delete(1.0, 'end')
        self.title_entered.focus()  # Place cursor back into the title entry box

    def search(self):
        Search(root)
        self.frame.pack_forget()


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
        config_menu.add_separator()
        config_menu.add_command(label='Start Fullscreen (' + fullscreen + ')', command=StartFullScreen)
        config_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='Config', menu=config_menu)

        # Code for the cascading Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Program Help  Ctrl+h', command=HelpWindow)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=AboutWindow)
        help_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        # Spacer to set the Search command apart from the rest of the manu
        menu_bar.add_command(label='         ', command=None, state='disabled')
        # Command to switch to the Search window
        menu_bar.add_command(label = 'Search Recipes', command=self.search)

        # Top frame for the recipe name entry
        nameLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Enter Recipe Title')
        self.title_frame = ttk.LabelFrame(self.frame, labelwidget=nameLabel)
        self.title_frame.grid(column=0, row=0, columnspan=2, padx=8, pady=4, sticky='W')

        # Left frame for the ingredients list
        ingLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Ingreidents')
        self.ing_frame = ttk.LabelFrame(self.frame, labelwidget=ingLabel)
        self.ing_frame.grid(column=0, row=1, padx=8, pady=4, sticky = 'news')
        self.ing_frame.rowconfigure(0, weight = 1)
        self.ing_frame.columnconfigure(0, weight = 1)

        # Right frame for the directions
        dirLabel = ttk.Label(foreground=label_text, background=label_bg, text=' Directions')
        self.dir_frame = ttk.LabelFrame(self.frame, labelwidget=dirLabel)
        self.dir_frame.grid(column=1, row=1, padx=8, pady=4, sticky='nwes')
        self.dir_frame.rowconfigure(0, weight = 1)
        self.dir_frame.columnconfigure(0, weight = 1)

        # Adding a text box entry widget for the recipe title
        self.title = tk.StringVar()
        self.title_entered = tk.Entry(self.title_frame, width=75, textvariable=self.title,
                                      bd=5, relief=tk.RIDGE)
        self.title_entered.configure(background = entry_bg, foreground = entry_text, insertbackground=insert_bg)
        self.title_entered.grid(column=0, row=2, padx=8, pady=(3, 8), sticky='W')
        self.title_entered.bind("<Tab>", self.focus_next_widget)
        tt.create_ToolTip(self.title_entered, 'Enter the title of the recipe here')

        # Add a scroll box for ingredients
        self.ingredients = scrolledtext.ScrolledText(self.ing_frame, width = 30, bd=5,\
                wrap=tk.WORD, relief=tk.RIDGE)
        self.ingredients.configure(background = entry_bg, foreground = entry_text, insertbackground=insert_bg)
        self.ingredients.vbar.configure(troughcolor = scroll_color, background = scroll_bg, activebackground = scrollbar_color)
        self.ingredients.grid(column=0, row=0, padx=8, pady=(0, 20), sticky=tk.N+tk.S+tk.E+tk.W)
        self.ingredients.bind("<Tab>", self.focus_next_widget)
        tt.create_ToolTip(self.ingredients, 'Enter ingredients here, one per line\nBegin line with a period to omit bullet point')

        # Add a scroll text box for directions
        self.directions = scrolledtext.ScrolledText(self.dir_frame, bd=5,\
                wrap=tk.WORD, relief=tk.RIDGE)
        self.directions.configure(background = entry_bg, foreground = entry_text, insertbackground=insert_bg)
        self.directions.vbar.configure(troughcolor = scroll_color, background = scroll_bg, activebackground = scrollbar_color)
        self.directions.grid(column=0, row=0, padx=8, pady=(0, 20), sticky=tk.N+tk.S+tk.E+tk.W)
        self.directions.bind("<Tab>", self.focus_next_widget)
        tt.create_ToolTip(self.directions, 'Enter the recipe instructions here')

        self.title_entered.focus()  # Place cursor into the title entry box


class DefaultPath():
    '''
    Brings up the dialog box to set a default save path for use as
    a starting save location when saving a file
    '''
    def __init__(self):
        '''
        Create the new window and the two buttons to
        either select location or cancel
        '''

        path = save_path
        self.pathwin = tk.Tk()
        self.pathwin.title('Set Default Save Path')
        if path is None:
            self.current_loc = ttk.Label(self.pathwin, text = 'The current default save path is not set.')
            self.current_loc.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        else:
            self.current_loc = ttk.Label(self.pathwin, text = "The current save path is set to '{}':\n ".format(path))
            self.current_loc.grid(column=1, row=1, columnspan=2, padx=(10), pady=(15, 0), sticky='WE')
        self.msg = ttk.Label(self.pathwin, text='Click Browse to select your default save location')
        self.msg.grid(column=1, row=2, columnspan=2, padx=10, pady=(10, 25), sticky='WE')
        self.button = ttk.Button(self.pathwin, text=' Browse ', command=self.set_path)
        self.button.grid(column=1, row=3, padx=10, pady=(0, 25), sticky='WE')
        self.cancel = ttk.Button(self.pathwin, text=' Cancel ', command=self.pathwin.destroy)
        self.cancel.grid(column=2, row=3, padx=10, pady=(0, 25), sticky='WE')

    def set_path(self):
        '''
        Get the chosen location and write it to CONFIG so it is remembered
        when the program is run in the future
        '''
        path = filedialog.askdirectory()
        config.set('DefaultSavePath', 'save_path', path)
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        self.msgbox()

    def msgbox(self):
        '''
        Confirmation popup that the default path was saved
        '''
        msg.showinfo(
            'Default Save Path Set', 'Your default save \npath has been set.\n\nThis will take effect \nthe next time you run \nthe program'
            )


class SetBulletPoints():

    # Brings up the dialog box to set whether to use bullet points in the ingredient list

    choice = 'None'

    def __init__(self):

        # Create the popup to select the configuration setting

        self.bpwin = tk.Toplevel(root)
        self.bpwin.title('Bullet point configuration')
        if use_bp == 'True':
            self.bp_status = ttk.Label(self.bpwin, text = 'Bullet points for the ingredients is currently set to True')
            self.bp_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        else:
            self.bp_status = ttk.Label(self.bpwin, text = 'Bullet points for the ingredients is currently set to False')
            self.bp_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        self.msg = ttk.Label(self.bpwin, text = 'Select whether you want to use bullet points')
        self.msg.grid(column=1, row=2, columnspan=2, padx=10, pady=(10, 25), sticky='WE')
        self.yes = ttk.Button(self.bpwin, text = 'Yes', command=lambda:[self.bp_true(), self.bpwin.destroy()])
        self.yes.grid(column=1, row=3, padx=10, pady=(0, 25), sticky='WE')
        self.no = ttk.Button(self.bpwin, text = 'No', command=lambda:[self.bp_false(), self.bpwin.destroy()])
        self.no.grid(column=2, row=3, padx=10, pady=(0, 25), sticky='WE')
        root.eval(f'tk::PlaceWindow {str(self.bpwin)} center')

    def bp_true(self):

        # Set the use_bp setting in the CONFIG file to True

        config.set("UseBulletPoints", "use_bp", "True")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'yes'
        self.bp_msgbox(choice)

    def bp_false(self):

        # Set the use_bp setting in the CONFIG file to False

        config.set("UseBulletPoints", "use_bp", "False")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'no'
        self.bp_msgbox(choice)

    def bp_msgbox(self, choice):
        '''
        Confirmation popup that the configuration choice was saved
        '''
        if choice == 'yes':
            bp_info = tk.Toplevel(root)
            bp_info.title('Bullet point configuration set')
            message = ttk.Label(bp_info,
                text = 'Bullet points will be used in the ingredients list\nPlease restart the application')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(bp_info, text = 'Ok', command=bp_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(bp_info)} center')
        else:
            bp_info = tk.Toplevel(root)
            bp_info.title('Bullet point configuration set')
            message = ttk.Label(bp_info,
                text = 'Bullet points will not be used in the ingredients list\nPlease restart the application')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(bp_info, text = 'Ok', command=bp_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(bp_info)} center')

class FilenameFormat():

    '''
    Brings up the dialog box to set whether to format the saved filenames
    Formatting will use the recipe title, converting capitals to lowercase
    and spaces to underscores.
    No formatting will use the recipe title as written for the filename.
    '''

    choice = 'None'

    def __init__(self):

        # Create the popup to select the configuration setting

        self.fnfwin = tk.Toplevel(root)
        self.fnfwin.title('Filename formatting configuration')
        if fn_format == 'True':
            self.fnf_status = ttk.Label(self.fnfwin, text = 'Filename formatting is currently set to True')
            self.fnf_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        else:
            self.fnf_status = ttk.Label(self.fnfwin, text = 'Filename formatting is currently set to False')
            self.fnf_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        self.msg = ttk.Label(self.fnfwin, text = 'Select whether you want to use bullet points')
        self.msg.grid(column=1, row=2, columnspan=2, padx=10, pady=(10, 25), sticky='WE')
        self.yes = ttk.Button(self.fnfwin, text = 'Yes', command=lambda:[self.fnf_true(), self.fnfwin.destroy()])
        self.yes.grid(column=1, row=3, padx=10, pady=(0, 25), sticky='WE')
        self.no = ttk.Button(self.fnfwin, text = 'No', command=lambda:[self.fnf_false(), self.fnfwin.destroy()])
        self.no.grid(column=2, row=3, padx=10, pady=(0, 25), sticky='WE')
        root.eval(f'tk::PlaceWindow {str(self.fnfwin)} center')

    def fnf_true(self):

        # Set the fn_format setting in the CONFIG file to True

        config.set("FormatFileName", "fn_format", "True")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'yes'
        self.fnf_msgbox(choice)

    def fnf_false(self):

        # Set the fn_format setting in the CONFIG file to False

        config.set("FormatFileName", "fn_format", "False")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'no'
        self.fnf_msgbox(choice)

    def fnf_msgbox(self, choice):
        '''
        Confirmation popup that the configuration choice was saved
        '''
        if choice == 'yes':
            fnf_info = tk.Toplevel(root)
            fnf_info.title('Filename formatting configuration set')
            message = ttk.Label(fnf_info,
                text = 'Filenames will be formatted to lowercase and spaces converted to underscores\nPlease restart the application')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(fnf_info, text = 'Ok', command=fnf_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(fnf_info)} center')
        else:
            fnf_info = tk.Toplevel(root)
            fnf_info.title('Filename formatting configuration set')
            message = ttk.Label(fnf_info,
                text = 'Filenames will be the unmodified text of the recipe title\nPlease restart the application')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(fnf_info, text = 'Ok', command=fnf_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(fnf_info)} center')

class UseDarkMode():

    # Brings up the dialog box to set whether to use dark mode for the application

    choice = 'None'

    def __init__(self):

        # Create the popup to select the configuration setting

        self.dmwin = tk.Toplevel(root)
        self.dmwin.title('Dark Mode configuration')
        if dark_mode == 'True':
            self.dm_status = ttk.Label(self.dmwin, text = 'You are currently using the application in Dark Mode')
            self.dm_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        else:
            self.dm_status = ttk.Label(self.dmwin, text = 'You are not currently using Dark Mode')
            self.dm_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        self.msg = ttk.Label(self.dmwin, text = 'Select whether you want to use Dark Mode')
        self.msg.grid(column=1, row=2, columnspan=2, padx=10, pady=(10, 25), sticky='WE')
        self.yes = ttk.Button(self.dmwin, text = 'Yes', command=lambda:[self.dm_true(), self.dmwin.destroy()])
        self.yes.grid(column=1, row=3, padx=10, pady=(0, 25), sticky='WE')
        self.no = ttk.Button(self.dmwin, text = 'No', command=lambda:[self.dm_false(), self.dmwin.destroy()])
        self.no.grid(column=2, row=3, padx=10, pady=(0, 25), sticky='WE')
        root.eval(f'tk::PlaceWindow {str(self.dmwin)} center')

    def dm_true(self):

        # Set the dark_mode setting in the CONFIG file to True

        config.set("UseDarkMode", "dark_mode", "True")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'yes'
        self.dm_msgbox(choice)

    def dm_false(self):

        # Set the dark_mode setting in the CONFIG file to False

        config.set("UseDarkMode", "dark_mode", "False")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'no'
        self.dm_msgbox(choice)

    def dm_msgbox(self, choice):
        '''
        Confirmation popup that the configuration choice was saved
        '''
        if choice == 'yes':
            dm_info = tk.Toplevel(root)
            dm_info.title('Dark Mode configuration set')
            message = ttk.Label(dm_info,
                text = 'You have turned Dark Mode on\nPlease restart the application')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(dm_info, text = 'Ok', command=dm_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(dm_info)} center')
        else:
            dm_info = tk.Toplevel(root)
            dm_info.title('Dark Mode configuration set')
            message = ttk.Label(dm_info,
                text = 'You have turned Dark Mode off\nPlease restart the application')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(dm_info, text = 'Ok', command=dm_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(dm_info)} center')

class StartFullScreen():
    # Brings up the dialog box to set whether to start the program in fullscreen mode

    choice = 'None'

    def __init__(self):

        # Create the popup to select the configuration setting

        self.fswin = tk.Toplevel(root)
        self.fswin.title('Fullscreen statup configuration')
        if fullscreen == 'True':
            self.fs_status = ttk.Label(self.fswin, text = 'The start in fullscreen option is currently set to True')
            self.fs_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        else:
            self.fs_status = ttk.Label(self.fswin, text = 'The start in fullscreen option is currently set to False')
            self.fs_status.grid(column=1, row=1, columnspan=2, padx=10, pady=(15, 0), sticky='WE')
        self.msg = ttk.Label(self.fswin, text = 'Select whether you want to start the program in fullscreen')
        self.msg.grid(column=1, row=2, columnspan=2, padx=10, pady=(10, 25), sticky='WE')
        self.yes = ttk.Button(self.fswin, text = 'Yes', command=lambda:[self.fs_true(), self.fswin.destroy()])
        self.yes.grid(column=1, row=3, padx=10, pady=(0, 25), sticky='WE')
        self.no = ttk.Button(self.fswin, text = 'No', command=lambda:[self.fs_false(), self.fswin.destroy()])
        self.no.grid(column=2, row=3, padx=10, pady=(0, 25), sticky='WE')
        root.eval(f'tk::PlaceWindow {str(self.fswin)} center')

    def fs_true(self):

        # Set the fullscreen setting in the CONFIG file to True

        config.set("StartFullscreen", "fullscreen", "True")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'yes'
        self.fs_msgbox(choice)

    def fs_false(self):

        # Set the fullscreen setting in the CONFIG file to False

        config.set("StartFullscreen", "fullscreen", "False")
        with open('CONFIG', 'w+') as configfile:
            config.write(configfile)
        choice = 'no'
        self.fs_msgbox(choice)

    def fs_msgbox(self, choice):
        '''
        Confirmation popup that the configuration choice was saved
        '''
        if choice == 'yes':
            fs_info = tk.Toplevel(root)
            fs_info.title('Fullscreen startup configuration set')
            message = ttk.Label(fs_info,
                text = 'The program will now start up in Fullscreen mode')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(fs_info, text = 'Ok', command=fs_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(fs_info)} center')
        else:
            fs_info = tk.Toplevel(root)
            fs_info.title('Fullscreen startup configuration set')
            message = ttk.Label(fs_info,
                text = 'The program will now start up scaled\nbased on your screen geometry')
            message.grid(column=1, row=1, padx=10, pady=(25, 25), sticky='WE')
            close = ttk.Button(fs_info, text = 'Ok', command=fs_info.destroy)
            close.grid(column=1, row=2, padx=10, pady=(0, 10), sticky='WE')
            root.eval(f'tk::PlaceWindow {str(fs_info)} center')


class HelpWindow():
    '''
    Pops up the window with the program usage information
    '''
    def __init__(self, master=None):
        '''
        Create the new window to hold the help text
        '''
        self.helpwin = tk.Tk()
        width = int(root.winfo_screenwidth() / 2.5)
        height = int(root.winfo_screenheight() / 1.4)
        self.helpwin.geometry('%sx%s' % (width, height))
        self.helpwin.configure(background = background)
        self.helpwin.columnconfigure(0, weight = 1)
        self.helpwin.rowconfigure(0, weight = 1)
        self.helpwin.title('Program Usage')
        self.help_text()

    def help_text(self):
        '''
        Create a scrollbox to hold the help information, open the external
        help.txt file and read the contents into the scrollbox
        vbar troughcolor is gray73, background is gray80
        button background is gray77
        '''

        self.help_box = scrolledtext.ScrolledText(self.helpwin,
                                                  wrap=tk.WORD, bd=5, relief=tk.RIDGE)
        self.help_box.configure(background = entry_bg, foreground = text_color)
        self.help_box.vbar.configure(troughcolor = '#bababa', background = '#cccccc')
        self.help_box.grid(column=0, row=0, padx=8, pady=(0, 20), sticky = 'nsew')
        self.help_box.insert(1.0, help_text)
        self.help_box.configure(state = 'disabled')
        self.help_button = tk.Button(self.helpwin, text='Close', command=self.helpwin.destroy)
        self.help_button.configure(foreground = text_color, background = '#c4c4c4')
        self.help_button.grid(column=0, row=1, padx=50, pady=(0, 15), sticky='we')

class AboutWindow():
    '''
    Pops up the window showing version and license info
    '''
    def __init__(self):
        '''
        Create the window to display the 'about' information
        '''
        self.aboutwin = tk.Tk()
        self.aboutwin.configure(background = background)
        self.aboutwin.title('About')
        self.about_text()

    def about_text(self):
        '''
        Create a text box to hold the about information, open the external
        file ABOUT, and read the contents into the text box
        button background is gray77
        '''
        width = 75
        height = 30
        self.about_box = tk.Text(self.aboutwin, width=width, height=height,
                                 wrap=tk.WORD, bd=5, relief=tk.RIDGE)
        self.about_box.configure(background = entry_bg, foreground = text_color)
        self.about_box.grid(column=0, row=0, padx=8, pady=(0, 20))
        self.about_box.insert(1.0, about_text)
        self.about_box.configure(state = 'disabled')
        self.about_button = tk.Button(self.aboutwin, text='Close', command=self.aboutwin.destroy)
        self.about_button.configure(foreground = text_color, background = '#c4c4c4')
        self.about_button.grid(column=0, row=1, padx=50, pady=(0, 15), sticky='WE')

class Search():

    '''
    The main window where the search is performed
    '''
    def __init__(self, master):
        '''
        Hack to prevent the loss of the menu bar when switching
        frames in full screen.
        If the program was launched in fullscreen, instantly resizing
        the window size down and back to full brings the menu back seamlessly.

        The else statement is for when the program was maximized after launch.
        The global fs variable is for when the screen was maximized only after
        switching to the search window.
        I know, I know...
        '''

        if fullscreen == 'True' or fullscreen == 'true':
            width = int(root.winfo_screenwidth() / 1.9)
            height = int(root.winfo_screenheight() / 1.2)
            root.geometry('%sx%s' % (width, height))
            root.attributes('-zoomed', True)

        else:
            global fs
            fs = 'F'
            w = (root.winfo_width())
            h = (root.winfo_height())
            root.geometry('%sx%s' % (w-1, h-1))



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

    # Function to perform a search of the ingredients in all recipes

    def ingSearch(self):
            rec_files = glob.glob(search_path, recursive = True)
            search_str = self.search_entered.get()
            self.search_results = {}
            # Clear the results and display boxes of previous search, if any
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


    # Function to perform a search of the recipe titles

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

    # Function to display the selected recipe in the display box

    def viewRec(self, event):
            # separate the file names and their full paths into lists
            key_list = list(self.search_results.keys()) # full paths to files
            val_list = list(self.search_results.values()) # filenames from search results
            for i in self.results.curselection():
                    file = self.results.get(i) # get the currently selected filename
                    # Get the position of the filename in the list
                    position = val_list.index(file)
                    # Get and save the full path from the same position in the key list
                    self.cur_path = key_list[position]
                    self.display.delete(1.0, 'end') # clear recipe display box
                    # Open selected recipe using the full path
                    with open(key_list[position], 'r') as f:
                            contents = f.read()
                            self.display.insert(1.0, contents)

    def saveEdit(self):
            edited_file = self.display.get(1.0, 'end-1c') # copy contents of recipe display box
            # Write the edits to the original file
            with open(self.cur_path, "w") as file:
                    file.write(edited_file)
                    file.close()
            self.savebutton.config(state='disabled') # Disable save button after saving file

    # Function to enable the save button when the mouse is clicked in the
    # recipe display box
    # Clicking the save button with the box empty resulted in silent errors
    # that show up when running from CLI

    def saveEnable(self, arg):
            self.savebutton.config(state='normal')

    def _quit(self):
        '''
        Function to exit GUI cleanly
        Bound to the Exit command on the file menu
        '''
        root.quit()
        root.destroy()

    # Function to switch to the main window

    def create(self):
        MAIN(root)
        self.frame.pack_forget()

    def create_widgets(self):
        '''
        Long method to create all widgets on the root window
        '''

        # Creating a Menu Bar
        # Menu is a smaller version than on the main window since the
        # file menu had no purpose here and the config menu was
        # unnecessary on both pages

        menu_bar = Menu(root)
        root.config(menu=menu_bar)
        menu_bar.config(background = background, foreground = text_color)
        menu_bar.add_command(label='Create New recipe', command=self.create)

        # Code for the cascading Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Program Help  Ctrl+h')
        help_menu.add_separator()
        help_menu.add_command(label='About')
        help_menu.configure(background = background, foreground = text_color)
        menu_bar.add_cascade(label='Help', menu=help_menu)

        menu_bar.add_command(label='Quit', command=self._quit)

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
        # Save button disabled initially. It becomes enabled when the mouse
        # is clicked in the display pane to make any edits.
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
# Start GUI
#=============

if __name__ == "__main__":
    app = MAIN(root)
    root.mainloop()


