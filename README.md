# ProHire - Job Portal

ProHire is a comprehensive job portal built with Django, designed to connect Job Seekers with Employers efficiently. It features role-based access control, smart job recommendations, and an admin analytics dashboard.

## Features

### Role-Based Access
- **Job Seekers**:
    - Register with resume upload and skills.
    - Search for jobs by title or location.
    - View smart recommendations based on skills.
    - Apply for jobs (status tracking).
- **Employers (HR)**:
    - Post detailed job openings.
    - Manage posted jobs via a dashboard.
    - View applications received.
- **Admin (Superuser)**:
    - Approve/Reject pending job posts.
    - View platform analytics (Users, Jobs, Applications).

### Key Functionalities
- **Smart Recommendations**: Jobs matching a seeker's skills are highlighted and prioritized.
- **Search Filtering**: Real-time filtering of job listings.
- **Secure Authentication**: Role-based permissions and secure password reset flow.
- **Admin Dashboard**: Analytics overview for platform administrators.

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation
1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd ProHire
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

## Usage Guide

1.  **Access the Portal**: Open http://127.0.0.1:8000/
2.  **Register**: Sign up as a "Job Seeker" or "Employer".
3.  **Job Seeker**: Fill in skills during registration to get better recommendations.
4.  **Employer**: Post jobs (Jobs are pending by default).
5.  **Admin**: Login at `/admin/` to approve jobs and `/adminpanel/analytics/` to view stats.

## Testing
Run the automated test suite to verify functionality:
```bash
python manage.py test users jobs
```
