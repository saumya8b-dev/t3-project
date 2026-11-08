# Entry point. Run the app with:   streamlit run main.py
#
# attendance policy is not exactly the same for each professor. Some professors are more strict than others.
# Some professors have more classes than others.
#
# Files:
#   gui.py            - Streamlit interface; calls logicfunctions and storage
#   logicfunctions.py - risk simulations, attendance maths, what-if scenarios
#   helpers.py        - small random/list helpers used by logicfunctions
#   storage.py        - load/save courses to data.csv
#   models.py         - the Course class
from gui import gui

gui()