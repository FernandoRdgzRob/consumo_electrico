from api import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ZERO = 0
NAME_MAX_LENGTH = 16
DEFAULT_MAX_LENGTH = 7


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False, unique=True)
    users = db.relationship("User", back_populates="role")
    creation_date = db.Column(db.Date)
    authorizations = db.relationship("Authorization", back_populates="role")
    default = db.Column(db.String(DEFAULT_MAX_LENGTH), unique=True)

    @db.validates("name")
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
        }
