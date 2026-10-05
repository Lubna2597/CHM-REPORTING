from flask import Blueprint, render_template, redirect, url_for, flash, send_file, request, current_app
from flask_login import login_required, current_user
from extensions import db
from models import WardReport, PaediatricWardReport, OGWardReport, DeathRecord, User
from forms import (
    WardReportForm, PaediatricWardReportForm, OGWardReportForm, DeathDetailForm,
    UserForm, ResetPasswordForm,
)
from datetime import datetime, date
from collections import Counter
from openpyxl.utils import get_column_letter
import pandas as pd
import io
import os

admin_bp = Blueprint('admin', __name__)


def _not_admin():
    """Returns a 403 response if the current user isn't admin, else None."""
    if current_user.role != "admin":
        return "Access denied: admin only.", 403
    return None


@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    denied = _not_admin()
    if denied:
        return denied

    selected_date_str = request.args.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    ward_reports = WardReport.query.filter_by(report_date=selected_date).all()
    male_reports = [r for r in ward_reports if r.ward_name == 'Male_Ward']
    female_reports = [r for r in ward_reports if r.ward_name == 'Female_Ward']

    paediatric_reports = PaediatricWardReport.query.filter_by(report_date=selected_date).all()
    og_reports = OGWardReport.query.filter_by(report_date=selected_date).all()

    ward_report_ids = [r.id for r in ward_reports]
    paediatric_report_ids = [r.id for r in paediatric_reports]
    og_report_ids = [r.id for r in og_reports]

    death_records = DeathRecord.query.filter(
        db.or_(
            DeathRecord.ward_report_id.in_(ward_report_ids),
            DeathRecord.paediatric_report_id.in_(paediatric_report_ids),
            DeathRecord.og_report_id.in_(og_report_ids),
        )
    ).all()

    death_rows = []
    for d in death_records:
        if d.ward_report_id:
            wr = next((r for r in ward_reports if r.id == d.ward_report_id), None)
            ward_label = wr.ward_name if wr else "Unknown"
        elif d.paediatric_report_id:
            ward_label = "Paediatric_Ward"
        elif d.og_report_id:
            ward_label = "OG_Ward"
        else:
            ward_label = "Unknown"
        death_rows.append({'record': d, 'ward': ward_label})

    death_totals = Counter(row['ward'] for row in death_rows)

    return render_template(
        'admin/dashboard.html',
        male_reports=male_reports,
        female_reports=female_reports,
        paediatric_reports=paediatric_reports,
        og_reports=og_reports,
        death_rows=death_rows,
        death_totals=death_totals,
        selected_date=selected_date,
        now=datetime.now(),
    )


# ---------- Ward (Male/Female) report edit/delete ----------

