from app.models import db


class Facility(db.Model):
    __tablename__ = 'facilities'

    facility_pk = db.Column(db.Integer, primary_key=True)
    fcode = db.Column(db.String(6))
    common_name = db.Column(db.String(32))
    location = db.Column(db.String(128))
