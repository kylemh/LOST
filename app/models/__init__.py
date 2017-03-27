from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

import app.models.roles
import app.models.users
import app.models.facilities
import app.models.assets
import app.models.asset_at
import app.models.requests
import app.models.in_transit
