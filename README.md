# ProHire - Job Portal Application

ProHire is a comprehensive job portal built with Django, allowing Job Seekers to apply for jobs and HR/Employers to post and manage job listings.

## Features
- **User Roles**: Job Seeker and Employer (HR).
- **Authentication**: Secure Login/Register/Logout.
- **Job Management**: HR can post, edit (future), and view applicants.
- **Job Search**: Seekers can search by title or location.
- **Application System**: Seekers can apply, view status, and track history.
- **Profile System**: Dedicated profiles for Seekers (Resume) and HR (Company Info).
- **Theme**: Dark/Light mode toggle.
- **Deployment**: Ready for Render.

## Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on how to deploy to Render.

## Local Development
1. Clone the repository.
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Migrate DB: `python manage.py migrate`
6. Run server: `python manage.py runserver`
