from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.alidayuSMS import AlidayuSMS

db = SQLAlchemy()
mail = Mail()
alidayuSMS = AlidayuSMS()