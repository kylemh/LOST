# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_asset_at = Table(
    'asset_at', metadata,
    Column('asset_fk', ForeignKey('assets.asset_pk'), nullable=False),
    Column('facility_fk', ForeignKey('facilities.facility_pk'), nullable=False),
    Column('arrive_dt', DateTime),
    Column('depart_dt', DateTime)
)


class Asset(Base):
    __tablename__ = 'assets'

    asset_pk = Column(Integer, primary_key=True, server_default=text("nextval('assets_asset_pk_seq'::regclass)"))
    asset_tag = Column(String(16))
    description = Column(Text)
    disposed = Column(Boolean)


class Facility(Base):
    __tablename__ = 'facilities'

    facility_pk = Column(Integer, primary_key=True, server_default=text("nextval('facilities_facility_pk_seq'::regclass)"))
    fcode = Column(String(6))
    common_name = Column(String(32))
    location = Column(String(128))


class InTransit(Base):
    __tablename__ = 'in_transit'

    in_transit_pk = Column(Integer, primary_key=True, server_default=text("nextval('in_transit_in_transit_pk_seq'::regclass)"))
    request_fk = Column(ForeignKey('requests.request_pk'), nullable=False)
    load_dt = Column(DateTime)
    unload_dt = Column(DateTime)

    request = relationship('Request')


class Request(Base):
    __tablename__ = 'requests'

    request_pk = Column(Integer, primary_key=True, server_default=text("nextval('requests_request_pk_seq'::regclass)"))
    asset_fk = Column(ForeignKey('assets.asset_pk'), nullable=False)
    user_fk = Column(ForeignKey('users.user_pk'), nullable=False)
    src_fk = Column(ForeignKey('facilities.facility_pk'), nullable=False)
    dest_fk = Column(ForeignKey('facilities.facility_pk'), nullable=False)
    request_dt = Column(DateTime)
    approve_dt = Column(DateTime)
    approved = Column(Boolean, nullable=False)
    approving_user_fk = Column(ForeignKey('users.user_pk'))
    completed = Column(Boolean, nullable=False)

    user = relationship('User', primaryjoin='Request.approving_user_fk == User.user_pk')
    asset = relationship('Asset')
    facility = relationship('Facility', primaryjoin='Request.dest_fk == Facility.facility_pk')
    facility1 = relationship('Facility', primaryjoin='Request.src_fk == Facility.facility_pk')
    user1 = relationship('User', primaryjoin='Request.user_fk == User.user_pk')


class Role(Base):
    __tablename__ = 'roles'

    role_pk = Column(Integer, primary_key=True, server_default=text("nextval('roles_role_pk_seq'::regclass)"))
    title = Column(String(32))


class User(Base):
    __tablename__ = 'users'

    user_pk = Column(Integer, primary_key=True, server_default=text("nextval('users_user_pk_seq'::regclass)"))
    role_fk = Column(ForeignKey('roles.role_pk'), server_default=text("1"))
    username = Column(String(16), nullable=False, unique=True)
    password = Column(String(16), nullable=False)
    active = Column(Boolean, server_default=text("true"))

    role = relationship('Role')