from api import db

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
ZERO = 0
NAME_MAX_LENGTH = 32
PASSWORD_MAX_LENGTH = 16


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.hitman.user.name,
            "email": self.hitman.user.email,
            "creation_date": str(self.creation_date.strftime('%d-%m-%Y')),
            "discharge_date": str(self.discharge_date.strftime('%d-%m-%Y')),
            "role": self.role.name
        }
