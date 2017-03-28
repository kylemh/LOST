from app.models import db


class Asset(db.Model):
    __tablename__ = 'assets'

    asset_pk = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(16))
    description = db.Column(db.Text)
    disposed = db.Column(db.Boolean)

    def __init__(self, asset_tag=None, description=None, disposed=False):
        self.asset_tag = asset_tag
        self.description = description
        self.disposed = disposed

    def __repr__(self):
        return '<Asset %r>' % self.asset_tag

