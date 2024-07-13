from datetime import datetime, timezone

import sqlalchemy as sqlalchemy
import sqlalchemy.orm as orm
from app.extensions import db


class Recipe(db.Model):
    __tablename__ = "recipes"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    making_time: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    serves: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    ingredients: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    cost: orm.Mapped[int] = orm.mapped_column(sqlalchemy.INTEGER, nullable=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: orm.Mapped[datetime] = orm.mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False, onupdate=lambda: datetime.now(timezone.utc))
    


class Filters:

    _from = None
    _to = None
    limit = 50      # it's good to have a default limit.
    offset = 0

    def __init__(self, _from=None, _to=None, limit=None, offset=None):
        self._from = _from
        self._to = _to
        self.limit = limit
        self.offset = offset
