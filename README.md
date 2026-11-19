# InkWell — Django Blogging Platform

A starter blogging application with authentication, post publishing, editing/deletion, comments, likes, categories, tags, search, a personal dashboard, and Django Admin.

## Requirements
- Python 3.10+
- pip

## Run locally

```bash
# 1. Extract the ZIP and enter the project folder
cd django_blog_platform

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database tables
python manage.py makemigrations blog
python manage.py migrate

# 5. Create an administrator account
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## First-use content setup
1. Log in to `/admin/`.
2. Add a few Categories and Tags.
3. Register a normal user from the website, or create one in admin.
4. Create a post from **My dashboard** and set its status to **Published**.
5. Published posts appear on the homepage. Drafts remain private to their author (and staff).

## Main routes
- `/` — published posts and search
- `/signup/` — registration
- `/accounts/login/` — login
- `/dashboard/` — current user's posts
- `/posts/new/` — create post
- `/posts/<slug>/` — post detail, likes, comments
- `/admin/` — Django administration

## Security and production checklist
This is a local-development starter, not a production deployment as-is:
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`.
- Load `SECRET_KEY` from an environment variable; never commit production secrets.
- Configure HTTPS, secure cookies, CSRF trusted origins, and a production web server.
- Use PostgreSQL (or another production database), backups, and proper static-file hosting.
- Add rate limiting/spam protection for comments and likes, email verification/password reset policy, and moderation workflows as needed.
- Consider rich-text sanitization if you add a WYSIWYG editor or accept HTML.
- Configure media uploads and a storage backend if adding featured images.
- Run `python manage.py check --deploy` before deployment.

## Tests
```bash
python manage.py test
```
"# Blog" 
