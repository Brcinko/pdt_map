"""
    map_server, author: Lukas Klescinec <lukas.klescinec@gmail.com>
    FIIT Slovak University of Technology 2016

    This module is part of school project on lesson Advanced Databases.
"""

import pprint
import db_connection
import settings
from string import replace


from flask import Flask, request, jsonify, json, render_template, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='frontend')
cors = CORS(app, resources={r"/*": {"origins": "*",
                                    "methods": " [GET, HEAD, POST, OPTIONS, PUT, PATCH, DELETE]",
                                    "headers": "*"}})


@app.route('/info', methods=['GET'])
def info():
    if request.method == 'GET':
        query = 'SELECT PostGIS_full_version();'
        postgis_ver = db_connection.execute_query(conn, query)
        settings.infos[0]['postgis_ver'] = str(postgis_ver)
        return jsonify({'infos': settings.infos})

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pubs', methods=['GET'])
def pubs():
    return render_template('pubs.html')


@app.route('/pubs_building', methods=['GET'])
def pubs_building():
    return render_template('pubs_building.html')


@app.route('/pubs_polygon', methods=['POST'])
def pubs_polygon():
    if request.method == 'POST':
        # print str(request.get_json(force=True))
        coords = request.get_json(force=True)
        print coords['lng'], coords['lat']
        query = 'SELECT ST_AsGeoJSON(ST_Transform(way,4326)), name AS geometry FROM planet_osm_point WHERE amenity = \'pub\' ORDER BY ST_TRANSFORM(way, 4326) <-> st_setsrid(ST_MakePoint(' + str(coords['lng']) + ', ' + str(coords['lat']) + '),4326) LIMIT 1;'
        # query = 'SELECT * FROM planet_osm_polygon WHERE ST_Distance_Sphere(way, ST_MakePoint(' + str(coords['lng']) + ', ' + str(coords['lat']) + ')) <= 100 * 1609.34;'
        print query
        pubs = db_connection.execute_query(conn, query)
        pubsx = list()
        for p in pubs:
            x = json.loads(p[0])
            pubsx.append({"type": "Feature",
                          "properties":
                          {"description": p[1],
                           "icon": "bar"},
                          "geometry": x })
        print str(pubsx)
        return json.dumps(pubsx)


@app.route('/pubs_info', methods=['GET'])
# @cross_origin()
def pubs_info():
    if request.method == 'GET':
        query = 'SELECT name AS description, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry FROM planet_osm_point WHERE amenity = \'pub\';'
        # query = 'SELECT row_to_json(fc) FROM ( SELECT \'FeatureCollection\' AS type, array_to_json(array_agg(f)) AS features FROM (SELECT \'Feature\' AS type , ST_AsGeoJSON(ST_Transform(way,4326))::json AS geometry, row_to_json((name, amenity)) AS properties FROM planet_osm_point WHERE amenity = \'pub\'   ) AS f )  AS fc;'
        pubs = db_connection.execute_query(conn, query)
        pubsx = list()
        for p in pubs:
            x = json.loads(p[1])
            pubsx.append({"type": "Feature",
                          "properties":
                            {"description": p[0],
                             "icon": "bar"},
                          "geometry":  x })
        return json.dumps(pubsx)
        # return jsonify(json.dumps(pubsx))

if __name__ == '__main__':
    # connect database
    conn = db_connection.open_connection()
    print "Database connected."
    # start API server
    app.run(debug=True, port=8080)

