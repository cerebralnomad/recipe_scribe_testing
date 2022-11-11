# Recipe Scribe 2.0 TESTING

This repo is the sandbox for testing of Recipe Scribe 2.0  
Files here are normally unstable, and contain broken or partially working features.  
The stable 1.0 version can be found at [https://github.com/cerebralnomad/Recipe-Scribe](https://github.com/cerebralnomad/Recipe-Scribe)

## Main Feature Addition

The main development feature being worked on is a search and display of your 
existing recipes with editing capabilities.

Recipe creation will remain the same, but a new panel will allow you to search 
your existing files by keyword as either a Title search or by ingredient.
Selecting the recipe from the search results will display it for viewing or editing
 
## Progress

The search function is complete. As is the ability to edit and save existing recipes.
That part was developed stand alone and I'm now working on incorporating that code 
back into the main program.

A few minor bug fixes previously unnoticed have also been fixed, such as the invisible 
line cursor in light mode. 

Have also added a configuration option to start the program full screen if desired.
Realized this was helpful after moving to a dev machine with a smaller screen.

### Update

Search function is completely incorporated.

The program now automatically restarts when changing some of the configuration
options so they take effect immediately without having to manually exit and
restart.

Changed the button colors to match the selected theme.

Need to test as is on a machine running python3.6 then add the program icon and
test again
After adding the icon to the previous version the program would only run if
python 3.10 was installed.
Not sure if it was caused by the way I coded it or by pyinstaller.

Added the ability to search for two ingredients in the same recipe.

Program icon added and is working. Need to test on 3.6





