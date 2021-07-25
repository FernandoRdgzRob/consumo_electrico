from api import db
from sqlalchemy.orm import validates
import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
ZERO = 0
NAME_MAX_LENGTH = 32
PASSWORD_MAX_LENGTH = 256


class Hitman(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date)
    promotion_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    promotion = db.relationship("Manager", foreign_keys=[promotion_id], backref=db.backref('hitman', order_by=id))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    manager = db.relationship("Manager", foreign_keys=[manager_id], backref=db.backref('assignees', order_by=id))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_dict(),
            "creation_date": str(self.creation_date.strftime('%d-%m-%Y')),
            "discharge_date": str(
                self.discharge_date.strftime('%d-%m-%Y')) if self.discharge_date is not None else self.discharge_date,
            "manager": self.manager if self.manager is None else self.manager.to_dict()
        }
