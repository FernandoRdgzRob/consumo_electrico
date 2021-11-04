from api import db


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        return {
            "id": self.id,
            "hits_created": self.hits_created if self.hits_created is None else map(lambda hit: hit.to_dict(),
                                                                                    self.hits_created),
            "user": None if self.hitman is None else self.hitman.user.to_dict(),
            "hitman": None if self.hitman is None else self.hitman.to_dict()
        }
