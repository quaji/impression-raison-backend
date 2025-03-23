pip install -r requirements.txt
gunicorn -b 0.0.0.0:8000 run:app
