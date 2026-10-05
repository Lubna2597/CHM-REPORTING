from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from extensions import db
from models import OGWardReport, DeathRecord
from forms import OGWardReportForm, DeathDetailForm

og_ward_bp = Blueprint('og_ward', __name__)


@og_ward_bp.route('/og-ward/form', methods=["GET", "POST"])
@login_required
def form():
    if current_user.ward_name != "OG_Ward":
        return "Access denied: this page is for O&G Ward only.", 403

    form = OGWardReportForm()

    if form.validate_on_submit():
        report = OGWardReport(
            previous_patient=form.previous_patient.data,
            new_admissions=form.new_admissions.data,
            discharge=form.discharge.data,
            refer=form.refer.data,
            death=form.death.data,
            still_present=form.still_present.data,
            nvd=form.nvd.data,
            dc=form.dc.data,
            c_section=form.c_section.data,
        )
        db.session.add(report)
        db.session.commit()

        if report.death > 0:
            session['death_report_id'] = report.id
            session['death_total'] = report.death
            session['death_current'] = 1
            session['death_ward'] = 'og'
            return redirect(url_for('og_ward.death_detail'))
        else:
            flash("Report submitted successfully.", "success")
            return redirect(url_for('og_ward.form'))

    return render_template('og_ward_form.html', form=form, ward_title="O&G Ward")


@og_ward_bp.route('/og-ward/death-detail', methods=["GET", "POST"])
@login_required
def death_detail():
    if current_user.ward_name != "OG_Ward":
        return "Access denied: this page is for O&G Ward only.", 403

    if 'death_report_id' not in session:
        flash("No death entries pending.", "info")
        return redirect(url_for('og_ward.form'))

    form = DeathDetailForm()

    if form.validate_on_submit():
        death_record = DeathRecord(
            og_report_id=session['death_report_id'],
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
            session.pop('death_ward', None)
            flash("All death records submitted. Report complete.", "success")
            return redirect(url_for('og_ward.form'))
        else:
            return redirect(url_for('og_ward.death_detail'))

    return render_template(
        'death_detail_form.html',
        form=form,
        current=session.get('death_current'),
        total=session.get('death_total'),
    )