from api import db
from datetime import datetime
from sqlalchemy.orm import validates, reconstructor
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ZERO = 0
NAME_MAX_LENGTH = 32


class Module(db.Model):
    fields_map = None
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.Date)
    name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False, unique=True)
    authorizations = db.relationship("Authorization", back_populates="module")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_on_load(**kwargs)

    @reconstructor
    def init_on_load(self, **kwargs):
        fields_map = kwargs.get("fields_map")

        if fields_map is not None:
            self.creation_date = datetime.today().date()
            self.name = fields_map.get("name")

    @validates("name")
    def validate_name(self, _key, value):
        assert value is not None
        assert isinstance(value, str)
        assert len(value) > ZERO
        assert len(value) < NAME_MAX_LENGTH
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "creation_date": str(self.creation_date.strftime("%d-%m-%Y")),
            "authorizations": [
                authorization.to_dict() for authorization in self.authorizations
            ],
        }
