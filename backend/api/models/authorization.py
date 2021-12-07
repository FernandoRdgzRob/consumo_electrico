from api import db
from datetime import datetime
from sqlalchemy.orm import reconstructor

ZERO = 0
NAME_MAX_LENGTH = 32


class Authorization(db.Model):
    fields_map = None
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.Date, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    permit = db.Column(db.String(255), nullable=False)
    role = db.relationship("Role", back_populates="authorizations")
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)
    module = db.relationship("Module", back_populates="authorizations")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_on_load(**kwargs)

    @reconstructor
    def init_on_load(self, **kwargs):
        fields_map = kwargs.get("fields_map")

        if fields_map is not None:
            self.creation_date = datetime.today().date()
            self.module = fields_map.get("module")
            self.permit = fields_map.get("permit")
            self.role = fields_map.get("role")

    def to_dict(self):
        return {
            "id": self.id,
            "creation_date": str(self.creation_date.strftime("%d-%m-%Y")),
            "role": self.role.name,
            "module": self.module.name,
            "permit": self.permit,
        }
