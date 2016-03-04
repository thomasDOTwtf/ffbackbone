from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, g  # noqa
from flask.ext.login import current_user, login_required
from datetime import datetime
from app.forms import *
from app.models import *

prefixes = Blueprint('prefixes', __name__, template_folder='templates')

@prefixes.route('/prefix')
@login_required
def list():
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
    return render_template('prefix/list.html.html',
                           prefixes=prefixes)


@prefixes.route('/prefix/<prefix_id>')
@login_required
def edit(prefix_id):
    prefix = Prefix.query.filter_by(id=prefix_id).options(
        db.subqueryload('nameservers')
    ).options(
        db.subqueryload('contacts')
    ).options(
        db.subqueryload('PrefixType')
    ).options(
        db.subqueryload('Site')
    ).options(
        db.subqueryload('Community')
    ).first_or_404()
    community = Community.query.filter_by(id=prefix.community_id).join(
        Contact,
        Community.contacts
    ).filter_by(id=current_user.id)
    if community.count() == 0:
        flash('You don''t belong to the Prefixes Community')  # noqa
        return redirect(url_for('prefixes.list'))

    nameservers = current_user.get_nameservers()
    return render_template(
        'prefix/detail.html',
        prefix=prefix,
        nameservers=nameservers)
