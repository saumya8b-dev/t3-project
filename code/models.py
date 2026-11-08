"""Course data model (kept separate from main.py/gui.py to avoid circular imports)."""


class Course:
    """One course's saved details.

    strictness_factor is stored as the index of the professor level
    (0 = Lenient, 1 = Moderate, 2 = Strict); attendance_threshold is a
    fraction (0.75 means 75%).
    """

    def __init__(self, name, strictness_factor=1, attendance_frequency=0,
                 total_classes=0, classes_so_far=0, attended_classes=0,
                 attendance_threshold=0.75):
        self.name = name
        self.strictness_factor = float(strictness_factor)
        self.attendance_frequency = float(attendance_frequency)
        self.total_classes = int(float(total_classes))
        self.classes_so_far = int(float(classes_so_far))
        self.attended_classes = int(float(attended_classes))
        self.attendance_threshold = float(attendance_threshold)