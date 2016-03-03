from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, g  # noqa
from flask.ext.login import current_user, login_required
from datetime import datetime
from app.forms import *
from app.models import *

nameservers = Blueprint('nameservers', __name__, template_folder='templates')

@nameservers.route('/nameserver/new', methods=['GET', 'POST'])
@login_required
def create():
    form = FormNameserver()
    form.community.query = current_user.get_communities()
    if form.validate_on_submit():
        nameserver = NameServer()
        form.populate_obj(nameserver)
        nameserver.Community = form.community.data
        db.session.add(nameserver)
        db.session.commit()
        flash('Nameserver has been created')
        return redirect(url_for('nameservers.list'))
    return render_template("nameserver/detail.html", form=form, edit=False)


@nameservers.route('/nameserver/delete/<nameserver_id>')
@login_required
def delete(nameserver_id):
    nameserver=NameServer.query.filter_by(id=nameserver_id)
    nameserver.delete()
    db.session.commit()
    flash('Nameserver deleted successfully!')
    return redirect(url_for('nameservers.list'))


@nameservers.route('/nameserver/<nameserver_id>', methods=['GET', 'POST'])
@login_required
def edit(nameserver_id):
    comm_subq = Community.query.filter(
        Community.contacts.contains(current_user)).subquery()
    this_nameserver = NameServer.query.filter_by(id=nameserver_id).join(comm_subq, AS.Community).first()
    if this_nameserver is None:
        flash('Access denied!')
        return redirect(url_for('index'))
    form = FormNameserver(obj=this_nameserver, edit=True)
    if this_nameserver.Community is not None:
        form.community.data = this_nameserver.Community
    form.community.query = current_user.get_communities()
    if form.validate_on_submit():
        form.populate_obj(this_nameserver)
        this_nameserver.changed = datetime.now()
        db.session.add(this_nameserver)
        db.session.commit()
        return redirect(url_for('nameservers.list'))
    return render_template("nameserver/detail.html", form=form, edit=True)


@nameservers.route('/nameserver')
@nameservers.route('/nameserver/')
@login_required
def list():
    return render_template("nameserver/list.html",nameservers=current_user.get_nameservers())