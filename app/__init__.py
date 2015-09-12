from flask import Flask

app = Flask(__name__)
app.secret_key = 'ReallySecretKeyUsedForImportantThings'
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[FFRL BackboneAdmin]'
app.config['FLASKY_MAIL_SENDER']='admin@ffrl.de'

from app import views

