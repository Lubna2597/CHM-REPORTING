from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from flask_login import login_user,logout_user,login_required
from models import User

auth_bp=Blueprint('auth',__name__)

WARD_ROUTES= {
    "Male_Ward":"male_ward.form",
    "Female_Ward":"female_ward.form",
    "Paediatric_Ward":"paediatric_ward.form",
    "OG_Ward":"og_ward.form",
}

@auth_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method =="POST":
        username=request.form.get('username')
        password=request.form.get('password')

        user=User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash("Login SuccessFul","success")
            if user.role=="admin":
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for(WARD_ROUTES[user.ward_name]))
        else:
            flash('Invalid username or password','danger')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out','info')
    return redirect(url_for('auth.login'))