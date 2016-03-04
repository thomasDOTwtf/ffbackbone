from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, g  # noqa
from flask.ext.login import current_user, login_required
from datetime import datetime
from app.forms import *
from app.models import *

asns = Blueprint('asns', __name__, template_folder='templates')

@asns.route('/asn/new', methods=['GET', 'POST'])
@login_required
def create():
    form = FormAS()
    form.communities.query = current_user.get_communities()
    form.contacts.query = current_user.get_contacts()
    form.submit.label.text='Create ASN'
    if form.validate_on_submit():
        asn = AS()
        form.populate_obj(asn)
        asn.created = datetime.now()
        asn.changed = datetime.now()
        db.session.add(asn)
        db.session.commit()
        flash('Customer Edge has been created')
        return redirect(url_for('asns.list'))
    return render_template("as/detail.html", form=form, edit=False)


@asns.route('/asn/delete/<asn_id>')
@login_required
def delete(asn_id):
    asn=AS.query.filter_by(id=asn_id)
    asn.delete()
    db.session.commit()
    flash('AS deleted successfully!')
    return redirect(url_for('asns.list'))


@asns.route('/asn/<asn_id>', methods=['GET', 'POST'])
@login_required
def edit(asn_id):
    comm_subq = Community.query.filter(
        Community.contacts.contains(current_user)).subquery()
    this_asn = AS.query.filter_by(id=asn_id).join(comm_subq, AS.Community).first()
    if this_asn is None:
        flash('Access denied!')
        return redirect(url_for('index'))
    form = FormAS(obj=this_asn, edit=True)
    form.communities.query = current_user.get_communities()
    form.contacts.query = current_user.get_contacts()
    form.submit.label.text='Update ASN'
    if form.validate_on_submit():
        form.populate_obj(this_asn)
        this_asn.changed = datetime.now()
        db.session.add(this_asn)
        db.session.commit()
        return redirect(url_for('asns.list'))
    return render_template("as/detail.html", form=form, edit=True)


@asns.route('/asn')
@asns.route('/asn/')
@login_required
def list():
    return render_template("as/list.html",asns=current_user.get_asns())