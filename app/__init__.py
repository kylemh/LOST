from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import datetime
import json

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import models, views
from models import db


# ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/failed_query', methods=['GET'])
def failed_query(query):
    return render_template('failed_query.html', query=query)


# Application Deployment
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