@admin_bp.route('/admin/ward-report/<int:report_id>/edit', methods=["GET", "POST"])
@login_required
def edit_ward_report(report_id):
    denied = _not_admin()
    if denied:
        return denied

    report = WardReport.query.get_or_404(report_id)
    form = WardReportForm(obj=report)

    if form.validate_on_submit():
        report.previous_patient = form.previous_patient.data
        report.new_admissions = form.new_admissions.data
        report.discharge = form.discharge.data
        report.refer = form.refer.data
        report.death = form.death.data
        report.still_present = form.still_present.data
        report.snake_bite = form.snake_bite.data
        db.session.commit()
        flash("Report updated.", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_report.html', form=form, title=f"Edit {report.ward_name} Report")


@admin_bp.route('/admin/ward-report/<int:report_id>/delete', methods=["POST"])
@login_required
def delete_ward_report(report_id):
    denied = _not_admin()
    if denied:
        return denied

    report = WardReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash("Report deleted.", "info")
    return redirect(url_for('admin.dashboard'))


# ---------- Paediatric report edit/delete ----------

@admin_bp.route('/admin/paediatric-report/<int:report_id>/edit', methods=["GET", "POST"])
@login_required
def edit_paediatric_report(report_id):
    denied = _not_admin()
    if denied:
        return denied

    report = PaediatricWardReport.query.get_or_404(report_id)
    form = PaediatricWardReportForm(obj=report)

    if form.validate_on_submit():
        report.previous_patient = form.previous_patient.data
        report.nicu_admissions = form.nicu_admissions.data
        report.nsc_admissions = form.nsc_admissions.data
        report.hdu_admissions = form.hdu_admissions.data
        report.discharge = form.discharge.data
        report.refer = form.refer.data
        report.death = form.death.data
        report.still_present = form.still_present.data
        report.snake_bite = form.snake_bite.data
        report.labour_room = form.labour_room.data
        report.admission_under_1month = form.admission_under_1month.data
        report.admission_under_1year = form.admission_under_1year.data
        report.admission_under_5year = form.admission_under_5year.data
        report.admission_over_5year = form.admission_over_5year.data
        db.session.commit()
        flash("Report updated.", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_report.html', form=form, title="Edit Paediatric Ward Report")


@admin_bp.route('/admin/paediatric-report/<int:report_id>/delete', methods=["POST"])
@login_required
def delete_paediatric_report(report_id):
    denied = _not_admin()
    if denied:
        return denied

    report = PaediatricWardReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash("Report deleted.", "info")
    return redirect(url_for('admin.dashboard'))


# ---------- O&G report edit/delete ----------

@admin_bp.route('/admin/og-report/<int:report_id>/edit', methods=["GET", "POST"])
@login_required
def edit_og_report(report_id):
    denied = _not_admin()
    if denied:
        return denied

    report = OGWardReport.query.get_or_404(report_id)
    form = OGWardReportForm(obj=report)

    if form.validate_on_submit():
        report.previous_patient = form.previous_patient.data
        report.new_admissions = form.new_admissions.data
        report.discharge = form.discharge.data
        report.refer = form.refer.data
        report.death = form.death.data
        report.still_present = form.still_present.data
        report.nvd = form.nvd.data
        report.dc = form.dc.data
        report.c_section = form.c_section.data
        db.session.commit()
        flash("Report updated.", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_report.html', form=form, title="Edit O&G Ward Report")


@admin_bp.route('/admin/og-report/<int:report_id>/delete', methods=["POST"])
@login_required
def delete_og_report(report_id):
    denied = _not_admin()
    if denied:
        return denied

    report = OGWardReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash("Report deleted.", "info")
    return redirect(url_for('admin.dashboard'))


# ---------- Death record edit/delete ----------

@admin_bp.route('/admin/death-record/<int:record_id>/edit', methods=["GET", "POST"])
@login_required
def edit_death_record(record_id):
    denied = _not_admin()
    if denied:
        return denied

    record = DeathRecord.query.get_or_404(record_id)
    form = DeathDetailForm(obj=record)

    if form.validate_on_submit():
        record.patient_name = form.patient_name.data
        record.father_name = form.father_name.data
        record.age = form.age.data
        record.admission_date = form.admission_date.data
        record.indoor_number = form.indoor_number.data
        record.death_date = form.death_date.data
        record.death_time = form.death_time.data
        record.diagnosis = form.diagnosis.data
        db.session.commit()
        flash("Death record updated.", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_death.html', form=form, title="Edit Death Record")


@admin_bp.route('/admin/death-record/<int:record_id>/delete', methods=["POST"])
@login_required
def delete_death_record(record_id):
    denied = _not_admin()
    if denied:
        return denied

    record = DeathRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash("Death record deleted.", "info")
    return redirect(url_for('admin.dashboard'))


# ---------- Excel export ----------

@admin_bp.route('/admin/export')
@login_required
def export_excel():
    denied = _not_admin()
    if denied:
        return denied

    ward_reports = WardReport.query.all()
    paediatric_reports = PaediatricWardReport.query.all()
    og_reports = OGWardReport.query.all()
    death_records = DeathRecord.query.all()

    def fmt_date(v):
        return v.strftime('%Y-%m-%d') if v else ''

    def fmt_time(v):
        return v.strftime('%H:%M') if v else ''

    ward_columns = ['Date', 'Ward', 'Previous Patient', 'New Admissions', 'Discharge',
                    'Refer', 'Death', 'Still Present', 'Snake Bite']
    ward_data = [{
        'Date': fmt_date(r.report_date), 'Ward': r.ward_name, 'Previous Patient': r.previous_patient,
        'New Admissions': r.new_admissions, 'Discharge': r.discharge, 'Refer': r.refer,
        'Death': r.death, 'Still Present': r.still_present, 'Snake Bite': r.snake_bite,
    } for r in ward_reports]
    ward_df = pd.DataFrame(ward_data, columns=ward_columns)

    paediatric_columns = ['Date', 'Previous Patient', 'NICU', 'NSC', 'HDU', 'Discharge',
                          'Refer', 'Death', 'Still Present', 'Snake Bite', 'Labour Room',
                          '<1 month', '<1 year', '<5 years', '>5 years']
    paediatric_data = [{
        'Date': fmt_date(r.report_date), 'Previous Patient': r.previous_patient,
        'NICU': r.nicu_admissions, 'NSC': r.nsc_admissions, 'HDU': r.hdu_admissions,
        'Discharge': r.discharge, 'Refer': r.refer, 'Death': r.death,
        'Still Present': r.still_present, 'Snake Bite': r.snake_bite, 'Labour Room': r.labour_room,
        '<1 month': r.admission_under_1month, '<1 year': r.admission_under_1year,
        '<5 years': r.admission_under_5year, '>5 years': r.admission_over_5year,
    } for r in paediatric_reports]
    paediatric_df = pd.DataFrame(paediatric_data, columns=paediatric_columns)

    og_columns = ['Date', 'Previous Patient', 'New Admissions', 'Discharge', 'Refer',
                  'Death', 'Still Present', 'NVD', 'D&C', 'C-Section']
    og_data = [{
        'Date': fmt_date(r.report_date), 'Previous Patient': r.previous_patient,
        'New Admissions': r.new_admissions, 'Discharge': r.discharge, 'Refer': r.refer,
        'Death': r.death, 'Still Present': r.still_present, 'NVD': r.nvd,
        'D&C': r.dc, 'C-Section': r.c_section,
    } for r in og_reports]
    og_df = pd.DataFrame(og_data, columns=og_columns)

    death_columns = ['Patient Name', "Father's Name", 'Age', 'Indoor Number',
                      'Admission Date', 'Death Date', 'Death Time', 'Diagnosis']
    death_data = [{
        'Patient Name': d.patient_name, "Father's Name": d.father_name, 'Age': d.age,
        'Indoor Number': d.indoor_number, 'Admission Date': fmt_date(d.admission_date),
        'Death Date': fmt_date(d.death_date), 'Death Time': fmt_time(d.death_time),
        'Diagnosis': d.diagnosis,
    } for d in death_records]
    death_df = pd.DataFrame(death_data, columns=death_columns)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        ward_df.to_excel(writer, sheet_name='Male_Female_Ward', index=False)
        paediatric_df.to_excel(writer, sheet_name='Paediatric_Ward', index=False)
        og_df.to_excel(writer, sheet_name='OG_Ward', index=False)
        death_df.to_excel(writer, sheet_name='Death_Records', index=False)

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for col_cells in worksheet.columns:
                max_len = max((len(str(cell.value)) for cell in col_cells if cell.value is not None), default=10)
                col_letter = get_column_letter(col_cells[0].column)
                worksheet.column_dimensions[col_letter].width = max(12, max_len + 2)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='hospital_report.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )


# ---------- Manual database backup download ----------

@admin_bp.route('/admin/backup-db')
@login_required
def backup_db():
    denied = _not_admin()
    if denied:
        return denied

    db_path = os.path.join(current_app.root_path, 'hospital.db')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return send_file(
        db_path,
        as_attachment=True,
        download_name=f'hospital_backup_{timestamp}.db',
    )


# ---------- User management ----------

@admin_bp.route('/admin/users')
@login_required
def manage_users():
    denied = _not_admin()
    if denied:
        return denied

    users = User.query.all()
    return render_template('admin/manage_user.html', users=users)


@admin_bp.route('/admin/users/add', methods=["GET", "POST"])
@login_required
def add_user():
    denied = _not_admin()
    if denied:
        return denied

    form = UserForm()

    if form.validate_on_submit():
        existing = User.query.filter_by(username=form.username.data).first()
        if existing:
            flash("That username already exists.", "danger")
        else:
            ward_name = form.ward_name.data if form.role.data == "ward" else None
            new_user = User(username=form.username.data, role=form.role.data, ward_name=ward_name)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("User added.", "success")
            return redirect(url_for('admin.manage_users'))

    return render_template('admin/add_user.html', form=form)


@admin_bp.route('/admin/users/<int:user_id>/delete', methods=["POST"])
@login_required
def delete_user(user_id):
    denied = _not_admin()
    if denied:
        return denied

    if user_id == current_user.id:
        flash("You cannot delete your own account while logged in.", "danger")
        return redirect(url_for('admin.manage_users'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "info")
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/admin/users/<int:user_id>/reset-password', methods=["GET", "POST"])
@login_required
def reset_password(user_id):
    denied = _not_admin()
    if denied:
        return denied

    user = User.query.get_or_404(user_id)
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(f"Password reset for {user.username}.", "success")
        return redirect(url_for('admin.manage_users'))

    return render_template('admin/reset_password.html', form=form, user=user)