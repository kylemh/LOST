from app.models import db


class Asset(db.Model):
    __tablename__ = 'assets'

    asset_pk = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(16))
    description = db.Column(db.Text)
    disposed = db.Column(db.Boolean)
