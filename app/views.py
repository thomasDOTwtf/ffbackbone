from app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import render_template, flash, redirect, session, url_for, request, g  # noqa
from flask.ext.login import login_user, logout_user, current_user, login_required  # noqa
from flask import Flask, Response
from flask.ext.login import LoginManager, UserMixin, login_required
from flask_bootstrap import Bootstrap
from datetime import datetime
from app.blueprints.contacts import contacts
from app.blueprints.asns import asns
from app.blueprints.customeredges import customeredges
from app.blueprints.prefixes import prefixes
from app.blueprints.communities import communities
from app.blueprints.session import session
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
app.register_blueprint(session)
app.register_blueprint(contacts)
app.register_blueprint(asns)
app.register_blueprint(customeredges)
app.register_blueprint(prefixes)
app.register_blueprint(communities)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Home')

@app.before_request
def before_request():
    g.user = current_user
