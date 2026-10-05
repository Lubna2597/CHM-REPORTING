from app import app
from extensions import db
from models import User

with app.app_context():
    users=[
        {"username": "maleWard","password":"1234","role":"ward","ward_name":"Male_Ward"},
        {"username": "femaleWard","password":"5678","role":"ward","ward_name":"Female_Ward"},
        {"username": "paedsWard","password":"9101112","role":"ward","ward_name":"Paediatric_Ward"},
        {"username": "OGWard","password":"13141516","role":"ward","ward_name":"OG_Ward"},
        {"username": "Admin","password":"Admin","role":"admin","ward_name":None}
    ]

    for u in users:
        existing=User.query.filter_by(username=u["username"]).first()
        if not existing:
            new_user=User(username=u["username"],role=u["role"],ward_name=u["ward_name"])
            new_user.set_password(u["password"])
            db.session.add(new_user)
    db.session.commit()
