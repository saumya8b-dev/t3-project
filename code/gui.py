import streamlit as st

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
                st.error(f"You would need **{needed}** more classes in a row to reach {min_pct:.0f}%, "
                         f"but only {classes_left} are left - you can't recover.")

        st.markdown("---")

        # ---- the planned leave ----
        st.markdown("<h4 style='color: black;'>Planned leave</h4>", unsafe_allow_html=True)
        if classes_left == 0:
            st.info("The course is over - no classes left to take leave from.")
            return

        leave_days = min(leave_days, classes_left)
        risk = lf.simulate_risk_factor(held, total_classes, leave_days, tests_expected)
        future_pct = lf.future_attendance_pct(attended, held, total_classes, leave_days)
        verdict = lf.safe_or_risky(risk, future_pct, min_pct, risk_threshold)

        r1, r2, r3 = st.columns(3)
        r1.metric("Chance a test hits your leave", f"{risk * 100:.1f}%")
        r2.metric("Final attendance after leave", f"{future_pct:.1f}%")
        r3.metric("Verdict", verdict)

        if verdict == "Safe":
            st.success(f"Taking {leave_days} day(s) off looks safe.")
        else:
            reasons = []
            if future_pct < min_pct:
                reasons.append(f"final attendance ({future_pct:.1f}%) would fall below {min_pct:.0f}%")
            if risk > risk_threshold:
                reasons.append(f"the test risk ({risk * 100:.1f}%) is above the {risk_threshold * 100:.0f}% limit for this professor")
            st.error(f"Taking {leave_days} day(s) off is risky: " + " and ".join(reasons) + ".")

        # max number of leave days that is still safe (leave starting from next class)
        max_safe = 0
        for d in range(1, classes_left + 1):
            r = lf.simulate_risk_factor(held, total_classes, d, tests_expected)
            f = lf.future_attendance_pct(attended, held, total_classes, d)
            if lf.safe_or_risky(r, f, min_pct, risk_threshold) == "Safe":
                max_safe = d
            else:
                break
        st.write(f"**Safe leave count:** about **{max_safe}** class(es) from the next class onwards.")

        # ---- what-if scenarios ----
        with st.expander("What-if scenarios"):
            w1, w2, w3 = st.columns(3)
            with w1:
                max_extra = st.number_input("Max extra tests if professor gets strict", min_value=1, value=3, step=1, key=f"extra_{course_name}")
            with w2:
                cancelled = st.number_input("Classes cancelled", min_value=0, value=2, step=1, key=f"cancel_{course_name}")
            with w3:
                quiz_len = st.number_input("Quiz week length (classes)", min_value=1, value=5, step=1, key=f"quizlen_{course_name}")

            rows = [
                lf.what_if_flu(attended, held, total_classes, tests_expected, min_pct, leave_days, risk_threshold),
                lf.what_if_professor_gets_strict(attended, held, total_classes, tests_expected, min_pct,
                                                 leave_days, int(max_extra), risk_threshold),
                lf.what_if_classes_cancelled(attended, held, total_classes, tests_expected, min_pct,
                                             int(cancelled), leave_days, risk_threshold),
                lf.what_if_sick_in_quiz_week(attended, held, total_classes, tests_expected, min_pct,
                                             leave_days, int(quiz_len), risk_threshold),
            ]
            st.table([
                {"Scenario": name,
                 "Test risk": f"{rk * 100:.1f}%",
                 "Final attendance": f"{fa:.1f}%",
                 "Verdict": vd}
                for name, rk, fa, vd in rows
            ])

    def main():
        initialize_session_state()
        render_sidebar()

        # Main Panel Header
        st.markdown(
            """
            <div style="background-color: #ffb347; padding: 12px; border-radius: 8px; text-align: center;">
                <h1 style="color: black; margin: 0; font-size: 28px;">Safe_Leave_Count</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

        #Course Selected
        course_name = st.session_state.selected_course
        if course_name:
            st.markdown(
                f"<h3 style='color: black;'>Course Selected: 📌 {course_name}</h3>",
                unsafe_allow_html=True,
            )

            saved = load_saved_course(course_name)  # prefill from data.csv if this course was saved before

            #Inputs
            c1, c2, c3 = st.columns(3)   #st.columns makes 3 columns st.number_input takes number inputs from the user
            with c1:
                total_classes = st.number_input(
                    "Total classes:", value=saved.total_classes if saved else None, step=1,
                    min_value=1, placeholder="e.g. 40", key=f"total_{course_name}")
            with c2:
                min_attendance_pct = st.number_input(
                    "Minimum attendance(%)",
                    value=int(round(saved.attendance_threshold * 100)) if saved else None,
                    step=1, min_value=1, max_value=100, placeholder="e.g. 75", key=f"minpct_{course_name}")
            with c3:
                default_level = int(saved.strictness_factor) if saved and 0 <= int(saved.strictness_factor) < len(LEVELS) else 1
                professor_strictness = st.selectbox(
                    "Professor strictness factor", LEVELS, index=default_level, key=f"strict_{course_name}")

            st.markdown("---") #makes a divider (line)

            # Live Attendance Inputs #makes 3 columns att=> attendance
            st.markdown("<h3 style='color: black;'>📊 Live Attendance & Leave Status</h3>", unsafe_allow_html=True)
            att_col1, att_col2, att_col3 = st.columns(3)
            with att_col1:
                classes_attended = st.number_input(
                    "Classes attended so far:", value=saved.attended_classes if saved else None, step=1,
                    min_value=0, placeholder="e.g. 30", key=f"att_{course_name}")
            with att_col2:
                classes_missed = st.number_input(
                    "Leaves / classes missed so far:",
                    value=(saved.classes_so_far - saved.attended_classes) if saved else None, step=1,
                    min_value=0, placeholder="e.g. 3", key=f"miss_{course_name}")
            with att_col3:
                leave_days = st.number_input(
                    "Planned leave (classes from next class):", value=1, step=1,
                    min_value=1, key=f"leave_{course_name}")

            if st.button("💾 Save course details", key=f"save_{course_name}"):
                if None in (total_classes, min_attendance_pct, classes_attended, classes_missed):
                    st.warning("Fill in all the details before saving.")
                else:
                    save_course(Course(
                        name=course_name,
                        strictness_factor=LEVELS.index(professor_strictness),
                        attendance_frequency=0,
                        total_classes=total_classes,
                        classes_so_far=int(classes_attended) + int(classes_missed),
                        attended_classes=classes_attended,
                        attendance_threshold=float(min_attendance_pct) / 100,
                    ))
                    st.success(f"Saved {course_name}.")

            st.markdown("---")

            # Lower Section: Analytics area & Logo
            graph_col, logo_col = st.columns([2, 1]) #[2,1] is the width ratio of columns
            with graph_col:
                st.markdown("<h4 style='color: black;'>Attendance Analytics</h4>", unsafe_allow_html=True)
                render_analytics(course_name, total_classes, min_attendance_pct, professor_strictness,
                                 classes_attended, classes_missed, leave_days)

            with logo_col:
                st.markdown("<h4 style='color: black;'>Logo</h4>", unsafe_allow_html=True)
                render_logo(is_compact=True)

        #No Course Selected
        else:
            st.markdown(
                "<h3 style='text-align: center; color: #555; margin-top: 20px;'>👈 Click a course code on the left sidebar to enter details and check leave counts.</h3>",
                unsafe_allow_html=True,
            )

            _, center_logo_col, _ = st.columns([1, 1, 1]) # [1,1,1] centers the logo with 2 blank columns on both sides
            with center_logo_col:
                render_logo(is_compact=False)

    main()


if __name__ == "__main__":
    gui()
