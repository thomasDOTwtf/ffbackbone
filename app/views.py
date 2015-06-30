from app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from db import *

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


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html', title='Home', user=user)
