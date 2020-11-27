import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, _
import logging
from logging.handlers import SMTPHandler
from oauthlib.oauth2 import WebApplicationClient
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), os.pardir, '.flaskenv')
load_dotenv(dotenv_path)


media_version = "1.3.7"


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'home'
login.login_message = _("Please log in first")
login.login_message_category = "danger"
mail = Mail(app)
moment = Moment(app)
babel = Babel(app)

google_client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])


from app import routes, models

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='[FAILURE] DanikTL',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


if __name__ == '__main__':
    app.run(debug=True)
