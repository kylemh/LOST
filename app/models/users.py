from app.models import db
from app.models import login_manager


class User(db.Model):
    __tablename__ = 'users'

    user_pk = db.Column(db.Integer, primary_key=True)
    role_fk = db.Column(db.ForeignKey('roles.role_pk'), server_default=1)
    username = db.Column(db.String(32), nullable=False, unique=True)
    salt = db.Column(db.String(72))
    password = db.Column(db.String(1024))
    active = db.Column(db.Boolean, server_default=str("True"))

    role = db.relationship('Role')

    def __init__(self, username=None, role=1):
        self.username = username
        self.role_fk = role

    def __repr__(self):
        return '<Username %r>' % self.username
