from flask import Flask

app = Flask(__name__)
app.secret_key = 'ReallySecretKeyUsedForImportantThings'
from app import views

