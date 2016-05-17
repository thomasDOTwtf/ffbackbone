from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, g  # noqa
from flask.ext.login import current_user, login_required
from datetime import datetime
from app.forms import *
from app.models import *
from netaddr import *

customeredges = Blueprint('customeredges', __name__, template_folder='templates')

@customeredges.route('/customeredge/<ce_id>', methods=['GET', 'POST'])
@login_required
def edit(ce_id):
    if current_user.is_ce_permitted(ce_id) is False:
        flash('You don''t belong to the CustomerEdge''s Community')  # noqa
        return redirect(url_for('customeredges.list'))
    ce = CustomerEdge.query.filter_by(id=ce_id).options(
        db.joinedload('asn')).options(db.lazyload('community')).first()
    sessions = PeeringSession.query.filter_by(ce_id=ce.id).options(
        db.joinedload('TunnelType')).options(db.joinedload('ProviderEdge'))
    form = CustomerEdgeForm(obj=ce, edit=True)
    form.asn.query = current_user.get_asns()
    form.community.query = current_user.get_communities()
    form.submit.label.text = 'Update Customer Edge'
    sessionform = SessionForm()
    sessionform.type.query = TunnelType.query
    if form.validate_on_submit():
        flash('CustomerEdge edited successfully!')
        return redirect(url_for('customeredges.list'))
    if sessionform.validate_on_submit():
        print('gen sessions')
        #Generate GRE tunnels, ips and sessions
        pes = ProviderEdge.query.all()
        for pe in pes:
            transfer = Prefix.get_availprefix(1,4,31)
            session = PeeringSession()
            session.pe_id = pe.id
            session.ce_id = ce_id
            session.pe_v4 = str(transfer[0])
            session.ce_v4 = str(transfer[1])
            session.tunneltype_id = 1
            session.enabled = 1
            db.session.add(session)
            db.session.commit()
        return redirect(url_for('customeredges.edit',ce_id=ce_id))
    return render_template(
        'customeredge/detail.html',
        ce=ce,
        sessions=sessions, form=form, sessionform=sessionform)

@customeredges.route('/customeredge/<ce_id>/<session_id>/<state>')
@login_required
def session_changestate(ce_id, session_id, state):
    if current_user.is_ce_permitted(ce_id) is False:
        flash('You don''t belong to the CustomerEdge''s Community')  # noqa
        return redirect(url_for('customeredges.list'))
    session = PeeringSession.query.filter_by(id=session_id).first()
    session.enabled = state
    db.session.add(session)
    db.session.commit()
    return redirect(url_for('customeredges.edit',ce_id=ce_id))

@customeredges.route('/customeredge/<ce_id>/deletesessions')
@login_required
def delete_sessions(ce_id):
    if current_user.is_ce_permitted(ce_id) is False:
        flash('You don''t belong to the CustomerEdge''s Community')  # noqa
        return redirect(url_for('customeredges.list'))
    ce = CustomerEdge.query.filter_by(id=ce_id).first()
    ce.sessions.delete()
    db.session.commit()
    return redirect(url_for('customeredges.edit', ce_id=ce_id))

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
    return render_template("customeredge/new.html", form=form)