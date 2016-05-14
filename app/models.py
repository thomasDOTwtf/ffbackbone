from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kennwort1@localhost/testdb?charset=utf8&use_unicode=0'  # noqa
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True;
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///c:\sql\sql.db'
db = SQLAlchemy(app)

CommunityASNs = db.Table(
    'CommunityASs',
    db.Column('community_id', db.Integer, db.ForeignKey('community.id')),
    db.Column('AS_id', db.Integer, db.ForeignKey('AS.id'))
)

ASContacts = db.Table(
    'ASContacts',
    db.Column('as_id', db.Integer, db.ForeignKey('AS.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
)

CommunityContacts = db.Table(
    'CommunityContacts',
    db.Column('community_id', db.Integer, db.ForeignKey('community.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
)

PrefixContacts = db.Table(
    'PrefixContacts',
    db.Column('prefix_id', db.Integer, db.ForeignKey('prefix.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
)

PrefixNameServers = db.Table(
    'PrefixNameServers',
    db.Column('prefix_id', db.Integer, db.ForeignKey('prefix.id')),
    db.Column('name_server_id', db.Integer, db.ForeignKey('name_server.id'))
)


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(260), unique=True)
    short = db.Column(db.String(6), unique=True)
    created = db.Column(db.DateTime)
    contacts = db.relationship(
            'Contact',
            secondary=CommunityContacts,
            back_populates="communities"
            )
    ces = db.relationship(
            'CustomerEdge',
            back_populates="community"
            )
    asns = db.relationship(
            'AS',
            secondary=CommunityASNs,
            backref=db.backref('Community', lazy='dynamic')
            )
    prefixes = db.relationship('Prefix', backref='Community', lazy='dynamic')
    nameservers = db.relationship(
        'NameServer',
        back_populates="community"
    )

    def __repr__(self):
        return self.name


class CustomerEdge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), unique=True)
    fqdn = db.Column(db.String(260), unique=True)
    ipv4 = db.Column(db.String(260), unique=True)
    ipv6 = db.Column(db.String(260), unique=True)
    asn_id = db.Column(db.Integer, db.ForeignKey('AS.id'))
    asn = db.relationship(
        'AS',
        back_populates="customeredges"
    )
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    community = db.relationship(
        'Community',
        back_populates="ces"
    )
    sessions = db.relationship(
            'PeeringSession',
            backref='CustomerEdge',
            lazy='dynamic'
            )

    def __repr__(self):
        return self.fqdn


class ProviderEdge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), unique=False)
    fqdn = db.Column(db.String(260), unique=True)
    ipv4 = db.Column(db.String(260), unique=True)
    ipv6 = db.Column(db.String(260), unique=True)
    asn_id = db.Column(db.Integer, db.ForeignKey('AS.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    sessions = db.relationship(
            'PeeringSession',
            backref='ProviderEdge',
            lazy='dynamic'
            )

    def __repr__(self):
        return self.fqdn


class AS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asn = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(260), unique=False)
    descr = db.Column(db.String(260), unique=False)
    created = db.Column(db.DateTime)
    changed = db.Column(db.DateTime)
    approved = db.Column(db.DateTime)
    contacts = db.relationship(
            'Contact',
            secondary=ASContacts,
            backref=db.backref('AS', lazy='dynamic')
            )
    communities = db.relationship(
            'Community',
            secondary=CommunityASNs,
            backref=db.backref('AS', lazy='dynamic')
            )
    provideredges = db.relationship(
            'ProviderEdge',
            backref='AS',
            lazy='dynamic',
            uselist='False'
            )
    customeredges = db.relationship(
        'CustomerEdge',
        back_populates="asn"
    )

    def isapproved(self):
        if self.approved is None:
            return False
        if self.created is None:
            return False
        if self.changed is None:
            return False
        if self.approved>=self.created:
            return True
        return False

    def __repr__(self):
        return 'AS{self.asn}'.format(self=self)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.Unicode(260), unique=True)
    nickname = db.Column(db.Unicode(260), unique=True)
    xmpp = db.Column(db.Unicode(260), unique=True)
    firstname = db.Column(db.Unicode(260), unique=False)
    lastname = db.Column(db.Unicode(260), unique=False)
    login = db.Column(db.Unicode(260), unique=True)
    password = db.Column(db.String(260), unique=True)
    handle = db.Column(db.String(260), unique=True)
    admin = db.Column(db.Boolean)
    communities = db.relationship(
        'Community',
        secondary=CommunityContacts,
        back_populates="contacts"
    )

    def __repr__(self):
        return '{self.nickname} ({self.mail})'.format(self=self)

    def get_communities(self):
        return Community.query.join(Community.contacts).filter(
        Contact.id.like(self.id)).options(
            db.contains_eager(Community.contacts)
            )

    def get_asns(self):
        comm_subq = Community.query.filter(
        Community.contacts.contains(self)).subquery()
        return AS.query.join(comm_subq, AS.Community)

    def get_contacts(self):
        comm_subq = Community.query.filter(
        Community.contacts.contains(self)).subquery()
        contacts=Contact.query.join(comm_subq, Contact.communities).options(db.subqueryload(Contact.communities))
        return contacts

    def get_nameservers(self):
        comm_subq = Community.query.filter(
        Community.contacts.contains(self)).subquery()
        return NameServer.query.join(comm_subq, NameServer.community)

    def get_customeredges(self):
        comm_subq = Community.query.filter(
        Community.contacts.contains(self)).subquery()
        return CustomerEdge.query.options(db.subqueryload(CustomerEdge.asn)).join(comm_subq, CustomerEdge.community)

    def is_ce_permitted(self, ce_id):
        customeredges = self.get_customeredges().filter_by(id=ce_id).all()
        if customeredges is None:
            return False
        else:
            return True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '{self.nickname} [{self.lastname}, {self.firstname}]'.format(self=self)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), unique=False)
    country = db.Column(db.String(2))
    city = db.Column(db.String(5))
    datacenter = db.Column(db.String(5))
    provideredges = db.relationship(
            'ProviderEdge',
            backref='Site',
            lazy='dynamic'
            )
    prefixes = db.relationship('Prefix', backref='Site', lazy='dynamic')

    def __repr__(self):
        return self.name


class PeeringSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pe_id = db.Column(db.Integer, db.ForeignKey('provider_edge.id'))
    ce_id = db.Column(db.Integer, db.ForeignKey('customer_edge.id'))
    pe_v4 = db.Column(db.String(260), unique=True)
    pe_v6 = db.Column(db.String(260), unique=True)
    ce_v4 = db.Column(db.String(260), unique=True)
    ce_v6 = db.Column(db.String(260), unique=True)
    enabled = db.Column(db.Boolean)
    tunneltype_id = db.Column(db.Integer, db.ForeignKey('tunnel_type.id'))

    def __repr__(self):
        return '{self.pe_v4} - {self.ce_v4}'.format(self=self)


class Prefix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(260), unique=True)
    version = db.Column(db.Integer)
    prefixtype_id = db.Column(db.Integer, db.ForeignKey('prefix_type.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    orghandle = db.Column(db.String(260))
    contacts = db.relationship(
            'Contact',
            secondary=PrefixContacts,
            backref=db.backref('Prefix', lazy='dynamic')
            )
    nameservers = db.relationship(
            'NameServer',
            secondary=PrefixNameServers,
            backref=db.backref('Prefix', lazy='dynamic')
            )
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))

    def __repr__(self):
        return self.prefix
    def get_orghandle(self):
        if self.orghandle is None:
            return "FFRL-Default"
        return self.orghandle
    effectiveorghandle = property(get_orghandle)


class PrefixType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), unique=True)
    prefixes = db.relationship('Prefix', backref='PrefixType', lazy='dynamic')

    def __repr__(self):
        return self.name


class NameServer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fqdn = db.Column(db.String(260), unique=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    community = db.relationship(
        'Community',
        back_populates="nameservers"
    )
    def __repr__(self):
        return self.fqdn


class TunnelType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    sessions = db.relationship(
            'PeeringSession',
            backref='TunnelType',
            lazy='dynamic'
            )

    def __repr__(self):
        return self.name


db.create_all()
