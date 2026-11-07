import random
import helpers as h
import math

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
    
def simulate_risk_factor(classes_so_far, total_classes, leave_days, tests_expected):
    classes_left = total_classes - classes_so_far
    tests_expected = min(tests_expected, classes_left) #to prevent more tests than there are classes left
    
    if classes_left <= 0 or leave_days <= 0 or tests_expected <= 0:
        return 0
        
    next_class = classes_so_far + 1
    last_class = total_classes

    # the classes you will miss i.e. from the next class
    last_missed_class = min(classes_so_far + leave_days, total_classes) #for a continous leave
    missed_classes = list(range(next_class, last_missed_class + 1)) #gives missed classes in a list

    total_simulations = 1000
    risky_count = 0
    for i in range(total_simulations):
        test_days = h.random_unique(tests_expected, next_class, last_class + 1)
        if h.compare_two_lists(test_days, missed_classes):
            risky_count += 1

    return risky_count / total_simulations
    
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

def future_attendance_pct(attended,left,leave_days,total):
    to_attend=left-leave_days
    return 100*(to_attend)/total

def safe_or_risky(risk, limit,future_attendance):
    if future_attendance<75:
        return "Risky"
    return "Safe"
    
def what_if(classes_attended, classes_held, total_classes, leave_days, tests_expected):
    classes_left = total_classes - classes_held
    # chance that a surprise test falls on a class you miss
    risk = simulate_risk_factor(classes_held, total_classes, leave_days, tests_expected)
    # attendance % at the end if you attend everything except the leave days
    future_attendance = 100 * (classes_attended + classes_left - leave_days) / total_classes
    return risk, future_attendance


def what_if_flu(classes_attended, classes_so_far, total_classes, tests_expected,
                min_attendance_pct, leave_days):
    classes_left = total_classes - classes_so_far
    future_classes = list(range(classes_so_far + 1, total_classes + 1))
    leave_days = min(leave_days, classes_left)
    tests = min(tests_expected, classes_left)

    total_simulations = 1000
    risky_count = 0
    if classes_left > 0:
        for i in range(total_simulations):
            start = random.randint(0, classes_left - leave_days) #This picks where the flu starts, as a position in the list
            missed_classes = future_classes[start:start + leave_days] #This cuts a slice out of the list of the classes you missed
            test_days = random.sample(future_classes, tests) #picks random test days
            if set(missed_classes) & set(test_days): #converts to set and takes intersection 
                risky_count += 1
    risk = risky_count / total_simulations

    future_attendance = future_attendance_pct(classes_attended, classes_so_far, total_classes, leave_days)
    return (f"{leave_days}-day flu", risk, future_attendance,
            safe_or_risky(risk, future_attendance, min_attendance_pct))


def what_if_professor_gets_strict(classes_attended, classes_so_far, total_classes, tests_expected, #same as flu but with tests on random days
                                  min_attendance_pct, leave_days, max_extra_tests):
    classes_left = total_classes - classes_so_far
    future_classes = list(range(classes_so_far + 1, total_classes + 1))
    leave_days = min(leave_days, classes_left)

    total_simulations = 1000
    risky_count = 0
    if classes_left > 0:
        for i in range(total_simulations):
            extra_tests = random.randint(1, max(1, max_extra_tests))   # random 1 to max
            tests = min(tests_expected + extra_tests, classes_left)
            start = random.randint(0, classes_left - leave_days)
            missed_classes = future_classes[start:start + leave_days]
            test_days = random.sample(future_classes, tests)
            if set(missed_classes) & set(test_days):
                risky_count += 1
    risk = risky_count / total_simulations

    future_attendance = future_attendance_pct(classes_attended, classes_so_far, total_classes, leave_days)
    return ("Professor gets strict", risk, future_attendance,
            safe_or_risky(risk, future_attendance, min_attendance_pct))


# 3) Classes cancelled: the user chooses how many are cancelled and the leave
def what_if_classes_cancelled(classes_attended, classes_so_far, total_classes, tests_expected,
                              min_attendance_pct, cancelled_classes, leave_days):
    new_total_classes = total_classes - cancelled_classes
    future_classes = list(range(classes_so_far + 1, total_classes + 1))

    total_simulations = 1000
    risky_count = 0
    if len(future_classes) > cancelled_classes:
        for i in range(total_simulations):
            cancelled = random.sample(future_classes, cancelled_classes) #picks 2 different random classes to cancel
            open_classes = [c for c in future_classes if c not in cancelled] #not cancelled
            days_off = min(leave_days, len(open_classes))
            tests = min(tests_expected, len(open_classes))
            start = random.randint(0, len(open_classes) - days_off)
            missed_classes = open_classes[start:start + days_off]
            test_days = random.sample(open_classes, tests)
            if set(missed_classes) & set(test_days):
                risky_count += 1
    risk = risky_count / total_simulations

    future_attendance = future_attendance_pct(classes_attended, classes_so_far, new_total_classes, leave_days)
    return (f"{cancelled_classes} classes cancelled", risk, future_attendance,
            safe_or_risky(risk, future_attendance, min_attendance_pct))


# 4) Sick in quiz week: the user chooses the sick days and the quiz week length
def what_if_sick_in_quiz_week(classes_attended, classes_so_far, total_classes, tests_expected,
                              min_attendance_pct, leave_days, quiz_week_length):
    classes_left = total_classes - classes_so_far
    future_classes = list(range(classes_so_far + 1, total_classes + 1))
    leave_days = min(leave_days, classes_left)
    quiz_week_length = min(quiz_week_length, classes_left)
    tests = min(tests_expected, classes_left)

    total_simulations = 1000
    risky_count = 0
    if classes_left > 0:
        for i in range(total_simulations):
            week_start = random.randint(0, classes_left - quiz_week_length) #picks where the quiz week begins in the list
            quiz_week = future_classes[week_start:week_start + quiz_week_length]
            quiz_day = random.choice(quiz_week) #picks the one day in that week when the quiz happens

            last_start = max(week_start, week_start + quiz_week_length - leave_days)
            sick_start = random.randint(week_start, last_start)
            missed_classes = future_classes[sick_start:sick_start + leave_days]

            test_days = random.sample(future_classes, tests)   
            if quiz_day in missed_classes or set(missed_classes) & set(test_days):
                risky_count += 1
    risk = risky_count / total_simulations

    future_attendance = future_attendance_pct(classes_attended, classes_so_far, total_classes, leave_days)
    return (f"Sick {leave_days} days in quiz week", risk, future_attendance,
            safe_or_risky(risk, future_attendance, min_attendance_pct))

