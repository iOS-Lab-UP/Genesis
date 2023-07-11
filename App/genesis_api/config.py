from dotenv import load_dotenv

import os
import secrets


# Specify the path to your .env file if it's not in the same directory as this file
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')

# Load the .env file
load_dotenv(dotenv_path)

class Config:

    
    # SQL Credentials
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    SQLALCHEMY_DATABASE_URI = "mysql://" + MYSQL_USER + ":" + \
        MYSQL_PASSWORD + "@" + MYSQL_HOST + "/" + MYSQL_DATABASE + "?charset=utf8mb4"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    
    # JWT Secret Key
    SECRET_KEY = secrets.token_hex(16)