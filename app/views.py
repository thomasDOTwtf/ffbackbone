from app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import render_template, flash, redirect, session, url_for, request, g  # noqa
from flask.ext.login import login_user, logout_user, current_user, login_required  # noqa
from flask import Flask, Response
from flask.ext.login import LoginManager, UserMixin, login_required
from flask_bootstrap import Bootstrap

from app.models import *
from app.forms import *
from app.email import *
import pprint

admin = Admin(app)
admin.add_view(ModelView(Community, db.session))
admin.add_view(ModelView(ProviderEdge, db.session))
admin.add_view(ModelView(CustomerEdge, db.session))
admin.add_view(ModelView(Site, db.session))
admin.add_view(ModelView(Prefix, db.session))
admin.add_view(ModelView(AS, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(PeeringSession, db.session))
admin.add_view(ModelView(NameServer, db.session))
admin.add_view(ModelView(TunnelType, db.session))
admin.add_view(ModelView(PrefixType, db.session))

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Contact.query.get(int(user_id))

Bootstrap(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Contact.query.filter_by(login=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@app.route('/user/<login>')
@login_required
def user(login):
    user = User.query.filter_by(login=login).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('base.html')


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.set_password(form.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@app.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = Contact.query.filter_by(mail=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.mail, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)


@app.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = Contact.query.filter_by(mail=form.email.data).first_or_404()
        if user is None:
            return redirect(url_for('index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('index'))
    return render_template('auth/reset_password.html', form=form)


@app.route('/prefixes')
@login_required
def prefixes():
    community = Community.query.join(
            Contact,
            Community.contacts
            ).filter_by(id=current_user.id).first_or_404()
    prefixes = Prefix.query.filter_by(
            community_id=community.id
            ).options(
                    db.joinedload('nameservers')
                    ).options(
                            db.joinedload('contacts')
                            ).options(
                                    db.subqueryload('PrefixType')
                                    ).options(db.subqueryload('Site'))
    if prefixes.count() == 0:
        flash('No prefixes are currently assigned to you.')  # noqa
        return redirect(url_for('index'))
    return render_template('backbone/prefixes.html',
                           prefixes=prefixes)


@app.route('/prefix/<prefix_id>')
@login_required
def prefix(prefix_id):
    return render_template('backbone/prefix.html')


@app.route('/customeredge/<ce_id>')
@login_required
def customeredge(ce_id):
    communities_self = Community.query.join(
            Contact,
            Community.contacts
            ).filter_by(id=current_user.id).join(
                    CustomerEdge,
                    Community.ces).options(
                            db.joinedload('ces')
                            ).filter_by(id=ce_id)
    if communities_self.count() == 0:
        flash('You don''t belong to the CustomerEdge''s Community')  # noqa
        return redirect(url_for('index'))
    ce = CustomerEdge.query.filter_by(id=ce_id).options(db.joinedload('AS')).options(db.lazyload('Community')).first()
    sessions = PeeringSession.query.filter_by(ce_id=ce.id).options(db.joinedload('TunnelType')).options(db.joinedload('ProviderEdge'))  #noqa
    return render_template(
            'backbone/customeredge.html',
            ce=ce,
            sessions=sessions)


@app.route('/contact/<contact_id>')
@login_required
def contact(contact_id):
    contact = Contact.query.filter_by(id=contact_id).first_or_404()
    communities_self = Community.query.join(
            Contact,
            Community.contacts
            ).filter_by(id=current_user.id)
    communities_edit = Community.query.join(
            Contact,
            Community.contacts
            ).filter_by(id=contact_id)
    same = False
    for community_self in communities_self:
        for community_edit in communities_edit:
            if community_edit.id == community_self.id:
                community_self.selected = True
                same = True
    if (current_user.admin is False and int(contact_id) != current_user.id) or (current_user.admin is True and same is False):  # noqa
        flash('You don''t have permissions to edit selected contact information')  # noqa
        return redirect(url_for('index'))
    return render_template('contact/detail.html',
                           contact=contact,
                           communities=communities_self)


@app.route('/contacts')
@login_required
def contacts():
    communities_self = Community.query.join(
            Contact,
            Community.contacts
            ).filter_by(id=current_user.id).options(db.joinedload('contacts'))
    contacts = set()
    for community_self in communities_self:
        for contact in community_self.contacts:
            if contact not in contacts:
                contact.communities = Community.query.join(
                                Contact,
                                Community.contacts
                                ).filter_by(id=contact.id)
                contacts.add(contact)
    return render_template('contact/list.html',
                           contacts=contacts,
                           admin=current_user.admin)


@app.route('/customeredges')
@login_required
def customeredges():
    communities_self = Community.query.join(
            Contact,
            Community.contacts
            ).filter_by(id=current_user.id).options(db.joinedload('contacts'))
    customeredges = set()
    for community_self in communities_self:
        for ce in community_self.ces:
            if ce not in customeredges:
                ce.community = community_self
                ce.asn = AS.query.filter_by(id=ce.asn_id).first()
                customeredges.add(ce)
    return render_template('backbone/customeredges.html',
                           customeredges=customeredges)


@app.route('/communities')
@login_required
def communities():
    communities_self = Community.query.join(
            Contact,
            Community.contacts
            ).options(db.joinedload('asns')).options(db.lazyload('nameservers')).filter_by(id=current_user.id).options(db.joinedload('contacts'))
    for community in communities_self:
        community.isfirst = True
        break
    return render_template('communities.html',
                           communities=communities_self,
                           count=communities_self.count()
                           )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
