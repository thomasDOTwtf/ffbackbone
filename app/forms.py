from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, IPAddress  # noqa
from wtforms import ValidationError


class LoginForm(Form):
    email = StringField('Login', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class CreateCustomerEdge(Form):
    shortname = StringField(
            'Short Name',
            validators=[Required(), Length(1, 16)])
    community = QuerySelectField(
            'Community',
            validators=[Required()], get_label='name')
    fqdn = StringField('FQDN', validators=[Required(), Length(1, 255)])
    asn = QuerySelectField('ASN', validators=[Required()])
    ipv4 = StringField('IPv4', validators=[Required(), IPAddress(ipv4=True)])
    ipv6 = StringField(
            'IPv6',
            validators=[Required(), IPAddress(ipv6=True, ipv4=False)])
    submit = SubmitField('Create CE')
