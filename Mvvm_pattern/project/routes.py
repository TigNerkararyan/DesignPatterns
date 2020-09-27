from project import app
from flask import render_template, request, url_for, redirect, flash
from project.models import User, db
from project.viewmodels import RegisterViewModel, EventViewModel
from project.forms import RegisterForm, EventForm

@app.route('/', methods=['GET'])
def index():
    all_user = User.query.all()
    events = EventViewModel.get_all_events()
    return render_template("index.html", title="Home page", form=all_user, events=events), 200

@app.route('/setup')
def setup():
    db.drop_all()
    db.create_all()
    return "OK", 200

@app.route('/wall')
def wall():
    return render_template("wall.html", title="Wall", events=EventViewModel.get_all_events()), 200


@app.route('/reservation')
def reservation():
    form = EventForm()
    return render_template("booking.html", title="Reservation", form=form), 200


@app.route('/booking', methods=['POST', 'GET'])
def booking():
    form = EventForm(request.form)
    event_view_model = EventViewModel(form, request)
    event_view_model.submit_event()
    return redirect(url_for('reservation'))


@app.route('/record')
def record():
    form = RegisterForm()
    return render_template("registration.html", title="Record", form=form), 200

@app.route('/register', methods=['POST'])
def register_check():
    form = RegisterForm(request.form)
    register_view_model = RegisterViewModel(form=form, method=request.method)
    register_view_model.validate()
    if register_view_model.getError():
        return render_template("registration.html", title="Record", form=form, error=register_view_model.getError())
    return redirect(url_for('record'))


@app.route('/users')
def users():
    all_user = User.query.all()
    return render_template("users.html", title="Users", users=all_user), 200