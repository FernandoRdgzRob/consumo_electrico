from sqlalchemy.orm import reconstructor
from datetime import datetime
from api import db

ZERO = 0.0


class Consumption(db.Model):
    fields_map = None
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.Date, nullable=False)
    consumption_datetime = db.Column(db.DateTime, nullable=False)
    consumption_amount = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship("Device", back_populates="consumptions")
    optimized_consumption_id = db.Column(
        db.Integer, db.ForeignKey("optimized_consumption.id")
    )
    optimized_consumption = db.relationship(
        "OptimizedConsumption", back_populates="real_consumption"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_on_load(**kwargs)

    @reconstructor
    def init_on_load(self, **kwargs):
        fields_map = kwargs.get("fields_map")

        if fields_map is not None:
            self.creation_date = datetime.today().date()
            self.device = fields_map.get("device")
            self.consumption_amount = fields_map.get("consumption_amount")
            self.consumption_datetime = fields_map.get("consumption_datetime")

    @db.validates("consumption_amount")
    def validate_consumption_amount(self, _key, value):
        assert value is not None
        assert value >= ZERO
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "creation_date": str(self.creation_date.strftime("%d-%m-%Y")),
            "consumption_datetime": str(self.creation_date.strftime("%d-%m-%Y")),
            "consumption_amount": self.consumption_amount,
            "device": self.device.to_dict(),
        }
