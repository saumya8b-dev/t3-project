import random
import helpers as h


def pretend_semesters(professor, miss_classes):
    '''This function simulates 1000 pretend versions of a semester
    and rolls a surprise test or activity in n leaves the student wishes to take
    If any one of them happens in a missed class, that pretend semester counts as a risky one.
    risk factor = number of risky semesters / total semesters
    if the risk factor is greater than 10%, the student would be advised to not take the leaves. 
    If the risk factor is less than 10%, the student would be advised to take the leaves.
    Assumption is that the user's leave will start next class onwards
    '''
    n = miss_classes
    risky_semesters = 0
    total_semesters = 1000
    classes_so_far = professor.classes_so_far
    total_classes = professor.total_classes

    for i in range(total_semesters):
        try:
            test_activity_days = h.random_unique(n, classes_so_far + 1, total_classes + 1)
        except ValueError:
            print('Subsequent classes less than intended leave')
        else:
            miss_class_list = list(range(classes_so_far + 1, classes_so_far + n + 1))
            risky = h.compare_two_lists(test_activity_days, miss_class_list)
            if risky:
                risky_semesters += 1

    risk_factor = risky_semesters/total_semesters
    print(risk_factor)
    #actual risk threshold will not be 0.1, but dependent on other factors
    risk_threshold = 0.1
    if risk_factor > risk_threshold:
        print('Too risky to miss class')
    else:
        print('Missing class is mostly safe')
            