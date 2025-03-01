# CyberShield - Security Forum

## Table of Contents
- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
- [Usage](#usage)

## About the Project
CyberShield is a security forum designed to provide a secure space for cybersecurity discussions. Users can create posts, comment on discussions, and vote on posts and comments. The forum includes features such as sorting posts by various criteria, filtering by topics, and a responsive design for mobile and desktop users.

## Built With
- [Django](https://www.djangoproject.com/) - The web framework used
- [Tailwind CSS](https://tailwindcss.com/) - For styling
- [jQuery](https://jquery.com/) - For DOM manipulation
- [Fuse.js](https://fusejs.io/) - For search functionality
- [AWS CloudFront](https://aws.amazon.com/cloudfront/) - For global hosting

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
4. Apply migrations
   ```sh
   python manage.py migrate
   ```
5. Create a superuser
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server
   ```sh
   python manage.py runserver
   ```

## Usage
1. Open your web browser and go to `http://127.0.0.1:8000/`
2. Register a new account or log in with the superuser account
3. Create, view, and interact with forum posts and comments
4. Use the sorting and filtering options to navigate through the posts

Enjoy using CyberShield for your cybersecurity discussions!

![CyberShield](media/CyberShield.png)
