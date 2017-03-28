from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

from app import views


"""Not using an ORM"""
# from app import views, models
# from app.models import db
# db.create_all()


# ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/failed_query', methods=['GET'])
def failed_query(query):
    return render_template('failed_query.html', query=query)
