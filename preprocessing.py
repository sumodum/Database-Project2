## To preprocess input from GUI such that it can be passed to backend
## to compute and generate the query plans
import json
from annotation import *
import psycopg2
import psycopg2.extras

## Read config.json to get credentials for database
def readConfigJSON():
    with open("config.json", "r") as file:
        config = json.load(file)

    return config

## Connect to selected PostgreSQL database
def connectPostgreSQL(configDB):
    try:
        conn = None
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host= configDB["host"],
            database=configDB["database"],
            user=configDB["user"],
            password=configDB["password"],
            #port:configDB["port"] ## uncomment line if database not hosted on cloud
        )

        print('Success')

        #  create a new cursor
        #cur = conn.cursor()
    except Exception as error:
        print('Cause: {}'.format(error))
        conn = None

    return conn

## Pass in query to PosgreSQL to get QEP
def getQEP(connected, query):
    try:
        if query != "" and connected:
            cur = connected.cursor()
            print('PostgreSQL database version:')
            cur.execute("EXPLAIN (FORMAT JSON) " + query)
            plan = cur.fetchall()
        else:
            return {"Please enter the right SQL query!" : None}
    except:
        return {"Please enter the right SQL query!" : None}

    annotate = Annotator()
    planNLP = annotate.wrapper(plan)

    return planNLP

## Pass in query to PosgreSQL to get top 3 alternative plans
def getAQP(connected ,query):
    # Get the top3 alternative plans
    alternatives = {}
    try:
        if query != "" and connected:
            cur = connected.cursor()
            ## Get AQP 1 Disable indexscan
            cur.execute("SET LOCAL enable_indexscan = FALSE")
            cur.execute("EXPLAIN (FORMAT JSON) " + query)
            plan1 = cur.fetchall()

            ## Get AQP 2 disable seqscan
            cur.execute("SET LOCAL enable_indexscan = TRUE")
            cur.execute("SET LOCAL enable_bitmapscan = FALSE")
            cur.execute("EXPLAIN (FORMAT JSON) " + query)
            plan2 = cur.fetchall()

            ## Get AQP 3 disable mergejoin
            cur.execute("SET LOCAL enable_bitmapscan = TRUE")
            cur.execute("SET LOCAL enable_mergejoin = FALSE")
            cur.execute("EXPLAIN (FORMAT JSON) " + query)
            plan3 = cur.fetchall()

            ## Get AQP 4 disable nextloop
            cur.execute("SET LOCAL enable_mergejoin = TRUE")
            cur.execute("SET LOCAL enable_nestloop = FALSE")
            cur.execute("EXPLAIN (FORMAT JSON) " + query)
            plan4 = cur.fetchall()

        else:
           return {"Please enter the right SQL query!" : None}
    except:
        return {"Please enter the right SQL query!" : None}

    annotate = Annotator()
    alternatives["Disabled IndexScan"] = annotate.wrapper(plan1)
    annotate = Annotator()
    alternatives["Disabled BitMapScan"] = annotate.wrapper(plan2)
    annotate = Annotator()
    alternatives["Disabled MergeJoin"] = annotate.wrapper(plan3)
    annotate = Annotator()
    alternatives["Disabled NestLoop"] = annotate.wrapper(plan4)
    return alternatives

## Get schema of selected database
def getSchema(connected):
    #connected = connectPostgreSQL()
    if connected:
        cursor = connected.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # cursor.execute("""SELECT table_schema, table_name
        #                   FROM information_schema.tables
        #                   WHERE table_schema != 'pg_catalog'
        #                   AND table_schema != 'information_schema'
        #                   AND table_type='BASE TABLE'
        #                   ORDER BY table_schema, table_name""")

        cursor.execute("SELECT table_name, column_name, data_type, character_maximum_length as length FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name, ordinal_position")

        tables = cursor.fetchall()
    else:
        return None
    return tables

## To extract schema names
def showSchema(tables):
    schema = {}
    cur_table = ""
    cur_col = ""
    for row in tables:
        if cur_table != row["table_name"]:
            schema[row["table_name"]] = [row["column_name"]]
            cur_table = row["table_name"]
        else:
            schema[row["table_name"]].append(row["column_name"])
            #schema.append("{}.{}".format(row["table_schema"], row["table_name"]))
            #print("{}.{}".format(row["table_schema"], row["table_name"]))

    return schema
