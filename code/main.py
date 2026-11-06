# attendance policy is not exactly the same for each professor. Some professors are more strict than others. 
# Some professors have more classes than others. Some professors have more frequent attendance checks than others. 
# This class is meant to simulate a professor's attendance policy and how it affects the student's ability to take leaves.
import logicfunctions as lf
#strictness factor is the factor which tells how strict the professor is
#attendance frequency is the frequency of attendance checks
class Course:
    def __init__(self, name, strictness_factor, attendance_frequency):
        self.name = name
        self.strictness_factor = strictness_factor
        self.attendance_frequency = attendance_frequency
        self.total_classes = int(input(f"Enter the total number of classes for {self.name}: "))
        self.classes_so_far = int(input(f"Enter the number of classes that have already occurred for {self.name}: "))
        self.attended_classes = int(input(f"Enter the number of classes attended by the student for {self.name}: "))
        self.attendance_threshold = 0.75

#initialise an empty list to store the professors
#prof1 is testing placeholder meant to be removed
#actual value will be loaded from a csv file
course1 = Course('A', 0.3, 0.5) 
professors = [course1]

lf.pretend_semesters(course1, 1)