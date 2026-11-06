import random
import helpers as h


def pretend_semesters(professor, miss_classes):
    '''This function simulates 1000 pretend versions of a semester
    and rolls a surprise test or activity in m assessment days.
    If any one of them happens in a missed class, that pretend semester counts as a risky one.
    risk factor = number of risky semesters / total semesters
    if the risk factor is greater than 10%, the student would be advised to not take the leaves. 
    If the risk factor is less than 10%, the student would be advised to take the leaves.
    Assumption is that the user's leave will start next class onwards and will go for n days
    '''
    n = miss_classes
    risky_semesters = 0
    total_semesters = 1000
    classes_so_far = professor.classes_so_far
    total_classes = professor.total_classes
    m = 5 #placeholder value for number of tests/activities expected in each semester
    #depends on the number of classes left, how strict the professor is etc
    for i in range(total_semesters):
        try:
            test_activity_days = h.random_unique(m, classes_so_far + 1, total_classes + 1)
        except ValueError:
            print('Subsequent classes less than intended leave')
            return
        else:
            miss_class_list = list(range(classes_so_far + 1, min(classes_so_far + n + 1, total_classes + 1)))
            risky = h.compare_two_lists(test_activity_days, miss_class_list)
            if risky:
                risky_semesters += 1

    risk_factor = risky_semesters/total_semesters
    print(risk_factor)
    #actual risk threshold will not be 0.1, but dependent on other factors like professor strictness and attendance frequency
    risk_threshold = 0.1
    if risk_factor >= risk_threshold:
        print('Too risky to miss class')
    else:
        print('Missing class is mostly safe')
        
strictness = {
    "Lenient professor":  {"m": 3, "threshold": 0.20}, #threshold-> max risk that could be taken
    "Moderate professor": {"m": 5, "threshold": 0.10},
    "Strict professor":   {"m": 8, "threshold": 0.05},
}
_levels= list(strictness)

def current_attendance(attended, held):
    return (100.0 * attended)/(held)
    
def risk_factor_simulation(classes_held, total_classes, leaves, m, total_semesters=1000):
    remaining= total_classes-classes_held
    ------ (left to be written) #risk factor
    
def classify_attendance_risk(p, min_p):
    if p >= min_p:
        return "Safe"
    diff = min_p - p
    if diff <= 2:
        return "Low"        # 73-74.99 when min is 75
    if diff <= 10:
        return "Moderate"   # 65-72.99
    return "High"           # below 65
    
def recover(attended, held, total, min_p): #no. of classes needed to recover to 75%
    p = min_p / 100
    remaining = total - held
    if held == 0 or attended / held >= p:
        return 0, True
    if p >= 1:
        return None, False
    x = math.ceil((p * held - attended) / (1 - p) - 0.00000001) #subtracted so that a number like 2.000000001 doesnt get round up to 3
    return (x, True) if x <= remaining else (x, False) #true/false to know if the student can recover from it or not

def future_attendance(attended,left,leave_days,total):
    to_attend=left-leave
    return 100*(to_attend)/total

def safe_or_risky(risk, limit,future_attendance):
    if future_attendance<75:
        return "Risky"
    return "Safe"
    
def what_if(classes_attended, classes_held, total_classes, leave_days, tests_expected):
    classes_left = total_classes - classes_held
    # chance that a surprise test falls on a class you miss
    risk = risk_factor_simulation(classes_held, total_classes, leave_days, tests_expected)
    # attendance % at the end if you attend everything except the leave days
    future_attendance = 100 * (classes_attended + classes_left - leave_days) / total_classes
    return risk, future_attendance

