'''
this python file will contain libraries for saving, storing, loading and modifying all the data
'''

import csv
import os

# always next to this file, so it works no matter where the app is launched from
csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv')

FIELDS = ["name", "strictness_factor", "attendance_frequency", "total_classes",
          "classes_so_far", "attended_classes", "attendance_threshold"]


def save_data(L):
    if not L:
        return
    with open(csv_file, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for i in L:
            w.writerow({k: getattr(i, k) for k in FIELDS})


def load_data(L, Course):
    if not os.path.exists(csv_file):
        return
    with open(csv_file, 'r', newline='') as f:
        r = csv.DictReader(f)
        for i in r:
            if not i.get("name"):
                continue
            L.append(Course(**i))


def load_course(name):
    """Return the saved Course whose name matches `name`, or None if there
    is no saved data for it (missing file, empty file, or course not saved)."""
    from models import Course  # imported here to keep storage.py independent of models at import time
    courses = []
    try:
        load_data(courses, Course)
    except (OSError, ValueError, TypeError, KeyError):
        return None
    for c in courses:
        if c.name == name:
            return c
    return None


def add_course(course, L):
    """Add a course, replacing any existing one with the same name."""
    for idx, existing in enumerate(L):
        if existing.name == course.name:
            L[idx] = course
            return
    L.append(course)