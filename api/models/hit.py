from api import db

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
ZERO = 0
NAME_MAX_LENGTH = 32
DESCRIPTION_MAX_LENGTH = 256
STATUS_MAX_LENGTH = 10


class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target_name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False)
    description = db.Column(db.String(DESCRIPTION_MAX_LENGTH))
    status = db.Column(db.String(STATUS_MAX_LENGTH), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    attempt_date = db.Column(db.Date)
    hitman_id = db.Column(db.Integer, db.ForeignKey('hitman.id'))
    hitman = db.relationship("Hitman", foreign_keys=[hitman_id], backref=db.backref('hits', order_by=id))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id],
                              backref=db.backref('hits_created', order_by=id))

    def to_dict(self):
        return {
            "id": self.id,
            "hitman": self.hitman if self.hitman is None else self.hitman.to_dict(),
            "creator": self.creator.to_dict(),
            "target_name": self.target_name,
            "description": self.description,
            "creation_date": str(self.creation_date.strftime('%d-%m-%Y')),
            "attempt_date": self.attempt_date if self.attempt_date is None else str(
                self.attempt_date.strftime('%d-%m-%Y'))
        }
