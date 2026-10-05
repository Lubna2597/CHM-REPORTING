from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, DateField, TimeField, SelectField
from wtforms.validators import InputRequired, DataRequired, Optional, NumberRange, Length


class Login(FlaskForm):
    name = StringField("User name", validators=[DataRequired(message="Username is required")])
    password = PasswordField("Password", validators=[DataRequired(message="Password is required")])
    submit = SubmitField("Login")


class WardReportForm(FlaskForm):
    previous_patient = IntegerField('Previous Patient', validators=[InputRequired(), NumberRange(min=0)])
    new_admissions = IntegerField('New Admissions', validators=[InputRequired(), NumberRange(min=0)])
    discharge = IntegerField('Discharge', validators=[InputRequired(), NumberRange(min=0)])
    refer = IntegerField('Refer', validators=[InputRequired(), NumberRange(min=0)])
    death = IntegerField('Death', validators=[InputRequired(), NumberRange(min=0)])
    still_present = IntegerField('Still Present', validators=[InputRequired(), NumberRange(min=0)])
    snake_bite = IntegerField('New Snake Bite', validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')


class PaediatricWardReportForm(FlaskForm):
    previous_patient = IntegerField('Previous Patient', validators=[InputRequired(), NumberRange(min=0)])
    nicu_admissions = IntegerField('New Admissions - NICU', validators=[InputRequired(), NumberRange(min=0)])
    nsc_admissions = IntegerField('New Admissions - NSC', validators=[InputRequired(), NumberRange(min=0)])
    hdu_admissions = IntegerField('New Admissions - HDU', validators=[InputRequired(), NumberRange(min=0)])
    discharge = IntegerField('Discharge', validators=[InputRequired(), NumberRange(min=0)])
    refer = IntegerField('Refer', validators=[InputRequired(), NumberRange(min=0)])
    death = IntegerField('Death', validators=[InputRequired(), NumberRange(min=0)])
    still_present = IntegerField('Still Present', validators=[InputRequired(), NumberRange(min=0)])
    snake_bite = IntegerField('New Snake Bite', validators=[InputRequired(), NumberRange(min=0)])
    labour_room = IntegerField('Labour Room', validators=[InputRequired(), NumberRange(min=0)])
    admission_under_1month = IntegerField('Admissions < 1 month', validators=[InputRequired(), NumberRange(min=0)])
    admission_under_1year = IntegerField('Admissions < 1 year', validators=[InputRequired(), NumberRange(min=0)])
    admission_under_5year = IntegerField('Admissions < 5 years', validators=[InputRequired(), NumberRange(min=0)])
    admission_over_5year = IntegerField('Admissions > 5 years', validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')


class OGWardReportForm(FlaskForm):
    previous_patient = IntegerField('Previous Patient', validators=[InputRequired(), NumberRange(min=0)])
    new_admissions = IntegerField('New Admissions', validators=[InputRequired(), NumberRange(min=0)])
    discharge = IntegerField('Discharge', validators=[InputRequired(), NumberRange(min=0)])
    refer = IntegerField('Refer', validators=[InputRequired(), NumberRange(min=0)])
    death = IntegerField('Death', validators=[InputRequired(), NumberRange(min=0)])
    still_present = IntegerField('Still Present', validators=[InputRequired(), NumberRange(min=0)])
    nvd = IntegerField('NVD', validators=[InputRequired(), NumberRange(min=0)])
    dc = IntegerField('D&C', validators=[InputRequired(), NumberRange(min=0)])
    c_section = IntegerField('C-Section', validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')


class DeathDetailForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    father_name = StringField("Father's Name", validators=[DataRequired()])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=0)])
    admission_date = DateField('Date of Admission', format='%Y-%m-%d', validators=[Optional()])
    indoor_number = StringField('Indoor Number')
    death_date = DateField('Date of Death', format='%Y-%m-%d', validators=[Optional()])
    death_time = TimeField('Time of Death', format='%H:%M', validators=[Optional()])
    diagnosis = StringField('Diagnosis')
    submit = SubmitField('Submit Death Record')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, message="Password must be at least 4 characters.")])
    role = SelectField('Role', choices=[('ward', 'Ward'), ('admin', 'Admin')], validators=[DataRequired()])
    ward_name = SelectField('Ward (only if role = Ward)', choices=[
        ('', '-- N/A --'),
        ('Male_Ward', 'Male_Ward'),
        ('Female_Ward', 'Female_Ward'),
        ('Paediatric_Ward', 'Paediatric_Ward'),
        ('OG_Ward', 'OG_Ward'),
    ])
    submit = SubmitField('Save User')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=4, message="Password must be at least 4 characters.")])
    submit = SubmitField('Reset Password')