from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, g  # noqa
from flask.ext.login import current_user, login_required
from datetime import datetime
from app.forms import *
from app.models import *

customeredges = Blueprint('customeredges', __name__, template_folder='templates')

@customeredges.route('/customeredge/<ce_id>')
@login_required
def edit(ce_id):
    customeredges = current_user.get_customeredges().filter_by(id=ce_id).all()
    if customeredges is None:
        flash('You don''t belong to the CustomerEdge''s Community')  # noqa
        return redirect(url_for('customeredges.list'))
    ce = CustomerEdge.query.filter_by(id=ce_id).options(
        db.joinedload('AS')).options(db.lazyload('Community')).first()
    sessions = PeeringSession.query.filter_by(ce_id=ce.id).options(
        db.joinedload('TunnelType')).options(db.joinedload('ProviderEdge'))
    return render_template(
        'backbone/customeredge.html',
        ce=ce,
        sessions=sessions)


@customeredges.route('/customeredge')
@login_required
def list():
    return render_template('backbone/customeredges.html',
                           customeredges=current_user.get_customeredges())


@customeredges.route('/customeredge/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateCustomerEdge()
    form.community.query = current_user.get_communities()
    form.asn.query = current_user.get_asns()
    if form.validate_on_submit():
        ce = CustomerEdge()
        ce.name = form.shortname.data
        ce.fqdn = form.fqdn.data
        ce.ipv4 = form.ipv4.data
        ce.ipv6 = form.ipv6.data
        ce.asn_id = form.asn.data.id
        db.session.add(ce)
        form.community.data.ces.append(ce)
        db.session.commit()
        flash('Customer Edge has been created')
        return redirect(url_for('customeredges.list'))
    return render_template("backbone/customeredge-create.html", form=form)