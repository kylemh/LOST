from app.models import db


class Facility(db.Model):
    __tablename__ = 'facilities'

    facility_pk = db.Column(db.Integer, primary_key=True)
    fcode = db.Column(db.String(6))
    common_name = db.Column(db.String(32))
    location = db.Column(db.String(128))

    def __init__(self, fcode=None, common_name=None, location=None):
        self.fcode = fcode
        self.common_name = common_name
        self.location = location

    def __repr__(self):
        return '<Facility %r>' % self.common_name
