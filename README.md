# Prime Rentals

## Quick start

```bash
git clone <repo-url>
cd prime_rentals
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata prime_demo.json  # optional sample data
python manage.py runserver
```

Open `http://127.0.0.1:8000/` to view the site.
