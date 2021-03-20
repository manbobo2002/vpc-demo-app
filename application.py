import json
import urllib.error
import urllib.request

from flask import Flask, request, abort, render_template

import db

database = db.DB()
application = Flask(__name__)
try:
    doc = urllib.request.urlopen("http://169.254.169.254/latest/dynamic/instance-identity/document", timeout=1).read()
except urllib.error.URLError:
    doc = None

if doc:
    application.config['REGION'] = json.loads(doc)['availabilityZone']
else:
    application.config['REGION'] = "unknown region"


@application.route("/")
def home():
    #country = database.query("SELECT LocID, Location, Variant, Time, PopMale, PopFemale, PopTotal, PopDensity from population;")
    country_list = database.query("SELECT DISTINCT Location from population;")
    year_data = database.query("SELECT DISTINCT Time from population;")

    #print(country)
    return render_template('main.html', countries=country_list, years=year_data)

@application.route("/facts" , methods=['GET', 'POST'])
def facts():
    country_name = request.form.get('country')
    #print(country_name)
    year_select = request.form.get('year')
    #print(year_select)
    country = database.query(f"SELECT LocID, Location, Variant, Time, PopMale, PopFemale, PopTotal, PopDensity from population where Location = '{country_name}' and Time = {year_select};")
    #print(country)
    return render_template('fact.html', country=country)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0', port=8443)
