from datetime import date

import streamlit as st

from standup_agent import (
    read_tasks,
    generate_ai_standup
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Daily Stand-up Reporter",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIMPLE FORMAL STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #2b3036;
    }

    /* Main content area */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Headings */
    h1 {
        color: #f4f6f8 !important;
    }

    h2, h3 {
        color: #e6e9ec !important;
    }

    /* Normal text */
    p {
        color: #d3d7db;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #20252b;
        border-right: 1px solid #3c434b;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f4f6f8 !important;
    }

    section[data-testid="stSidebar"] label {
        color: #d8dde2 !important;
    }

    section[data-testid="stSidebar"] p {
        color: #aeb5bd !important;
    }

    /* Sidebar text inputs */
    section[data-testid="stSidebar"] input {
        background-color: #f5f6f7 !important;
        color: #222831 !important;
        border-radius: 6px !important;
    }

    /* Text areas */
    textarea {
        background-color: #f5f6f7 !important;
        color: #222831 !important;
        border: 1px solid #adb5bd !important;
        border-radius: 8px !important;
        font-size: 15px !important;
    }

    textarea:focus {
        border-color: #4f8c88 !important;
        box-shadow: 0 0 0 1px #4f8c88 !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #353c44;
        border: 1px solid #4c5661;
        border-radius: 8px;
        padding: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #b9c1c9;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* Primary button */
    button[kind="primary"] {
        background-color: #3f7774 !important;
        color: white !important;
        border: none !important;
        border-radius: 7px !important;
        font-weight: 600 !important;
    }

    button[kind="primary"]:hover {
        background-color: #315f5d !important;
    }

    /* Other buttons */
    div.stButton > button {
        border-radius: 7px;
        font-weight: 600;
    }

    div.stDownloadButton > button {
        border-radius: 7px;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border-color: #4a525b !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Report Details")

    developer_name = st.text_input(
        "Developer Name",
        value="Anmol"
    )

    project_name = st.text_input(
        "Project Name",
        value="Customer Portal"
    )

    team_name = st.text_input(
        "Team Name",
        value="Development Team"
    )

    report_date = st.date_input(
        "Report Date",
        value=date.today()
    )

    st.divider()

    st.caption(
        "Enter the developer's task updates and generate "
        "a concise AI-assisted daily stand-up report."
    )


# ============================================================
# TITLE
# ============================================================

st.title("📋 Daily Stand-up Reporter")

st.caption(
    "AI-assisted generation of concise daily development updates"
)

st.divider()


# ============================================================
# REPORT DETAILS SUMMARY
# ============================================================

detail1, detail2, detail3, detail4 = st.columns(4)

with detail1:
    st.caption("Developer")
    st.write(f"**{developer_name}**")

with detail2:
    st.caption("Project")
    st.write(f"**{project_name}**")

with detail3:
    st.caption("Team")
    st.write(f"**{team_name}**")

with detail4:
    st.caption("Date")
    st.write(
        f"**{report_date.strftime('%d %b %Y')}**"
    )


st.divider()


# ============================================================
# LOAD DEFAULT TASKS
# ============================================================

default_done_tasks = read_tasks(
    "data/done.txt"
)

default_progress_tasks = read_tasks(
    "data/in_progress.txt"
)

default_done_text = "\n".join(
    default_done_tasks
)

default_progress_text = "\n".join(
    default_progress_tasks
)


# ============================================================
# TASK INPUT
# ============================================================

left_col, right_col = st.columns(
    2,
    gap="large"
)


with left_col:

    st.subheader("Completed Work")

    done_input = st.text_area(
        "Completed tasks",
        value=default_done_text,
        height=240,
        placeholder="Enter one completed task per line",
        label_visibility="collapsed"
    )


with right_col:

    st.subheader("Work In Progress")

    progress_input = st.text_area(
        "In-progress tasks",
        value=default_progress_text,
        height=240,
        placeholder="Enter one in-progress task per line",
        label_visibility="collapsed"
    )


# ============================================================
# CONVERT INPUT INTO LISTS
# ============================================================

done_tasks = [
    task.strip()
    for task in done_input.splitlines()
    if task.strip()
]

in_progress_tasks = [
    task.strip()
    for task in progress_input.splitlines()
    if task.strip()
]


# ============================================================
# TASK COUNTS
# ============================================================

st.write("")

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "Completed",
        len(done_tasks)
    )

with metric2:
    st.metric(
        "In Progress",
        len(in_progress_tasks)
    )

with metric3:
    st.metric(
        "Total Tasks",
        len(done_tasks) + len(in_progress_tasks)
    )


st.divider()


# ============================================================
# GENERATE BUTTON
# ============================================================

left_space, center_button, right_space = st.columns(
    [1, 2, 1]
)

with center_button:

    generate_button = st.button(
        "Generate Daily Update",
        type="primary",
        use_container_width=True
    )


# ============================================================
# GENERATE AI REPORT
# ============================================================

if generate_button:

    if not done_tasks and not in_progress_tasks:

        st.warning(
            "Please enter at least one task."
        )

    else:

        try:

            with st.spinner(
                "Generating daily update..."
            ):

                report = generate_ai_standup(
                    done_tasks,
                    in_progress_tasks
                )

            st.session_state["report"] = report

        except Exception as error:

            st.error(
                f"Unable to generate report: {error}"
            )


# ============================================================
# DISPLAY GENERATED REPORT
# ============================================================

if "report" in st.session_state:

    st.divider()

    st.subheader("Generated Team Update")

    st.info(
        st.session_state["report"]
    )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    report_text = f"""Daily Stand-up Report

Developer: {developer_name}
Project: {project_name}
Team: {team_name}
Date: {report_date.strftime('%d %b %Y')}

Completed Tasks: {len(done_tasks)}
In Progress Tasks: {len(in_progress_tasks)}

Team Update:
{st.session_state["report"]}
"""


    download_col, clear_col = st.columns(2)


    with download_col:

        st.download_button(
            label="Download Report",
            data=report_text,
            file_name="daily_standup_report.txt",
            mime="text/plain",
            use_container_width=True
        )


    with clear_col:

        if st.button(
            "Clear Generated Report",
            use_container_width=True
        ):

            del st.session_state["report"]

            st.rerun()