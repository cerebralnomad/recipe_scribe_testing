#! /usr/bin/env python3

import glob

search_path = '/home/clay/Documents/recipes/**/*'

files = glob.glob(search_path, recursive = True)

# Search contents of files (ingredient search)

# Print and input statements for CLI testing purposes
# =================================================

class Main():
        def __init__(self):

            print("Choose the search type (1 or 2)")
            print("    1. Ingredient search")
            print("    2. Filename search" + '\n')

            search_type = input('Search type: ')
            print('')

            search_str = input("Enter search term: ")
            print('')

            if search_type == "1":
                    s = IngredientSearch()
                    s.ingSearch(search_str)

            if search_type == "2":
                    s = TitleSearch()
                    s.titleSearch(search_str)


class IngredientSearch():

        def ingSearch(self, term):

            search_str = term
            
            for file in files:
                    try:
                            with open(file, 'r') as f:
                                    contents = f.read()
                            if search_str in contents:
                                    result = file.rsplit('/', 2)
                                    print(result[1] + "/" + result[2])
                                    file.close()
                    except:
                            pass


# Search filenames

class TitleSearch():

        def titleSearch(self, term):

            search_str = term
            for file in files:
                    if search_str in file:
                            results = file.rsplit('/', 2)
                            print(results[1] + "/" + results[2])



Main()



