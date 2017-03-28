from app.models import db


class Request(db.Model):
    __tablename__ = 'requests'

    request_pk = db.Column(db.Integer, primary_key=True)
    asset_fk = db.Column(db.ForeignKey('assets.asset_pk'), nullable=False)
    user_fk = db.Column(db.ForeignKey('users.user_pk'), nullable=False)
    src_fk = db.Column(db.ForeignKey('facilities.facility_pk'), nullable=False)
    dest_fk = db.Column(db.ForeignKey('facilities.facility_pk'), nullable=False)
    request_dt = db.Column(db.DateTime)
    approve_dt = db.Column(db.DateTime)
    approved = db.Column(db.Boolean, nullable=False)
    approving_user_fk = db.Column(db.ForeignKey('users.user_pk'))
    completed = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', primaryjoin='Request.approving_user_fk == User.user_pk')
    asset = db.relationship('Asset')
    facility = db.relationship('Facility', primaryjoin='Request.dest_fk == Facility.facility_pk')
    facility1 = db.relationship('Facility', primaryjoin='Request.src_fk == Facility.facility_pk')
    user1 = db.relationship('User', primaryjoin='Request.user_fk == User.user_pk')

    def __init__(self, approved=False, completed=False):
        self.approved = approved
        self.completed = completed

    def __repr__(self):
        return '<Request %r>' % self.request_pk
