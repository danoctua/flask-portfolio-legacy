import os, json

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(basedir, "app", "data", "db_credentials")) as file:
    db_credentials = json.load(file)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SOME-very-SECRET-key'
    SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{host}/{db_name}?charset=utf8".format(
        username=db_credentials['username'],
        password=db_credentials['password'],
        host=db_credentials['host'],
        db_name=db_credentials['database_name']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', None)
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", None)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['danik4tl@gmail.com']
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    LANGUAGES = ['en', 'ru', "pl"]
