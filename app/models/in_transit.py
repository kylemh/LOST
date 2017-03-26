from app.models import db


class InTransit(db.Model):
    __tablename__ = 'in_transit'

    in_transit_pk = db.Column(db.Integer, primary_key=True)
    request_fk = db.Column(db.ForeignKey('requests.request_pk'), nullable=False)
    load_dt = db.Column(db.DateTime)
    unload_dt = db.Column(db.DateTime)

    request = db.relationship('Request')
