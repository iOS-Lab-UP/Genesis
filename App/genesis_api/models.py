from genesis_api import db
from sqlalchemy import Index
from sqlalchemy.orm import joinedload, class_mapper
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta
from enum import Enum


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
        def convert_value(value):
            # Convert enums to their value (assuming it's serializable)
            if isinstance(value, Enum):
                # or str(value) if you want the enum's name instead
                return value.value
            # Convert datetime objects to string in 'YYYY-MM-DD' format
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d')
            # Add other conversions here if needed
            return value

        return {
            column.name: convert_value(getattr(self, column.name))
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

    @classmethod
    def get_data_with_all_children(cls, session, **filters):
        """
        Retrieve records with all related objects based on specified filters.

        :param session: The SQLAlchemy session to use for database interactions.
        :param filters: Conditions for filtering records.
        :return: A list of instances of the calling class.
        """
        try:
            # Get all relationship keys for the model
            relationship_keys = cls._relationship_keys()

            # Create a query with options to joinedload all relationships
            query = session.query(cls).filter_by(**filters)
            for key in relationship_keys:
                query = query.options(joinedload(key))

            # Execute the query
            records = query.all()

            return records
        except Exception as e:
            # Log the error for debugging purposes
            print(f"An error occurred while retrieving data: {e}")
            return None

    @classmethod
    def _relationship_keys(cls) -> list:
        """
        Get all relationship keys for the class.
        """
        mapper = class_mapper(cls)
        return [relationship.key for relationship in mapper.relationships]


"""""""""""""""""""""
" ASSOCIATION TABLES"
"""""""""""""""""""""

medical_history_user_image_association = db.Table('MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION',
                                                  db.Column('medical_history_id', db.Integer, db.ForeignKey(
                                                      'MEDICAL_HISTORY.id'), primary_key=True),
                                                  db.Column('user_image_id', db.Integer, db.ForeignKey(
                                                      'USER_IMAGE.id'), primary_key=True)
                                                  )

medical_history_prescription_association = db.Table('MEDICAL_HISTORY_PRESCRIPTION_ASSOCIATION',
                                                    db.Column('medical_history_id', db.Integer, db.ForeignKey(
                                                        'MEDICAL_HISTORY.id'), primary_key=True),
                                                    db.Column('prescription_id', db.Integer, db.ForeignKey(
                                                        'PRESCRIPTION.id'), primary_key=True)
                                                    )

user_image_ml_diagnostic_association = db.Table('USER_IMAGE_ML_DIAGNOSTIC_ASSOCIATION',
                                                db.Column('user_image', db.Integer, db.ForeignKey(
                                                    'USER_IMAGE.id'), primary_key=True),
                                                db.Column('ml_diagnostic', db.Integer, db.ForeignKey(
                                                    'ML_DIAGNOSTIC.id'), primary_key=True)
                                                )


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
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    birth_date = db.Column(db.Date)
    cedula = db.Column(db.String(255), nullable=True)
    profile_id = db.Column(db.Integer, db.ForeignKey(
        'PROFILE.id'), nullable=False)

    # Relationships
    patients = db.relationship('DoctorPatientAssociation', back_populates='doctor',
                               foreign_keys='DoctorPatientAssociation.doctor_id')
    doctor = db.relationship('DoctorPatientAssociation', back_populates='patient',
                             uselist=False, foreign_keys='DoctorPatientAssociation.patient_id')

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

    def expire(self) -> None:
        """
        Expire the code and delete the registry from the database (hard delete).
        """

        db.session.delete(self)

    def is_expired(self) -> bool:
        """
        Check if the code is expired.
        The code is considered expired if it's more than 10 minutes old.
        """
        expiration_threshold = self.last_update + timedelta(minutes=5)
        return datetime.utcnow() > expiration_threshold


class Image(BaseModel):
    """"
    A model class that represents an image in the application.
    """

    __tablename__ = 'IMAGE'
    path = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)


class UserImage(BaseModel):
    """
    A model class that represents a user's image in the application.
    """
    __tablename__ = 'USER_IMAGE'
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('IMAGE.id'), nullable=False)
    image = db.relationship('Image', backref='user_image', lazy=True)
    user = db.relationship('User', backref='user_image', lazy=True)

    # Relationships
    ml_diagnostics = db.relationship(
        "MlDiagnostic", secondary=user_image_ml_diagnostic_association, backref="user_images")


class MlDiagnostic(BaseModel):
    """
    A model class that....
    """
    __tablename__ = 'ML_DIAGNOSTIC'
    sickness = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    precision = db.Column(db.Float, nullable=False)


class DoctorPatientAssociation(BaseModel):
    """
    A model class that represents the association between doctors and patients.
    """
    __tablename__ = 'DOCTOR_PATIENT_ASSOCIATION'
    doctor_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('USER.id'))

    # Relationships
    doctor = db.relationship("User", foreign_keys=[doctor_id])
    patient = db.relationship("User", foreign_keys=[patient_id])


class MedicalHistory(BaseModel):
    """
    A model class that represents a medical history in the application.
    """
    __tablename__ = 'MEDICAL_HISTORY'

    # Foreign key
    association_id = db.Column(db.Integer, db.ForeignKey(
        'DOCTOR_PATIENT_ASSOCIATION.id'), nullable=False)

    # Observation field
    observation = db.Column(db.Text, nullable=True)

    # Timestamps
    date_of_visit = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    next_appointment_date = db.Column(db.Date, nullable=False)

    # Details
    diagnostic = db.Column(db.Text)
    symptoms = db.Column(db.Text)

    # Confidential Notes
    private_notes = db.Column(db.Text, nullable=True)

    # Follow-up
    follow_up_required = db.Column(db.Boolean, default=False)

    # Patient Feedback
    patient_feedback = db.Column(db.Text, nullable=True, default=None)

    # Relationships
    association = db.relationship(
        "DoctorPatientAssociation", backref="medical_histories")
    user_images = db.relationship(
        "UserImage", secondary=medical_history_user_image_association, backref="medical_histories")
    prescriptions = db.relationship(
        "Prescription", secondary=medical_history_prescription_association, backref="medical_histories")


class FrequencyUnit(Enum):
    minute = 'minute'
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'


class Prescription(BaseModel):
    """
    A model class that represents a prescription in the application.
    """
    __tablename__ = 'PRESCRIPTION'

    treatment = db.Column(db.String(255), nullable=False,
                          comment='Name of the medicine prescribed')
    indications = db.Column(
        db.Text, comment='Detailed indications for the patient')
    dosage = db.Column(db.String(100), nullable=False,
                       comment='Dosage of the medicine')
    frequency_value = db.Column(
        db.Integer, nullable=False, comment='The numerical value of the frequency (e.g., every 2 hours, every 3 days, etc.)')
    frequency_unit = db.Column(db.Enum(FrequencyUnit), nullable=False,
                               comment='The unit of time for the frequency (minutes, hours, days, weeks, or months)')
    start_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow, comment='Start date of the medication')
    end_date = db.Column(
        db.DateTime, comment='End date of the medication, can be NULL if indefinite or as needed')
    notifications_enabled = db.Column(
        db.Boolean, default=True, comment='Whether notifications for this prescription are enabled')


class Medicines(BaseModel):
    __tablename__ = 'MEDICINES'

    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Double, nullable=False)
    is_discontinued = db.Column(db.Boolean, nullable=False)
    manufacturer_name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    pack_size_label = db.Column(db.String(255), nullable=False)
    short_composition1 = db.Column(db.String(255), nullable=False)
    short_composition2 = db.Column(db.String(255), nullable=False)
