import streamlit as st
import sqlite3
import pandas as pd


DB_NAME = "jobs.db"


def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df


st.set_page_config(page_title="DEET Job Portal", layout="wide")

st.title("🚀 DEET Automated Job Discovery Portal")

df = load_data()

if df.empty:
    st.warning("No jobs found in database. Run scraper first.")
    st.stop()

# ---------------------------
# Metrics
# ---------------------------
st.subheader("📊 Job Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df))
col2.metric("Unique Companies", df["company"].nunique())
col3.metric("Unique Locations", df["location"].nunique())

st.divider()

# ---------------------------
# Filters
# ---------------------------
st.sidebar.header("🔍 Filters")

company_filter = st.sidebar.multiselect(
    "Select Company",
    options=sorted(df["company"].dropna().unique())
)

location_filter = st.sidebar.multiselect(
    "Select Location",
    options=sorted(df["location"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["category"].dropna().unique())
)

search_query = st.sidebar.text_input("🔎 Search by Title")

filtered_df = df.copy()

if company_filter:
    filtered_df = filtered_df[filtered_df["company"].isin(company_filter)]

if location_filter:
    filtered_df = filtered_df[filtered_df["location"].isin(location_filter)]

if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False)
    ]

# ---------------------------
# Display Section
# ---------------------------
st.subheader(f"📋 Showing {len(filtered_df)} Jobs")

st.dataframe(
    filtered_df[
        [
            "company",
            "title",
            "location",
            "category",
            "scraped_at",
            "url"
        ]
    ],
    column_config={
        "url": st.column_config.LinkColumn(
            "Apply Here",
            help="Click to open job page",
            display_text="Open Job"
        )
    },
    use_container_width=True
)