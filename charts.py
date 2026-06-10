import pandas as pd
import plotly.express as px


def applications_by_month_chart(jobs_df: pd.DataFrame):
    """Create a monthly applications bar chart."""
    if jobs_df.empty:
        return px.bar(title="Applications by Month")

    df = jobs_df.copy()
    df["application_date"] = pd.to_datetime(df["application_date"], errors="coerce")
    df = df.dropna(subset=["application_date"])
    df["month"] = df["application_date"].dt.to_period("M").dt.to_timestamp()

    grouped = df.groupby("month").size().reset_index(name="count")
    fig = px.bar(
        grouped,
        x="month",
        y="count",
        labels={"month": "Month", "count": "Applications"},
        title="Applications by Month",
        color_discrete_sequence=["#2C7BE5"],
    )
    fig.update_layout(template="plotly_white")
    return fig


def status_distribution_pie(jobs_df: pd.DataFrame):
    """Create a status distribution pie chart."""
    if jobs_df.empty:
        return px.pie(names=["No Data"], values=[1], title="Status Distribution")

    grouped = jobs_df["status"].value_counts().reset_index()
    grouped.columns = ["status", "count"]
    fig = px.pie(
        grouped,
        names="status",
        values="count",
        title="Status Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(template="plotly_white")
    return fig


def top_companies_chart(jobs_df: pd.DataFrame):
    """Create a bar chart for top applied companies."""
    if jobs_df.empty:
        return px.bar(title="Top Companies Applied To")

    grouped = jobs_df["company_name"].value_counts().nlargest(10).reset_index()
    grouped.columns = ["company_name", "applications"]
    fig = px.bar(
        grouped,
        x="applications",
        y="company_name",
        orientation="h",
        title="Top Companies Applied To",
        color="applications",
        color_continuous_scale="Blues",
    )
    fig.update_layout(template="plotly_white", yaxis_title="Company")
    return fig


def interview_conversion_rate_chart(jobs_df: pd.DataFrame):
    """Create a chart showing interview conversion results."""
    if jobs_df.empty:
        return px.bar(title="Interview Conversion Rate")

    total_interviews = len(jobs_df[jobs_df["status"] == "Interview"])
    total_offers = len(jobs_df[jobs_df["status"] == "Offer"])
    total_applications = len(jobs_df)

    data = [
        {"label": "Applications", "count": total_applications},
        {"label": "Interviews", "count": total_interviews},
        {"label": "Offers", "count": total_offers},
    ]
    fig = px.bar(
        pd.DataFrame(data),
        x="label",
        y="count",
        title="Interview Conversion Rate",
        text="count",
        color="label",
        color_discrete_sequence=["#2C7BE5", "#8E44AD", "#28B463"],
    )
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig
