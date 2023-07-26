from genesis_api import db

from sqlalchemy import Index
from flask_bcrypt  import check_password_hash
from datetime import datetime, timedelta

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
    def __repr__(self) -> str:
        """
        Returns a string representation of the model.
        """
        column_strings = []
        for column, value in self.to_dict().items():
            column_strings.append(f"{column}={value}")

        return f"{self.__class__.__name__}({', '.join(column_strings)})"

    @classmethod
    def get_data(cls, obj_id: int) -> object:
        """
        Retrieves an object by its ID and status.
        """
        try:
            return cls.query.filter_by(id=obj_id, status=True).first()
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
    cedula = db.Column(db.String(255), nullable=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('PROFILE.id'), nullable=False)


    def check_password(self, password: str) -> bool:
        """
        Checks if the password matches the user's password.
        """
        return check_password_hash(self.password_hash, password)



class Profile(BaseModel):
    """
    A model class that represents a profile in the application.
    """
    __tablename__ = 'PROFILE'
    profile = db.Column(db.String(255), nullable=False)

class VerificationCode(BaseModel):
    """
    A model class that represents a verification code in the application.
    """
    __tablename__ = 'VERIFICATION_CODE'
    code = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False)

    def expire(self, session) -> None:
        """
        Expire the code and delete the registry from the database (hard delete).
        """

        session.delete(self)


    def is_expired(self) -> bool:
        """
        Check if the code is expired.
        The code is considered expired if it's more than 10 minutes old.
        """
        expiration_threshold = self.last_update + timedelta(minutes=5)
        return datetime.utcnow() > expiration_threshold
