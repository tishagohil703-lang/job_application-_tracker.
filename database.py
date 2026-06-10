import sqlite3
from pathlib import Path
from typing import List, Optional

import pandas as pd


class JobDatabase:
    """Encapsulates SQLite operations for the job application tracker."""

    def __init__(self, db_path: str = "jobs.db"):
        project_root = Path(__file__).resolve().parent
        self.db_path = str(project_root / db_path)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self) -> None:
        """Create the jobs table if it does not already exist."""
        create_query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_role TEXT,
            salary TEXT,
            job_location TEXT,
            application_date TEXT,
            status TEXT,
            interview_date TEXT,
            notes TEXT
        )
        """
        with self.connection:
            self.connection.execute(create_query)

    def add_job(
        self,
        company_name: str,
        job_role: str,
        salary: str,
        job_location: str,
        application_date: str,
        status: str,
        interview_date: str,
        notes: str,
    ) -> None:
        """Insert a new job application record."""
        insert_query = """
        INSERT INTO jobs (
            company_name,
            job_role,
            salary,
            job_location,
            application_date,
            status,
            interview_date,
            notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.connection:
            self.connection.execute(
                insert_query,
                (
                    company_name,
                    job_role,
                    salary,
                    job_location,
                    application_date,
                    status,
                    interview_date,
                    notes,
                ),
            )

    def update_job(
        self,
        job_id: int,
        company_name: str,
        job_role: str,
        salary: str,
        job_location: str,
        application_date: str,
        status: str,
        interview_date: str,
        notes: str,
    ) -> None:
        """Update an existing job application record by ID."""
        update_query = """
        UPDATE jobs
        SET
            company_name = ?,
            job_role = ?,
            salary = ?,
            job_location = ?,
            application_date = ?,
            status = ?,
            interview_date = ?,
            notes = ?
        WHERE id = ?
        """
        with self.connection:
            self.connection.execute(
                update_query,
                (
                    company_name,
                    job_role,
                    salary,
                    job_location,
                    application_date,
                    status,
                    interview_date,
                    notes,
                    job_id,
                ),
            )

    def delete_job(self, job_id: int) -> None:
        """Remove a job application record from the database."""
        delete_query = "DELETE FROM jobs WHERE id = ?"
        with self.connection:
            self.connection.execute(delete_query, (job_id,))

    def fetch_all_jobs(self) -> pd.DataFrame:
        """Return all job applications as a Pandas DataFrame."""
        query = "SELECT * FROM jobs ORDER BY application_date DESC"
        return pd.read_sql_query(query, self.connection)

    def fetch_jobs(
        self,
        search_text: str = "",
        status_filter: str = "All",
    ) -> pd.DataFrame:
        """Fetch jobs filtered by search text and status."""
        base_query = "SELECT * FROM jobs"
        parameters: List[str] = []
        conditions: List[str] = []

        if search_text:
            search_clause = (
                "company_name LIKE ? OR job_role LIKE ? OR job_location LIKE ? OR notes LIKE ?"
            )
            search_pattern = f"%{search_text}%"
            conditions.append(search_clause)
            parameters.extend([search_pattern] * 4)

        if status_filter and status_filter != "All":
            conditions.append("status = ?")
            parameters.append(status_filter)

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += " ORDER BY application_date DESC"
        return pd.read_sql_query(base_query, self.connection, params=parameters)

    def fetch_job_by_id(self, job_id: int) -> Optional[sqlite3.Row]:
        """Get a job record by ID."""
        query = "SELECT * FROM jobs WHERE id = ?"
        cursor = self.connection.execute(query, (job_id,))
        return cursor.fetchone()
