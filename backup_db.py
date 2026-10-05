import shutil
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

os.makedirs(BACKUP_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_path = os.path.join(BACKUP_DIR, f"hospital_backup_{timestamp}.db")

shutil.copy2(DB_PATH, backup_path)
print(f"Backup created: {backup_path}")

# Keep only the most recent 30 backups so this folder doesn't grow forever
backups = sorted(f for f in os.listdir(BACKUP_DIR) if f.startswith("hospital_backup_"))
if len(backups) > 30:
    for old_backup in backups[:-30]:
        os.remove(os.path.join(BACKUP_DIR, old_backup))
        print(f"Removed old backup: {old_backup}")