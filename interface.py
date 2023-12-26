## To generate

from flask import Flask, render_template, request
from preprocessing import *

# import psycopg2

app = Flask(__name__)
config = readConfigJSON()

@app.route('/' , methods=["GET", "POST"])
def mainpage():
    availableDB = []
    p_query = ""
    ap_query = {}
    schemas = {}
    selectedDB = ""
    query = ""
    if request.method == "POST":
        selectedDB = options()
        connection = connectPostgreSQL(config[selectedDB])
        schemas = showSchema(getSchema(connection))

        ## Retrieve SQL query from input
        query = request.form["query"]
        ## Get QEPS
        p_query = getQEP(connection, query)
        ## Get AQPs
        ap_query = getAQP(connection, query)

    for key in config:
        availableDB.append(key)
    print(availableDB)

    # Render HTML page to display GUI
    return render_template("mainpage.html",
                           DBs=availableDB,
                           selected = selectedDB,
                           que = query,
                           p_query = p_query,
                           ap_query = ap_query,
                           schema = schemas)


def options():
    selectedDB = request.form["database"]

    return selectedDB
