# ...existing code...

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication settings
LOGIN_URL = 'login'  # Use the name of your custom login URL pattern
LOGIN_REDIRECT_URL = 'forum_list'  # Redirect to forum list after login

# ...existing code...