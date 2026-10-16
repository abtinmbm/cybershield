# CyberShield

**A full-stack forum for discussing cybersecurity, built with Django.**
1st place of 32 teams, Coding & Programming, FBLC Canada National Leadership Conference 2025. I was the sole developer on a three-person team.

![CyberShield](media/CyberShield.png)

## Features

- **Live feed without page reloads:** threaded posts and comments, voting, topic filtering and multi-criteria sorting, served by Django REST Framework endpoints and updated with AJAX.
- **Abuse protection:** Django authentication, CSRF protection on every form, reCAPTCHA on sign-up and login, and moderator roles.
- **Typo-tolerant search:** client-side fuzzy search with Fuse.js, so partial or misspelled queries still find posts.
- **Rich posts:** CKEditor 5 for formatted content and Pillow for profile images.
- **Responsive design** with Tailwind CSS for desktop and mobile.

## Tech stack

| Layer | Tools |
| --- | --- |
| Backend | Django, Django REST Framework, SQLite (development) |
| Frontend | HTML, Tailwind CSS, JavaScript, jQuery (AJAX), Fuse.js |
| Security | Django auth, CSRF protection, django-recaptcha, moderator roles |
| Libraries | django-admin-interface, django-ckeditor-5, Pillow |
| Deployment | AWS (CloudFront CDN) |

## Running locally

Requires Python 3.8+.

```bash
git clone https://github.com/abtinmbm/cybershield.git
cd cybershield
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo          # sample users, posts and comments
python manage.py createsuperuser        # your own admin account
python manage.py runserver
```

Then open http://127.0.0.1:8000/ (admin at `/admin`).

### Configuration

Secrets are read from environment variables. Without them the app runs in local development mode with Google's public reCAPTCHA test keys.

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key (required in production) |
| `DJANGO_DEBUG` | `1` for development (default), `0` for production |
| `RECAPTCHA_PUBLIC_KEY`, `RECAPTCHA_PRIVATE_KEY` | Your reCAPTCHA site keys |
