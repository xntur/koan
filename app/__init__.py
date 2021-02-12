from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes, db

if __name__ == '__main__':
    app.run()
