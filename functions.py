#Written by Feras Yahya. Helper functions for main module reportCard_gen.py

import pandas
import sys

'''
A function for reading files from command line input and returns a list of the file names.
'''

def read_files(*args):
    list = []
    for x in range(1, len(*args) -1):
        pandas.read_csv(sys.argv[x]).to_json(str(x) + ".json")
        list.append(str(x) +".json")
    return list

'''
A function for validating weights of a course. Takes a file parameter. Returns false if weights are not 100, else
returns true.
'''

def weight_validator(dict):
    Total_weight = 0                #A variable used for checking total weight of all courses is 100

    for id, val in dict['weight'].items():

        Total_weight += val

        if (dict['course_id'].get(id) != dict['course_id'].get( str(int(id)+1),None )):
            if (Total_weight != 100):
                return False
            else:
                Total_weight = 0

    return True
