from flask import Flask, url_for
from config import Config
from extensions import db, login_manager
from flask_login import current_user
from apscheduler.schedulers.background import BackgroundScheduler
import shutil
import os
from datetime import datetime

from models import User

from routes.auth import auth_bp
from routes.male_ward import male_ward_bp
from routes.female_ward import female_ward_bp
from routes.paediatric_Ward import paediatric_ward_bp
from routes.og_ward import og_ward_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(male_ward_bp)
    app.register_blueprint(female_ward_bp)
    app.register_blueprint(paediatric_ward_bp)
    app.register_blueprint(og_ward_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


WARD_HOME_ROUTES = {
    'Male_Ward': 'male_ward.form',
    'Female_Ward': 'female_ward.form',
    'Paediatric_Ward': 'paediatric_ward.form',
    'OG_Ward': 'og_ward.form',
}


@app.context_processor
def inject_nav_info():
    home_url = None
    home_label = None
    if current_user.is_authenticated:
        if current_user.role == "admin":
            home_url = url_for('admin.dashboard')
            home_label = "Dashboard"
        else:
            endpoint = WARD_HOME_ROUTES.get(current_user.ward_name)
            if endpoint:
                home_url = url_for(endpoint)
                home_label = current_user.ward_name.replace('_', ' ')
    return dict(home_url=home_url, home_label=home_label)


# ---------- Automatic daily database backup (runs on whatever machine the app runs on) ----------

def backup_database():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "hospital.db")
    backup_dir = os.path.join(base_dir, "backups")
    os.makedirs(backup_dir, exist_ok=True)

    if not os.path.exists(db_path):
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(backup_dir, f"hospital_backup_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    print(f"[Backup] Created {backup_path}")

    # Keep only the most recent 30 backups
    backups = sorted(f for f in os.listdir(backup_dir) if f.startswith("hospital_backup_"))
    if len(backups) > 30:
        for old in backups[:-30]:
            os.remove(os.path.join(backup_dir, old))


# Flask's debug reloader runs two processes; this guard makes sure the scheduler
# only starts once, not twice.
if os.environ.get("WERKZEUG_RUN_MAIN") != "true" or not app.debug:
    backup_database()  # one backup immediately on every app start
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=backup_database, trigger="cron", hour=23, minute=59)
    scheduler.start()


if __name__ == "__main__":
    app.run(debug=True)