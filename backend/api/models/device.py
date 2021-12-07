from api import db
from sqlalchemy.orm import reconstructor
from datetime import datetime

ZERO = 0
NAME_MAX_LENGTH = 64
SORT_MAX_LENGTH = 16


class Device(db.Model):
    fields_map = None
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False, unique=True)
    type = db.Column(db.String(NAME_MAX_LENGTH), nullable=False, unique=False)
    min_c = db.Column(db.Float, default=0.0)
    average_consumption = db.Column(db.Float, default=0.0)
    max_c = db.Column(db.Float, default=0.0)
    freq_time = db.Column(db.Float, default=0.0)
    turn_off = db.Column(db.Boolean, default=True)
    sort = db.Column(db.String(SORT_MAX_LENGTH))
    metering = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="devices")
    consumptions = db.relationship("Consumption", back_populates="device")
    optimized_consumptions = db.relationship(
        "OptimizedConsumption", back_populates="device"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_on_load(**kwargs)

    @reconstructor
    def init_on_load(self, **kwargs):
        fields_map = kwargs.get("fields_map")

        if fields_map is not None:
            self.creation_date = datetime.today().date()
            self.name = fields_map.get("name")
            self.type = fields_map.get("type")
            self.user = fields_map.get("user")
            self.min_c = fields_map.get("min_c")
            self.average_consumption = fields_map.get("average_consumption")
            self.max_c = fields_map.get("max_c")
            self.freq_time = fields_map.get("freq_time")
            self.turn_off = fields_map.get("turn_off")
            self.sort = fields_map.get("sort")
            self.metering = fields_map.get("metering")

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
            "user": self.user.to_dict(),
        }
