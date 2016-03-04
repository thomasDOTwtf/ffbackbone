from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import  g
from flask.ext.login import current_user,LoginManager
from flask_bootstrap import Bootstrap
from app.blueprints.contacts import contacts
from app.blueprints.asns import asns
from app.blueprints.nameservers import nameservers
from app.blueprints.customeredges import customeredges
from app.blueprints.prefixes import prefixes
from app.blueprints.communities import communities
from app.blueprints.session import session
from app.models import *
from app.email import *

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
app.register_blueprint(nameservers)
app.register_blueprint(asns)
app.register_blueprint(customeredges)
app.register_blueprint(prefixes)
app.register_blueprint(communities)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', contact=current_user)


@app.before_request
def before_request():
    g.user = current_user
