# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_clef_secrete_robuste'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///location.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
