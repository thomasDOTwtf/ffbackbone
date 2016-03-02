from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, g  # noqa
from flask.ext.login import current_user, login_required
from datetime import datetime
from app.forms import *
from app.models import *

communities = Blueprint('communities', __name__, template_folder='templates')

@communities.route('/community')
@login_required
def list():
    communities_self = Community.query.join(
        Contact,
        Community.contacts
    ).options(db.joinedload('asns')).options(
        db.lazyload('nameservers')
    ).filter_by(id=current_user.id).options(
        db.joinedload('contacts')).all()
    if communities_self is not None:
        communities_self[0].isfirst = True
    return render_template('communities.html',
                           communities=communities_self,
                           count=len(communities_self))
