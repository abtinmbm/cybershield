# CyberShield - Security Forum

## Table of Contents
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [APIs and Libraries](#apis-and-libraries)
- [Authentication](#authentication)
- [Future Growth and Technical Development Goals](#future-growth-and-technical-development-goals)
- [Tech Stack Explanation](#tech-stack-explanation)

## About the Project
CyberShield is a security forum designed to provide a secure space for cybersecurity discussions. Users can create posts, comment on discussions, and vote on posts and comments. The forum includes features such as sorting posts by various criteria, filtering by topics, and a responsive design for mobile and desktop users.

## Getting Started
To get a local copy up and running follow these simple steps.

### Prerequisites
- Python 3.8+
- Django 3.2+

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/your_username/cybershield.git
   ```
2. Navigate to the project directory
   ```sh
   cd cybershield
   ```
3. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
4. Generate migrations
   ```sh
   python manage.py makemigrations
   ```
5. Apply migrations
   ```sh
   python manage.py migrate
   ```
6. Load demo data
   ```sh
   python manage.py loaddata demo
   ```
7. Run the development server
   ```sh
   python manage.py runserver
   ```

## Usage
1. Open your web browser and go to `http://127.0.0.1:8000/`
2. Register a new account or log in with the superuser account at `http://127.0.0.1:8000/admin` within the demo data (User: MainAdmin Password: Abtin123!!)
3. Create, view, and interact with forum posts and comments
4. Use the sorting and filtering options to navigate through the posts

Enjoy using CyberShield for your cybersecurity discussions!

<<<<<<< HEAD
## APIs and Libraries
CyberShield leverages several APIs and libraries to enhance its functionality:
- **jQuery**: Used for DOM manipulation and handling AJAX requests for dynamic content updates.
- **Fuse.js**: Provides efficient search functionality within the forum.
- **Django REST Framework**: Utilized for creating APIs to handle data interactions between the frontend and backend.


## Authentication
CyberShield uses Django's built-in authentication system to manage user registration, login, and permissions. This ensures secure access to the forum's features and protects user data.


## Tech Stack Explanation
- **Django**: Chosen for its robust framework and ease of use in building secure web applications.
- **Tailwind CSS**: Provides a utility-first approach to styling, making it easy to create responsive and modern designs.
- **SQLite**: Used as the database for development due to its simplicity and ease of setup. Can be replaced with more scalable options like PostgreSQL for production.
- **AWS CloudFront**: Ensures global content delivery with low latency and high transfer speeds.
- 
   ## Backend Framework
- **Django** - Python web framework that powers the application's server-side logic, models, views, and templates

## Database
- **SQLite** - Lightweight database used for development (as seen in the questions about pushing db.sqlite to GitHub)

## Frontend Technologies
- **HTML/CSS** - Standard markup and styling
- **Tailwind CSS** - Utility-first CSS framework for responsive design
- **JavaScript** - Client-side scripting for dynamic interactions

## Python Libraries
- **django-admin-interface** - Enhanced Django admin UI
- **django-ckeditor-5** - Rich text editor integration for content creation
- **django-recaptcha** - Google reCAPTCHA integration for form security
- **Pillow** - Python Imaging Library for processing images (profile pictures, etc.)

## JavaScript Libraries
- **jQuery** - Used extensively for DOM manipulation and AJAX requests
- **Fuse.js** - Lightweight fuzzy-search library (mentioned in README)

## Security Features
- **Django Authentication System** - Used for user registration, login, and permissions
- **CSRF Protection** - Implemented in forms using Django's built-in protection
- **reCAPTCHA** - Added to login and signup forms for bot prevention

## Third-Party Services
- **AWS CloudFront** - Content delivery network 

![CyberShield](media/CyberShield.png)
