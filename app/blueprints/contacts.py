from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, g  # noqa
from flask.ext.login import current_user, login_required
from app.forms import *
from app.models import *

contacts = Blueprint('contacts', __name__, template_folder='templates')


@contacts.route('/contacts')
@login_required
def list():
    return render_template('contact/list.html',
                           contacts=current_user.get_contacts(),
                           admin=current_user.admin)


@contacts.route('/contact/new', methods=['GET', 'POST'])
@login_required
def create():
    form = FormContact()
    form.community.query = current_user.get_communities()
    if form.validate_on_submit():
        contact = Contact()
        form.populate_obj(contact)
        db.session.add(contact)
        contact.Community = form.community.data
        db.session.commit()
        flash('Contact has been created')
        return redirect(url_for('contacts.list'))
    return render_template("contact/detail.html", form=form)


@contacts.route('/contact/<contact_id>', methods=['GET', 'POST'])
@login_required
def edit(contact_id):
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
    if (current_user.admin is False and int(contact_id) != current_user.id) or (
                    current_user.admin is True and same is False):  # noqa
        flash('You don''t have permissions to edit selected contact information')  # noqa
        return redirect(url_for('index'))
    form = FormContact(obj=contact, edit=True)
    form.community.query = current_user.get_communities()
    if contact.Community is not None:
        form.community.data = contact.Community
    if form.validate_on_submit():
        form.populate_obj(contact)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('contacts.list'))
    return render_template('contact/detail.html',
                           contact=contact,
                           communities=communities_self,
                           form=form)
