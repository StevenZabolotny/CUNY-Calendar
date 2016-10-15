import flask
from apiclient import discovery
from oauth2client import client
import httplib2
import json
import yaml
import mysql.connector
import sql

app = flask.Flask(__name__)
CLIENT_SECRET_FILE = "client_secrets.json"

@app.route('/', methods=["GET", "POST"])
def index():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        return flask.redirect(flask.url_for('auth'))     
    return flask.render_template("index.html")

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets('client_secrets.json',
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    #,include_granted_scopes=True)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('auth'))

@app.route("/auth")
def auth():
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    creds = yaml.safe_load(credentials.to_json())
    n = sql.getName(creds["client_id"])
    if n == 0:
        return flask.redirect(flask.url_for("register"))
    else:
        return flask.redirect(flask.url_for("user"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "GET":
        return flask.render_template("register.html")
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    creds = yaml.safe_load(credentials.to_json())
    fname = flask.request.form["fname"]
    lname = flask.request.form["lname"]
    sql.addName(creds["client_id"], fname, lname)
    uname = sql.getName(creds["client_id"])
    cpuser = flask.request.form["cpuser"]
    cppw = flask.request.form["cppw"]
    cfuser = flask.request.form["cfuser"]
    cfpw = flask.request.form["cfpw"]
    sql.addAccount(uname, cpuser, cppw, cfuser, cfpw)
    return flask.redirect(flask.url_for("user"))

@app.route("/user")
def user():
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    creds = yaml.safe_load(credentials.to_json())
    uname = sql.getName(creds["client_id"])
    fname = uname.split(".")[0]
    lname = uname.split(".")[1]
    return flask.render_template("user.html", fname=fname, lname=lname)

if __name__ == '__main__':
    sql.createTables()
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()
