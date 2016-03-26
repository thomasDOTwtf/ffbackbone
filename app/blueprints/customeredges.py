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
        db.joinedload('asn')).options(db.lazyload('community')).first()
    sessions = PeeringSession.query.filter_by(ce_id=ce.id).options(
        db.joinedload('TunnelType')).options(db.joinedload('ProviderEdge'))
    form = CustomerEdgeForm(obj=ce, edit=True)
    form.asn.query = current_user.get_asns()
    form.community.query = current_user.get_communities()
    sessionform = SessionForm()
    sessionform.type.query = TunnelType.query
    return render_template(
        'customeredge/detail-old.html',
        ce=ce,
        sessions=sessions, form=form, sessionform=sessionform)


@customeredges.route('/customeredge')
@login_required
def list():
    ces = current_user.get_customeredges()
    return render_template('customeredge/list.html',
                           customeredges=ces)

@customeredges.route('/customeredge/delete/<ce_id>')
@login_required
def delete(ce_id):
    this_edge=CustomerEdge.query.filter_by(id=ce_id)
    this_edge.delete()
    db.session.commit()
    flash('CustomerEdge has been deleted successfully')
    return redirect(url_for('customeredges.list'))

@customeredges.route('/customeredge/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CustomerEdgeForm()
    form.community.query = current_user.get_communities()
    form.asn.query = current_user.get_asns()
    form.submit.label.text='Create CustomerEdge'
    if form.validate_on_submit():
        ce = CustomerEdge()
        form.populate_obj(ce)
        db.session.add(ce)
        db.session.commit()
        flash('Customer Edge has been created')
        return redirect(url_for('customeredges.list'))
    return render_template("customeredge/detail.html", form=form)