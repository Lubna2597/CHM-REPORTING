from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    ward_name = db.Column(db.String(50), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class WardReport(db.Model):
    """Shared by Male_Ward and Female_Ward."""
    id = db.Column(db.Integer, primary_key=True)
    ward_name = db.Column(db.String(50), nullable=False)
    report_date = db.Column(db.Date, nullable=False, default=date.today)

    previous_patient = db.Column(db.Integer, default=0)
    new_admissions = db.Column(db.Integer, default=0)
    discharge = db.Column(db.Integer, default=0)
    refer = db.Column(db.Integer, default=0)
    death = db.Column(db.Integer, default=0)
    still_present = db.Column(db.Integer, default=0)
    snake_bite = db.Column(db.Integer, default=0)

    deaths = db.relationship('DeathRecord', backref='ward_report', lazy=True)


class PaediatricWardReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False, default=date.today)

    previous_patient = db.Column(db.Integer, default=0)
    nicu_admissions = db.Column(db.Integer, default=0)
    nsc_admissions = db.Column(db.Integer, default=0)
    hdu_admissions = db.Column(db.Integer, default=0)
    discharge = db.Column(db.Integer, default=0)
    refer = db.Column(db.Integer, default=0)
    death = db.Column(db.Integer, default=0)
    still_present = db.Column(db.Integer, default=0)
    snake_bite = db.Column(db.Integer, default=0)
    labour_room = db.Column(db.Integer, default=0)

    admission_under_1month = db.Column(db.Integer, default=0)
    admission_under_1year = db.Column(db.Integer, default=0)
    admission_under_5year = db.Column(db.Integer, default=0)
    admission_over_5year = db.Column(db.Integer, default=0)

    deaths = db.relationship('DeathRecord', backref='paediatric_report', lazy=True)


class OGWardReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False, default=date.today)

    previous_patient = db.Column(db.Integer, default=0)
    new_admissions = db.Column(db.Integer, default=0)
    discharge = db.Column(db.Integer, default=0)
    refer = db.Column(db.Integer, default=0)
    death = db.Column(db.Integer, default=0)
    still_present = db.Column(db.Integer, default=0)

    nvd = db.Column(db.Integer, default=0)       # Normal Vaginal Delivery
    dc = db.Column(db.Integer, default=0)         # D&C
    c_section = db.Column(db.Integer, default=0)

    deaths = db.relationship('DeathRecord', backref='og_report', lazy=True)


class DeathRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ward_report_id = db.Column(db.Integer, db.ForeignKey('ward_report.id'), nullable=True)
    paediatric_report_id = db.Column(db.Integer, db.ForeignKey('paediatric_ward_report.id'), nullable=True)
    og_report_id = db.Column(db.Integer, db.ForeignKey('og_ward_report.id'), nullable=True)

    patient_name = db.Column(db.String(150), nullable=False)
    father_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255))
    admission_date = db.Column(db.Date)
    indoor_number = db.Column(db.String(50))
    death_date = db.Column(db.Date)
    death_time = db.Column(db.Time)
    diagnosis = db.Column(db.String(255))