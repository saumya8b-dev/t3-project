# attendance policy is not exactly the same for each professor. Some professors are more strict than others. 
# Some professors have more classes than others. Some professors have more frequent attendance checks than others. 
# This class is meant to simulate a professor's attendance policy and how it affects the student's ability to take leaves.
import logicfunctions as lf
import storage as st
#strictness factor is the factor which tells how strict the professor is
#attendance frequency is the frequency of attendance checks
class Course:
    def __init__(self, name=None, strictness_factor=None, attendance_frequency=None, 
                 total_classes=None, classes_so_far=None, attended_classes=None, attendance_threshold=0.75):
        if name == None:
            self.name = input('Course name: ')
            self.strictness_factor = float(input(f"Enter the strictness factor for {self.name}: "))
            self.attendance_frequency = float(input(f"Enter the attendance frequency for {self.name}: "))
            self.total_classes = int(input(f"Enter the total number of classes for {self.name}: "))
            self.classes_so_far = int(input(f"Enter the number of classes that have already occurred for {self.name}: "))
            self.attended_classes = int(input(f"Enter the number of classes attended by the student for {self.name}: "))
            self.attendance_threshold = 0.75
        else:
            self.name = name
            self.strictness_factor = float(strictness_factor)
            self.attendance_frequency = float(attendance_frequency)
            self.total_classes = int(total_classes)
            self.classes_so_far = int(classes_so_far)
            self.attended_classes = int(attended_classes)
            self.attendance_threshold = float(attendance_threshold)
#initialise an empty list to store the courses
L = []
#actual value will be loaded from a csv file
#this code demonstrates how data can be loaded and saved to and fro csv, not actual code.
#load and save to csv was successful
st.load_data(L, Course)

course1 = Course() 
L.append(course1)
st.save_data(L)


print([i.name for i in L])
#lf.pretend_semesters(course1, 1)