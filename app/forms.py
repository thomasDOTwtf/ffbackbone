from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, HiddenField,DateTimeField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, IPAddress  # noqa
from wtforms import ValidationError


class LoginForm(Form):
    email = StringField('Login', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class CustomerEdgeForm(Form):
    name = StringField(
            'Short Name',
            validators=[DataRequired(), Length(1, 16)])
    community = QuerySelectField(
            'Community',
            validators=[DataRequired()], get_label='name')
    fqdn = StringField('FQDN', validators=[DataRequired(), Length(1, 255)])
    asn = QuerySelectField('ASN', validators=[DataRequired()])
    ipv4 = StringField('IPv4', validators=[DataRequired(), IPAddress(ipv4=True)])
    ipv6 = StringField(
            'IPv6',
            validators=[DataRequired(), IPAddress(ipv6=True, ipv4=False)])
    submit = SubmitField('Create CE')


class FormAS(Form):
    asn = IntegerField('ASN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(1, 16)])
    descr = StringField('Description', validators=[Length(1, 255)])
    communities = QuerySelectMultipleField('Community', validators=[DataRequired()])
    contacts = QuerySelectMultipleField('Contact')
    submit = SubmitField('Submit')


class FormNameserver(Form):
    fqdn = StringField('FQDN', validators=[DataRequired()])
    community = QuerySelectField('Community', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FormContact(Form):
    def my_password_check(form, field):
        if not form.edit.object_data:
            if field.data is None:
                raise ValidationError('Password should not be empty')
            if len(field.data) < 8:
                raise ValidationError('Password should be at least 8 chars')
    edit = HiddenField()
    password = HiddenField()
    firstname = StringField('Firstname', validators=[DataRequired(), Length(1, 255)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(1, 255)])
    mail = StringField('E-Mail', validators=[Email(), DataRequired(), Length(1, 255)])
    xmpp = StringField('XMPP', validators=[Email(), Length(1, 255)])
    nickname = StringField('Nickname', validators=[DataRequired(), Length(1, 255)])
    handle = StringField('Handle', validators=[DataRequired(), Length(1, 255)])
    login = StringField('Login', validators=[DataRequired(), Length(1, 255)])
    newpassword = PasswordField('Password', validators=[my_password_check])
    admin = BooleanField('Admin')
    communities = QuerySelectMultipleField('Community', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FormCommunity(Form):
    name = StringField('Name', validators=[DataRequired(), Length(1, 255)])
    short = StringField('Short', validators=[DataRequired(), Length(1, 8)])
    submit = SubmitField('Update Community')
