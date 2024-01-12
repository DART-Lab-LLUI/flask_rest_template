from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

from server.models.auth import Role, User
from server.user_mng import bp
from server.user_mng.decorator import role_required_web
from server.extensions import db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3)])
    submit = SubmitField('Login')


class SetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=3)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('new_password')])
    submit = SubmitField('Set Password')


class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3)])
    roles = SelectMultipleField('Roles', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Add User')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.verify_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('user_mng.user_management'))
                else:
                    flash('Invalid username or password.')
            else:
                flash('Invalid username or password.')

    return render_template('login.html', form=form)


@bp.route('/', methods=['GET'])
@login_required
@role_required_web("admin")
def user_management():
    form = NewUserForm()
    form.roles.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]

    users = User.query.all()

    return render_template('user_management.html', form=form, users=users)


@bp.route('/delete_user/<int:id>')
@login_required
@role_required_web("admin")
def delete_user(id):
    user = User.query.get_or_404(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    flash(f'User {id} deleted')
    return redirect(url_for('user_mng.user_management'))


@bp.route('/set_password/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required_web("admin")
def set_password(id):
    user = User.query.get_or_404(id)
    form = SetPasswordForm()
    if form.validate_on_submit():
        user.password = form.new_password.data  # Your method to hash and set the new password
        db.session.commit()
        flash('Password updated successfully')
        return redirect(url_for('user_mng.user_management'))

    return render_template('set_password.html', form=form, user=user)


@bp.route('/add_user', methods=['POST'])
@login_required
@role_required_web("admin")
def add_user():
    form = NewUserForm()
    username = form.username.data
    password = form.password.data
    role_ids = form.roles.data

    if User.query.filter_by(username=username).first() is not None:
        flash('User already exists')
    else:
        new_user = User(username=username, password=password)
        for role_id in role_ids:
            role = Role.query.get(role_id)
            new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully')

    return redirect(url_for('user_mng.user_management'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged-out')
    return redirect(url_for('user_mng.login'))
