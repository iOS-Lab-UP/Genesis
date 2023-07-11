from genesis_api import db
from datetime import datetime
from sqlalchemy import Index


class BaseModel(db.Model):
    """
    An abstract base model class that defines some common attributes for all models in the application.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=True)
    creation_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the model.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def get_data(cls, obj_id: int) -> object:
        """
        Retrieves an object by its ID.
        """
        try:
            return cls.query.get(obj_id)
        except:
            return None


class User(BaseModel):
    """
    A model class that represents a user in the application.
    """
    __tablename__ = 'USER'
    __table_args__ = (
        Index('idx_username', 'username'),
        Index('idx_email', 'email'),
        Index('idx_creation_date', 'creation_date')
    )
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    birth_date = db.Column(db.Date)
