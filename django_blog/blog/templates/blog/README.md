Django Blog — Authentication & Post Management

Key features:
- User registration (with email + avatar + bio)
- Login and Logout (using Django auth views)
- Profile view/update
- Post CRUD (List, Detail, Create, Update, Delete)
- Comment system (Create, Update, Delete) — only comment authors can edit/delete
- Tagging (comma-separated) and search across title/content/tags

How to run (dev):
1. pip install -r requirements.txt  # include django, pillow for images
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver
6. Open http://127.0.0.1:8000/

Testing:
- Register a new user; try login/logout.
- Create a post as authenticated user; edit/delete as author.
- Add comments while logged in; try editing/deleting from another account to verify permissions.
- Use search bar to search keywords and tags.

Notes:
- For image upload support, install Pillow: pip install pillow.
- For production media/static serving, configure proper storage (e.g., S3) and static collection.
- If you prefer tag management, replace Tag model with django-taggit for an easier UX.
