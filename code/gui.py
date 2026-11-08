import streamlit as st

PAGE_TITLE = "Safe Leave Count"
PAGE_ICON = "📅"
COURSES = ["CS101", "PH101", "CH101", "CH102", "HS101", "ME101", "CH103", "MA101", "NO101"]

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
    if st.session_state.selected_course:
        st.markdown(
            f"<h3 style='color: black;'>Course Selected: 📌 {st.session_state.selected_course}</h3>",
            unsafe_allow_html=True,
        )

        #Inputs
        c1, c2, c3 = st.columns(3)   #st.columns makes 3 columns st.number_input takes number inputs from the user
        with c1:
            total_classes = st.number_input("Total classes:", value=None, step=1, min_value=1, placeholder="e.g. 40")
        with c2:
            min_attendance_pct = st.number_input("Minimum attendance(%)", value=None, step=1, min_value=1, max_value=100, placeholder="e.g. 75")
        with c3:
            professor_strictness = st.selectbox("Professor strictness factor", ["Lenient professor", "Moderate professor", "Strict professor"])

        st.markdown("---") #makes a divider (line)

        # Live Attendance Inputs #makes 2 columns att=> attendance
        st.markdown("<h3 style='color: black;'>📊 Live Attendance & Leave Status</h3>", unsafe_allow_html=True)
        att_col1, att_col2 = st.columns(2)
        with att_col1:
            classes_attended = st.number_input("Classes attended so far:", value=None, step=1, min_value=0, placeholder="e.g. 30")
        with att_col2:
            classes_missed = st.number_input("Leaves / classes missed so far:", value=None, step=1, min_value=0, placeholder="e.g. 3")

        st.markdown("---")

        # Lower Section: Analytics area & Logo (add your new functions here)
        graph_col, logo_col = st.columns([2, 1]) #[2,1] is the width ratio of columns
        with graph_col:
            st.markdown("<h4 style='color: black;'>Attendance Analytics</h4>", unsafe_allow_html=True)
            # TODO: add your analytics / calculations here

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


if __name__ == "__main__":
    main()
