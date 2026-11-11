import streamlit as st
import matplotlib.pyplot as plt

import logicfunctions as lf
import storage
from models import Course


def gui():
    PAGE_TITLE = "Safe Leave Count"
    PAGE_ICON = "📅"
    COURSES = ["CS101", "PH101", "CH101", "CH102", "HS101", "ME101", "CH103", "MA101", "NO101"]
    LEVELS = list(lf.strictness)  # ["Lenient professor", "Moderate professor", "Strict professor"]

    # Define a safe fallback if LOGO_BASE64 isn't set elsewhere
    LOGO_BASE64 = globals().get("LOGO_BASE64", None)
    #define logo/photos in base 64 or remove entirely if we have to

    # ==========================================
    # PAGE SETUP & STYLING
    # ==========================================
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide") #sets the browser tab title and icon and layout="wide" makes the content use the full screen width.

    st.markdown( #to add custom css #ffe5b4 -> peach #ffa54f -> orange !important so it does not get overwritten (input labels)
        """
        <style>
        .stApp { background-color: #ffe5b4; }
        section[data-testid="stSidebar"] { background-color: #ffa54f; }
        .stNumberInput label p, .stSelectbox label p, .stSlider label p, div[data-baseweb="select"] span {
            color: black !important;
            font-weight: 600 !important;
        }
        .header-anchor-link, [data-testid="stHeaderAnchor"] {
                display: none !important;
                }
        /* force light rendering even if the browser/OS is in dark mode */
        :root, .stApp { color-scheme: light !important; }
        /* catch-all: any text that isn't covered below stays black */
        .stApp, .stApp *, [data-testid="stSidebar"] * { color: black !important; }
        .stApp input::placeholder { color: #777 !important; }
        
        /* FIX: Input boxes border styling to remove harsh black borders and match theme */
        .stApp input, .stApp textarea { 
            color: black !important; 
            background-color: white !important; 
            border: 1px solid #e68a00 !important;
            border-radius: 8px !important;
        }
        .stApp input:focus, .stApp textarea:focus {
            border-color: #cc7a00 !important;
            box-shadow: 0 0 0 1px #cc7a00 !important;
        }
        div[data-baseweb="select"] > div { 
            background-color: white !important; 
            border: 1px solid #e68a00 !important;
            border-radius: 8px !important;
        }
        [data-testid="stNumberInput"] > div > div {
            border: 1px solid #e68a00 !important;
            border-radius: 8px !important;
            background-color: white !important;
        }

        /* buttons (sidebar course buttons + save button): light background, dark text */
        .stButton > button, [data-testid^="stBaseButton"], [data-testid="stSidebar"] button {
            background-color: #fff3e0 !important;
            border: 1px solid #e68a00 !important;
            border-radius: 8px !important;
        }
        .stButton > button:hover, [data-testid^="stBaseButton"]:hover, [data-testid="stSidebar"] button:hover {
            background-color: #ffd699 !important;
            border-color: #cc7a00 !important;
        }
        .stButton > button:active, [data-testid^="stBaseButton"]:active { background-color: #ffb347 !important; }
        /* number input +/- stepper buttons */
        [data-testid="stNumberInput"] button { background-color: #fff3e0 !important; }
        /* keep all normal text dark on the light background (Streamlit's dark mode makes it white) */
        .stApp p, .stApp li, .stApp label, .stApp label p,
        .stApp [data-testid="stMarkdownContainer"] p,
        [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *,
        [data-testid="stMetricValue"], [data-testid="stMetricValue"] *,
        [data-testid="stExpander"] summary, [data-testid="stExpander"] summary *,
        [data-testid="stTable"] th, [data-testid="stTable"] td {
            color: black !important;
        }
        [data-testid="stExpander"] { background-color: #fff3e0; border-radius: 8px; }
        [data-testid="stTable"] table { background-color: #fff3e0; }
        </style>
        """,
        unsafe_allow_html=True, #to render html and css
    )

    # ==========================================
    # HELPER FUNCTIONS
    # ==========================================
    def initialize_session_state(): #checks if any course is selected or not
        if "selected_course" not in st.session_state:
            st.session_state.selected_course = None

    def render_sidebar(): #Renders the sidebar navigation and course buttons
        with st.sidebar:
            st.markdown(
                "<h2 style='text-align: center; color: black;'>Safe leave count</h2>",
                unsafe_allow_html=True,
            )
            st.markdown("---")

            for course in COURSES:
                if st.button(course, use_container_width=True, key=f"btn_{course}"): #key updates when course is changed i.e. course clicked is shown
                    st.session_state.selected_course = course

            st.markdown("---")

    def render_logo(is_compact=False):
        """Renders the logo or a dashed placeholder box."""
        if LOGO_BASE64:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="{LOGO_BASE64}" style="width: 100%; border-radius: 8px;">
                </div>
                """,
                unsafe_allow_html=True,
            )
        else: #to be removed
            padding = "10px" if is_compact else "30px"
            st.markdown(
                f"""
                <div style="border: 2px dashed #ffa54f; padding: {padding}; text-align: center; border-radius: 8px; background-color: #fff3e0;">
                    <p style="color: #555; margin:0;"><b>[Logo Placeholder]</b><br>Your logo will appear here</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def load_saved_course(name):
        """Returns the saved Course for `name`, or None."""
        return storage.load_course(name)

    def save_course(course):
        courses = []
        try:
            storage.load_data(courses, Course)
        except (OSError, ValueError, TypeError):
            courses = []
        storage.add_course(course, courses)
        storage.save_data(courses)

    # ---- GRAPH 1 FUNCTION: Attendance Over the Rest of the Course ----
    def plot_attendance_projection(x_classes, y_lines):
        plt.figure(figsize=(8, 4))

        plt.plot(x_classes, y_lines["no_leave"], label="Attend all remaining", color="green", marker="o")
        plt.plot(x_classes, y_lines["with_leave"], label="With planned leave", color="orange", marker="o")
        plt.plot(x_classes, y_lines["min_req"], label="Minimum required", color="red", linestyle="--")

        plt.title("Attendance Over the Rest of the Course")
        plt.xlabel("Class Number")
        plt.ylabel("Attendance (%)")
        plt.ylim(0, 105)
        plt.grid(True)
        plt.legend()

        st.pyplot(plt)

    # ---- GRAPH 2 FUNCTION: Leave Days vs. Final Attendance ----
    def plot_leave_vs_attendance(x_leave, y_lines):
        plt.figure(figsize=(6, 4))

        plt.plot(x_leave, y_lines["final_att"], label="Final attendance", color="blue", marker="o")
        plt.plot(x_leave, y_lines["min_req"], label="Minimum required", color="red", linestyle="--")

        plt.title("Leave Days vs. Final Attendance")
        plt.xlabel("Leave Days (Classes Skipped)")
        plt.ylabel("Final Attendance (%)")
        plt.ylim(0, 105)
        plt.grid(True)
        plt.legend()

        st.pyplot(plt)

    # ---- GRAPH 3 FUNCTION: Leave Days vs. Test Risk ----
    def plot_leave_vs_risk(x_leave, y_lines):
        plt.figure(figsize=(6, 4))

        plt.plot(x_leave, y_lines["test_risk"], label="Chance of surprise test", color="purple", marker="o")
        plt.plot(x_leave, y_lines["risk_limit"], label="Professor risk threshold", color="red", linestyle="--")

        plt.title("Leave Days vs. Test Risk")
        plt.xlabel("Leave Days (Classes Skipped)")
        plt.ylabel("Test Risk (%)")
        plt.ylim(0, 105)
        plt.grid(True)
        plt.legend()

        st.pyplot(plt)

    def render_analytics(course_name, total_classes, min_attendance_pct, professor_strictness,
                         classes_attended, classes_missed, leave_days):
        """All the calculations/results for the selected course."""
        if None in (total_classes, min_attendance_pct, classes_attended, classes_missed):
            st.info("Fill in total classes, minimum attendance, classes attended and classes missed to see the analysis.")
            return

        total_classes = int(total_classes)
        min_pct = float(min_attendance_pct)
        attended = int(classes_attended)
        held = attended + int(classes_missed)
        leave_days = int(leave_days)

        if held > total_classes:
            st.error("Attended + missed classes can't be more than the total number of classes.")
            return
        if held == 0:
            st.info("No classes held yet - nothing to analyse.")
            return

        settings = lf.strictness[professor_strictness]
        tests_expected = settings["m"]
        risk_threshold = settings["threshold"]
        classes_left = total_classes - held

        # ---- current standing ----
        current_pct = lf.current_attendance(attended, held)
        level = lf.classify_attendance_risk(current_pct, min_pct)
        needed, can_recover = lf.recover(attended, held, total_classes, min_pct)

        m1, m2, m3 = st.columns(3)
        m1.metric("Current attendance", f"{current_pct:.1f}%")
        m2.metric("Attendance status", level)
        m3.metric("Classes left", classes_left)

        if level != "Safe":
            if needed is None:
                st.warning("A 100% minimum can't be recovered once a class has been missed.")
            elif can_recover:
                st.warning(f"You need to attend the next **{needed}** classes in a row to get back to {min_pct:.0f}%.")
            else:
                st.error(f"You would need **{needed}** more classes in a row to reach {min_
