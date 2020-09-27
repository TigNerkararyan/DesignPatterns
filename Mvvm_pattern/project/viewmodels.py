import re
from project.models import User, Event, db
from flask import flash

class RegisterViewModel(object):

    def __init__(self, form, method):
        self.email = ""
        self.username = ""
        self.password = ""
        self.isAdmin = False
        self.error = ""
        self.register_success = False
        self.new_user = User
        self.form = form
        self.method = method

    def validateUsername(self):
        if self.username == "":
            self.error += "'{} ' Username is not available.\n".format(self.username)
            return False
        return True

    def validatePassword(self):
        if self.password == "":
            self.error += "Your password is not suitable for use."
            return False
        return True

    def validateEmail(self):
        if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.email) is None:
            self.error += "'{}' e-mail address is not available.\n".format(self.email)
            return False
        return True

    def getError(self):
        return self.error

    def getRegisterSuccess(self):
        return self.register_success

    def getRegisteredUser(self):
        return self.new_user

    def checkValidation(self):
        if self.validateEmail() and self.validateUsername() and self.validatePassword():
            self.new_user = User(self.username, self.email, self.password, self.isAdmin)
            db.session.add(self.new_user)
            db.session.commit()
            self.register_success = True

    def validate(self):
        if self.method == "POST":
            self.username = self.form.username.data
            self.password = self.form.password.data
            self.email = self.form.email.data
            self.checkValidation()

            if self.register_success:
                flash("Registration Successful " + self.getRegisteredUser().username, "success")
            else:
                flash(self.getError(), "danger")
        else:
            flash(self.form.errors, "danger")

class EventViewModel(object):
    def __init__(self, form, request):
        self.date = ""
        self.form = form
        self.username = request.values.get('username')
        self.request_method = request.method
        self.request = request

    def validate_event_exist(self):
        return Event.query.filter_by(date=self.date).first()

    def submit_event(self):
        if self.request_method == "POST":
            self.date = self.form.date.data
            user_id = 0
            for item in User.query.filter_by(username=self.username):
                user_id+= item.id
            if self.validate_event_exist():
                flash("The date and time you selected are unfortunately full : " + "(" + self.date + "). Try to choose another date.", "danger")
            else:
                event = Event(self.date)
                db.session.add(event)
                for item in User.query.filter_by(username=self.username):
                    item.event.append(event)
                    db.session.add(item)
                    flash("Booked : " + "(" + self.date + "). You can see from your profile.", "success")
                    db.session.commit()
        else:
            flash(self.form.errors, "danger")

    @staticmethod
    def get_all_events():
        return Event.query.order_by(Event.id.desc()).all()