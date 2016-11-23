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


@app.route('/nearest_pub', methods=['GET'])
def nearest_pub():
    return render_template('nearest_pub.html')


@app.route('/pubs_in_district', methods=['GET'])
def pubs_in_city():
    return render_template('pubs_in_district.html')


@app.route('/get_districts', methods=['GET'])
def get_districts():
    if request.method == 'GET':
        query = 'SELECT name FROM planet_osm_polygon WHERE admin_level = \'8\' AND name like \'okres%\';'
        districts = db_connection.execute_query(conn, query)
        districtsx = list()
        for d in districts:
            districtsx.append(d[0])
            # print str(districtsx)
        # print str(districtsx)
        return json.dumps({"districts" : districtsx})


@app.route('/get_district', methods=['GET'])
def get_district():
    if request.method == 'GET':
        print(request.args['district'])
        query = 'select ST_AsGeoJSON( ST_Transform(way, 4326)), name from planet_osm_line where admin_level = \'8\' and name like \'' + request.args['district'] + '\';'
        district = db_connection.execute_query(conn, query)
        districtx = list()
        for d in district:
            x = json.loads(d[0])
            print str(x)
            districtx.append({"type": "Feature",
                          "properties": {},
                          "geometry": x })
        return json.dumps(districtx)

@app.route('/nearest_pub_point', methods=['POST'])
def nearest_pub_point():
    if request.method == 'POST':
        # print str(request.get_json(force=True))
        coords = request.get_json(force=True)
        # print coords['lng'], coords['lat']
        query = 'SELECT ST_AsGeoJSON(ST_Transform(way,4326)), name AS geometry FROM planet_osm_point WHERE amenity = \'pub\' ORDER BY ST_TRANSFORM(way, 4326) <-> st_setsrid(ST_MakePoint(' + str(coords['lng']) + ', ' + str(coords['lat']) + '),4326) LIMIT 1;'
        # query = 'SELECT * FROM planet_osm_polygon WHERE ST_Distance_Sphere(way, ST_MakePoint(' + str(coords['lng']) + ', ' + str(coords['lat']) + ')) <= 100 * 1609.34;'
        # print query
        pubs = db_connection.execute_query(conn, query)
        pubsx = list()
        for p in pubs:
            x = json.loads(p[0])
            pubsx.append({"type": "Feature",
                          "properties":
                          {"description": p[1],
                           "icon": "bar"},
                          "geometry": x })
        # print str(pubsx)
        return json.dumps(pubsx)


@app.route('/get_pubs_in_district', methods=['GET'])
def get_pubs_in_district():
    if request.method == 'GET':
        print(request.args['district'])
        query = 'select way from planet_osm_polygon where admin_level = \'8\' and name like \'' + request.args['district'] + '\';'
        district_geom = db_connection.execute_query(conn, query)
        print str(district_geom[0])
        query = 'SELECT ST_AsGeoJSON(ST_transform(way,4326)), name FROM planet_osm_polygon WHERE amenity = \'pub\' OR amenity = \'restaurant\' AND ST_Within(way,\'' + district_geom[0][0] + '\' ) = True ;'
        # query = 'SELECT ST_AsGeoJSON(ST_transform(way,4326)), name FROM planet_osm_polygon WHERE amenity = \'pub\' OR amenity = \'restaurant\' AND ST_Within(way,(select way from planet_osm_polygon where admin_level = \'8\' and name like \'' + request.args['district'] + '\') ) = True LIMIT 100;'
        pubs = db_connection.execute_query(conn, query)
        pubsx = list()
        for p in pubs:
            x = json.loads(p[0])
            pubsx.append({"type": "Feature",
                          "geometry":  x })
        return json.dumps(pubsx)



@app.route('/get_city_polygon', methods=['GET'])
def get_city_polygon():
    if request.method == 'GET':
        print(request.args['city'])
        query = 'SELECT ST_AsGeoJSON(ST_Transform(way, 4326)), way from planet_osm_polygon WHERE place = \'city\' OR place = \'town\' and name = \'' + request.args['city'] + '\' LIMIT 1'
        cities = db_connection.execute_query(conn, query)
        citiesx = list()
        for c in cities:
            x = json.loads(c[0])
            citiesx.append({"way": c[1],
                            "geometry": x})
        # print citiesx[0]['geometry']['coordinates'][0]
        return json.dumps(citiesx)


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


if __name__ == '__main__':
    # connect database
    conn = db_connection.open_connection()
    print "Database connected."
    # start API server
    app.run(debug=True, port=8080)

