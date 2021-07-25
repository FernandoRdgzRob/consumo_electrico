from api import db

ZERO = 0
NAME_MAX_LENGTH = 32


class Authorization(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.Date, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship("Role", back_populates="authorizations")
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    module = db.relationship("Module", back_populates="authorizations")
    permit_id = db.Column(db.Integer, db.ForeignKey('permit.id'), nullable=False)
    permit = db.relationship("Permit", back_populates="authorizations")

    def to_dict(self):
        return {
            "id": self.id,
            "creation_date": str(self.creation_date.strftime('%d-%m-%Y')),
            "role": self.role.name,
            "module": self.module.name,
            "permission": self.permission.name
        }
