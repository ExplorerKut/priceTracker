import pandas
from os.path import exists

file_exists= exists("test.csv")
if not file_exists:
    with open("test.csv",'w') as file_new:
        pass