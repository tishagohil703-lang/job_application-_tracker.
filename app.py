import streamlit as st
import pandas as pd

from database import JobDatabase
from charts import (
    applications_by_month_chart,
    status_distribution_pie,
    top_companies_chart,
    interview_conversion_rate_chart,
)

# Configure the Streamlit page with a modern title and layout.
st.set_page_config(
    page_title="Job Application Tracker",
    page_icon="💼",
    layout="wide",
)

# Create or connect to the SQLite database.
db = JobDatabase("jobs.db")

STATUS_OPTIONS = ["Applied", "Interview", "Offer", "Rejected", "Other"]


def format_date(date_string: str) -> str:
    """Return the date string unchanged if it is empty or invalid."""
    try:
        return pd.to_datetime(date_string).date().isoformat()
    except Exception:
        return ""


def dashboard_page(jobs_df: pd.DataFrame) -> None:
    """Render the analytics dashboard with metrics and charts."""
    st.markdown("# Dashboard")
    st.markdown(
        "Track application performance with total counts, success rate, and hiring charts."
    )

    total_applications = len(jobs_df)
    total_interviews = len(jobs_df[jobs_df["status"] == "Interview"])
    total_offers = len(jobs_df[jobs_df["status"] == "Offer"])
    total_rejections = len(jobs_df[jobs_df["status"] == "Rejected"])
    success_rate = (
        round((total_offers / total_applications) * 100, 1)
        if total_applications > 0
        else 0
    )

    # Display key summary metrics in a responsive layout.
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Applications", total_applications)
    col2.metric("Interviews", total_interviews)
    col3.metric("Offers", total_offers)
    col4.metric("Rejections", total_rejections)
    col5.metric("Success Rate", f"{success_rate}%")

    st.markdown("---")
    with st.container():
        chart1_col, chart2_col = st.columns((2, 1))
        chart1_col.plotly_chart(
            applications_by_month_chart(jobs_df),
            use_container_width=True,
        )
        chart2_col.plotly_chart(
            status_distribution_pie(jobs_df),
            use_container_width=True,
        )

    st.markdown("---")
    with st.container():
        chart3_col, chart4_col = st.columns(2)
        chart3_col.plotly_chart(
            top_companies_chart(jobs_df),
            use_container_width=True,
        )
        chart4_col.plotly_chart(
            interview_conversion_rate_chart(jobs_df),
            use_container_width=True,
        )


def job_management_page() -> None:
    """Render the job management interface for adding, editing, searching, and deleting jobs."""
    st.markdown("# Job Management")
    st.markdown("Add new applications, update status, and keep your job search organized.")

    search_text = st.text_input("Search jobs", placeholder="Search by company, role, location...")
    status_filter = st.selectbox("Filter by status", ["All"] + STATUS_OPTIONS)

    jobs_df = db.fetch_jobs(search_text=search_text, status_filter=status_filter)

    with st.expander("Add a new job application", expanded=True):
        with st.form("add_job_form"):
            company_name = st.text_input("Company Name")
            job_role = st.text_input("Job Role")
            salary = st.text_input("Salary")
            job_location = st.text_input("Job Location")
            application_date = st.date_input("Application Date")
            status = st.selectbox("Status", STATUS_OPTIONS, index=0)
            interview_date = st.date_input("Interview Date", disabled=(status != "Interview"))
            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Add Job")
            if submitted:
                db.add_job(
                    company_name=company_name,
                    job_role=job_role,
                    salary=salary,
                    job_location=job_location,
                    application_date=application_date.isoformat(),
                    status=status,
                    interview_date=interview_date.isoformat()
                    if status == "Interview"
                    else "",
                    notes=notes,
                )
                st.success("Job application added successfully.")
                st.rerun()

    st.markdown("## Current Applications")
    st.dataframe(jobs_df, use_container_width=True)

    if not jobs_df.empty:
        selected_job_id = st.selectbox(
            "Select a job to edit or delete",
            jobs_df["id"].tolist(),
            format_func=lambda x: f"{x} - {jobs_df[jobs_df['id'] == x]['company_name'].values[0]}"
            if len(jobs_df[jobs_df['id'] == x]) > 0
            else str(x),
        )

        job_record = db.fetch_job_by_id(selected_job_id)
        if job_record is not None:
            with st.form("edit_job_form"):
                company_name = st.text_input("Company Name", value=job_record["company_name"])
                job_role = st.text_input("Job Role", value=job_record["job_role"])
                salary = st.text_input("Salary", value=job_record["salary"])
                job_location = st.text_input(
                    "Job Location", value=job_record["job_location"]
                )
                app_date = (
                    pd.to_datetime(job_record["application_date"]).date()
                    if job_record["application_date"]
                    else pd.to_datetime("today").date()
                )
                application_date = st.date_input("Application Date", value=app_date)
                status = st.selectbox(
                    "Status", STATUS_OPTIONS, index=STATUS_OPTIONS.index(job_record["status"]) if job_record["status"] in STATUS_OPTIONS else 0
                )
                interview_date_value = (
                    pd.to_datetime(job_record["interview_date"]).date()
                    if job_record["interview_date"]
                    else pd.to_datetime("today").date()
                )
                interview_date = st.date_input(
                    "Interview Date", value=interview_date_value, disabled=(status != "Interview")
                )
                notes = st.text_area("Notes", value=job_record["notes"])

                update_submitted = st.form_submit_button("Update Job")
                delete_submitted = st.form_submit_button("Delete Job")

                if update_submitted:
                    db.update_job(
                        job_id=selected_job_id,
                        company_name=company_name,
                        job_role=job_role,
                        salary=salary,
                        job_location=job_location,
                        application_date=application_date.isoformat(),
                        status=status,
                        interview_date=interview_date.isoformat()
                        if status == "Interview"
                        else "",
                        notes=notes,
                    )
                    st.success("Job application updated.")
                    st.rerun()

                if delete_submitted:
                    db.delete_job(selected_job_id)
                    st.warning("Job application deleted.")
                    st.experimental_rerun()

    else:
        st.info("No job applications match the current filters. Add your first job to get started.")


def analytics_page(jobs_df: pd.DataFrame) -> None:
    """Render the analytics section with multiple charts for job search insights."""
    st.markdown("# Analytics")
    st.markdown(
        "Visualize your application workflow, discover top companies, and measure interview conversion."
    )

    st.plotly_chart(applications_by_month_chart(jobs_df), use_container_width=True)
    st.plotly_chart(status_distribution_pie(jobs_df), use_container_width=True)
    st.plotly_chart(top_companies_chart(jobs_df), use_container_width=True)
    st.plotly_chart(interview_conversion_rate_chart(jobs_df), use_container_width=True)


def main() -> None:
    """Main function to route between pages and render the Streamlit app."""
    st.sidebar.title("Job Tracker")
    st.sidebar.markdown("Organize applications, interviews, and offers in one place.")
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Job Management", "Analytics"],
    )

    jobs_df = db.fetch_jobs()

    if page == "Dashboard":
        dashboard_page(jobs_df)
    elif page == "Job Management":
        job_management_page()
    else:
        analytics_page(jobs_df)


if __name__ == "__main__":
    main()
