from app.models import db

t_asset_at = db.Table(
    'asset_at', db.metadata,
    db.Column('asset_fk', db.ForeignKey('assets.asset_pk'), nullable=False),
    db.Column('facility_fk', db.ForeignKey('facilities.facility_pk'), nullable=False),
    db.Column('arrive_dt', db.DateTime),
    db.Column('depart_dt', db.DateTime)
)