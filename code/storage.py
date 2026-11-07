'''
this python file will contain libraries for saving, storing, loading and modifying all the data
'''

import csv
csv_file = 'data.csv'
def save_data(L):
    if not L:
        return
    with open(csv_file, 'w', newline = '') as f:
        header = L[0].__dict__.keys()
        w = csv.DictWriter(f, fieldnames = header)
        w.writeheader()
        for i in L:
            w.writerow(i.__dict__)
def load_data(L, Course):
    with open(csv_file, 'r', newline = '') as f:
        r = csv.DictReader(f)
        for i in r:
            course = Course(**i)
            L.append(course)
def add_course(course, L):
    L.append(course)
