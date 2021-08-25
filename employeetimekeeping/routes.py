
from datetime import date, datetime
from flask import render_template, flash, redirect, url_for, request
from employeetimekeeping.models import User, Activity
from flask.helpers import url_for
from employeetimekeeping.forms import RegistrationForm, LoginForm
from employeetimekeeping import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/user_activity', methods=['GET', 'POST'])
@login_required
def userActivities():
    current_date = datetime.now().strftime('%y-%m-%d')
    if request.method == 'POST':
        if request.form.get('start_shift') == 'Start shift':
            print('This is start shift')

            current_activities = Activity.query.filter_by(user_id=current_user.id)
            todays_activity = None
            if(current_activities.count()>0):
                todays_activity = [activity for activity in current_activities if activity.shift_start.strftime('%y-%m-%d') == current_date][0]

            if todays_activity:
                flash(f"Shift already started", 'danger')
            else:
                activity = Activity(shift_start=(datetime.now()), relatedUser=current_user)
                db.session.add(activity)
                db.session.commit()
                flash(f"Shift started successfully", 'success')

        elif request.form.get('end_shift') == 'End shift':
            current_activities = Activity.query.filter_by(user_id=current_user.id)
            todays_activity = None
            if(current_activities.count()>0):
                todays_activity = [activity for activity in current_activities if activity.shift_start.strftime('%y-%m-%d') == current_date][0]

            if not todays_activity:
                flash(f"You have to start your shift before you can end it", 'danger')
            elif todays_activity.shift_end:
                flash(f"Shift already ended", 'danger')
            elif not todays_activity.shift_start:
                flash(f"You have not started your shift yet", 'danger')
            else:
                todays_activity.shift_end = datetime.now()
                db.session.commit()
                flash(f"Shift ended successfully", 'success')

        elif request.form.get('start_lunch') == 'Start lunch':
            current_activities = Activity.query.filter_by(user_id=current_user.id)
            todays_activity = None
            if(current_activities.count()>0):
                print('activites found')
                todays_activity = [activity for activity in current_activities if activity.shift_start.strftime('%y-%m-%d') == current_date][0]
            
            if not todays_activity:
                print('11111111')
                flash(f"You have to start your shift to take a lunch break", 'danger')
            elif not todays_activity.shift_start:
                print('2222222')
                flash(f"You have to start your shift to take a lunch break", 'danger')
            elif todays_activity.shift_end:
                flash(f"You need to be on a active shift to take a lunch break", 'danger')
            elif todays_activity.lunch_start and not todays_activity.lunch_end:
                flash(f"You are already on lunch", 'danger')
            elif todays_activity.lunch_start and todays_activity.lunch_end:
                flash(f"You are already taken your lunch today", 'danger')
            elif todays_activity.break_start and not todays_activity.break_end:
                flash(f"You are on a break cannot start a lunch", 'danger')
            else:
                print('adding lunch start time')
                todays_activity.lunch_start = datetime.now()
                db.session.commit()
                flash(f"Lunch started successfully", 'success')

        elif request.form.get('end_lunch') == 'End lunch':
            current_activities = Activity.query.filter_by(user_id=current_user.id)
            todays_activity = None
            if(current_activities.count()>0):
                todays_activity = [activity for activity in current_activities if activity.shift_start.strftime('%y-%m-%d') == current_date][0]
            
            if not todays_activity:
                flash(f"You have to start your shift to end a lunch break", 'danger')
            elif not todays_activity.shift_start:
                flash(f"You have to start your shift to take a lunch break", 'danger')
            elif todays_activity.shift_end:
                flash(f"You need to be on a active shift to take a lunch break", 'danger')
            elif todays_activity.lunch_end:
                flash(f"You have already ended your lunch", 'danger')
            elif todays_activity.lunch_start:
                todays_activity.lunch_end = datetime.now()
                db.session.commit()
                flash(f"Lunch ended successfully", 'success')
            else:
                flash(f"You have to start your lunch before you can end it", 'danger')

        elif request.form.get('start_break') == 'Start break':
            current_activities = Activity.query.filter_by(user_id=current_user.id)
            todays_activity = None
            if(current_activities.count()>0):
                todays_activity = [activity for activity in current_activities if activity.shift_start.strftime('%y-%m-%d') == current_date][0]
            
            if not todays_activity:
                flash(f"You have to start your shift to take a break", 'danger')
            elif not todays_activity.shift_start:
                flash(f"You have to start your shift to take a break", 'danger')
            elif todays_activity.shift_end:
                flash(f"You need to be on a active shift to take a break", 'danger')
            elif todays_activity.break_start and not todays_activity.break_end:
                flash(f"You are already on a break", 'danger')
            elif todays_activity.break_start and todays_activity.break_end:
                flash(f"You are already taken your break today", 'danger')
            elif todays_activity.lunch_start and not todays_activity.lunch_end:
                flash(f"You are on a break cannot start a break", 'danger')
            else:
                todays_activity.break_start = datetime.now()
                db.session.commit()
                flash(f"Break started successfully", 'success')

        elif request.form.get('end_break') == 'End break':
            print('ending break')
            current_activities = Activity.query.filter_by(user_id=current_user.id)
            todays_activity = None
            if(current_activities.count()>0):
                todays_activity = [activity for activity in current_activities if activity.shift_start.strftime('%y-%m-%d') == current_date][0]
            
            if not todays_activity:
                flash(f"You have to start your shift to end you break", 'danger')
            elif not todays_activity.shift_start:
                flash(f"You have to start your shift to end a lunch break", 'danger')
            elif todays_activity.shift_end:
                flash(f"You need to be on a active shift to end a lunch break", 'danger')
            elif todays_activity.break_end:
                flash(f"You have already ended your break", 'danger')
            elif todays_activity.break_start:
                todays_activity.break_end = datetime.now()
                db.session.commit()
                flash(f"Break ended successfully", 'success')
            else:
                flash(f"You have start your break before you can end it", 'danger')


        return redirect(url_for('userActivities'))

    print('Fetching user activities')

    # This is GET posrtion
    user_activities = Activity.query.filter_by(user_id=current_user.id)
    return render_template('userActivity.html', activities=user_activities)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print('user is autheticated')
        return redirect(url_for('userActivities'))
    registerForm = RegistrationForm()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data).decode('utf-8')
        user =  User(name=registerForm.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {registerForm.username.data}", 'succecss')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=registerForm)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('user is autheticated')
        return redirect(url_for('userActivities'))
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(name=loginForm.username.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user, remember=loginForm.remember.data)
            next_page = request.args.get('next')
            return  redirect(next_page) if next_page else redirect(url_for('userActivities'))
        else:
            flash(f"login unsuccessful, check username and password", 'danger')
    return render_template('login.html', title='Login', form=loginForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')