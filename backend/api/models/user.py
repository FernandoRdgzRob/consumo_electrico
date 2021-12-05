from api import db
import re

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
ZERO = 0
NAME_MAX_LENGTH = 32
EMAIL_MAX_LENGTH = 64
PASSWORD_MAX_LENGTH = 256


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False)
    email = db.Column(db.String(EMAIL_MAX_LENGTH), nullable=False, unique=True)
    creation_date = db.Column(db.Date)
    password = db.Column(db.String(PASSWORD_MAX_LENGTH), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    role = db.relationship("Role", back_populates="users")
    devices = db.relationship("Device", back_populates="user")

    @db.validates("name")
    def validate_name(self, _key, value):
        assert value is not None
        assert isinstance(value, str)
        assert len(value) > ZERO
        assert len(value) < NAME_MAX_LENGTH
        return value

    @db.validates("email")
    def validate_email(self, _key, value):
        assert re.match(EMAIL_REGEX, value)
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "creation_date": str(self.creation_date.strftime("%d-%m-%Y")),
            "role": self.role.to_dict(),
        }
