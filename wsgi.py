from application import application

if __name__ == "__main__":
    application.run()

# gunicorn --bind 0.0.0.0:80 wsgi:application

