import streamlit as st
import sqlite3
import pandas as pd


DB_NAME = "jobs.db"


def load_jobs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY scraped_at DESC", conn)
    conn.close()
    return df


# 1. Page Configuration
st.set_page_config(
    layout="wide",
    page_title="DEET | Digital Employment Exchange",
    initial_sidebar_state="expanded",
)

# --- INITIALIZE SESSION STATES ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Syncing Profile Data with Login/Signup
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "name": "",
        "email": "",
        "mobile": "",
    }


def nav_to(page_name: str) -> None:
    st.session_state.page = page_name


# 2. Custom CSS
st.markdown(
    """
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

    .stApp { background-color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0; }
    
    /* Auth Container */
    .auth-card {
        max-width: 450px;
        margin: 0 auto;
        padding: 40px;
        background: white;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .user-profile { padding: 10px; margin-bottom: 10px; border-bottom: 1px solid #eee; }
    .user-name { font-weight: bold; font-size: 16px; margin-bottom: 0; color: #1E293B; }
    .user-email { color: #64748B; font-size: 12px; }

    .notif-bar { background-color: #001F3F; color: white; padding: 12px 20px; border-radius: 8px; font-size: 14px; margin-bottom: 25px; }
    .banner-card { padding: 25px; border-radius: 15px; color: white; height: 160px; margin-bottom: 20px; }
    .blue-grad { background: linear-gradient(135deg, #4EA8DE, #1E88E5); }
    .pink-grad { background: linear-gradient(135deg, #F06292, #D81B60); }
    
    .progress-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    .bar-bg { background: #E2E8F0; border-radius: 10px; height: 8px; width: 100%; margin-top: 10px; }
    .bar-fill { background: #001F3F; height: 8px; border-radius: 10px; width: 64%; }

    .icon-box { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 15px; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center; }
    .stat-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; text-align: center; }
    .stat-val { font-size: 26px; font-weight: 700; color: #0F172A; }
    .stat-lbl { font-size: 12px; color: #64748B; font-weight: 500; }
    
    /* Logo Alignment */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- AUTHENTICATION ROUTING ---
if not st.session_state.logged_in:
    # Centered Logo for Auth Pages
    col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
    with col_l2:
        st.image("img.jpeg", width=250)

    if st.session_state.auth_mode == "login":
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.title("Login")
        st.caption("Access the Digital Employment Exchange")

        login_email = st.text_input("Email / Mobile Number")
        login_pass = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True, type="primary"):
            if login_email:  # Basic check
                st.session_state.user_data["name"] = login_email.split("@")[0].capitalize()
                st.session_state.user_data["email"] = login_email
                st.session_state.logged_in = True
                st.rerun()

        st.write("---")
        if st.button("New User? Signup", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    else:  # Signup
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.title("Signup")
        st.caption("Create your DEET account")

        s_name = st.text_input("Full Name")
        s_email = st.text_input("Email")
        s_mobile = st.text_input("Mobile Number")
        s_pass = st.text_input("Password", type="password")

        if st.button("Create Account", use_container_width=True, type="primary"):
            if s_name and s_email and s_mobile:
                st.session_state.user_data = {
                    "name": s_name,
                    "email": s_email,
                    "mobile": s_mobile,
                }
                st.session_state.logged_in = True
                st.rerun()

        if st.button("Already have an account? Login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD (Only shown when logged in) ---
else:
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        # Added Logo to Top of Sidebar
        st.image("img.jpeg", use_container_width=True)
        # Logic to handle different data structures
        u = st.session_state.user_data
        # If database format (a.py) exists, use it; otherwise use the hardcoded format (app.py)
        display_name = u.get("name", u.get("first_name", "User"))
        if u.get("surname"):
            display_name += f" {u.get('surname')}"

        st.markdown(
            f"""
            <div class="sidebar-profile">
                <div class="user-avatar"><i class="fas fa-user-circle"></i></div>
                <p class="user-name">{display_name}</p>
                <p class="user-email">{u.get('email', '')}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("Home", use_container_width=True):
            nav_to("Home")
        if st.button("My Profile", use_container_width=True):
            nav_to("My Profile")
        if st.button("Jobs", use_container_width=True):
            nav_to("Jobs")
        if st.button("AI Recommendations", use_container_width=True):
            nav_to("AI Recommendations")
        if st.button("Activity", use_container_width=True):
            nav_to("Activity")
        if st.button("Conversation", use_container_width=True):
            nav_to("Conversation")
        if st.button("Interviews", use_container_width=True):
            nav_to("Interviews")

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- PAGE CONTENT ---
    if st.session_state.page == "Home":
        # Header with Logo for Home Page
        head_col1, head_col2 = st.columns([1, 4])
        with head_col1:
            st.image("img.jpeg", width=180)

        st.markdown(
            '<div class="notif-bar">Beware of fraud — do not pay anyone claiming to provide jobs for fees.</div>',
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                '<div class="banner-card blue-grad"><h2>Find Jobs</h2><p>Get Hired on-the-go</p></div>',
                unsafe_allow_html=True,
            )
        with col_b:
            st.markdown(
                '<div class="banner-card pink-grad"><h2>Skill Development</h2><p>Enrol to Upskill Today</p></div>',
                unsafe_allow_html=True,
            )

        st.write("##")
        i1, i2, i3, i4, i5, i6 = st.columns(6)
        links = [
            ("far fa-user", "Profile"),
            ("far fa-file-alt", "Resume"),
            ("fas fa-wave-square", "Activity"),
            ("far fa-comment-dots", "Chat"),
            ("far fa-calendar-alt", "Interviews"),
            ("far fa-bell", "Alerts"),
        ]
        for i, col in enumerate([i1, i2, i3, i4, i5, i6]):
            with col:
                st.markdown(
                    f'<div class="icon-box"><div style="font-size:24px;"><i class="{links[i][0]}" style="color:#001F3F;"></i></div><div style="font-size:12px;">{links[i][1]}</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("### Activity")
        s1, s2, s3, s4 = st.columns(4)
        act_labels = ["Jobs Applied", "Interested", "Shortlisted", "Rejected"]
        for i, col in enumerate([s1, s2, s3, s4]):
            with col:
                st.markdown(
                    f'<div class="stat-card"><div class="stat-val">0</div><div class="stat-lbl">{act_labels[i]}</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("### Interviews")
        v1, v2, v3, v4 = st.columns(4)
        istats = ["Scheduled", "Hired", "Rejected", "On Hold"]
        for i, col in enumerate([v1, v2, v3, v4]):
            with col:
                st.markdown(
                    f'<div class="stat-card"><div class="stat-val">0</div><div class="stat-lbl">{istats[i]}</div></div>',
                    unsafe_allow_html=True,
                )

    elif st.session_state.page == "My Profile":
        st.subheader("Profile Details")
        st.markdown(
            f"""
            <div class="progress-card">
                <div style="display:flex; justify-content:space-between;">
                    <span><b>{st.session_state.user_data['name']}</b><br><small>{st.session_state.user_data['mobile']}</small></span>
                </div>
                <p style="margin-top:15px; font-size:12px; color:grey;">Profile Completed - 64%</p>
                <div class="bar-bg"><div class="bar-fill"></div></div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        with st.container():
            st.text_input("Full Name", value=st.session_state.user_data["name"])
            st.text_input("Email", value=st.session_state.user_data["email"])
            st.text_area(
                "Summary*",
                "Looking for a job in Ecommerce, Sales and Marketing roles.",
            )
            st.text_input("Highest Qualification*", "INTER / 12th class -- MPC")
            st.text_input("Pursuing Qualification*", "DEGREE - TECHNICAL -- BE/Btech (CSE)")
            st.button("Save Profile Details", type="primary")

    elif st.session_state.page == "Jobs":
        st.subheader("Available Jobs")

        try:
            df = load_jobs()
        except Exception as e:
            st.error(f"Error loading jobs: {e}")
            df = pd.DataFrame()

        if df.empty:
            st.warning("No jobs found in database. Please run the scraper.")
        else:
            # Job statistics (from original app)
            st.markdown(
                '### <i class="fas fa-chart-bar"></i> Job Statistics',
                unsafe_allow_html=True,
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Jobs", len(df))
            with col2:
                st.metric("Unique Companies", df["company"].nunique())
            with col3:
                st.metric("Unique Locations", df["location"].nunique())

            st.markdown("---")
            st.markdown(
                '#### <i class="fas fa-filter"></i> Filters',
                unsafe_allow_html=True,
            )

            f1, f2, f3 = st.columns(3)
            with f1:
                company_filter = st.multiselect(
                    "Company",
                    options=sorted(df["company"].dropna().unique()),
                )
            with f2:
                location_filter = st.multiselect(
                    "Location",
                    options=sorted(df["location"].dropna().unique()),
                )
            with f3:
                department_filter = st.multiselect(
                    "Department",
                    options=sorted(df["department"].dropna().unique()),
                )

            search_query = st.text_input("Search by Job Title")

            filtered_df = df.copy()

            if company_filter:
                filtered_df = filtered_df[filtered_df["company"].isin(company_filter)]

            if location_filter:
                filtered_df = filtered_df[filtered_df["location"].isin(location_filter)]

            if department_filter:
                filtered_df = filtered_df[
                    filtered_df["department"].isin(department_filter)
                ]

            if search_query:
                filtered_df = filtered_df[
                    filtered_df["title"].str.contains(
                        search_query, case=False, na=False
                    )
                ]

            st.markdown(
                f'### <i class="fas fa-list"></i> Showing {len(filtered_df)} Jobs',
                unsafe_allow_html=True,
            )

            st.dataframe(
                filtered_df[
                    [
                        "company",
                        "title",
                        "location",
                        "department",
                        "posted_date",
                        "scraped_at",
                        "apply_url",
                    ]
                ],
                column_config={
                    "apply_url": st.column_config.LinkColumn(
                        "Apply Here",
                        help="Click to open job page",
                        display_text="Open Job",
                    )
                },
                use_container_width=True,
                hide_index=True,
            )

    elif st.session_state.page == "Interviews":
        st.subheader("Your Interviews")
        st.warning("No interviews scheduled at the moment.")
        st.image(
            "https://via.placeholder.com/800x200.png?text=Keep+Applying+to+get+Interviews",
            use_container_width=True,
        )

    else:
        st.subheader(st.session_state.page)
        st.info("This section is under development.")