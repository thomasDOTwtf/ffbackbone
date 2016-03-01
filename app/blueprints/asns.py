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
    form.community.query = current_user.get_communities()
    if form.validate_on_submit():
        asn = AS()
        form.populate_obj(asn)
        asn.created = datetime.now()
        asn.changed = datetime.now()
        db.session.add(asn)
        asn.Community = form.community.data
        db.session.commit()
        flash('Customer Edge has been created')
        return redirect(url_for('asn_list'))
    return render_template("as/detail.html", form=form)


@asns.route('/asn/delete/<asn_id>')
@login_required
def delete(asn_id):
    asn=AS.query.filter_by(id=asn_id)
    asn.delete()
    db.session.commit()
    flash('AS deleted successfully!')
    return redirect(url_for('asn_list'))


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
    if this_asn.Community is not None:
        form.community.data = this_asn.Community
    form.community.query = current_user.get_communities()
    if form.validate_on_submit():
        form.populate_obj(this_asn)
        this_asn.changed = datetime.now()
        db.session.add(this_asn)
        db.session.commit()
        return redirect(url_for('asn_list'))
    return render_template("as/detail.html", form=form)


@asns.route('/asns')
@login_required
def list():
    return render_template("as/list.html",asns=current_user.get_asns())