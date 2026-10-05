from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from extensions import db
from models import WardReport, DeathRecord
from forms import WardReportForm, DeathDetailForm

male_ward_bp = Blueprint('male_ward', __name__)


@male_ward_bp.route('/male-ward/form', methods=["GET", "POST"])
@login_required
def form():
    if current_user.ward_name != "Male_Ward":
        return "Access denied: this page is for Male Ward only.", 403

    form = WardReportForm()

    if form.validate_on_submit():
        report = WardReport(
            ward_name="Male_Ward",
            previous_patient=form.previous_patient.data,
            new_admissions=form.new_admissions.data,
            discharge=form.discharge.data,
            refer=form.refer.data,
            death=form.death.data,
            still_present=form.still_present.data,
            snake_bite=form.snake_bite.data,
        )
        db.session.add(report)
        db.session.commit()

        if report.death > 0:
            session['death_report_id'] = report.id
            session['death_total'] = report.death
            session['death_current'] = 1
            return redirect(url_for('male_ward.death_detail'))
        else:
            flash("Report submitted successfully.", "success")
            return redirect(url_for('male_ward.form'))

    return render_template('male_ward_form.html', form=form, ward_title="Male Ward")


@male_ward_bp.route('/male-ward/death-detail', methods=["GET", "POST"])
@login_required
def death_detail():
    if current_user.ward_name != "Male_Ward":
        return "Access denied: this page is for Male Ward only.", 403

    if 'death_report_id' not in session:
        flash("No death entries pending.", "info")
        return redirect(url_for('male_ward.form'))

    form = DeathDetailForm()

    if form.validate_on_submit():
        death_record = DeathRecord(
            ward_report_id=session['death_report_id'],
            patient_name=form.patient_name.data,
            father_name=form.father_name.data,
            age=form.age.data,
            admission_date=form.admission_date.data,
            indoor_number=form.indoor_number.data,
            death_date=form.death_date.data,
            death_time=form.death_time.data,
            diagnosis=form.diagnosis.data,
        )
        db.session.add(death_record)
        db.session.commit()

        session['death_current'] += 1

        if session['death_current'] > session['death_total']:
            session.pop('death_report_id', None)
            session.pop('death_total', None)
            session.pop('death_current', None)
            flash("All death records submitted. Report complete.", "success")
            return redirect(url_for('male_ward.form'))
        else:
            return redirect(url_for('male_ward.death_detail'))

    return render_template(
        'death_detail_form.html',
        form=form,
        current=session.get('death_current'),
        total=session.get('death_total'),
    )